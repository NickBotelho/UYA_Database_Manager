import struct
MODE={ #3,4
    '00':"Siege",
    '01':"CTF",
    '10':"Deathmatch"
}
SUBMODES = { 
    # '1':"no_teams", #13
    # "1":"base_attrition" #20
    'isTeams':13, #1 = yes, means u can swap teams only 0 in DM
    "isAttrition":20, #1 = yes #consitutes also as chaos ctf

}


def gamerulesParser(num):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)
    returns game MODE andd game SUBMODE/ type'''
    num = int(num) if type(num) != 'int' else num
    num = struct.pack('<I', num).hex()
    num=num[2:] #cut off the front 2 bytes
    num = int(num,16)
    num = format(num, "#026b")[2:]
    game_mode = MODE[num[3:5]]
    isTeams = True if num[SUBMODES['isTeams']] == '1' else False
    isAttrition = True if num[SUBMODES['isAttrition']]== '1' else False
    
    if game_mode == MODE['00']:
        game_type = "Attrition" if isAttrition else "Normal"
    elif game_mode == MODE['01']:
        game_type = "Chaos" if isAttrition else "Normal"
    elif game_mode == MODE['10']:
        game_type = "Teams" if isTeams else "FFA"
    else:
        game_type = "Game Type Not Found"
    return game_mode, game_type

