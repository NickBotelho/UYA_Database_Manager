from collections import deque
import os
from blarg.utils.utils import *

class tcp_0012_player_left:
    def __init__(self, unk1:str='00'):
        self.name = os.path.basename(__file__).strip(".py")
        self.id = b'\x00\x12'
        self.unk1 = unk1

    @classmethod
    def serialize(self, data: deque):
        unk1 = data.popleft()
        return {'event':14, 'player':unk1}

    def to_bytes(self):
        return self.id + \
            hex_to_bytes(self.unk1)

    def __str__(self):
        return f"{self.name}; unk1:{self.unk1}"
