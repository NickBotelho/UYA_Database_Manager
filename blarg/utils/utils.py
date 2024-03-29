import traceback
from collections import deque
from hashlib import sha512

def short_bytes_to_int(byte1, byte2):
    data = byte2 + byte1
    data = int(data, 16)
    return data

def bytes_to_int_little(data):
    return int.from_bytes(data, byteorder='little')

def bytes_to_int_big(data):
    return int.from_bytes(data, byteorder='big')

def int_to_bytes_little(bytelength, data, signed=False):
    return data.to_bytes(bytelength, 'little', signed=signed)

def int_to_bytes_big(bytelength, data):
    return data.to_bytes(bytelength, 'big')

def bytes_to_hex(data:bytes):
    return data.hex().upper()

def hex_to_bytes(hex:str):
    return bytes(bytearray.fromhex(hex))

def bytes_from_hex(hex:str):
    return bytes(bytearray.fromhex(hex))

def bytes_to_str(data: bytes) -> str:
    res = ''
    for b in data:
        if b == 0x00:
            return res
        res += chr(b)
    return res

def str_to_bytes(data: str, length: int) -> bytes:
    str_bytes = data
    assert(length > len(data))
    while (len(str_bytes) != length):
        str_bytes += '\0'
    return str_bytes.encode()

def hex_to_int_little(hex: str):
    return bytes_to_int_little(hex_to_bytes(hex))

def hex_to_str(data: str):
    return bytes_to_str(hex_to_bytes(data))


def generateFlagIDs(map = 'bakisi_isle', nodes = True, base = True):
    '''returns red flag, blue flag ids'''
    map = map.lower()
    red, blue = 0, 0
    if map == 'bakisi_isle':
        red = int('66', 16)
        if not nodes: #4,5,4,5,4,4,4
            red -= 30
        if not base:
            red -= 4
    elif map == 'hoven_gorge':
        red = int('6A', 16)
        if not nodes: #5,3,4,1,4,2,5
            red -= 26
        if not base:
            red -= 4
    elif map == 'outpost_x12':
        red = int('65', 16)
        if not nodes: #3,3,3,3,3,3 2behicle rockets
            red -= 20
        if not base:
            red -= 4
    elif map == 'korgon_outpost':
        red = int('54', 16)
        if not nodes: #4,4,4,4,4
            red -= 19
        if not base:
            red -= 4
    elif map == 'metropolis':
        red = int('5B', 16)
        if not nodes: #4,4,3,3,4,4
            red -= 22
        if not base:
            red -= 4
    elif map == 'blackwater_city':
        red = int('52', 16)
        if not nodes: #5,5,5,5
            red -= 20
        if not base:
            red -= 4
    elif map == 'command_center':
        red = int('14', 16)
    elif map == 'blackwater_dox':
        red = int('0F', 16)
    elif map == 'aquatos_sewers':
        red = int('13', 16)
    elif map == 'marcadia_palace':
        red = int('14', 16)
        
    blue = red - 1
    red = hex(red)[2:] if len(hex(red)[2:]) > 1 else f"0{hex(red)[2:]}"
    blue = hex(blue)[2:] if len(hex(blue)[2:]) > 1 else f"0{hex(blue)[2:]}"
    flags = [blue.upper() + "1000F7", red.upper() + "1000F7"]
    
    return flags
def generateHealthIDs(map = 'bakisi_isle', mode = "CTF", nodes = True, base = True):
    #TDM no troopers?
    #tdm troopers = false, base = true
    res = []
    map = map.lower()
    if map == 'bakisi_isle': #done
        #10 troopers
        red = int('54', 16)
        boxes = 5
        if mode != "Deathmatch":
            if not nodes: #4,4,3,3,4,4
                red -= 30
            if not base:
                red -= 4
        else:
            red-=40

        res = [node for node in range(red, red+boxes)]
    elif map == 'hoven_gorge': #done
        #4 troopers
        red = int('58', 16)
        boxes = 8
        if mode != "Deathmatch":
            if not nodes: #4,4,3,3,4,4
                red -= 26
            if not base:
                red -= 4
        else:
            red-=36

        res = [node for node in range(red, red+boxes)]
    elif map == 'outpost_x12': #done
        #10 troopers 
        red = int('52', 16)
        boxes = 5
        if mode != "Deathmatch":
            if not nodes: #4,4,3,3,4,4
                red -= 20
            if not base:
                red -= 4
        else:
            red-=30

        res = [node for node in range(red, red+boxes)]
    elif map == 'korgon_outpost':
        #10 troopers (actually 9 + mystery trooper)
        red = int('45', 16) #done
        boxes = 6
        if mode != "Deathmatch":
            if not nodes: #4,4,3,3,4,4
                red -= 19
            if not base:
                red -= 4
        else:
            red-=29
        res = [node for node in range(red, red+boxes)]
    elif map == 'metropolis': #done
        #4 troopers + 5mystery = 9
        red = int('49', 16)
        boxes = 3
        if mode != "Deathmatch":
            if not nodes:
                red -= 22
            if not base:
                red -= 4
        else:
            red-=32

        res = [node for node in range(red, red+boxes)]
    elif map == 'blackwater_city': #done
        #8 troopers
        red = int('43', 16)
        boxes = 4
        if mode != "Deathmatch":
            if not nodes: #5,5,5,5
                red -= 20
            if not base:
                red -= 4
        else:
            red-=30
        res = [node for node in range(red, red+boxes)]
    elif map == 'command_center':
        red = int('10', 16)
        boxes = 1
        res = [node for node in range(red, red+boxes)]
    elif map == 'blackwater_dox':
        red = int('0A', 16)
        boxes = 2
        res = [node for node in range(red, red+boxes)]
    elif map == 'aquatos_sewers':
        red = int('0D', 16)
        boxes = 3
        res = [node for node in range(red, red+boxes)]
    elif map == 'marcadia_palace':
        red = int('0E', 16)
        boxes = 3
        res = [node for node in range(red, red+boxes)]

        
    res = [hex(node)[2:].upper() if len(hex(node)[2:]) > 1 else f"0{hex(node)[2:]}".upper() for node in res]
    ids = [box + "1000F7" for box in res]
    return ids
def generateBaseIDs(map = 'bakisi_isle', nodes = True, base = True):
    '''returns red flag, blue flag ids'''
    if base == False: return []

    map = map.lower()
    red, blue = 0, 0
    if map == 'bakisi_isle':
        red = int('53', 16)
        if not nodes: #4,5,4,5,4,4,4
            red -= 30
        if not base:
            red -= 4
    elif map == 'hoven_gorge':
        red = int('56', 16)
        if not nodes: #5,3,4,1,4,2,5
            red -= 26
        if not base:
            red -= 4
    elif map == 'outpost_x12':
        red = int('4F', 16)
        if not nodes: #3,3,3,3,3,3
            red -= 20
        if not base:
            red -= 4
    elif map == 'korgon_outpost':
        red = int('45', 16)
        if not nodes: #4,4,4,4,4
            red -= 19
        if not base:
            red -= 4
    elif map == 'metropolis':
        red = int('42', 16)
        if not nodes: #4,4,3,3,4,4
            red -= 22
        if not base:
            red -= 4
    elif map == 'blackwater_city':
        red = int('42', 16)
        if not nodes: #5,5,5,5
            red -= 20
        if not base:
            red -= 4
    elif map == 'command_center':
        return []
    elif map == 'blackwater_dox':
        return []
    elif map == 'aquatos_sewers':
        return []
    elif map == 'marcadia_palace':
        return []
        
    blue = red - 1
    red = hex(red)[2:] if len(hex(red)[2:]) > 1 else f"0{hex(red)[2:]}"
    blue = hex(blue)[2:] if len(hex(blue)[2:]) > 1 else f"0{hex(blue)[2:]}"
    return [blue.upper(), red.upper()]

# print(generateHealthIDs("hoven_gorge",nodes = False,  base = True))
# print(generateHealthIDs("blackwater_city",nodes = False,base = True))
# print(generateFlagIDs("blackwater_city",nodes = False,base = True))
# print(generateHealthIDs("bakisi_isle"))