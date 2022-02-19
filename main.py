import Server
import time
import os
from mongodb import Database
import Game
import logging

player_stats = Database("UYA","Player_Stats")
players_online = Database("UYA","Players_Online")
game_history = Database("UYA", "Game_History")
games_active = Database("UYA","Games_Active")
clans = Database("UYA", "Clans")
elo=Database("UYA", 'Elo')
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

DEBUG = False
if __name__ == "__main__":
    players = {}
    games = {}
    players_online.clear()
    games_active.clear()
    #init logger###
    level = 'DEBUG' if DEBUG else "INFO"
    logger = logging.getLogger("UYA Database Manager")
    logger.setLevel(logging.getLevelName(level))
    formatter = logging.Formatter("%(name)s | %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.getLevelName(level))
    logger.addHandler(sh)
    ######

    logger.info("Running")
    while True:
        logger.debug("Getting Players...")
        players, offline_players = Server.getOnlinePlayers(players, clans, player_stats) #dict of {player id --> Player obj}
        player_stats.updateOnlinePlayersStats(players, offline_players, elo)
        players_online.addOnlinePlayers(players)
        players_online.logPlayersOff(offline_players)

        games, ended_games = Server.getGames(games)
        Game.cacheStats(games, player_stats)

        games_active.addGames(games)
        games_active.cancelGames(ended_games, player_stats, game_history, elo, logger)
        
        logger.debug("Waiting...")
        time.sleep(60*.5 if not DEBUG else 2*.5)

    
    
