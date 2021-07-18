import struct
OTHER_RULES = {
    'base_defenses' : 19,
    "spawn_charge_boots":18,   
    'spawn_weapons':17,
    'unlimited_ammo':16,
    "player_names":9,
    "vehicles":1,

}

def advancedRulesParser(num):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)
    returns game MODE andd game SUBMODE/ type'''
    advanced_rules = {}
    num = int(num) if type(num) != 'int' else num
    num = struct.pack('<I', num).hex()
    num=num[2:] #cut off the front 2 bytes
    num = int(num,16)
    num = format(num, "#026b")[2:]
    advanced_rules['baseDefenses'] = True if num[OTHER_RULES['base_defenses']] == '1' else False
    advanced_rules['spawn_charge_boots'] = True if num[OTHER_RULES['spawn_charge_boots']] == '1' else False
    advanced_rules['spawn_weapons'] = True if num[OTHER_RULES['spawn_weapons']] == '1' else False
    advanced_rules["player_names"] = True if num[OTHER_RULES["player_names"]] == '1' else False
    advanced_rules['vehicles'] = True if num[OTHER_RULES['vehicles']] == '0' else False
    return advanced_rules
    
