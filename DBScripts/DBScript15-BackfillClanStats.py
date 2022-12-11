# '''
# For stats I think we want wins, losses, kills, deaths - newStats?
# break it down by gamemode?

# we also want a game history
# '''
import copy
from mongodb import Database
from collections import Counter

gameModeStats = {
    'kills':0,
    'deaths':0,
    "wins":0,
    "losses":0
}

newStats = {
    "ctf":copy.deepcopy(gameModeStats),
    "siege":copy.deepcopy(gameModeStats),
    "tdm":copy.deepcopy(gameModeStats),
    "overall":copy.deepcopy(gameModeStats)
}

modeMapper={
    "CTF":"ctf",
    "Siege":"siege",
    "Deathmatch":"tdm"
}

player_stats = Database("UYA","Player_Stats")
players_online = Database("UYA","Players_Online")
game_history = Database("UYA", "Game_History")
games_active = Database("UYA","Games_Active")
clans = Database("UYA", "Clans_Backup")


def calculateClanStats(clans, player_stats, game_result, isWinner, mode, gameId):
    def getClan(playerStats, username):
        player = playerStats.collection.find_one({"username_lowercase":username.lower()})
        if not player: return None

        return player['clan_name']

    def updateStore(clans, stats, clanName, mode, gameId):
        if clanName == 'Team Skeet':
            print("g")
        clanDoc= clans.collection.find_one({"clan_name":clanName})
        if not clanDoc: return 

        overall = dict(Counter(clanDoc['advanced_stats']['overall']) + Counter(stats))
        gamemode = dict(Counter(clanDoc['advanced_stats'][modeMapper[mode]]) + Counter(stats))
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

    def getTeamStats(result):
        kills = sum([player['kills'] for player in result])
        deaths = sum([player['deaths'] for player in result])
        return{
            "kills":kills,
            'deaths':deaths,
            'wins': 1 if isWinner else 0,
            'losses': 0 if isWinner else 1
        }

    team = [player['username'].lower() for player in game_result['winners' if isWinner else 'losers']]
    if len(team) < 2: return None

    clan = None
    i=0
    for username in team:
        if 'not rev' == username: return False
        playerClan = getClan(player_stats, username)
        if playerClan == None or playerClan == '':
            return False
        
        if i == 0:
            clan = playerClan
        else:
            if clan != playerClan:
                return False
        i+=1
    
    #check for leader
    clanDocument = clans.collection.find_one({"clan_name":clan})
    if not clanDocument:
        return False

    # clanLeader = clanDocument['leader_account_name'].lower()
    # if clanLeader not in team:
    #     return False


    print(f"Team {team} is a clan {clan}")

    stats = getTeamStats(game_result['winners' if isWinner else 'losers'])
    updateStore(clans, stats, clan, mode, gameId)
    return True

for clan in clans.collection.find():
    clans.collection.find_one_and_update({"clan_name":clan['clan_name']},
    {
        "$set":{
            "advanced_stats":newStats,
            "game_history":[]
        }
    })

for game in game_history.collection.find({"entry_number":{"$gte":1500}}):
    results = game['game_results']
    if 'disconnect' in results: continue

    mode = game['gamemode']
    calculateClanStats(clans, player_stats, results, True, mode, game['game_id'])
    calculateClanStats(clans, player_stats, results, False, mode, game['game_id'])
    