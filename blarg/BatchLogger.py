from mongodb import Database, isBot
import traceback
import datetime
import requests
from blarg.constants.constants import STREAK_CONTRACT
# logs = Database("UYA", "Logger")
VALUES = {

    'CRITICAL':50,
    'ERROR':40,
    'WARNING':30,
    'INFO':20,
    'DEBUG':10,
    'NOTSET':0,

    }  

class BatchLogger():
        
    def __init__(self, level = "DEBUG", id = 0) -> None:
        self.level = VALUES[level]
        self.batch = []
        self.cache = []
        self.id = id
        self.map = None
        self.mongo = Database("UYA", "Logger", live = True)
        self.exists = False
        self.coords = {}
        self.players = {} #username to state/result dict
        self.scores = {}
        self.currentMessage = 0
        self.cacheMessage = 0
        self.startTime = None
        self.status = 1
    def debug(self, message):
        if type(message) != str:
            message = str(message)
        if self.level <= 10:
            self.batch.append(message)
    def info(self, message):
        if type(message) != str:
            message = str(message)
        if self.level <= 20:
            self.batch.append(message)
    def warning(self,message):
        if type(message) != str:
            message = str(message)
        if self.level<=30:
            self.batch.append(message)
    def error(self,message):
        if type(message) != str:
            message = str(message)
        if self.level<=40:
            self.batch.append(message)
    def critical(self, message):
        if type(message) != str:
            message = str(message)
        if self.level <= 50:
            self.batch.append(message)
    def flush(self, players):
        # self.batch = []
        self.players = {}
        self.coords = {}
        for i in players:
            players[i].unPlace()
    def setMap(self, m):
        self.map = m
    def print(self):
        for message in self.batch:
            print(message)
    def getBatch(self):
        return self.batch
    def last(self):
        print(self.batch[-1])
        return self.batch[-1]
    def setCoords(self, info):
        self.coords['x'] = info[0]
        self.coords['y'] = info[1]
        self.coords['names'] = info[2]
        self.coords['color'] = info[3]
        self.coords['hp'] = info[4]
        self.coords['hasFlag'] = info[5]
        self.coords['rotations'] = info[6]
    def setStates(self, players):
        self.players = {}
        for i in players:
            self.players[players[i].username] = players[i].getState()
    def setResults(self, players):
        self.players = {}
        for i in players:
            self.players[players[i].username] = players[i].getResult()
    def setPlayerStore(self, players):
        self.players = {}
        for i in players:
            self.players[players[i].username] = players[i].getStore()
    def setBatch(self,batch):
        self.batch = []
        self.batch = batch
    def setScores(self, scores):
        self.scores = scores
    def log(self, running = True):
        if self.status == 1:
            try:
                now = datetime.datetime.now()
                duration = now - self.startTime if self.startTime != None else now - now
                seconds = str(duration.seconds%60)
                seconds = seconds if len(seconds) > 1 else f"0{seconds}"
                if not self.exists:
                    existing = self.mongo.collection.find_one({'dme_id':self.id})
                    if existing != None:
                        self.mongo.collection.find_one_and_delete({'dme_id':self.id})
                    self.mongo.collection.insert_one({
                        'dme_id':self.id,
                        'map':self.map,
                        'start_time':self.startTime,
                        'logger':self.batch,
                        'graph': self.coords,
                        'player_states': self.players,
                        'scores':self.scores,
                        'batch_num':self.currentMessage,
                        'isRunning': running,
                    })
                    self.exists = True
                else:
                    self.mongo.collection.find_one_and_update({
                        'dme_id':self.id
                    },
                    {
                        '$set':{
                            'logger':self.batch[self.currentMessage:] if len(self.cache) != len(self.batch) else self.cache[self.cacheMessage:],
                            'graph': self.coords,
                            'player_states': self.players,
                            'scores':self.scores,
                            'batch_num':self.currentMessage,
                            'duration': "{}:{}".format(duration.seconds//60, seconds),
                        }
                    })
                if len(self.cache) != len(self.batch):
                    self.cacheMessage = self.currentMessage
                    self.cache = list(self.batch)
                    self.currentMessage = len(self.batch)
            except Exception as e:
                print("Problem logging")
                print(traceback.format_exc())
    def close(self, uyaTrackerId, players, quits, scores, winningTeamColor, isBotGame):
        '''close the game and save the states'''
        self.status = 2 #not the same as LiveGame Status
        for quitter in quits:
            players[quitter.username] = quitter
        self.setResults(players)
        now = datetime.datetime.now()
        liveHistory = Database("UYA", "LiveGame_History")
        duration = now - self.startTime if self.startTime != None else now - now
        try:           
            self.mongo.collection.find_one_and_delete({
                    'dme_id':self.id
                })
        except Exception as e:
            print("problem closing")
            print(e)
        finally:
            if uyaTrackerId != None and len(self.scores) > 1 and isBotGame == False:
                try:
                    liveHistory.collection.insert_one({
                        'game_id':uyaTrackerId,
                        'winning_team':winningTeamColor,
                        'scores':scores, 
                        'results':self.players,
                        'duration': "{}:{}".format(duration.seconds//60, duration.seconds%60),
                        'number_of_batches':self.currentMessage,
                    })
                except Exception as e:
                    print("Problem peristing game into LiveGame_History")
                    print(e)
                finally:
                    self.updatePlayersStore(players.values(), quits, winningTeamColor)

            self.mongo.client.close()
            liveHistory.client.close()
    def updatePlayersStore(self, active, quits, winningTeam):
        '''merge with stats in the store'''
        stats = Database("UYA", "Player_Stats")
        mergeSet(stats, active, winningTeam)
        mergeSet(stats, quits, winningTeam)
        stats.client.close()
    # def log(self, running = True):
    #     # URL = 'http://127.0.0.1:5000/live/log'
    #     URL = 'http://uyatracker.herokuapp.com/live/log'
    #     if self.status == 1:
    #         try:
    #             now = datetime.datetime.now()
    #             duration = now - self.startTime if self.startTime != None else now - now
    #             seconds = str(duration.seconds%60)
    #             seconds = seconds if len(seconds) > 1 else f"0{seconds}"
    #             update = { 
    #                 'dme_id':self.id,
    #                 'map':self.map,
    #                 # 'start_time':str(self.startTime),
    #                 'logger':self.batch,
    #                 'graph': self.coords,
    #                 'player_states': self.players,
    #                 'scores':self.scores,
    #                 'batch_num':self.currentMessage,
    #                 'isRunning': running,
    #                 'duration': "{}:{}".format(duration.seconds//60, seconds),
    #             }
    #             res = requests.post(URL, json = update)
    #             if len(self.cache) != len(self.batch):
    #                 self.cacheMessage = self.currentMessage
    #                 self.cache = list(self.batch)
    #                 self.currentMessage = len(self.batch)
    #         except Exception as e:
    #             print("Problem logging HTTP")
    #             print(traceback.format_exc())

def mergeDicts (existing, new):
    '''merge a new dict onto the existing dict, summing matching keys and merging non existing ones from new'''
    for key in new:
        if key not in existing:
            existing[key] = new[key]
        else:
            if type(existing[key]) == dict:
                mergeDicts(existing[key], new[key])
            elif type(existing[key]) == int or type(existing[key]) == float:
                existing[key] += new[key]
    return existing
def mergeSet(stats, players, winningTeam):
    for player in players:
        playerStore = stats.collection.find_one({"username_lowercase":player.username.lower()})
        if not playerStore: continue
        advancedStats = playerStore['advanced_stats']
        if "live" not in advancedStats:
            advancedStats['live'] = {}
        if "streaks" not in advancedStats:
            advancedStats['streaks'] = STREAK_CONTRACT
        advancedStats['streaks'] = updateStreaks(advancedStats['streaks'], player, winningTeam)
        mergeDicts(advancedStats['live'], player.getStore())
        stats.collection.find_one_and_update(
        {
            "_id":playerStore["_id"]
        },
        {
            "$set":{
                "advanced_stats":advancedStats
            }
        }
    )
def updateStreaks(streaks, player, winningTeam):
    if player.team == winningTeam:
        streaks['current_winstreak'] += 1
        streaks['current_losingstreak'] = 0
    else:
        streaks['current_winstreak'] = 0 
        streaks['current_losingstreak'] +=1 

    streaks['best_winstreak'] = max(streaks['best_winstreak'], streaks['current_winstreak']) 
    streaks['best_losingstreak'] = max(streaks['best_losingstreak'], streaks['current_losingstreak'])
    streaks['bestKillstreak'] = max(player.killTracker.bestKillStreak,streaks['bestKillstreak'] )
    streaks['bestDeathstreak'] = max(player.deathTracker.bestDeathStreak,streaks['bestDeathStreak'] )
    streaks['medals'] = mergeDicts(streaks['medals'], player.medals.getState())
    return streaks


# STREAK_CONTRACT = {
#     'current_winstreak':0,
#     'best_winstreak':0,
#     'current_losingstreak':0,
#     'best_losingstreak':0,
#     'bestKillstreak':0,
#     'nukes':0, #25 kill streaks
#     'bestDeathStreak':0,
#     'distributors':0, #25death streaks
#     'undying':0,
#     'radioactives':0,
# }