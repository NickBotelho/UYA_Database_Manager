from mongodb import Database
def reset(medal, username):
    stats= Database("UYA", "Player_Stats")
    player = stats.collection.find_one({"username_lowercase":username})
    advancedStats = player['advanced_stats']

    advancedStats['live']['medals'][medal] = 0
    advancedStats['live/min']['medals'][medal] = 0
    advancedStats['live/gm']['medals'][medal] = 0

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


reset("lockon", "bananatart")