from mongodb import Database
import copy
STREAK_CONTRACT = {
    'current_winstreak':0,
    'best_winstreak':0,
    'current_losingstreak':0,
    'best_losingstreak':0,
    'bestKillstreak':0,
    'bestDeathstreak':0,
}
def parseBitstring(bitstring):
    currWins, currLosses = 0, 0
    bestWins, bestLosses = 0, 0

    for game in bitstring:
        if game == '1':
            currWins+=1
            bestWins = max(currWins, bestWins)
            currLosses = 0
        else:
            currLosses+=1
            bestLosses = max(currLosses, bestLosses)
            currWins = 0

    return bestWins, bestLosses, currWins, currLosses
def updateTeam(game, container, result='0', type='disconnect'):
    if type in game['game_results']:
        winners = game['game_results'][type]
        for player in winners:
            if player['username'] not in container:
                container[player['username']] = result
            else:
                container[player['username']] += result
    return container
def run():
    nameToBitstring={}
    nameToBitstringCtf={}
    nameToBitstringSiege={}
    nameToBitstringTdm={}
    games = Database("UYA", "Game_History")
    stats = Database("UYA", "Player_Stats_Backup")
    i=0
    print("Backcalculating streaks...")
    for game in games.collection.find():
        if i%500 == 0: print(f"{i} Games...")
        if 'winners' in game['game_results']:
            nameToBitstring = updateTeam(game, nameToBitstring, '1', 'winners')
            if game['gamemode'] == "CTF":
                nameToBitstringCtf = updateTeam(game, nameToBitstringCtf, "1", 'winners')
            elif game['gamemode'] == "Siege":
                nameToBitstringSiege = updateTeam(game, nameToBitstringSiege, "1", 'winners')
            else:
                nameToBitstringTdm = updateTeam(game, nameToBitstringTdm, "1", 'winners')

        if 'losers' in game['game_results']:
            nameToBitstring = updateTeam(game, nameToBitstring, '0', 'losers')
            if game['gamemode'] == "CTF":
                nameToBitstringCtf = updateTeam(game, nameToBitstringCtf, "0", 'losers')
            elif game['gamemode'] == "Siege":
                nameToBitstringSiege = updateTeam(game, nameToBitstringSiege, "0", 'losers')
            else:
                nameToBitstringTdm = updateTeam(game, nameToBitstringTdm, "0", 'losers')
        if 'disconnect' in game['game_results']:
            nameToBitstring = updateTeam(game, nameToBitstring, '0', 'disconnect')
            if game['gamemode'] == "CTF":
                nameToBitstringCtf = updateTeam(game, nameToBitstringCtf, "0", 'disconnect')
            elif game['gamemode'] == "Siege":
                nameToBitstringSiege = updateTeam(game, nameToBitstringSiege, "0", 'disconnect')
            else:
                nameToBitstringTdm = updateTeam(game, nameToBitstringTdm, "0", 'disconnect')
        i+=1


    # print("Parsing bitstrings and updating players...")
    # for name in nameToBitstring:
    #     contract = copy.deepcopy(STREAK_CONTRACT)
    #     streaks = parseBitstring(nameToBitstring[name])
    #     contract['best_winstreak'] = streaks[0]
    #     contract['best_losingstreak'] = streaks[1]
    #     contract['current_winstreak'] = streaks[2]
    #     contract['current_losingstreak'] = streaks[3]
    #     stats.collection.find_one_and_update({
    #         "username":name
    #     },
    #     {
    #         "$set":{
    #             "advanced_stats.streaks": contract
    #         }
    #     })

    print("Filling in player...")
    for player in stats.collection.find():
        name = player['username']
        contract = copy.deepcopy(STREAK_CONTRACT)
        contractCtf = copy.deepcopy(STREAK_CONTRACT)
        contractSiege = copy.deepcopy(STREAK_CONTRACT)
        contractTdm = copy.deepcopy(STREAK_CONTRACT)

        if name in nameToBitstring:
            streaks = parseBitstring(nameToBitstring[name])
            contract['best_winstreak'] = streaks[0]
            contract['best_losingstreak'] = streaks[1]
            contract['current_winstreak'] = streaks[2]
            contract['current_losingstreak'] = streaks[3]

        if name in nameToBitstringCtf:
            streaks = parseBitstring(nameToBitstringCtf[name])
            contractCtf['best_winstreak'] = streaks[0]
            contractCtf['best_losingstreak'] = streaks[1]
            contractCtf['current_winstreak'] = streaks[2]
            contractCtf['current_losingstreak'] = streaks[3]

        if name in nameToBitstringSiege:
            streaks = parseBitstring(nameToBitstringSiege[name])
            contractSiege['best_winstreak'] = streaks[0]
            contractSiege['best_losingstreak'] = streaks[1]
            contractSiege['current_winstreak'] = streaks[2]
            contractSiege['current_losingstreak'] = streaks[3]

        if name in nameToBitstringTdm:
            streaks = parseBitstring(nameToBitstringTdm[name])
            contractTdm['best_winstreak'] = streaks[0]
            contractTdm['best_losingstreak'] = streaks[1]
            contractTdm['current_winstreak'] = streaks[2]
            contractTdm['current_losingstreak'] = streaks[3]


        stats.collection.find_one_and_update({
            "username":name
        },
        {
            "$set":{
                "advanced_stats.streaks":{
                    'overall':contract,
                    'ctf':contractCtf,
                    'siege':contractSiege,
                    'deathmatch':contractTdm,
                }
            }
        })



    
run()

# stats = Database("UYA", "Player_Stats_Backup")
# for player in stats.collection.find().sort("advanced_stats.streaks.overall.best_winstreak", -1).limit(10):
#     print(player['username'], player['advanced_stats']['streaks']['overall']['best_winstreak'])

