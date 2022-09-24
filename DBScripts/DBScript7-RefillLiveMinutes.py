from mongodb import Database


def run():
    stats = Database("UYA", "Player_Stats_Backup")

    for player in stats.collection.find():
        print(f"Updating {player['username']}")
        advancedStats = player['advanced_stats']
        advancedStats['live/min']['live_seconds'] = advancedStats['live']['live_games'] * 20 * 60 
        advancedStats['live']['live_seconds'] = advancedStats['live']['live_games'] * 20 * 60 
        advancedStats['live/gm']['live_seconds'] = advancedStats['live']['live_games'] * 20 * 60 

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