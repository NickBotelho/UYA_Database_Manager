import struct


TIME = {
    '000':'no_time_limit',
    '001':"5_minutes",
    '010':"10_minutes",
    '011':"15_minutes",
    "100":"20_minutes",
    "101":"25_minutes",
    "110":"30_minutes",
    "111":"35_minutes",
}

def timeParser(num):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)'''
    num = int(num) if type(num) != 'int' else num
    num = struct.pack('<I', num).hex()
    num=num[0:2]
    num = int(num,16)
    num = format(num, "#010b")[2:]
    game_time = num[5:]  
    game_time = TIME[game_time]
    return game_time