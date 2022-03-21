
from Parsers.MapParser import mapParser
from Parsers.WeaponParser import weaponParser
from Parsers.TimeParser import timeParser
from Parsers.GamerulesParser import gamerulesParser
from Parsers.AdvancedRulesParser import advancedRulesParser
from Parsers.ToLadderstatswide import HextoLadderstatswide
from HashId import hash_id
import time
import os
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

GAME_STATUS = {
    1:"Staging",
    2:"In_Progress",
    3:'Ended',
}

class Game():
    def __init__(self, packet) -> None:
        self.packet = packet
        self.parse()
        self.cached_stats = {}
    def parse(self):
        self.status = self.packet['status']
        self.id = hash_id(self.packet)
        self.player_ids = [player['account_id'] for player in self.packet['players']]
        self.player_names = [player['username'] for player in self.packet['players']]
        self.dme_id = self.packet['dme_world_id']

        ##########Status##########
        self.creation_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.packet['created_date']))
        self.status = GAME_STATUS[self.packet['status']] if self.packet['status'] in GAME_STATUS else "Zombie/Ghost Game"
        self.start_time = time.time() if self.status == 'In_Progress' else None
        self.end_time = None
        ##########Weapons#########
        self.weapons = weaponParser(self.packet['player_skill_level'])

        ###########RULES##########
        self.rules = int(self.packet['generic_field_3'])
        self.map = mapParser(self.rules)
        self.game_length = timeParser(self.rules)
        self.game_mode, self.game_submode = gamerulesParser(self.rules)
        self.advanced_rules = advancedRulesParser(self.rules)

    def __str__(self) -> str:
        return "{} | {} ({} Players) MAP: {} GAMEMODE: {} ({}) WEAPONS: {} TIME: {}  ADVANCED:{}".format(self.creation_time, self.status, len(self.player_ids),self.map, 
        self.game_mode,self.game_submode, self.weapons, self.game_length, self.advanced_rules)
    def details(self):
        res = {
            'host':self.player_names[0],
            'status':self.status,
            'map':self.map,
            'gamemode':self.game_mode, #array [mode, submode]
            'weapons':self.weapons, #array of weapons,
            'players':self.player_names,
        }
        return res
    def checkIfStart(self, status, lobby):
        '''Checks if the game is in progress and if it is, will cement the player ids'''
        if self.status == "Staging" and status == 2:
            self.start_time = time.time()
            self.player_ids = [player['account_id'] for player in lobby]
            self.player_names = [player['username'] for player in lobby]
            self.status = GAME_STATUS[2]
            return True
        return False
    def updatePlayers(self, lobby):
        '''updates the players in the staging'''
        self.player_ids = [player['account_id'] for player in lobby]
        self.player_names = [player['username'] for player in lobby]


def cacheStats(games, player_stats):
    for game_id in games:
        if games[game_id].status == "In_Progress" and len(games[game_id].cached_stats) == 0:
            player_ids = games[game_id].player_ids
            for id in player_ids:
                player_info =  player_stats.collection.find_one({'account_id':id})
                if player_info:
                    games[game_id].cached_stats[id] = player_info['stats']
                else:
                    print('Player not found trying to cache stats')



# def printGames(games):
#     '''accepts list of games and print'''
#     for game in games:
#         print(games[game])

    


class MediusWorldStatus:
    WORLD_INACTIVE = 0
    WORLD_STAGING = 1
    WORLD_ACTIVE = 2
    WORLD_CLOSED = 3
    WORLD_PENDING_CREATION = 4
    WORLD_PENDING_CONNECT_TO_GAME = 5