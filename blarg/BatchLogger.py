from mongodb import Database, isBot
import traceback
import datetime
import requests
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
        self.mongo = Database("UYA", "Logger")
        self.exists = False
        self.coords = {}
        self.players = {} #username to state/result dict
        self.scores = {}
        self.currentMessage = 0
        self.cacheMessage = 0
        self.startTime = None
        self.status = 1
        self.updateId = 0
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
            if uyaTrackerId != None and len(self.players) > 2 and isBotGame == False:
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
            self.mongo.client.close()
            liveHistory.client.close()
    def updatePlayersStore(self, active, quits):
        '''merge with stats in the store'''
        stats = Database("UYA", "Player_Stats_Backup")
        mergeSet(stats, active)
        mergeSet(stats, quits)
        stats.client.close()
    def log(self, running = True):
        # URL = 'http://127.0.0.1:5000/live/log'
        URL = 'http://uyatracker.herokuapp.com/live/log'
        if self.status == 1:
            try:
                now = datetime.datetime.now()
                duration = now - self.startTime if self.startTime != None else now - now
                seconds = str(duration.seconds%60)
                seconds = seconds if len(seconds) > 1 else f"0{seconds}"
                update = { 
                    'dme_id':self.id,
                    'map':self.map,
                    # 'start_time':str(self.startTime),
                    'logger':self.batch if self.currentMessage == 0 else self.batch[self.currentMessage:] if len(self.cache) != len(self.batch) else self.cache[self.cacheMessage:],
                    'graph': self.coords,
                    'player_states': self.players,
                    'scores':self.scores,
                    'batch_num':self.currentMessage,
                    'isRunning': running,
                    'duration': "{}:{}".format(duration.seconds//60, seconds),
                    'updateId':self.updateId
                }
                res = requests.post(URL, json = update)
                if len(self.cache) != len(self.batch):
                    self.cacheMessage = self.currentMessage
                    self.cache = list(self.batch)
                    self.currentMessage = len(self.batch)
            except Exception as e:
                print("Problem logging HTTP")
                print(traceback.format_exc())
            finally:
                self.updateId+=1

def mergeDicts (existing, new):
    '''merge a new dict onto the existing dict, summing matching keys and merging non existing ones from new'''
    pass
    for key in new:
        if key not in existing:
            existing[key] = new[key]
        else:
            if type(existing[key]) == dict:
                mergeDicts(existing[key], new[key])
            elif type(existing[key]) == int or type(existing[key]) == float:
                existing[key] += new[key]
def mergeSet(stats, players):
    for player in players:
        playerStore = stats.collection.find_one({"username_lowercase":player.username.lower()})
        if not playerStore: continue
        advancedStats = playerStore['advanced_stats']
        if "live" not in advancedStats:
            advancedStats['live'] = {}
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
