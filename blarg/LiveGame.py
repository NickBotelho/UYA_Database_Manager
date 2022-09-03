
from cProfile import run
import matplotlib.pyplot as plt
import numpy as np
import requests
import logging
import datetime
from blarg.DMEPlayer import Player
from blarg.utils.utils import bytes_from_hex, bytes_to_str, hex_to_bytes
from blarg.BatchLogger import BatchLogger
from mongodb import Database
import datetime
from blarg.constants.constants import TIMES
from blarg.utils.utils import generateFlagIDs, generateHealthIDs
from Parsers.GamestateGameSettingsParser import hasNodes
from HashId import hash_id
from sys import maxsize
GAMES = 'http://107.155.81.113:8281/robo/games'
GAME_EVENTS = {'020C', '020A', '0200', '020E', '0204', '0003'}
EVENTS = {
    0:"Flag Captured",
    1:"Flag Saved",
    2:"Flag Picked Up",
    3:"Turret Shields Closing",
    4:"Item Picked Up",
    5:"Flag Dropped",
    6:"Respawning",
    7:"Killed",
    8:"Firing",
    9:"Game Starting",
    10:"Game Created",
    11:"Player Joined",
    12:"Taking Damage",
    13:"Time",
    14:"Player Left",
}
STATE = {
    0:'Staging',
    1:'In Progress',
    2:"Game Complete",
    3:"Game Logged"
}
# READY_MAPS = {
#     'Bakisi_Isle',
#     'Blackwater_Dox',
#     'Metropolis'
# }
READY_MODES = {
    'CTF'
}
AI = {
    255:'suicide',
    246:'Trooper',
    248:'Drones',
    249:"Shock Droids"
}
class LiveGame():
    def __init__(self, dme_id = None, delay = True, delayTime = 15) -> None:
        '''
        itos = index to string
        ntt = name to team
        nts = name to skin
        teams = teams
        '''
        self.dme_id = dme_id
        self.refreshRate = 1
        self.x, self.y, self.names = [], [] ,[] #Used for graphing
        self.current_time = 0
        self.itos, self.ntt, self.nts, self.teams = {}, {}, {}, {}
        self.scores = {}
        self.state = 0
        self.lobby = {}
        self.players = {} #lobby idx to player objs
        self.liveMap = True
        self.startTime = None
        self.flags = []
        self.quitPlayers = []
        self.hasNodes = None
        self.locationList = {}
        # level = 'DEBUG'
        level = "INFO"
        # level = "CRITICAL"
        self.logger = BatchLogger(level, self.dme_id)
        self.createTime = datetime.datetime.now()
        self.startTime = datetime.datetime.now()
        self.delay = delay
        self.numPlaced = 0
        self.uyaTrackerId = None
        self.clogger = 0
        self.isBotGame = False
        self.weapons = []
        if delay:
            self.delayTime = delayTime #in seconds
            self.pipe = []
    def load(self, packet_id, serialized, packet):
        '''Insert a packet and its info
        -It will add it to the time queue to add delay and if there are any ready it will manage them'''
        running = True
        if not self.delay or self.state != 1:
            return self.manage(packet_id, serialized, packet)
        else:
            #push the info and time to the queue
            info = (packet_id, serialized, packet)
            timestamp = datetime.datetime.now()
            self.pipe.append((info, timestamp))
            #check the difference between now and the timestamp on the top of the queue
            difference = timestamp - self.pipe[0][1]
            while running and len(self.pipe) > 0 and difference.seconds >= self.delayTime:
                info = self.pipe.pop(0)[0]
                running = self.manage(info[0], info[1], info[2])
                difference = timestamp - self.pipe[0][1] if len(self.pipe) > 0 else None
                if running == False: break
            return running




    def manage(self, packet_id, serialized, packet):
        '''Accepts a packet and its info
        it will manage the packet and direct it to the propper destination based on its info'''
        if packet_id == '0209' and packet['type'] == 'udp' and serialized['packet_num'] % self.refreshRate == 0 and self.liveMap:
            self.placeOnMap(serialized, packet)
        # elif packet['type'] == 'tcp' and (packet_id == '0211' or packet_id == '0210' or packet_id == '0003'):
        #     self.staging(packet_id, serialized, packet)
        elif packet['type'] == 'tcp' and packet_id == '000D':
            self.parseLobby(packet_id)
            self._initPlayers()
            self.startGame(serialized, packet)
        elif packet['type'] == 'tcp' and packet_id == '0004' and self.state == 0:
            self.hasNodes = hasNodes(serialized['game_settings']) if self.hasNodes == None else self.hasNodes
            self.lobby = serialized
            # self.parseLobby()
        elif packet_id in GAME_EVENTS and self.state == 1:
            self.processEvent(packet_id, serialized, packet)
        elif self.state == 0 and packet_id == '0209' and packet['type'] == 'udp':
            self.parseLobby(packet_id)
            self._initPlayers()
            self.startGame(serialized, packet)
        return self.state != 2
    def startGame(self, serialized, packet):
        '''triggers on game start'''
        print(f"{self.dme_id}: GAME STARTING")
        self.logger.info(f"Game Starting...")
        self.state = 1
        self.startTime = datetime.datetime.now()
        self.logger.startTime = self.startTime
        res = requests.get(GAMES).json()
        self.game = None
        self.current_time = 0
        for game in res:
            if game['dme_world_id'] == self.dme_id:
                self.game = game
                break
        self.uyaTrackerId = hash_id(self.game)
        for team in set(self.ntt.values()):
            self.teams[team] = [player for player in self.ntt if self.ntt[player] == team]
        self.logger.debug(self.teams)
        self.map = game['map']
        self.registerGuns(game['weapons'])
        self.logger.setMap(self.map)
        self.mode = game['game_mode']
        self.limit = game['cap_limit'] if 'cap_limit' in game else None #ctf
        self.limit = game['frag'] if 'frag' in game else self.limit #dm
        self.limit = maxsize if self.limit == 0 else self.limit
        self.time_limit = TIMES[game['game_length']] if TIMES[game['game_length']] != None else None
        self.scores = {team:0 for team in self.ntt.values()}
        self.hasNodes = self.hasNodes if self.hasNodes != None else False
        self.hp_boxes = generateHealthIDs(self.map.lower(), nodes = self.hasNodes, base = game['advanced_rules']['baseDefenses'])
        self.flags = generateFlagIDs(self.map, nodes = self.hasNodes, base=game['advanced_rules']['baseDefenses']) if self.mode == "CTF" else []
        print(self.hasNodes,game['advanced_rules']['baseDefenses'], self.hp_boxes, self.flags)
        print(self.teams)
        self.logger.critical(f"LIMIT = {self.limit}")
        self.logger.setScores(self.scores)
        if not self.isImplemented():
            self.logger.critical("GAME TYPE NOT IMPLEMENTED")
            self.liveMap = False
            # self.game = None
    def processEvent(self, packet_id, serialized, packet):
        '''process and logs a game event
        Acceptable packets include 020C, 020A (respawn), udp 0200 (death) 
        '''
        if packet_id == '020C' and packet['type'] == 'tcp':
            if 'event' in serialized:
                event = serialized['event']
                update = None
                username = self.itos[int(packet['src'])]
                if event == 0:
                    self.players[int(packet['src'])].cap()
                    team = self.ntt[username]
                    update = f"{username} capped the flag"
                    self.logger.info(update)
                    self.scores[team] += 1
                    self.logger.setScores(self.scores)
                elif event == 1:
                    if serialized['flag_update_type'] != "flag_return":
                        update = f"{username} saved the flag"
                    else:
                        update = f"Flag returned to base due to inactivity"
                elif event == 2:
                    print(int(packet['src']), serialized)
                    item = serialized['object_id'][:2]
                    if item in self.flags:
                        update = f"{username} has picked up the flag"
                        self.players[int(packet['src'])].pickupFlag()
                elif event == 5:
                    print(int(packet['src']), serialized)
                    update = f"{username} has dropped the flag"
                    self.players[int(packet['src'])].dropFlag()
                elif event == 4:
                    print(int(packet['src']), serialized)

                    item = serialized['item_picked_up_id'][0:2]
                    if item in self.hp_boxes:
                        update = f"{self.itos[int(packet['src'])]} grabbed health"
                        self.players[int(packet['src'])].heal()
                if update != None:
                    self.logger.info(update)             
        elif packet_id == '020A' and packet['type'] == 'tcp':
            self.logger.info(f"{self.itos[int(serialized['player'])]} {EVENTS[serialized['event']]}")
            self.players[int(serialized['player'])].respawn()

        elif packet_id == '020E' and packet['type'] == 'udp': #FIRING
            self.players[int(packet['src'])].fire(serialized['weapon'], serialized['player_hit'])
            if serialized['player_hit'] != "FF" and serialized['weapon'].lower() == 'flux':
                self.players[int(serialized['player_hit'])].stageNick(self.players[int(packet['src'])])
            self.logger.debug(f"{self.itos[int(serialized['src'])]} is {EVENTS[serialized['event']]} a {serialized['weapon']}")
        elif packet_id == '0204' and packet['type'] == 'tcp': #KILLS
            if serialized['killer_id'] > 7:
                self.logger.info(f"{self.itos[int(serialized['killed_id'])]} Died")
                if self.mode == 'Deathmatch':
                    username = self.itos[int(serialized['killed_id'])]
                    team = self.ntt[username]
                    self.scores[team] -=1
            else:
                self.logger.info(f"{self.itos[int(serialized['killer_id'])]} {EVENTS[serialized['event']]} {self.itos[int(serialized['killed_id'])]} with {serialized['weapon']}")
                self.players[int(serialized['killer_id'])].kill(enemy = self.players[int(serialized['killed_id'])], weapon = serialized['weapon'])
                if self.mode == 'Deathmatch':
                    username = self.itos[int(serialized['killer_id'])]
                    team = self.ntt[username]
                    self.scores[team] +=1
            self.players[int(serialized['killed_id'])].death()
        elif packet_id == '0003' and packet['type'] == 'tcp':
            messages = serialized['messages']
            for message in messages:
                if message['type'] == 'health':
                    self.players[packet['src']].checkNick(message['health'])
                    self.players[packet['src']].adjustHP(message['health'])
         
        return self.isComplete()
    def placeOnMap(self, serialized, packet):
        serialized['coord'].pop()
        point = serialized['coord']
        rotation = serialized['cam1_x']
        player_idx = int(packet['src'])
        clog_limit = 250 if not self.isBotGame else 500
        self.locationList[player_idx] = 1 if player_idx not in self.locationList else self.locationList[player_idx]+1
        try:
            player = self.players[player_idx]
            if player.isPlaced == False:
                player.place(point, rotation)
                self.numPlaced+=1

            if self.clogger >= clog_limit:
                # print(self.locationList)
                print(f"unclogging{self.clogger}...{self.numPlaced} {[str(self.players[p]) for p in self.players]}")
                self.removeQuitPlayer()
            self.clogger +=1
            
            display = True if self.numPlaced >= len(self.players) else False
            if display:
                colors = [self.players[i].team for i in self.players]
                x = [self.players[i].x for i in self.players]
                y = [self.players[i].y for i in self.players]
                hp = [self.players[i].hp for i in self.players]
                names = [self.players[i].username for i in self.players]
                hasFlag = [self.players[i].hasFlag for i in self.players]
                rotations = [self.players[i].rotation for i in self.players]
                self.logger.setCoords((x, y, names, colors, hp, hasFlag, rotations))
                self.logger.setStates(self.players)
                self.logger.log()
                self.logger.flush(self.players)
                self.numPlaced, self.clogger = 0, 0
        except:
            print(f"{self.dme_id} Problem in placeOnMap with {player_idx} not being in self.players possibly.\n \
                self.players: {self.players}")


    def isImplemented(self):
        # return self.map in READY_MAPS and self.mode in READY_MODES
        return True
    def removeQuitPlayer(self):
        quitter = None
        for player in self.players.values():
            if player.isPlaced == False:
                self.logger.info(f"{player.username} has left the game")
                print(f"{player.username} has left the game")
                player.quit()
                quitter = player
                break
        del self.players[quitter.lobby_idx]
        self.quitPlayers.append(quitter)
        for player in self.players.values():
            player.isPlaced = False
        self.clogger = 0

        self.state = 2
        for player in self.players.values():
            if player.isBot == False:
                self.state = 1
        if self.state == 2:
            self.endGame()
    def getState(self):
        return STATE[self.state]
    def isLoaded(self):
        return self.delay and len(self.pipe) > 0
    def parseLobby(self, packet_id):
        #go through lobby:
        for i in range(8):
            field = f"p{i}_username"
            if field in self.lobby:
                if self.lobby[field] != '':
                    self.itos[i] = self.lobby[field]

                    field = f"p{i}_team"
                    self.ntt[self.itos[i]] = self.lobby[field]

                    field = f"p{i}_skin"
                    self.nts[self.itos[i]] = self.lobby[field]
            else:
                print(f'Error parsing game lobby for {self.dme_id}.\n\
                    The lobby is as follows = {self.lobby}\n\
                        as a result trying to parse from packet {packet_id}')
        self.isBotGame = self.checkForBots()
        self.logger.debug(str(self.itos))
        self.logger.debug(str(self.ntt))
        self.logger.debug(str(self.nts))
    def checkForBots(self):
        for username in self.itos.values():
            if len(username) >= 3:
                if username[:3].lower() == "cpu":
                    return True
        return False
    def _initPlayers(self):
        for player_idx in self.itos:
            username = self.itos[player_idx]
            self.players[player_idx] = Player(username, player_idx, self.ntt[username])
    def displayPlayers(self):
        for idx in self.players:
            self.logger.info(str(self.players[idx]))
    def endGame(self):
        if self.state < 3:
            winningTeamColor = self.getWinningTeam()
            self.logger.log()
            self.logger.close(self.uyaTrackerId, self.players, self.quitPlayers, winningTeamColor)
            self.logger.updatePlayersStore(self.players.values(), self.quitPlayers)
            self.state = 3
            print(f"Closing ID: {self.dme_id}")
            print(f"{self.dme_id} Results: {[str(self.players[p]) for p in self.players]} | DCs: {[str(p) for p in self.quitPlayers]}")
    def getWinningTeam(self):
        '''Return a string of the team with the highest score'''
        print("calculating winning team")
        print(self.scores)
        winningTeam = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        print(f"winning team {winningTeam}")
        return winningTeam[0]
    def isComplete(self):
        '''returns true if the game is complete'''
        for team in self.scores:
            if self.scores[team] == self.limit:
                self.logger.info(f"Game Ending {team} wins!")
                self.endGame()
                return True
        
        currentTime = datetime.datetime.now()
        duration = currentTime - self.startTime
        if self.time_limit != None and ((duration.total_seconds() - self.delayTime)//60) > self.time_limit:
            self.logger.info("Time is up!")
            self.endGame()
            return True

        if ((duration.total_seconds() - self.delayTime)//60) > 120:
            self.logger.info("Stale game")
            self.endGame()
            return True

        return False
    def registerGuns(self, weapons):
        for player in self.players.values():
            for weapon in weapons:
                player.addWeapon(weapon)


#So when a player G's up it sends a 0211 packet with their name, color, skin
#ctf = = 'cap_limit'
#tdm = 'frag'
#Deathmatch 
