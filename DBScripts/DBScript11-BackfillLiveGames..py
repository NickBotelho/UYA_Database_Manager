from mongodb import Database
import blankRatios
import copy
def isReal(game):
    return game['duration_minutes'] > 2 and len(game['results']) > 1
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
def getAverageDict(existing, games):
    new = {}
    for key in existing:
        if type(existing[key]) == dict:
            new[key] = getAverageDict(existing[key], games)
        elif type(existing[key]) == int or type(existing[key]) == float:
            new[key] = round(existing[key] / games, 2)
    return new
def getPerMinDict(existing, totalMins):
    new = {}
    for key in existing:
        if type(existing[key]) == dict:
            new[key] = getPerMinDict(existing[key], totalMins)
        elif type(existing[key]) == int or type(existing[key]) == float:
            new[key] = round(existing[key] / totalMins, 2)
    return new
def updatePlayer(player, game):
    pass


def run():
    games = Database("UYA", "LiveGame_History")
    stats = Database("UYA", "Player_Stats")
    usernameToStats = {}

    #accumulate
    for game in games.collection.find():
        if not isReal(game): continue

        playerNames = [name.lower() for name in list(game['results'].keys())]
        playerNameKeys = [name for name in list(game['results'].keys())]
        for i, username in enumerate(playerNames):
            if username not in usernameToStats:
                usernameToStats[username] = {
                    'live':copy.deepcopy(blankRatios.blank_live_contract),
                    'live/gm':copy.deepcopy(blankRatios.blank_live_contract),
                    'live/min':copy.deepcopy(blankRatios.blank_live_contract),
                }
            playerResults = game['results'][playerNameKeys[i]]
            del playerResults['killHeatMap']
            del playerResults['deathHeatMap']
            del playerResults['nonPlayerDeathHeatMap']
            del playerResults['kill_info']
            del playerResults['death_info']
            del playerResults['disconnected']
            del playerResults['team']
            del playerResults['bestKillstreak']
            usernameToStats[username]['live'] = mergeDicts(usernameToStats[username]['live'], playerResults)
            usernameToStats[username]['live']['live_games']+=1  
            usernameToStats[username]['live']['live_seconds']+=game['duration_minutes'] * 60 + game['duration_seconds'] 

    for name, player in usernameToStats.items():
        player['live/gm'] = getAverageDict(player['live'], player['live']['live_games'])
        player['live/min'] = getPerMinDict(player['live'], player['live']['live_seconds']//60)
        player['live/gm']['live_games'] = player['live']['live_games']
        player['live/min']['live_games'] = player['live']['live_games']
        player['live/gm']['live_seconds'] = player['live']['live_seconds']
        player['live/min']['live_seconds'] = player['live']['live_seconds']
        stats.collection.find_one_and_update(
            {
                'username_lowercase':name
            },
            {
                "$set":{
                    "advanced_stats.live":player['live'],
                    "advanced_stats.live/gm":player['live/gm'],
                    "advanced_stats.live/min":player['live/min'],
                }
            }
        )



run()
# checkForDupes()


