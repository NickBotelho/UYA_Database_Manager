from collections import deque

from blarg.utils.utils import bytes_to_str, hex_to_bytes

class tcp_0210_player_join:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        result = {}
        # packet = data[48]
        # packet = hex_to_bytes(packet)
        # print(bytes_to_str(packet))
        data = "".join(list(data))
        packet = data[96:]
        packet = hex_to_bytes(packet)
        result['player_joined'] = bytes_to_str(packet)

        

        return result
