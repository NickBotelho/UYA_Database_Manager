from collections import deque
from blarg.utils.utils import *

class tcp_0018_initial_sync:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        result = {'name': 'initial sync'}

        #data.popleft() ## Unknown

        for _ in range(4): # 02000000
            data.popleft()

        # Get source
        result['src'] = data.popleft()

        for _ in range(7): # 000000C0000264
            data.popleft()

        result['time1'] = data.popleft() + data.popleft()

        for _ in range(6): # 000000000000
            data.popleft()

        result['time2'] = data.popleft() + data.popleft()

        for _ in range(9): # 000001000000001002
            data.popleft()

        result['src2'] = data.popleft()

        for _ in range(70): # C0A8010200006B8F99EC1BAF06D2674284B5305EE6E38B1DE7331F2FBF31DE497228B7C52162F18DAE8913C40C43C0E890D14EEE16AD07C64FD9281D8B972D78BE78D1B290CE
            data.popleft()

        return result
