import pymongo
import time
from config import MongoPW, MongoUser
from Parsers.ToLadderstatswide import HextoLadderstatswide
from CalculateStatLine import calculateStatLine
import os
try:
    if not MongoPW or not MongoUser:
        MongoPW = os.environ("MongoPW")
        MongoUser = os.environ("MongoUser")
except:
    print(MongoPW, MongoUser)
    print('failed to load credentials')
    exit(1)
    
PLAYER_STATUS={
    0:"Offline",
    2:"Lobby",
    3:"In Game"
}
class Database():
    def __init__(self,db,collection):
        self.client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.jydx7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(MongoUser, MongoPW))
        self.db = self.client[db]
        self.collection = self.db[collection]
    def getDB(self):
        return self.db
    def getCollection(self):
        return self.collection
    def clear(self):
        '''Wipe a collection'''
        if self.collection.count() == 0: return None
        if self.collection.name == 'Players_Online' or self.collection.name == 'Games_Active': #Protection to not whipe stats or game history
            self.collection.delete_many({})
    def addToDB(self, name, player_info):      
        player = self.collection.find_one({"name":name})
        if player == None:
            self.collection.insert_one(
                {
                    "username":name,
                    'account_id':player_info.id,
                    'status':player_info.status,
                    "numLogins":1,
                    "stats":HextoLadderstatswide(player_info.ladderstatswide),
                    "match_history":{},
                    "last_login":None                     
                }
            )
        else:         
            logins = int(player['numLogins'])
            logins+=1
            self.collection.find_one_and_update(
                {
                    "_id":player["_id"]
                },
                {
                    "$set":{
                        "numLogins":logins
                    }
                }
            )
    def logPlayerOff(self, online, name):
        player = self.collection.find_one({"name":name})   
        start = online[name]
        fin = time.time()
        id = player["_id"]
        session_time = int((abs(start-fin)/60))
        total_time = float(player["time_minutes"])
        total_time_hours = total_time/60
        self.collection.find_one_and_update(
            {
                "_id":id
            },
            {
                "$set":{
                    "time_minutes": (total_time + session_time),
                    "time_hours": (total_time_hours + (session_time/60))
                    }
            }
        )
    def updateTime(self, player, time):
        self.collection.find_one_and_update(
                {
                    "_id":player["_id"]
                },
                {
                    "$set":{
                        "time_minutes":time,
                        "time_hours":time/60
                    }
                }
            )
    def getTime(self,name, online):
        player = self.collection.find_one({"name":name})
        if player != None:
            if name in online: #if the player is online, we'll update in real time
                startTime = online[name]
                currentTime = time.time()
                currentTime = abs(currentTime - startTime) / 60 #current session time in minutes
                storedTime = float(player["time_minutes"])
                storedTime+= currentTime
                self.updateTime(player, storedTime)
                online[name] = time.time()
                player = self.collection.find_one({"name":name})
            storedTime = int(player["time_minutes"])
            if storedTime <= 60:
                return "{} Minutes.".format(storedTime)
            else:
                return "{:.1f} Hours".format(player['time_hours'])
        return None
    def addToSmokeLine(self, name, mention, time):
        player = self.collection.find_one({"name":name})
        if player == None:
            self.collection.insert(
                {
                    "name":name,
                    "discord_mention":mention,
                    "enter_time":time
                }
            )
        else:
            self.collection.find_one_and_update( #reset their time
                {
                    "_id":player["_id"]
                },
                {
                    "$set":{
                        "enter_time":time
                    }
                }
            )
    def getSmokersFromDB(self):
        smokeLine = {}
        smokePing = {}
        for person in self.collection.find():
            smokeLine[person['name']] = person['enter_time']
            smokePing[person['name']] = person['discord_mention']
        return smokeLine, smokePing
    def deleteSmoker(self, name):
        self.collection.delete_one({"name":name})
    def getTop10(self, stat):
        res = "NAME\t\t\tHOURS\n"
        i = 0
        for player in self.collection.find().sort([(stat,-1)]):
            if i < 10:
                i+=1
                res +="{}. {}\t {:.1f}\n".format(i, player['name'], player['time_hours'])
        return res
    def updateOnlinePlayersStats(self, onlinePlayers, offline_players):
        '''onlinePlayers is a dict id --> player object'''
        '''will add new players to DB and check some stuff every 5 mins'''
        '''Will logg players off'''
 
        for id in onlinePlayers:
            player = self.collection.find_one({"account_id":id})
            if player == None:
                self.addToDB(onlinePlayers[id].username, onlinePlayers[id])
            
            elif player['status'] == 0:
                self.collection.find_one_and_update( #player logging in
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':onlinePlayers[id].status,
                            'numLogins':player['numLogins'] + 1,
                            'last_login':time.time(),
                            'stats':HextoLadderstatswide(onlinePlayers[id].ladderstatswide)
                        }
                    }
                )
            else:
                self.collection.find_one_and_update( #normal update
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':onlinePlayers[id].status,
                            'stats':HextoLadderstatswide(onlinePlayers[id].ladderstatswide)
                            #advanced stats here
                        }
                    }
                )
        ################LOG PLAYERS OUT###############################
        for id in offline_players:
            self.collection.find_one_and_update( #reset their time
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':0,
                            'stats':HextoLadderstatswide(offline_players[id].ladderstatswide)
                        }
                    }
                )
    def logPlayersOff(self, offline_ids):
        '''Removes all ids in list from the collection'''
        for id in offline_ids:
            self.collection.find_one_and_delete({'account_id':id})
            
    def addOnlinePlayers(self, players):
        '''Add players to the online list if theyre not on it'''
        for id in players:
            player = self.collection.find_one({'account_id':id})
            if player == None:
                self.collection.insert_one(
                    {
                        "username":players[id].username,
                        'account_id':players[id].id,
                        'status':PLAYER_STATUS[players[id].status]
                    }
                )
    def addGames(self, games):
        '''add new games to the activate games collection'''
        for id in games:
            game = self.collection.find_one({'game_id':id})
            if not game:
                self.collection.insert_one(
                    {
                        'game_id':games[id].id,
                        'details':games[id].details()
                    }
            )
            else:
                self.collection.find_one_and_update(
                    {
                        "game_id":id
                    },
                    {
                        "$set":{
                            'details.status':games[id].status,
                            
                        }
                    }
                )
    def addGameToGameHistory(self, game, game_results):
        '''Adds a finished game to the history collection wite game as game object and results and res from calculate stat line function'''
        self.collection.insert_one(
            {
                'game_id':game.id,
                'map':game.map,
                'gamemode':game.game_mode,
                'submode':game.game_submode,
                'advanced_rules':game.advanced_rules,
                'minutes': (game.end_time- game.start_time) // 60,
                'weapons':game.weapons,
                'player_ids':game.player_ids,
                'game_results':game_results,
                # 'date':time.strftime('(%H:%M) %m/%d/%Y', game.start_time),
                'date':game.start_time
            }
        )
    def addGameToPlayerHistory(self, game_id, player_ids):
        for id in player_ids:
            player = self.collection.find_one({'account_id': id})
            match_history = player['match_history']
            match_history[str(game_id)] = player['stats']['overall']['games_played']
            self.collection.find_one_and_update(
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'match_history':match_history,
                            
                        }
                    }
                )
    def cancelGames(self, ended_games, player_stats, game_history):
        '''Ended Games is a dict of id --> ended Game object and player stats is the DB object holding new stats'''
        '''removes ended games from the active games collection'''
        '''before we dump the game, we'll add it to the history collection'''
        for id in ended_games:
            #add to history###
            ended_games[id].end_time = time.time()
            game_results = self.calculateGameStats(ended_games[id], player_stats)
            ##################
            self.collection.find_one_and_delete({'game_id':id})

            if game_results: #will be none if games flagged as fake 
                game_history.addGameToGameHistory(ended_games[id], game_results)
                player_stats.addGameToPlayerHistory(id, ended_games[id].player_ids)

    def calculateGameStats(self, game, player_stats):

        '''returns true if the game was legit and finished, false if fake game or didnt finish'''
        teams = {
            'winners':[],
            'losers':[]
        }
        total_kills = 0
        
        for id in game.player_ids:
            updated_player_entry = player_stats.collection.find_one({'account_id':id})
            if len(game.cached_stats) == 0:
                return None
            else:
                cache = game.cached_stats[id]
            stat_line = calculateStatLine(updated_player_entry, cache, game)
            total_kills+=stat_line['kills']
            #check to see if tie ################################
            if stat_line['game_result'] == 'tie' and 'tie' not in teams:
                teams['tie'] = []
            #####################################################
             #check to see if disconnected ################################
            if stat_line['game_result'] == 'disconnect' and 'disconnect' not in teams:
                teams['disconnect'] = []
            #####################################################


            if stat_line['game_result'] == 'win':
                teams['winners'].append(stat_line)
            elif stat_line['game_result'] == 'loss':
                teams['losers'].append(stat_line)
            elif stat_line['game_result'] == 'disconnect':
                teams['disconnect'].append(stat_line)
            else:
                teams['tie'].append(stat_line)
        return teams if total_kills > 0 else None


    

# client = pymongo.MongoClient("mongodb+srv://nick:{}@cluster0.yhf0e.mongodb.net/UYA-Bot?retryWrites=true&w=majority".format(mongoPW))
# print(client.list_database_names())
# db = client['uya-bot']
# collection = db['time-played']




# for i in player_stats.collection.find().sort([('stats.squats',1)]):
#     print(i)


      



