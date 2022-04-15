from collections import deque
from blarg.utils.utils import *

class tcp_020A_player_respawn:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        
        result = {}
        result['event'] = 6
        result['player'] = data.popleft()
        result['unk'] = ''.join([data.popleft() for i in range(31)])
        return result
