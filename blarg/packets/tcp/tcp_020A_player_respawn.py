from collections import deque
from blarg.utils.utils import *
from blarg.packets.tcp.tcp_020C_in_game_info import tcp_020C_in_game_info

class tcp_020A_player_respawn:
    def __init__(self):
        self.packParse = tcp_020C_in_game_info()

    def serialize(self, data: deque):
        
        result = {}
        result['event'] = 6
        result['player'] = data.popleft()
        result['unk'] = ''.join([data.popleft() for i in range(31)])
        if len(data) > 2:
            id = data.popleft() + data.popleft()
            if id == '020C':
                pack_info = self.packParse.serialize(data)
                result['pack_info'] = pack_info

        return result
