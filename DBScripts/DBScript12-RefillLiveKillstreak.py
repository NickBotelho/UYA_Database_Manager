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
    statsStore = Database("UYA", "Player_Stats")
    legacy = Database("UYA", "Game_History")
    nameToStreaks = {}
    
    for game in games.collection.find():
        legacyGame = legacy.collection.find_one({"game_id":game["game_id"]})
        if not legacyGame: continue
        mode = legacyGame["gamemode"].lower()

        for player, stats in game['results'].items():
            if player not in nameToStreaks:
                playerStats = statsStore.collection.find_one({"username_lowercase":player.lower()})
                streaks = {
                    "overall":playerStats['advanced_stats']['streaks']['overall']['bestKillstreak'],
                    "ctf":playerStats['advanced_stats']['streaks']['ctf']['bestKillstreak'],
                    "siege":playerStats['advanced_stats']['streaks']['siege']['bestKillstreak'],
                    "deathmatch":playerStats['advanced_stats']['streaks']['deathmatch']['bestKillstreak']
                }
                nameToStreaks[player] = streaks
            nameToStreaks[player]['overall'] = max(nameToStreaks[player]['overall'], stats['bestKillstreak'])
            nameToStreaks[player][mode] = max(nameToStreaks[player][mode], stats['bestKillstreak'])
    for name, killstreaks in nameToStreaks.items():
        statsStore.collection.find_one_and_update({
            "username_lowercase":name.lower()
        },{
            "$set":{
                "advanced_stats.streaks.overall.bestKillstreak":killstreaks['overall'],
                "advanced_stats.streaks.ctf.bestKillstreak":killstreaks['ctf'],
                "advanced_stats.streaks.siege.bestKillstreak":killstreaks['siege'],
                "advanced_stats.streaks.deathmatch.bestKillstreak":killstreaks['deathmatch'],
            }
        })

run()
# checkForDupes()


