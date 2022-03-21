from collections import deque
from blarg.utils.utils import *

class udp_0200_player_death:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        CODs = {
            '7A':"Suicide",
            '39':"Kill Feed",
            '76':"Time Out in Glitch"
        }
        result = {}
        result['event'] = 7
        result['player_dead'] = data.popleft()
        cod = data.popleft() #cause of death
        result['cause of death'] = CODs[cod] if cod in CODs else "unknown death"
        return result

