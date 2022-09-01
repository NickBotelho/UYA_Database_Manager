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
            red -= 24
        if not base:
            red -= 4
    elif map == 'outpost_x12':
        red = int('65', 16)
        if not nodes: #3,3,3,3,3,3
            red -= 18
        if not base:
            red -= 4
    elif map == 'korgon_outpost':
        red = int('54', 16)
        if not nodes: #4,4,4,4,4
            red -= 20
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
    return [blue.upper(), red.upper()]
def generateHealthIDs(map = 'bakisi_isle', nodes = True, base = True):
    res = []
    map = map.lower()
    if map == 'bakisi_isle': #done
        red = int('54', 16)
        boxes = 5

        if not nodes: #4,4,3,3,4,4
            red -= 30
        if not base:
            red -= 4
        res = [node for node in range(red, red+boxes)]
    elif map == 'hoven_gorge': #done
        red = int('57', 16)
        boxes = 8
        if not nodes: #4,4,3,3,4,4
            red -= 24
        if not base:
            red -= 4
        res = [node for node in range(red, red+boxes)]
    elif map == 'outpost_x12': #done
        red = int('50', 16)
        boxes = 5
        if not nodes: #4,4,3,3,4,4
            red -= 18
        if not base:
            red -= 4
        res = [node for node in range(red, red+boxes)]
    elif map == 'korgon_outpost':
        red = int('46', 16) #done
        boxes = 6
        if not nodes: #4,4,3,3,4,4
            red -= 20
        if not base:
            red -= 4
        res = [node for node in range(red, red+boxes)]
    elif map == 'metropolis': #done
        red = int('43', 16)
        boxes = 3
        if not nodes: #4,4,3,3,4,4
            red -= 22
        if not base:
            red -= 4
        res = [node for node in range(red, red+boxes)]

    elif map == 'blackwater_city': #done
        red = int('43', 16)
        boxes = 4
        if not nodes: #5,5,5,5
            red -= 20
        if not base:
            red -= 4
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
    return res

# print(generateHealthIDs(map = "metropolis", nodes = False, base=False))
# print(generateFlagIDs(nodes=False, base=True))