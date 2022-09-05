import Server
import time
import os
from mongodb import Database
import Game
import logging
from blarg.blarg import Blarg

import asyncio
from collections import deque
import json
import threading


os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

async def update(logger):
    player_stats = Database("UYA","Player_Stats")
    players_online = Database("UYA","Players_Online")
    game_history = Database("UYA", "Game_History")
    games_active = Database("UYA","Games_Active")
    clans = Database("UYA", "Clans")
    elo=Database("UYA", 'Elo')

    live = Database("UYA", "Logger")
    live.clear()
    live.client.close()

    players = {}
    games = {}
    players_online.clear()
    games_active.clear()

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
        await asyncio.sleep(60*.5)

async def threadCheck():
    minutes = 15
    while True:
        print(f"Active threads {threading.active_count()}")
        await asyncio.sleep(60*minutes)
        
async def main(logger):
    config = read_config("blarg/config.json")
    blarg = Blarg(config)

    socket = loop.create_task(blarg.read_websocket())
    stats = loop.create_task(update(logger))
    garbageCollection = loop.create_task(blarg.garbageCollect())

    # await asyncio.wait([stats])
    await asyncio.wait([stats, socket, garbageCollection])
    # await asyncio.wait([socket, garbageCollection, threads])




def read_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        return json.loads(f.read())


# DEBUG = True
DEBUG = False
if __name__ == "__main__":
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
    loop = asyncio.get_event_loop()


    loop.run_until_complete(main(logger))
    loop.close()




    
    





