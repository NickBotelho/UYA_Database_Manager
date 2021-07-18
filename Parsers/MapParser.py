import struct
MAPS = {
    "00001":"Bakisi_Isle",
    "00010":"Hoven_Gorge",
    "00011":"Outpost_x12",
    "00100":"Korgon_Outpost",
    "00101":"Metropolis",
    "00110":"Blackwater_City",
    "00111":"Command_Center",
    "01001":'Aquatos_Sewers',
    "01000": "Blackwater_Dox",
    "01010":"Marcadia_Palace",
}


def mapParser(num):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)'''
    num = int(num) if type(num) != 'int' else num
    num = struct.pack('<I', num).hex()
    num=num[0:2]
    num = int(num,16)
    num = format(num, "#010b")[2:]
    game_map = num[:5]
    game_map = MAPS[game_map]
    return game_map
    
# MapParser(3898886210)


class MapBytes:
    BAKISI_ISLE = 8
    HOVEN_GORGE = 10
    OUTPOST_X12 = 18
    KORGON_ISLE = 20
    METROPOLIS = 28
    BLACKWATER_CITY = 30
    COMMAND_CENTER = 38
    BLACKWATER_DOX = 40
    MARCADIA_PALACE = 50

    