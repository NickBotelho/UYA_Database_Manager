from collections import deque
from blarg.utils.utils import *
from blarg.constants.constants import WEAPON_MAP
'''
P0 moby: 1
P1 moby: 268435457
P2 moby: 536870913
P0 n60 :
P0 bltz:
P0 flux:
P0 rckt:
P0 grav:
P0 mine:
P0 lava:
P0 mrph:
P1 hypr:
P1 flux: 4108
P2 flux: 4208
'''

object_id_map = {
    1: 0,
    268435457: 1,
    536870913: 2,
    4294967295: -1
}

WEAPON_MAP_SRC = {
    'n60': '0{}08',
    'blitz': '0{}08',
    'flux': '4{}08',
    'rocket': '0{}08',
    'grav': '0{}08',
    'mine': '0{}08',
    'lava': '0{}08',
    'morph': '0{}01',
    'hyper': '0{}02',
}
PLAYER_MAP = {
    "00":0,
    "10":1,
    "20":2,
    "30":3,
    "40":4,
    "50":5,
    "60":6,
    "70":7,
}
def hitPlayer(info):
    meat = info[:6]
    receiving = info[6:]
    return meat == "010000" and receiving in PLAYER_MAP

class udp_020E_player_firing:
    def __init__(self):
        pass

    def serialize(self, data: deque):

        packet = {}
        weapon = WEAPON_MAP[data.popleft()]
        data.popleft()
        temp = ''.join([data.popleft() for i in range(2)])
        src_player = int(temp[1])

        time = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
        moby_id = ''.join([data.popleft() for i in range(4)])

        if moby_id not in object_id_map.keys():
            object_id = moby_id
        else:
            object_id = object_id_map[moby_id]

        unk2 = (''.join([data.popleft() for i in range(4)]))
        unk3 = (''.join([data.popleft() for i in range(4)]))
        unk4 = (''.join([data.popleft() for i in range(4)]))
        unk5 = (''.join([data.popleft() for i in range(4)]))
        unk6 = (''.join([data.popleft() for i in range(4)]))
        unk7 = (''.join([data.popleft() for i in range(4)]))

        packet['src'] = src_player
        packet['isHit'] = hitPlayer(moby_id)
        packet["player_hit"] = PLAYER_MAP[moby_id[6:]] if packet['isHit'] else "FF"
        packet['weapon'] = weapon
        packet['receiving_id'] = moby_id
        packet['object_id'] = object_id
        packet['unk2'] = unk2
        packet['unk3'] = unk3
        packet['unk4'] = unk4
        packet['unk5'] = unk5
        packet['unk6'] = unk6
        packet['unk7'] = unk7
        packet['event'] = 8
        return packet

