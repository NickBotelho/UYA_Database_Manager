import base64
from Parsers.Ladderstatswide_Byte_Field import ladderstatswide_bytes_field

def Base64toLadderstatswide(base, bytes_field):
    hx = base64.b64decode(base).hex() #base64 converted to hex
    output = {}
    bytes_visited = 0
    for i in range(0,len(hx),8):
        hex_field = hx[i:i+8]
        value = int(hex_field, 16) #big endian int 32
        bytes_visited+=4
        if bytes_visited in bytes_field:
            field = bytes_field[bytes_visited]
        else:
            field = None
        if field!= None:
            output[field] = value
    return output

WEAPONS = 80
SIEGE = 152
TDM = 188
CTF = 216
OTHER = 264
def HextoLadderstatswide(hx):
    '''input is hex string output dict of stats to values'''
    output = {
        'overall' : {}, #[8,44]
        'weapons' : {}, #[80,148],
        'siege':{}, #[152,184]
        "tdm":{}, #[188,212]
        "ctf":{}, #[216,252]
        "other":{}, #[264:]
    }
    section = 'overall'
    bytes_visited = 0
    for i in range(0,len(hx),8):
        if bytes_visited == WEAPONS: section = "weapons"
        if bytes_visited == SIEGE: section = "siege"
        if bytes_visited == TDM: section = 'tdm'
        if bytes_visited == CTF: section = "ctf"
        if bytes_visited == OTHER: section = 'other'
        hex_field = hx[i:i+8]
        little_endian = []
        for j in range(0,8,2):
            bits = hex_field[j:j+2]
            little_endian.append(bits)
        little_endian = "".join(little_endian[::-1])
        value = int(little_endian, 16) #big endian int 32
        if bytes_visited in ladderstatswide_bytes_field:
            field = ladderstatswide_bytes_field[bytes_visited]
        else:
            field = None
        if field!= None:
            output[section][field] = value
        bytes_visited+=4
    return output

# poop="28000000000000000000000001000000000000000F0000000A0000000900000000000000270000000200000002000000FFFFFFFF000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000002000000000000000000000000000000020000000000000001000000000000000F0000000A00000000000000270000000200000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000FFFFFFFF09000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004100000000000000000000000100000000000000000000000000000000000000000000000000000000000000"
# four = "28000000000000000300000004000000000000004E0000007C0000000A00000000000000560000000000000007000000FFFFFFFF00000000000000000000000000000000000000000000000000000000000000000000000000000000000000001300000007000000510000003E000000000000000000000000000000000000000C0000000900000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000000000000220000003C00000000000000030000000300000001000000000000002C000000400000000000000056000000000000000C0000000600000004000000FFFFFFFF00000000040000000600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500000000000000000000000600000000000000000000000000000000000000000000000000000000000000"
# print("FourBolt",HextoLadderstatswide(four))
# print("poop",HextoLadderstatswide(poop, bytes_field))
# import requests
# g = requests.get('https://uya.raconline.gg/tapi/robo/players').text.strip()
# print(g)
