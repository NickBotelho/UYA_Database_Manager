from CalculateStatLine import calculateStatLine
from mongodb import Database
def rating(kills, deaths, flux_kills, flags):
        flag_bonus = 8
        rating = ((kills+(flag_bonus*flags))/deaths) * (flux_kills/kills)
        return rating

def calculateAdvancedStats(player):
    '''player is a mongoDB document for a player'''
    res = {}
    kills = player['stats']['overall']['kills']
    deaths = player['stats']['overall']['deaths']
    flux_kills = player['stats']['weapons']['flux_kills']
    blitz_kills = player['stats']['weapons']['blitz_kills']
    flags = player['stats']['ctf']['ctf_caps']
    res['k/d'] = round(kills/deaths, 2)


    res['flux_usage'] = round(flux_kills/kills, 2)
    res['flux/blitz_ratio'] = round(flux_kills/blitz_kills, 2)



    return res
    

    



player_stats = Database("UYA","Player_Stats")
nick = player_stats.collection.find_one({'account_id': 18})
print(calculateAdvancedStats(nick))
game_history = Database("UYA", "Game_History")

print(game_history.collection.count())
# for player in player_stats.collection.find().sort():
#     username = player['username']
#     player_stats.collection.find_one_and_update(
#         {
#             'username':username
#         },
#         {
#             "$set":{
#                 'username_lowercase':username.lower().strip()
#             }
#         }
#     )
    
for game in game_history.collection.find({'gamemode':"Deathmatch"}):
    winners = game['game_results']['winners']
    wcaps = 0
    for player in winners:
        wcaps+=player['kills']
    losers = game['game_results']['losers']
    lcaps = 0
    for player in losers:
        lcaps+=player['kills']
    game_history.collection.find_one_and_update(
        {
            "game_id":game['game_id']
        },
        {
            "$set":{
                'game_results.winner_score':wcaps,
                'game_results.loser_score':lcaps
            }
        }
    )
