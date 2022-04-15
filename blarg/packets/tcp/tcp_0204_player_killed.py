from collections import deque
from blarg.utils.utils import *
import os
import random
from blarg.constants.constants import WEAPON_MAP, KILL_MSG_MAP

'''
killer_id = 255 -> suicide
killer_id = 246 -> trooper
killer_id = 248 -> drones
'''

class tcp_0204_player_killed:
    def __init__(self, killer_id:int=None,
                           unk1:str='39',
                           killed_id:int=None,
                           weapon:str=None,
                           kill_msg:str=None,
                           unk2:str='00000001000000'
                        ):
        pass

        

    def serialize(self, data: deque):
        killer_id = hex_to_int_little(data.popleft())
        unk1 = data.popleft()
        killed_id = hex_to_int_little(data.popleft())
        weapon = WEAPON_MAP[data.popleft()]
        kill_msg = KILL_MSG_MAP[data.popleft()]
        unk2 = ''.join([data.popleft() for i in range(7)])
        packet = {
            'event':7,
            'killer_id':killer_id,
            'killed_id':killed_id,
            'weapon':weapon
        }
        return packet

    def to_bytes(self):
        return self.id + \
            int_to_bytes_little(1, self.killer_id) + \
            hex_to_bytes(self.unk1) + \
            int_to_bytes_little(1, self.killed_id) + \
            hex_to_bytes({v: k for k, v in WEAPON_MAP.items()}[self.weapon]) + \
            hex_to_bytes({v: k for k, v in KILL_MSG_MAP.items()}[self.kill_msg]) + \
            hex_to_bytes(self.unk2)

    def __str__(self):
        return f"{self.name}; killer_id:{self.killer_id} unk1:{self.unk1} killed_id:{self.killed_id} " + \
                f"weapon:{self.weapon} kill_msg:{self.kill_msg} unk2:{self.unk2}"