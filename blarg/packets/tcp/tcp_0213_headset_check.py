from collections import deque

class tcp_0213_headset_check:
    def __init__(self):
        pass

    def serialize(self, data: deque):

        result = {}

        # '00000000' (4 bytes, just an integer, usually 0)
        buf = ''.join([data.popleft() for i in range(4)])

        return result
