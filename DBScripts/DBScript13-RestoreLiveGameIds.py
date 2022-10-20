from mongodb import Database
import blankRatios
import copy
def defineQuery(game):
    if len(str(game['game_id'])) <= 3:
        for player, info in game['results'].items():
            if info['team'] == game['winning_team']:
                queryPlayerStats = info
                queryPlayer = player
                return queryPlayer, queryPlayerStats            
    return 0, 0
def run():
    for game in legacyGames:
        # print(f"Examining game {game['game_id']} | {game['entry_number']}")
        results = game['game_results']
        if 'winners' not in results: continue
        winners = results['winners']
        for player in winners:
            if player['username'] == queryPlayer:
                if player['kills'] == queryInfo['kills'] and player['deaths'] == queryInfo['deaths']:
                    print(f"Mapping suggested for {game['game_id']} to live game {currentGame['game_id']}")
                    mappings[currentGame['game_id']] = game['game_id']


mappings= {}
games = Database("UYA", "LiveGame_History")
stats = Database("UYA", "Player_Stats")
legacy = Database("UYA", "Game_History")
liveGames = list(games.collection.find())
legacyGames = list(legacy.collection.find({"entry_number":{"$gte":2500}}))
while len(liveGames) > 0:
    currentGame = liveGames.pop(0)
    queryPlayer, queryInfo = defineQuery(currentGame)
    if queryInfo == 0: break
    run()

for badId, realId in mappings.items():
    games.collection.find_one_and_update({
        "game_id":badId
    },
    {
        "$set":{
            "game_id":realId
        }
    })
# checkForDupes()


