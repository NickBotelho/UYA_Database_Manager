from collections import deque
from blarg.utils.utils import *

class tcp_020B_map_destruction:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        
        result = {}
        result['event'] = 'map being destroyed!'
        return result
