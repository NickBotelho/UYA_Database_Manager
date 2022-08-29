from mongodb import Database
import traceback
import datetime
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
        self.liveHistory = Database("UYA", "LiveGame_History")
        self.exists = False
        self.coords = {}
        self.players = {}
        self.scores = {}
        self.currentMessage = 0
        self.cacheMessage = 0
        self.startTime = None
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
    def setStates(self, players):
        self.players = {}
        for i in players:
            self.players[players[i].username] = players[i].getState()
    def setBatch(self,batch):
        self.batch = []
        self.batch = batch
    def setScores(self, scores):
        self.scores = scores
    def log(self):
        try:
            now = datetime.datetime.now()
            duration = now - self.startTime if self.startTime != None else now - now
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
                        'duration': "{}:{}".format(duration.seconds//60, duration.seconds%60),

                    }
                })
            if len(self.cache) != len(self.batch):
                self.cacheMessage = self.currentMessage
                self.cache = list(self.batch)
                self.currentMessage = len(self.batch)
        except Exception as e:
            print("Problem logging")
            print(traceback.format_exc())

    def close(self, uyaTrackerId, players):
        '''close the game and save the states'''
        self.setStates(players)
        now = datetime.datetime.now()
        duration = now - self.startTime if self.startTime != None else now - now
        try:
            self.mongo.collection.find_one_and_delete({
                'dme_id':self.id
            })
            self.liveHistory.collection.insert_one({
                'game_id':uyaTrackerId,
                'results':self.players,
                'duration': "{}:{}".format(duration.seconds//60, duration.seconds%60),
                'number_of_batches':self.currentMessage,


            })
        except Exception as e:
            print("Problem closing")
            print(e)


