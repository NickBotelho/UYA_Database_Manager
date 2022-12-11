import requests
from Parsers.ToLadderstatswide import HextoLadderstatswide
from Player import Player
from Game import Game
from HashId import hash_id

PLAYERS_API = 'http://103.214.110.220:8281/robo/players'
GAMES_API = 'http://103.214.110.220:8281/robo/games'
def getOnlinePlayers(players, clans, player_stats):
    '''Returns a dict of playername --> Player class object that hold various things (see player.py)
    Will also log off players who got off '''
    try:
        res = requests.get(PLAYERS_API).json()
    except:
        res = {}

    online_players = set()
    for player in res:
        online_players.add(player['account_id'])
        update = True
        if player['account_id'] in players: 
            #if the player is already online
            players[player['account_id']].softUpdate(player)
            update = players[player['account_id']].updateCache()
        if update:
            plyr = Player(player)
            if not plyr.isBot: #make sure player is not a bot
                players[player['account_id']] = plyr
                clans.updateClans(players[player['account_id']],  player_stats)


    offline_ids = {}
    for player_id in players: #loop that check if a cached player is not in the online list and logs them off
        if player_id not in online_players:
            offline_ids[player_id] = players[player_id]
    for id in offline_ids:
        del players[id]

    return players, offline_ids


def getGames(games):
    '''Returns a list of active games'''
    try:
        res = requests.get(GAMES_API).json()
    except:
        res = {}
    active_games = set()
    for i, game in enumerate(res):
        if len(game['players']) > 0:
            game_id = hash_id(game)
            active_games.add(game_id)
            if game_id not in games: 
                games[game_id]= Game(game)
            else:
                if games[game_id].status == 'Staging':
                    games[game_id].updatePlayers(game['players'])
                    games[game_id].checkIfStart(game['status'], game['players'])

    ended_games = {}
    for id in games:
        if id not in active_games:
            ended_games[id] = games[id]
    for id in ended_games:
        del games[id]
    return games, ended_games



class MediusWorldStatus:
    WORLD_INACTIVE = 0
    WORLD_STAGING = 1
    WORLD_ACTIVE = 2
    WORLD_CLOSED = 3
    WORLD_PENDING_CREATION = 4
    WORLD_PENDING_CONNECT_TO_GAME = 5


class MediusPlayerStatus:
    MEDIUS_PLAYER_DISCONNECTED = 0
    MEDIUS_PLAYER_IN_AUTH_WORLD = 1
    MEDIUS_PLAYER_IN_CHAT_WORLD = 2
    MEDIUS_PLAYER_IN_GAME_WORLD = 3
    MEDIUS_PLAYER_IN_OTHER_UNIVERSE = 4