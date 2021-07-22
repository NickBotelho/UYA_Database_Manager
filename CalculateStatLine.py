SMALL_MAPS={"Marcadia_Palace","Blackwater_Dox",'Aquatos_Sewers',"Command_Center"}
WEAPONS_CONVERT = {
    
    "Lava Gun": "lava_gun",
    "Morph O' Ray": 'morph',
    "Mines":'mines',
    "Gravity Bomb":'gravity_bomb',
    "Rockets":'rockets',
    "Blitz":'blitz',
    "N60":'n60',
    "Flux":'flux'

}        
def calculateStatLine(updated, cache, game):
    '''upddated is an entire mongo entry for the player'''
    '''cached is just a dict of the old stats'''

    game_result = None

    if updated['stats']['overall']['wins'] > cache['overall']['wins']: game_result = 'win'
    if updated['stats']['overall']['losses'] > cache['overall']['losses']: game_result = 'loss'
    if updated['stats']['overall']['games_played'] == cache['overall']['games_played']: game_result = 'disconnect'
    game_result = 'tie' if not game_result else game_result
    
    kills = updated['stats']['overall']['kills'] - cache['overall']['kills']
    deaths = updated['stats']['overall']['deaths'] - cache['overall']['deaths']
    suicicdes = updated['stats']['overall']['suicides'] - cache['overall']['suicides']
    res = {
        'username':updated['username'],
        'game_result':game_result,
        'kills':kills,
        'deaths':deaths,
        'suicides':suicicdes,
    }

    if game.game_mode == 'CTF':
        res['caps'] = updated['stats']['ctf']['ctf_caps'] - cache['ctf']['ctf_caps']
        res['saves'] = updated['stats']['ctf']['ctf_saves'] - cache['ctf']['ctf_saves']
        ###check for if game has nodes and bases
        if game.map not in SMALL_MAPS:
            if game.advanced_rules['baseDefenses']:
                res['base_dmg'] = updated['stats']['overall']['overall_base_dmg'] - cache['overall']['overall_base_dmg'] 
    elif game.game_mode == 'Siege':
        res['base_dmg'] = updated['stats']['overall']['overall_base_dmg'] - cache['overall']['overall_base_dmg'] 
        res['nodes'] = updated['stats']['overall']['nodes'] - cache['overall']['nodes']
   
    weapons = {}
    gun = 'wrench'
    weapons['{}_kills'.format(gun)] = updated['stats']['weapons']['{}_kills'.format(gun)] - cache['weapons']['{}_kills'.format(gun)]
    weapons['{}_deaths'.format(gun)] = updated['stats']['weapons']['{}_deaths'.format(gun)] - cache['weapons']['{}_deaths'.format(gun)]

    for gun in game.weapons:
        gun = WEAPONS_CONVERT[gun]
        weapons['{}_kills'.format(gun)] = updated['stats']['weapons']['{}_kills'.format(gun)] - cache['weapons']['{}_kills'.format(gun)]
        weapons['{}_deaths'.format(gun)] = updated['stats']['weapons']['{}_deaths'.format(gun)] - cache['weapons']['{}_deaths'.format(gun)]
    res['weapons'] = weapons
    return res