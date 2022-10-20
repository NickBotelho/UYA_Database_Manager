from mongodb import Database
import blankRatios

def run():
    stats = Database("UYA", "Player_Stats")

    for player in stats.collection.find():
        advancedStats = player['advanced_stats']
        if "live" not in advancedStats or advancedStats['live']['live_games'] == 0:
            stats.collection.find_one_and_update(
                {
                    "_id":player["_id"]
                },
                {
                    "$set":{
                        "advanced_stats.live":blankRatios.blank_live_contract,
                        "advanced_stats.live/gm":blankRatios.blank_live_contract,
                        "advanced_stats.live/min":blankRatios.blank_live_contract,
                    }
                }
            )

run()