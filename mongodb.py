import enum
import pymongo
import time
from config import MongoPW, MongoUser
from Parsers.ToLadderstatswide import HextoLadderstatswide
from CalculateStatLine import calculateStatLine
import os
import blankRatios
import requests
from Parsers.ClanStatsParser import getClanTag
from Parsers.ClanStatswideParser import HexToClanstatswide
from Parsers.ToLadderstatswide import HextoLadderstatswide
import urllib.parse
from collections import Counter

os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()
try:
    if not MongoPW or not MongoUser:
        print("Loading Credentials")
        MongoPW = os.environ["MongoPW"]
        MongoUser = os.environ["MongoUser"]
except:
    print('failed to load credentials')
    exit(1)

PLAYER_STATUS={
    0:"Offline",
    2:"Lobby",
    3:"In Game"
}
class Database():
    def __init__(self,db,collection, live = False):
        if live:
            self.client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.xipwxkq.mongodb.net/?retryWrites=true&w=majority".format(MongoUser, MongoPW))
        else:
            self.client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.jydx7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(MongoUser, MongoPW))
        self.db = self.client[db]
        self.collection = self.db[collection]
    def getDB(self):
        return self.db
    def getCollection(self):
        return self.collection
    def clear(self):
        '''Wipe a collection'''
        if self.collection.count_documents({}) == 0: return None
        if self.collection.name != 'Player_Stats' or self.collection.name != 'Game_History': #Protection to not whipe stats or game history
            self.collection.delete_many({})
    def addToDB(self, name, player_info, elo):      
        player = self.collection.find_one({"name":name})
        if player == None:
            self.collection.insert_one(
                {
                    "username":name,
                    'account_id':player_info.id,
                    'status':player_info.status,
                    "numLogins":1,
                    "stats": HextoLadderstatswide(player_info.ladderstatswide),
                    "match_history":{},
                    "last_login":None,
                    'username_lowercase':name.lower().strip(),
                    "advanced_stats":{
                        'per_gm':blankRatios.blank_per_game,
                        'per_min':blankRatios.blank_per_minute,
                        'elo':blankRatios.blank_elo,
                        'live':blankRatios.blank_live_contract,
                        'live/gm':blankRatios.blank_live_contract,
                        'live/min':blankRatios.blank_live_contract,
                        'streaks':blankRatios.blank_streaks,
                    },
                    'clan_id' : player_info.clan_id,
                    'clan_tag': player_info.clan_tag,
                    'clan_name':player_info.clan_name,       
                    'elo_id':self.getEloId(elo, name),
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
    def getEloId(self, elo, player):
        url = 'http://103.214.110.220:8281/robo/alts/{}'
        try:
            encoded_name = urllib.parse.quote(player)
            accounts = requests.get(url.format(encoded_name))

            accounts=accounts.json() if accounts.status_code == 200 else [player]
            if accounts == '[]' or len(accounts) == 1:
                fresh_id = elo.collection.count_documents({})

                elo.collection.insert_one({
                    'elo_id':fresh_id,
                    'overall':1200,
                    'CTF':1200,
                    "Siege":1200,
                    'Deathmatch':1200,
                    'accounts' : [player],
                })
                return fresh_id
            for i, alt in enumerate(accounts):
                alt_id = self.collection.find_one({'username':alt})
                if alt_id != None or i <= len(accounts) - 1:
                    if alt_id == None: continue
                    alt_id = alt_id['elo_id']
                    eloAccount = elo.collection.find_one({'elo_id':alt_id})
                    if eloAccount == None: continue
                    alts = eloAccount['accounts']
                    alts.append(player)
                    elo.collection.find_one_and_update(
                        {
                            'elo_id':alt_id
                        },
                        {
                            '$set':{
                                'accounts':alts
                            }
                        }
                    )
                    return alt_id
                else:
                    fresh_id = elo.collection.count_documents({})
                    elo.collection.insert_one({
                    'elo_id': fresh_id,
                    'overall':1200,
                    'CTF':1200,
                    "Siege":1200,
                    'Deathmatch':1200,
                    'accounts' : [player],
                    })
                    return fresh_id
        except:
            print(f"Error assigning Elo id to {player}")
            print("RECOMPILE ELO!")
        print(f"Assigned ID {elo.collection.count_documents({})} to {player}")
        return elo.collection.count_documents({})
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
    def updateOnlinePlayersStats(self, onlinePlayers, offline_players, elo):
        '''onlinePlayers is a dict id --> player object'''
        '''will add new players to DB and check some stuff every 5 mins'''
        '''Will logg players off'''
 
        for id in onlinePlayers:
            player = self.collection.find_one({"account_id":id})
            if player == None:
                stats = HextoLadderstatswide(onlinePlayers[id].ladderstatswide)
                if stats_cheated(stats) or isBot(onlinePlayers[id].username):
                    continue
                else:
                    self.addToDB(onlinePlayers[id].username, onlinePlayers[id], elo)
            
            elif player['status'] == 0:
                if player['elo_id'] == -1: self.checkForAlts(player['username'], elo)
                self.collection.find_one_and_update( #player logging in
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':onlinePlayers[id].status,
                            'numLogins':player['numLogins'] + 1,
                            'last_login':time.time(),
                            'stats':HextoLadderstatswide(onlinePlayers[id].ladderstatswide),
                            'clan_id':onlinePlayers[id].clan_id,
                            'clan_tag':onlinePlayers[id].clan_tag,
                            'clan_name':onlinePlayers[id].clan_name,
                        }
                    }
                )
            else:
                if player['elo_id'] == -1: self.checkForAlts(player['username'], elo)
                self.collection.find_one_and_update( #normal update
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':onlinePlayers[id].status,
                            'stats':HextoLadderstatswide(onlinePlayers[id].ladderstatswide),
                            'clan_id':onlinePlayers[id].clan_id,
                            'clan_tag':onlinePlayers[id].clan_tag,
                            'clan_name':onlinePlayers[id].clan_name,

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
                            'stats':HextoLadderstatswide(offline_players[id].ladderstatswide),
                            'clan_id':offline_players[id].clan_id,
                            'clan_tag':offline_players[id].clan_tag,
                            'clan_name':offline_players[id].clan_name,

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
            if isBot(players[id].username): continue #bot check
            player = self.collection.find_one({'account_id':id})
            if player == None:
                self.collection.insert_one(
                    {
                        "username":players[id].username,
                        'account_id':players[id].id,
                        'status':PLAYER_STATUS[players[id].status],
                        'clan_id':players[id].clan_id,
                        'clan_tag':players[id].clan_tag,
                        'clan_name':players[id].clan_name,
                    }
                )
            else:
                self.collection.find_one_and_update(
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'status':PLAYER_STATUS[players[id].status]                  
                        }
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
                        "dme_id":games[id].dme_id,
                        'details':games[id].details(),
                        
                    }
            )
            else:
                self.collection.find_one_and_update(
                    {
                        "game_id":id
                    },
                    {
                        "$set":{
                            'details':games[id].details()
                            
                        }
                    }
                )
    def addGameToGameHistory(self, game, game_results):
        '''Adds a finished game to the history collection wite game as game object and results and res from calculate stat line function'''
        date = time.strftime("%a, %d %b %Y", time.localtime())
        entries = self.collection.count_documents({})
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
                'date':date, # Thu, 28 Jun 2001
                'entry_number' : entries+1
            }
        )
    def addGameToPlayerHistory(self, game_id, player_ids, game_history, elo, logger):
        '''add a recent game to players stats'''
        game = game_history.collection.find_one( #grab the game
                {
                    'game_id':game_id
                }
            )
        ######Calculate elo stats for the teams#####
        isTie = True if 'tie' in game['game_results'] else False
            
        if not isTie:
            teams, overall_e = self.calculateGameElo(elo, game, logger )
            teams, gamemode_e = self.calculateGameElo(elo, game, logger, type = game['gamemode'])


        ############################################
        for id in player_ids: #go through each player
            player = self.collection.find_one({'account_id': id})
            match_history = player['match_history']
            player_elo = elo.collection.find_one({"elo_id":player['elo_id']})
            username = player['username']
            streaks = player['advanced_stats']['streaks']

            match_history[str(game_id)] = player['stats']['overall']['games_played']


            per_game = per_gm(player, game)
            per_minute = per_min(player, game)
            if not isTie:
                player_elo = updateElo(username, player_elo,teams, overall_e, K=64, type = 'overall')
                player_elo = updateElo(username, player_elo,teams, gamemode_e, K=64, type = game['gamemode'])

                if game['gamemode'] == "Siege":
                    siegeStreak = streaks['siege']
                    overallStreak = streaks['overall']
                    isWin = username in teams[0]
                    if isWin:
                        siegeStreak['current_winstreak']+=1
                        siegeStreak['current_losingstreak']=0
                        overallStreak['current_winstreak']+=1
                        overallStreak['current_losingstreak']=0
                    else:
                        siegeStreak['current_winstreak']=0
                        siegeStreak['current_losingstreak']+=1
                        overallStreak['current_winstreak']=0
                        overallStreak['current_losingstreak']+=1
                    streaks['siege']['best_winstreak'] = max(streaks['siege']['best_winstreak'], siegeStreak['current_winstreak'])
                    streaks['siege']['best_losingstreak'] = max(streaks['siege']['best_losingstreak'], siegeStreak['best_losingstreak'])
                    streaks['overall']['best_winstreak'] = max(streaks['overall']['best_winstreak'], overallStreak['current_winstreak'])
                    streaks['overall']['best_losingstreak'] = max(streaks['overall']['best_losingstreak'], overallStreak['best_losingstreak'])
            
                elo.collection.find_one_and_update(
                    {'elo_id':player['elo_id']},
                    {
                        "$set":{
                            'overall':player_elo['overall'],
                            game['gamemode']:  player_elo[game['gamemode']]
                        }
                    }

                )
            self.collection.find_one_and_update(
                    {
                        "account_id":id
                    },
                    {
                        "$set":{
                            'match_history':match_history,
                            'advanced_stats.per_gm':per_game,
                            'advanced_stats.per_min':per_minute,
                            'advanced_stats.elo':{
                                'overall':player_elo['overall'],
                                'CTF': player_elo['CTF'],
                                'Siege': player_elo['Siege'],
                                'Deathmatch' :player_elo['Deathmatch'],
                            },
                            'advanced_stats.streaks':streaks

                            
                        }
                    }
                )
    def cancelGames(self, ended_games, player_stats, game_history, elo, clans, logger):
        '''Ended Games is a dict of id --> ended Game object and player stats is the DB object holding new stats'''
        '''removes ended games from the active games collection'''
        '''before we dump the game, we'll add it to the history collection'''
        for id in ended_games:
            #add to history###
            ended_games[id].end_time = time.time()
            game_results = None
            try:
                game_results = self.calculateGameStats(ended_games[id], player_stats, logger)
                ####Check for clan war with gamee results
                winnerIsClan = self.calculateClanStats(clans, player_stats, game_results, isWinner = True, game = ended_games[id], logger = logger)
                loserIsClan = self.calculateClanStats(clans, player_stats, game_results, isWinner = False, game = ended_games[id], logger = logger)
            except:
                logger.error("Game was not logged. either bot game or stat cheater")
            finally:
                self.collection.find_one_and_delete({'game_id':id})

                if game_results: #will be none if games flagged as fake 
                    game_history.addGameToGameHistory(ended_games[id], game_results)
                    player_stats.addGameToPlayerHistory(id, ended_games[id].player_ids, game_history, elo, logger)

    def calculateGameStats(self, game, player_stats, logger):

        '''returns true if the game was legit and finished, false if fake game or didnt finish'''
        'goes through each player in the game andd finds the difference between the cached stats and their updated stats'
        teams = {
            'winners':[],
            'losers':[],
            'winner_score':0,
            'loser_score':0,
        }
        total_kills = 0
        isCheating = False
        isCPU = game.isCPU
        if isCPU:
            return False
        for id in game.player_ids:
            cache= None
            updated_player_entry = player_stats.collection.find_one({'account_id':id})
            updatedStats = requests.get(f"http://103.214.110.220:8281/robo/accounts/id/{id}").json()
            playerStats = {}
            playerStats['stats'] = HextoLadderstatswide(updatedStats['ladderstatswide'])
            if len(game.cached_stats) == 0:
                return None
            else:
                cache = game.cached_stats[id]
            try:
                stat_line = calculateStatLine(updated_player_entry, playerStats, cache, game)
            except:
                logger.error(f"Problem calculating stat line for player id {id} in game id {game.id}")

            isCheating = True if stat_line['kills'] > 300 else False 
            total_kills+=stat_line['kills']
            #check to see if tie ################################
            if stat_line['game_result'] == 'tie' and 'tie' not in teams:
                teams['tie'] = []
                teams['total_score'] = 0
            #####################################################
             #check to see if disconnected ################################
            if stat_line['game_result'] == 'disconnect' and 'disconnect' not in teams:
                teams['disconnect'] = []
            #####################################################

            if game.game_mode == "CTF":
                isCheating = True if stat_line['caps'] > 50 else False
                isCheating = True if stat_line['saves'] > 50 else False

            if stat_line['game_result'] == 'win':
                teams['winners'].append(stat_line)
                #####Calculate the score of the game
                if game.game_mode == 'CTF':
                    teams['winner_score'] += stat_line['caps']
                elif game.game_mode == 'Siege':
                    teams['winner_score'] += stat_line['base_dmg']
                else:
                    teams['winner_score'] += stat_line['kills'] - stat_line['suicides']
            elif stat_line['game_result'] == 'loss':
                teams['losers'].append(stat_line)
                #####Calculate the score of the game
                if game.game_mode == 'CTF':
                    teams['loser_score'] += stat_line['caps']
                elif game.game_mode == 'Siege':
                    teams['loser_score'] += stat_line['base_dmg']
                else:
                    teams['loser_score'] += stat_line['kills'] - stat_line['suicides']
            elif stat_line['game_result'] == 'disconnect':
                teams['disconnect'].append(stat_line)
            else:
                teams['tie'].append(stat_line)
                if game.game_mode == 'CTF':
                    teams['total_score'] += stat_line['caps']
                elif game.game_mode == 'Siege':
                    teams['total_score'] += stat_line['base_dmg']
                else:
                    teams['total_score'] += stat_line['kills'] - stat_line['suicides']


        if 'total_score' in teams:
            teams['winner_score'], teams['loser_score'] = teams['total_score']//2, teams['total_score']//2
        return teams if total_kills > 0 and not isCheating else None

    def calculateClanStats(self, clans, player_stats, game_result, isWinner, game, logger):
        def getClan(playerStats, username):
            player = playerStats.collection.find_one({"username_lowercase":username.lower()})
            if not player: return None

            return player['clan_name']
        def getTeamStats(game_result, isWinner):
            teamPlayerObjects = game_result['winners' if isWinner else 'losers']
            kills = sum([player['kills'] for player in teamPlayerObjects])
            deaths = sum([player['deaths'] for player in teamPlayerObjects])
            return{
                "kills":kills,
                'deaths':deaths,
                'wins': 1 if isWinner else 0,
                'losses': 0 if isWinner else 1
            }

        def updateClanStats(clans, gameResults, clanName, gameId, mode):
            modeMapper={
                "CTF":"ctf",
                "Siege":"siege",
                "Deathmatch":"tdm"
            }
            clanDoc= clans.collection.find_one({"clan_name":clanName})
            if not clanDoc: return False

            overall = dict(Counter(clanDoc['advanced_stats']['overall']) + Counter(gameResults))
            gamemode = dict(Counter(clanDoc['advanced_stats'][modeMapper[mode]]) + Counter(gameResults))
            history = clanDoc['game_history']
            history.append(gameId)

            clans.collection.find_one_and_update(
                {"clan_name":clanName},
                {
                    "$set":{
                        f"advanced_stats.{modeMapper[mode]}":gamemode,
                        'advanced_stats.overall':overall,
                        'game_history':history,
                    }
                }
            )
            return True

        if not game_result: return None
        if 'disconnect' in game_result or 'tie' in game_result: return None

        team = [player['username'].lower() for player in game_result['winners' if isWinner else 'losers']]
        if len(team) <2 : return None

        clan = None
        i=0
        for username in team:
            playerClan = getClan(player_stats, username)

            if playerClan == None or playerClan == '':
                logger.debug(f"Team {team} is not a clan")
                return False
            
            if i == 0:
                clan = playerClan
            else:
                if clan != playerClan:
                    logger.debug(f"Team {team} is not a clan")
                    return False
            i+=1
        
        #check for leader
        clanDocument = clans.collection.find_one({"clan_name":clan})
        if not clanDocument:
            logger.debug(f"Clan {clan} not found in uyatracker")
            return False

        # clanLeader = clanDocument['leader_account_name'].lower()
        # if clanLeader not in team:
        #     logger.debug(f"Clan {clan}'s leader {clanLeader} was not present in team {team}")
        #     return False


        gameStats = getTeamStats(game_result, isWinner)
        updated = updateClanStats(clans, gameStats, clan, gameId = game.id, mode = game.game_mode)
        logger.debug(f"Team {team} is a clan, able to update stats = {updated}")
        return True

    def calculateGameElo(self, elo, game, logger, type = 'overall'):
        results = game['game_results']
        winner_names = [player['username'] for player in results['winners']]
        loser_names = [player['username'] for player in results['losers']]
        winner_elo, loser_elo = 0, 0
        for name in winner_names:
            try:
                player = self.collection.find_one({'username': name})
                if player['elo_id'] == -1:
                    logger.warning("Player with elo id of -1 finished a game")
                    self.checkForAlts(name, elo)
                else:
                    player_elo = elo.collection.find_one({'elo_id':player['elo_id']})[type]
                winner_elo+=player_elo
            except:
                logger.critical("Error Grabbing Elo of {} with id {}".format(name, player['elo_id']))
                logger.critical("need to recompile elo!!")
                winner_elo+=1200

        for name in loser_names:
            try:
                player = self.collection.find_one({'username': name})
                if player['elo_id'] == -1:
                    logger.warning("Player with elo id of -1 finished a game")
                    self.checkForAlts(name, elo)
                else:
                    player_elo = elo.collection.find_one({'elo_id':player['elo_id']})[type]
                loser_elo+=player_elo  
            except:
                logger.critical("Error Grabbing Elo of {} with id {}".format(name, player['elo_id']))
                logger.critical("need to recompile elo!!")
                loser_elo+=1200

        loser_elo/=len(loser_names) if len(loser_names) > 0 else 1
        winner_elo/=len(winner_names) if len(winner_names) > 0 else 1
        winner_e, loser_e = getExpected(winner_elo,loser_elo)
        return (winner_names, loser_names), (winner_e, loser_e)
    def addNewClan(self, clan_id):
        '''add new clan to DB given clan id'''
        CLANS_API = 'http://103.214.110.220:8281/robo/clans/id' #/id
        existing_clan = self.collection.find_one({'clan_id':clan_id})
        if existing_clan != None:
            #This executes if a new clan has the same ID as a deleted clan
            self.collection.find_one_and_delete({'clan_id':clan_id})
        try:
            res = requests.get(f"{CLANS_API}/{clan_id}").json()
        except:
            res = {}
        if len(res) > 0:
            self.collection.insert_one(
                    {
                        "clan_name":res['clan_name'],
                        'clan_id':res['clan_id'],
                        'leader_account_id':res['leader_account_id'],
                        'leader_account_name':res['leader_account_name'],
                        "stats": HexToClanstatswide(res['clan_statswide']),
                        'clan_tag': res['clan_tag'],
                        'member_names':[],
                        'member_ids':[],
                        'clan_name_lower': res['clan_name'].lower()         
                    }
                )


    def updateClans(self, player, player_stats):
        '''
        Scan through all the clans of people on
        if the clan is new, add it into the DB
        if the player left an old clan, we take him out of it and put into new one'''
        try:
            cached_player = player_stats.collection.find_one({"account_id":player.id}) #DB information

            if cached_player!= None:

                cached_clan_id = cached_player['clan_id']
                cached_clan_name = cached_player['clan_name']

                if player.clan_id != -1:
                    clan = self.collection.find_one({'clan_name':player.clan_name})
                    if clan == None:
                        self.addNewClan(player.clan_id)
                
                
                old_clan = self.getClan(cached_clan_id)
                if old_clan != None:
                    if old_clan['clan_name'] != player.clan_name or old_clan['clan_id'] != player.clan_id:
                        updatedIds = old_clan['member_ids']
                        updatedIds.remove(player.id)
                        updatedNames = old_clan['member_names']
                        updatedNames.remove(player.username)

                        
                        if len(updatedIds) > 0:
                            self.collection.find_one_and_update(
                                {
                                    "clan_id":old_clan['clan_id']
                                },
                                {
                                    "$set":{
                                        'member_ids':updatedIds,
                                        'member_names':updatedNames                  
                                    }
                                }
                            )
                        else:
                            self.collection.find_one_and_delete({"clan_id":old_clan['clan_id']})
                    elif old_clan['clan_tag'] != player.clan_tag:
                        self.collection.find_one_and_update(
                            {
                                'clan_id':player.clan_id
                            },
                            {
                            "$set":{
                                    'clan_tag':player.clan_tag             
                                }
                            }
                        )


                if player.clan_id != cached_clan_id or player.clan_name != cached_clan_name:
                    new_clan = self.getClan(player.clan_id)
                    updatedIds = new_clan['member_ids']
                    updatedNames = new_clan['member_names']

                    if player.id not in updatedIds:
                        updatedIds.append(player.id)
                        updatedNames.append(player.username)
                    self.collection.find_one_and_update(
                            {
                                "clan_id":player.clan_id
                            },
                            {
                                "$set":{
                                    'member_ids':updatedIds,
                                    'member_names':updatedNames                  
                                }
                            }
                        )
                
                if player.clan_id == cached_clan_id and player.clan_name == cached_clan_name and player.clan_id != -1:
                    current_clan = self.getClan(player.clan_id)
                    ids = current_clan['member_ids']
                    names = current_clan['member_names']
                    update = False

                    if player.id not in ids:
                        ids.append(player.id)
                        update = True
                    
                    if player.username not in names:
                        names.append(player.username)
                        update = True

                    if update:
                        self.collection.find_one_and_update(
                            {
                                "clan_id":player.clan_id
                            },
                            {
                                "$set":{
                                    'member_ids':ids,
                                    'member_names':names                  
                                }
                            }
                        )






                
        except Exception as e:
            print(f"Error on player: {player.username}, clan {player.clan_id}\
| {player.clan_name}...with error as {e}")

    def getClan(self, id):
        '''get a clan object from id'''
        return self.collection.find_one({"clan_id":id})
    def checkForAlts(self, player, elo):
        url = 'http://103.214.110.220:8281/robo/alts/{}'
        encoded_name = urllib.parse.quote(player)
        accounts = requests.get(url.format(encoded_name))

        accounts=accounts.json() if accounts.status_code == 200 else [player]
        if accounts == '[]' or len(accounts) == 1:
            fresh_id = elo.collection.count_documents({})

            elo.collection.insert_one({
                'elo_id':fresh_id,
                'overall':1200,
                'CTF':1200,
                "Siege":1200,
                'Deathmatch':1200,
                'accounts' : [player],
            })
            self.collection.find_one_and_update({
                'username':player
            },
            {
                '$set':{
                    'elo_id':fresh_id
                }
            })
            return None
        for i, alt in enumerate(accounts):
            alt_id = self.collection.find_one({'username':alt})
            if alt_id != None or i <= len(accounts) - 1:
                if alt_id == None: continue
                alt_id = alt_id['elo_id']
                eloAccount = elo.collection.find_one({'elo_id':alt_id})
                if eloAccount == None: continue
                alts = eloAccount['accounts']
                alts.append(player)
                elo.collection.find_one_and_update(
                    {
                        'elo_id':alt_id
                    },
                    {
                        '$set':{
                            'accounts':alts
                        }
                    }
                )
                self.collection.find_one_and_update({
                    'username':player
                },
                {
                    '$set':{
                        'elo_id':alt_id
                    }
                })
                return None
            fresh_id = elo.collection.count_documents({})
            elo.collection.insert_one({
            'elo_id': fresh_id,
            'overall':1200,
            'CTF':1200,
            "Siege":1200,
            'Deathmatch':1200,
            'accounts' : [player],
            })
            self.collection.find_one_and_update({
                'username':player
            },
            {
                '$set':{
                    'elo_id':fresh_id
                }
            })
            return None
        print(f"Error assigning Elo id to {player} after completed game")
        return elo.collection.count_documents({})
                




def getExpected(r1, r2):
    r1 = 10**(r1/400)
    r2 = 10**(r2/400)

    e1 = r1/(r1+r2)
    e2 = r2/(r1+r2)

    return e1, e2
def getAdjusted(old, expected, K, win=1):
    '''win = 1 if won'''
    return int(old + (K * (win - expected)))    
def stats_cheated(stats):
    '''checks if a players total stats are cheated
    check1 : KD is not more than 10
    check2: the amount of suicides is not 10x more than kills which is ridiculous'''
    return True if (stats['overall']['kills'] // (stats['overall']['deaths']+1) > 10) \
        or (stats['overall']['suicides'] // (stats['overall']['kills']+1) > 10) else False   

def per_gm(player, game):
    stats = player['stats']['overall']
    ctf = player['stats']['ctf']
    weapons = player['stats']['weapons']

    game_map = game['map']
    maps = player['advanced_stats']['per_gm']['maps']
    maps[game_map] +=1

    flux_gms= player['advanced_stats']['per_gm']['flux_gms']
    blitz_gms= player['advanced_stats']['per_gm']['grav_gms']
    grav_gms= player['advanced_stats']['per_gm']['grav_gms']

    flux_gms = flux_gms + 1 if 'Flux' in game['weapons'] else flux_gms
    blitz_gms = blitz_gms + 1 if 'Blitz' in game['weapons'] else blitz_gms
    grav_gms = grav_gms + 1 if 'Gravity Bomb' in game['weapons'] else grav_gms

    try:
        per_game = {
            'kills/death': round(stats['kills'] / stats['deaths'], 2),
            'wins/loss': round(stats['wins'] / stats['losses'], 2),
            'kills/gm' : round(stats['kills'] / stats['games_played'], 2),
            'deaths/gm' : round(stats['deaths'] / stats['games_played'], 2),
            'suicides/gm' : round(stats['suicides'] / stats['games_played'], 2),
            'caps/gm' : round(ctf['ctf_caps']/ (ctf['ctf_wins'] + ctf['ctf_losses']), 2),
            'saves/gm' : round(ctf['ctf_saves']/ (ctf['ctf_wins'] + ctf['ctf_losses']), 2),
            'flux_kills/gm' : round(weapons['flux_kills'] / flux_gms, 2),
            'blitz_kills/gm' : round(weapons['blitz_kills'] / blitz_gms, 2),
            'gravity_bomb_kills/gm' : round(weapons['gravity_bomb_kills'] / grav_gms, 2),
            'flux_deaths/gm' : round(weapons['flux_deaths'] / flux_gms, 2),
            'blitz_deaths/gm' : round(weapons['blitz_deaths'] / blitz_gms, 2),
            'gravity_bomb_deaths/gm' : round(weapons['gravity_bomb_deaths'] / grav_gms, 2),
            'flux_gms':flux_gms,
            'grav_gms': grav_gms,
            'blitz_gms' :blitz_gms,
            'maps':maps
        }
    except:
        per_game = {
            'kills/death':0,
            'wins/loss':0,
            'kills/gm' : 0,
            'deaths/gm' : 0,
            'suicides/gm' : 0,
            'caps/gm' : 0,
            'saves/gm' : 0,
            'flux_kills/gm' :0,
            'blitz_kills/gm' : 0,
            'gravity_bomb_kills/gm' : 0,
            'flux_deaths/gm' : 0,
            'blitz_deaths/gm' : 0,
            'gravity_bomb_deaths/gm' :0,
            'flux_gms':flux_gms,
            'grav_gms': grav_gms,
            'blitz_gms' :blitz_gms,
            'maps' : maps,
        }

    return per_game

def per_min(player, game):
    stats = player['stats']['overall']
    ctf = player['stats']['ctf']
    weapons = player['stats']['weapons']

    ctf_mins = player['advanced_stats']['per_min']['ctf_mins']
    siege_mins = player['advanced_stats']['per_min']['siege_mins']
    tdm_mins = player['advanced_stats']['per_min']['deathmatch_mins']
    flux_mins= player['advanced_stats']['per_min']['flux_mins']
    blitz_mins= player['advanced_stats']['per_min']['grav_mins']
    grav_mins= player['advanced_stats']['per_min']['grav_mins']

    ctf_mins = ctf_mins + game['minutes'] if game['gamemode'] == 'CTF' else ctf_mins
    siege_mins = siege_mins + game['minutes'] if game['gamemode'] == 'Siege' else siege_mins
    tdm_mins = tdm_mins + game['minutes'] if game['gamemode'] == 'Deathmatch' else tdm_mins

    game_map = game['map']
    game_minutes = game['minutes']
    minutes = player['advanced_stats']['per_min']['total_mins'] + game_minutes

    maps = player['advanced_stats']['per_min']['maps']
    maps[game_map] += game_minutes


    flux_mins = flux_mins + game_minutes if 'Flux' in game['weapons'] else flux_mins
    blitz_mins = blitz_mins + game_minutes if 'Blitz' in game['weapons'] else blitz_mins
    grav_mins = grav_mins + game_minutes if 'Gravity Bomb' in game['weapons'] else grav_mins

    try:
        per_minute = {
            'kills/min' : round(stats['kills'] / minutes, 2),
            'deaths/min' : round(stats['deaths'] / minutes, 2),
            'suicides/min' : round(stats['suicides'] / minutes, 2),
            'avg_game_length' : round(minutes/ stats['games_played'], 2),
            'caps/min' : round(ctf['ctf_caps']/ ctf_mins, 2),
            'saves/min' : round(ctf['ctf_saves']/ ctf_mins, 2),
            'flux_kills/min' : round(weapons['flux_kills'] / flux_mins, 2),
            'blitz_kills/min' : round(weapons['blitz_kills'] / blitz_mins, 2),
            'gravity_bomb_kills/min' : round(weapons['gravity_bomb_kills'] / grav_mins, 2),
            'flux_deaths/min' : round(weapons['flux_deaths'] / flux_mins, 2),
            'blitz_deaths/min' : round(weapons['blitz_deaths'] / blitz_mins, 2),
            'gravity_bomb_deaths/min' : round(weapons['gravity_bomb_deaths'] / grav_mins, 2),
            'total_mins':minutes,
            'flux_mins':flux_mins,
            'blitz_mins':blitz_mins,
            'grav_mins':grav_mins,
            'ctf_mins': ctf_mins,
            'siege_mins': siege_mins,
            'deathmatch_mins': tdm_mins,
            'maps':maps
        }
    except:
        per_minute = {
            'kills/min' : 0,
            'deaths/min' : 0,
            'suicides/min' : 0,
            'avg_game_length' : 0,
            'caps/min' : 0,
            'saves/min' : 0,
            'flux_kills/min' : 0,
            'blitz_kills/min' : 0,
            'gravity_bomb_kills/min' : 0,
            'flux_deaths/min' : 0,
            'blitz_deaths/min' : 0,
            'gravity_bomb_deaths/min' : 0,
            'total_mins':minutes,
            'flux_mins':flux_mins,
            'blitz_mins':blitz_mins,
            'grav_mins':grav_mins,
            'ctf_mins': ctf_mins,
            'siege_mins': siege_mins,
            'deathmatch_mins': tdm_mins,
            'maps':maps
        }

    return per_minute

def updateElo(username, player_elo, teams, e, K=64, type = 'overall'):
    '''
    player_elo = elo mongo doc for player
    teams[0] = winning team
    teams[1] = losing teams
    e[0] = winner_expected value
    e[1] = loser_expected_value
    '''



    if username in teams[0]:
        player_elo[type] = getAdjusted(player_elo[type], e[0], K, 1)
    else:
        player_elo[type] = getAdjusted(player_elo[type], e[1], K, 0)

    return player_elo

def isBot(username):
    '''bot names have prefixes of cpu so return false if the prefix is not cpu'''
    if len(username) <3: return False

    return username[:3].lower() == 'cpu'




# client = pymongo.MongoClient("mongodb+srv://nick:{}@cluster0.yhf0e.mongodb.net/UYA-Bot?retryWrites=true&w=majority".format(mongoPW))
# print(client.list_database_names())
# db = client['uya-bot']
# collection = db['time-played']




# for i in player_stats.collection.find().sort([('stats.squats',1)]):
#     print(i)


      



