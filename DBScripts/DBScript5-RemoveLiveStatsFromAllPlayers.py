from mongodb import Database

shell = {
            "name": "buttFuckah",
            "hp": 100,
            "kills": 0,
            "deaths": 2,
            "caps": 0,
            "team": "blue",
            "distance_travelled": 0.77,
            "hasFlag": False,
            "flag_pickups": 0,
            "flag_drops": 0,
            "health_boxes": 0,
            "nicks_given": 0,
            "nicks_received": 0,
            "weapons": {
                "Wrench": {
                    "weapon": "Wrench",
                    "kills": 0,
                    "isV2": False,
                    "shots": 0,
                    "hits": 0,
                    "accuracy": 0,
                    "killstreak": 0
                },
                "Flux": {
                    "weapon": "Flux",
                    "kills": 0,
                    "isV2": False,
                    "shots": 5,
                    "hits": 0,
                    "accuracy": 0,
                    "killstreak": 0
                },
                "Blitz": {
                    "weapon": "Blitz",
                    "kills": 0,
                    "isV2": False,
                    "shots": 8,
                    "hits": 0,
                    "accuracy": 0,
                    "killstreak": 0
                },
                "Gravity Bomb": {
                    "weapon": "Gravity Bomb",
                    "kills": 0,
                    "isV2": False,
                    "shots": 3,
                    "hits": 0,
                    "accuracy": 0,
                    "killstreak": 0
                }
            },
            "killHeatMap": [],
            "deathHeatMap": [
                [10734, 10711],
                [14599, 13311]
            ]
        }



def run():
    stats = Database("UYA", "Player_Stats_Backup")

    for player in stats.collection.find():
        if 'live' in player['advanced_stats'] or 'streaks' in player['advanced_stats']:
            adv = player['advanced_stats']
            if 'live' in player['advanced_stats']:
                del adv['live']
            if 'streaks' in player['advanced_stats']:
                del adv['streaks']

            stats.collection.find_one_and_update({
                "_id" : player['_id']
            },
            {
                "$set":{
                    "advanced_stats" :adv
                }
            })

        

run()