from mongodb import Database
import blankRatios

def run():
    stats= Database("UYA", "Player_Stats")
    backup= Database("UYA", "Player_Stats_Backup")

    for player in stats.collection.find():
        advancedStats = player['advanced_stats']
        backupPlayer = backup.collection.find_one({"username":player['username']})
        if backupPlayer != None and backupPlayer['advanced_stats']['live']['live_games'] > 0:
            advancedStats['live']=backupPlayer['advanced_stats']['live']
            advancedStats['live/gm']=backupPlayer['advanced_stats']['live/gm']
            advancedStats['live/min']=backupPlayer['advanced_stats']['live/min']
            advancedStats['streaks']=backupPlayer['advanced_stats']['streaks']
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
        else:
            advancedStats['live']=blankRatios.blank_live_contract
            advancedStats['live/gm']=blankRatios.blank_live_contract
            advancedStats['live/min']=blankRatios.blank_live_contract
            advancedStats['streaks']=blankRatios.blank_streaks
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