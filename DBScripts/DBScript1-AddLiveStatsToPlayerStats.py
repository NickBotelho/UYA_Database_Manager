from mongodb import Database

shell = {
    "live_games":0,
    'live_seconds':0,
    "kills": 0,
    "deaths": 0,
    "saves": 0,
    "caps": 0,
    "distance_travelled": 0,
    "flag_distance": 0,
    "noFlag_distance": 0,
    "flag_pickups": 0,
    "flag_drops": 0,
    "health_boxes": 0,
    "packs_grabbed":0,
    "nicks_given": 0,
    "nicks_received": 0,
    "weapons": {
        "Wrench": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Hypershot": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Holo Shield": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Flux": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Blitz": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Gravity Bomb": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Lava Gun": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Rockets": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Morph O' Ray": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Mines": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "N60": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        }
    },
    'medals':{
        "nuke":0,
        "brutal":0,
        "relentless":0,
        "bloodthirsty":0,
        "merciless":0,
        'undying': 0,
        'distributor':0,
        'thickskull': 0,
        'bloodfilled':0,
        'brutalized':0,
        'radioactive':0,
        'shifty':0,
        'lockon':0,
        'juggernaut':0,
        'olympiad':0,
        'dropper':0,
        'healthrunner':0,
        'ratfuck':0,
        'machinegun':0,
        'heatingup':0,
        'untouchable':0,
        },
    "controller": {
                "Select": {
                    "holds": 0,
                    "presses": 0
                },
                "Start": {
                    "holds": 0,
                    "presses": 0
                },
                "Up": {
                    "holds": 0,
                    "presses": 0
                },
                "Right": {
                    "holds": 0,
                    "presses": 0
                },
                "Down": {
                    "holds": 0,
                    "presses": 0
                },
                "Left": {
                    "holds": 0,
                    "presses": 0
                },
                "R2": {
                    "holds": 0,
                    "presses": 0
                },
                "L1": {
                    "holds": 0,
                    "presses": 0
                },
                "L2": {
                    "holds": 0,
                    "presses": 0
                },
                "R1": {
                    "holds": 0,
                    "presses": 0
                },
                "Triangle": {
                    "holds": 0,
                    "presses": 0
                },
                "Circle": {
                    "holds": 0,
                    "presses": 0
                },
                "X": {
                    "holds": 0,
                    "presses": 0
                },
                "Square": {
                    "holds": 0,
                    "presses": 0
                }
            }

}   


def getAverageDict(existing, games):
    new = {}
    games = 1 if games == 0 else games
    for key in existing:
        if type(existing[key]) == dict:
            new[key] = getAverageDict(existing[key], games)
        elif type(existing[key]) == int or type(existing[key]) == float:
            new[key] = round(existing[key] / games, 2)
    return new
def getPerMinDict(existing, totalMins):
    new = {}
    totalMins = 1 if totalMins == 0 else totalMins
    for key in existing:
        if type(existing[key]) == dict:
            new[key] = getPerMinDict(existing[key], totalMins)
        elif type(existing[key]) == int or type(existing[key]) == float:
            new[key] = round(existing[key] / totalMins, 2)
    return new
def mergeDicts (existing, new):
    '''merge a new dict onto the existing dict, summing matching keys and merging non existing ones from new'''
    pass
    for key in new:
        if key not in existing:
            existing[key] = new[key]
        else:
            if type(existing[key]) == dict:
                mergeDicts(existing[key], new[key])
            elif type(existing[key]) == int or type(existing[key]) == float:
                existing[key] += new[key]
def run():
    stats = Database("UYA", "Player_Stats_Backup")

    for player in stats.collection.find():
        print(f"Updating {player['username']}")
        advancedStats = player['advanced_stats']
        if "live" not in advancedStats:
            advancedStats['live'] = {}
        mergeDicts(advancedStats['live'], shell)
        advancedStats['live/gm'] = getAverageDict(advancedStats['live'], advancedStats['live']['live_games'])
        advancedStats['live/min'] = getPerMinDict(advancedStats['live'], advancedStats['live']['live_seconds'])
        stats.collection.find_one_and_update(
            {
                "_id":player["_id"]
            },
            {
                "$set":{
                    "advanced_stats":advancedStats
                }
            }
        )
        # break

run()