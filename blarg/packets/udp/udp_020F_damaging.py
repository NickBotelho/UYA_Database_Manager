from collections import deque
from blarg.utils.utils import *

class udp_020F_damaging:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        result = {}
        result['event'] = 12

        return result

