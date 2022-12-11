from mongodb import Database
import datetime
from Parsers.ToLadderstatswide import HextoLadderstatswide
import requests

stats = Database("UYA", "Player_Stats")
legacy = Database("UYA", "Game_History")
# legacyGames = list(legacy.collection.find({"entry_number":{"$gte":4000}}))
# idsToUsername = {}
# usernameToIds = {}
# for player in stats.collection.find():
#     # idsToUsername[player['account_id']] = player['username_lowercase']
#     # print(f"is {player['account_id']} = {player['username_lowercase']}?")
#     # dec = input()
#     # if dec != "n":
#     #     print("k thanks")
#     # else:
#     #     break
#     username = player['username_lowercase']
#     if username in usernameToIds:
#         a = usernameToIds[username]
#         b = player['account_id']
#         print(f"{username} | {a} | {b}")
#         rightId = input()
#         usernameToIds[username] = rightId

#         stats.collection.delete_one({
#             "username_lowercase":username,
#             'account_id': b if rightId == a else a
#         })
#     else:
#         usernameToIds[username] = player['account_id']
#         idsToUsername[player['account_id']] = username

# today = datetime.datetime.now()
# deleteGames = [1667344287.8746]
# for game in legacyGames:
#     date = game['date']
#     date = datetime.datetime.strptime(date, "%a, %d %b %Y")
#     if abs((date-today).days) > 5:
#         continue
#     usernames = []
#     try:
#         usernames = [idsToUsername[i] for i in game['player_ids']]
#     except:
#         print(f"someone not found in {game['player_ids']} | {game['game_id']} | {game['date']}")


#     if abs((date-today).days) > 5:
#         continue
#     else:
#         print(f"{game['map']} | {game['gamemode']} | {game['game_id']}")
#         print(usernames)
#         print("keep game?")
#         dec = input()
#         if dec == 'n':
#             legacy.collection.delete_one({"game_id": game['game_id']})
#             deleteGames.append(game['game_id'])



# print(deleteGames)

# deleteGames = [1667344287.8746, 1667348139.953, 1667351597.0257, 1667353957.3858, 1667378885.3478, 1667379591.9879, 1667388755.118, 
# 1667389869.7181, 1667406900.3887, 1667478365.052, 1667478803.473, 1667484839.975, 1667642553.321, 1667643776.732, 1667655571.8217, 
# 1667656113.5318, 1667657196.0422, 1667658140.1824, 1667658922.953, 1667659505.2831, 1667659943.7833, 1667660510.4438, 1667661202.474, 
# 1667661707.8641, 1667662329.1342, 1667662766.2245, 1667663117.346, 1667663731.7647, 1667664954.15]

# for player in stats.collection.find():
#     games = player['match_history']
#     removes = set()
#     last = -1
#     for gameId, gameNum in games.items():
#         if gameNum < last or gameId in deleteGames:
#             removes.add(gameId)
#             print(f"removing gameId {gameId} from {player['username']}")
#         else:
#             last = gameNum
#     for remove in removes:
#         del games[remove]

#     stats.collection.find_and_modify({
#         "username":player['username']
#     },{
#         "$set":{
#             'match_history':games
#         }
#     })


playerIdToGames={}
for game in legacy.collection.find():
    gameId = game['game_id']
    for playerId in game['player_ids']:
        if playerId not in playerIdToGames:
            playerIdToGames[playerId] = {}

        playerIdToGames[playerId][str(gameId)] = len(playerIdToGames[playerId])
    






i  = 1
while i < 2500:
    if i not in playerIdToGames:
        print(f"{i} never played a game, no update")
        i+=1
        continue
    url = f"http://103.214.110.220:8281/robo/accounts/id/{i}"
    info = requests.get(url = url).json()
    if 'ladderstatswide' not in info:
        i+=1
        continue

    parsed = HextoLadderstatswide(info['ladderstatswide'])

    player = stats.collection.find_one({"account_id":info["account_id"]})
    if player == None:
        print(f"{info['username']} not in uyatracker")
    elif player['username_lowercase'] != info['username'].lower():
        print(f"mismatch with {player['username_lowercase']} and {info['username'].lower()}")
    else:
        print(f"{i} updated!")
        stats.collection.find_one_and_update(
            {'account_id': i},
            {
                "$set":{
                    "stats":parsed,
                    "match_history":playerIdToGames[i]
                }
            }
        )
    i+=1

