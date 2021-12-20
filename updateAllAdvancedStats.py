
from mongodb import Database
import json
import os
from time import gmtime, strftime
from loadElos import loadElos

player_stats = Database("UYA","Player_Stats")
players_online = Database("UYA","Players_Online")
game_history = Database("UYA", "Game_History")
games_active = Database("UYA","Games_Active")
player_stats_backup = Database("UYA","Player_Stats_Backup")
overall_elos = loadElos("elosv2(OVERALL).txt")
ctf_elos = loadElos("elosv2(CTF).txt")
siege_elos = loadElos("elosv2(Siege).txt")
dm_elos = loadElos("elosv2(Deathmatch).txt")
def updateAllAdvancedStats():
    for player in player_stats.collection.find():
        print("updating {}...".format(player['username']))
        game_ids = player['match_history'].keys()
        minutes, ctf_mins, flux, blitz, grav = 0, 0, 0, 0, 0
        flux_gms, blitz_gms, grav_gms = 0, 0, 0
        siege_mins,  tdm_mins = 0, 0
        map_game_count = {
                "Bakisi_Isle":0,
                "Hoven_Gorge":0,
                "Outpost_x12":0,
                "Korgon_Outpost":0,
                "Metropolis":0,
                "Blackwater_City":0,
                "Command_Center":0,
                'Aquatos_Sewers':0,
                "Blackwater_Dox":0,
                "Marcadia_Palace":0
            }
        map_min_count ={
            "Bakisi_Isle":0,
            "Hoven_Gorge":0,
            "Outpost_x12":0,
            "Korgon_Outpost":0,
            "Metropolis":0,
            "Blackwater_City":0,
            "Command_Center":0,
            'Aquatos_Sewers':0,
            "Blackwater_Dox":0,
            "Marcadia_Palace":0
        }
        for id in game_ids:
            
            id = float(id)
            game = game_history.collection.find_one({
                'game_id':id
            })
            minutes+=game['minutes']
            ctf_mins = ctf_mins + game['minutes'] if game['gamemode'] == 'CTF' else ctf_mins
            siege_mins = siege_mins + game['minutes'] if game['gamemode'] == 'Siege' else siege_mins
            tdm_mins = tdm_mins + game['minutes'] if game['gamemode'] == 'Deathmatch' else tdm_mins
            flux = flux + game['minutes'] if 'Flux' in game['weapons'] else flux
            blitz = blitz + game['minutes'] if 'Blitz' in game['weapons'] else blitz
            grav = grav + game['minutes'] if 'Gravity Bomb' in game['weapons'] else grav

            flux_gms = flux_gms + 1 if 'Flux' in game['weapons'] else flux_gms
            blitz_gms = blitz_gms + 1 if 'Blitz' in game['weapons'] else blitz_gms
            grav_gms = grav_gms + 1 if 'Gravity Bomb' in game['weapons'] else grav_gms

            map_game_count[game['map']] +=1
            map_min_count[game['map']] += game['minutes']



        stats = player['stats']['overall']
        ctf = player['stats']['ctf']
        weapons = player['stats']['weapons']
        try:
            per_minute = {
                'kills/min' : round(stats['kills'] / minutes, 2),
                'deaths/min' : round(stats['deaths'] / minutes, 2),
                'suicides/min' : round(stats['suicides'] / minutes, 2),
                'avg_game_length' : round(minutes/ stats['games_played'], 2),
                'caps/min' : round(ctf['ctf_caps']/ ctf_mins, 2),
                'saves/min' : round(ctf['ctf_saves']/ ctf_mins, 2),
                'flux_kills/min' : round(weapons['flux_kills'] / flux, 2),
                'blitz_kills/min' : round(weapons['blitz_kills'] / blitz, 2),
                'gravity_bomb_kills/min' : round(weapons['gravity_bomb_kills'] / grav, 2),
                'flux_deaths/min' : round(weapons['flux_deaths'] / flux, 2),
                'blitz_deaths/min' : round(weapons['blitz_deaths'] / blitz, 2),
                'gravity_bomb_deaths/min' : round(weapons['gravity_bomb_deaths'] / grav, 2),
                'total_mins':minutes,
                'flux_mins':flux,
                'blitz_mins':blitz,
                'grav_mins':grav,
                'ctf_mins': ctf_mins,
                'siege_mins': siege_mins,
                'deathmatch_mins': tdm_mins,
                'maps':map_min_count
            }
            per_game = {
                'kills/death': round(stats['kills'] / stats['deaths'], 2),
                'wins/loss': round(stats['wins'] / stats['losses'], 2),
                'kills/gm' : round(stats['kills'] / stats['games_played'], 2),
                'deaths/gm' : round(stats['deaths'] / stats['games_played'], 2),
                'suicides/gm' : round(stats['suicides'] / stats['games_played'], 2),
                'caps/gm' : round(ctf['ctf_caps']/ (ctf['ctf_wins'] + ctf['ctf_losses']), 2),
                'saves/gm' : round(ctf['ctf_saves']/ (ctf['ctf_wins'] + ctf['ctf_losses']), 2),
                'flux_kills/gm' : round(weapons['flux_kills'] / flux_gms, 2),
                'blitz_kills/gm' : round(weapons['blitz_kills'] / blitz_gms, 2),
                'gravity_bomb_kills/gm' : round(weapons['gravity_bomb_kills'] / grav_gms, 2),
                'flux_deaths/gm' : round(weapons['flux_deaths'] / flux_gms, 2),
                'blitz_deaths/gm' : round(weapons['blitz_deaths'] / blitz_gms, 2),
                'gravity_bomb_deaths/gm' : round(weapons['gravity_bomb_deaths'] / grav_gms, 2),
                'flux_gms':flux_gms,
                'grav_gms': grav_gms,
                'blitz_gms' :blitz_gms,
                'maps' : map_game_count,

            }
            elo = {
                'overall':1200 if player['username'] not in overall_elos else overall_elos[player['username']],
                'CTF':1200 if player['username'] not in ctf_elos else ctf_elos[player['username']],
                'Siege':1200 if player['username'] not in siege_elos else siege_elos[player['username']],
                'Deathmatch':1200 if player['username'] not in dm_elos else dm_elos[player['username']],
            }
        except:
            print("Error on {}".format(player['username']))
            per_game = {
                'kills/death':0,
                'wins/loss':0,
                'kills/gm' : 0,
                'deaths/gm' : 0,
                'suicides/gm' : 0,
                'caps/gm' : 0,
                'saves/gm' : 0,
                'flux_kills/gm' :0,
                'blitz_kills/gm' : 0,
                'gravity_bomb_kills/gm' : 0,
                'flux_deaths/gm' : 0,
                'blitz_deaths/gm' : 0,
                'gravity_bomb_deaths/gm' :0,
                'flux_gms':flux_gms,
                'grav_gms': grav_gms,
                'blitz_gms' :blitz_gms,
                'maps' : map_game_count,
            }
            per_minute = {
                'kills/min' : 0,
                'deaths/min' : 0,
                'suicides/min' : 0,
                'avg_game_length' : 0,
                'caps/min' : 0,
                'saves/min' : 0,
                'flux_kills/min' : 0,
                'blitz_kills/min' : 0,
                'gravity_bomb_kills/min' : 0,
                'flux_deaths/min' : 0,
                'blitz_deaths/min' : 0,
                'gravity_bomb_deaths/min' : 0,
                'total_mins':minutes,
                'flux_mins':flux,
                'blitz_mins':blitz,
                'grav_mins':grav,
                'ctf_mins': ctf_mins,
                'siege_mins': siege_mins,
                'deathmatch_mins': tdm_mins,
                'maps':map_min_count
            }
            elo = {
                'overall':1200,
                'CTF':1200,
                'Siege':1200,
                'Deathmatch':1200,
            }

        player_stats.collection.find_one_and_update(
            {
                'account_id' : player['account_id']
            },
            {
                "$set":{
                    'advanced_stats.per_min': per_minute,
                    'advanced_stats.per_gm' : per_game,
                    'advanced_stats.elo' : elo,


                    
                }
                
            }
        )

# updateAllAdvancedStats()
    