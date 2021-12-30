import Server
import time
import os
from mongodb import Database
import Game
player_stats = Database("UYA","Player_Stats")
players_online = Database("UYA","Players_Online")
game_history = Database("UYA", "Game_History")
games_active = Database("UYA","Games_Active")
# clans = Database("UYA", "clans")
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()


DEBUG = True
if __name__ == "__main__":
    players = {}
    games = {}
    players_online.clear()
    games_active.clear()
    print("Running...")
    if not DEBUG:
        while True:
            players, offline_players = Server.getOnlinePlayers(players) #dict of {player id --> Player obj}
            player_stats.updateOnlinePlayersStats(players, offline_players)
            players_online.addOnlinePlayers(players)
            players_online.logPlayersOff(offline_players)

            games, ended_games = Server.getGames(games)
            Game.cacheStats(games, player_stats)
            games_active.addGames(games)
            games_active.cancelGames(ended_games, player_stats, game_history)
            
            time.sleep(60*.5)
    else:
        while True:
            print("Getting Players...")
            players, offline_players = Server.getOnlinePlayers(players) #dict of {player id --> Player obj}
            print("Updating DBs...")
            player_stats.updateOnlinePlayersStats(players, offline_players)
            players_online.addOnlinePlayers(players)
            players_online.logPlayersOff(offline_players)


            print("Getting Games....")
            games, ended_games = Server.getGames(games)
            print(games)
            print("Updating game DBs")
            Game.cacheStats(games, player_stats)
            games_active.addGames(games)
            games_active.cancelGames(ended_games, player_stats, game_history)
            # Game.printGames(games)

            print("Waiting...")
            time.sleep(1.5)

    
    
