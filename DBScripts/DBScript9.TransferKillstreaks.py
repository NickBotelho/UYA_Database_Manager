from mongodb import Database
import blankRatios

def run():
    stats= Database("UYA", "Player_Stats")
    backup= Database("UYA", "Player_Stats_Backup")

    for player in stats.collection.find():
        advancedStats = player['advanced_stats']
        backupPlayer = backup.collection.find_one({"username":player['username']})
        if backupPlayer != None and backupPlayer['advanced_stats']['live']['live_games'] > 0:
            advancedStats['streaks']['overall']['bestKillstreak']=backupPlayer['advanced_stats']['streaks']['overall']['bestKillstreak']
            advancedStats['streaks']['overall']['bestDeathstreak']=backupPlayer['advanced_stats']['streaks']['overall']['bestDeathstreak']
            
            advancedStats['streaks']['ctf']['bestKillstreak']=backupPlayer['advanced_stats']['streaks']['ctf']['bestKillstreak']
            advancedStats['streaks']['ctf']['bestDeathstreak']=backupPlayer['advanced_stats']['streaks']['ctf']['bestDeathstreak']
            
            advancedStats['streaks']['siege']['bestKillstreak']=backupPlayer['advanced_stats']['streaks']['siege']['bestKillstreak']
            advancedStats['streaks']['siege']['bestDeathstreak']=backupPlayer['advanced_stats']['streaks']['siege']['bestDeathstreak']
            
            advancedStats['streaks']['deathmatch']['bestKillstreak']=backupPlayer['advanced_stats']['streaks']['deathmatch']['bestKillstreak']
            advancedStats['streaks']['deathmatch']['bestDeathstreak']=backupPlayer['advanced_stats']['streaks']['deathmatch']['bestDeathstreak']
            
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