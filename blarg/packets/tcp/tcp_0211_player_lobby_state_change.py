from collections import deque

from blarg.utils.utils import *

class tcp_0211_player_lobby_state_change:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        # Length = 32
        assert data.popleft() + data.popleft() + data.popleft() + data.popleft() == '00000000'
        packet_data = {}

        team_map = {
            '00': 'blue',
            '01': 'red',
            '02': 'green',
            '03': 'orange',
            '04': 'yellow',
            '05': 'purple',
            '06': 'aqua',
            '07': 'pink'
        }
        packet_data['team'] = team_map[data.popleft()]

        skin_map = {
            '00': 'ratchet',
            '01': 'robo',
            '02': 'thug',
            '03': 'tyhrranoid',
            '04': 'blarg',
            '05': 'ninja',
            '06': 'snow man',
            '07': 'bruiser',
            '08': 'gray',
            '09': 'hotbot',
            '0A': 'gladiola',
            '0B': 'evil clown',
            '0C': 'beach bunny',
            '0D': 'robo rooster',
            '0E': 'buginoid',
            '0F': 'branius',
            '10': 'skrunch',
            '11': 'bones',
            '12': 'nefarious',
            '13': 'trooper',
            '14': 'constructobot',
            '15': 'dan'
        }
        ready_map = {
            '06': 'ready',
            '01': 'not ready',
            '00': 'no change',
            '02': 'broadcast not ready',
            '04': 'change team request',
            '08': 'unk, player in-game ready(?)'
        }
        packet_data['skin'] = skin_map[data.popleft()]
        player_ready = data.popleft()
        packet_data['player_ready'] = ready_map[player_ready]
        packet_data['username'] = hex_to_str(''.join([data.popleft() for i in range(14)]))

        return packet_data
