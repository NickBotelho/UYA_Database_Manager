from collections import deque
from blarg.utils.utils import *
from blarg.constants.constants import TEAM_MAP, SKIN_MAP, WEAPON_MAP, HP_MAP
player_id_map = {
    '0000': -1,
    '0100': 0,
    '0300': 1,
    '0600': 2,
    '0900': 3,
}
class tcp_0003_broadcast_lobby_state:
    def __init__(self):
        pass

    def serialize(self, data: deque):
        packet = {}
        packet['unk1'] = data.popleft() # 01

        packet['num_messages'] = bytes_to_int_little(hex_to_bytes(data.popleft()))
        messages = []
        # packet['src'] = player_id_map[data.popleft() + data.popleft()]
        packet['src'] = data.popleft() + data.popleft()

        for i in range(packet['num_messages']):
            sub_message = {
                'type':None
            }
            broadcast_type = data.popleft()
            #assert broadcast_type in ['02','03','05']

            if broadcast_type == '05': # Ready/Unready
                sub_message['type'] = 'ready/unready'
                for player_id in range(8):
                    val = data.popleft()
                    data.popleft()
                    sub_message[f'p{player_id}'] = val == '06'
            elif broadcast_type == '03': # Color
                sub_message['type'] = 'colors'
                for player_id in range(8):
                    val = data.popleft()
                    data.popleft()
                    sub_message[f'p{player_id}'] = TEAM_MAP[val]
            elif broadcast_type == '02': # Skins
                sub_message['type'] = 'skins'
                for player_id in range(8):
                    val = data.popleft()
                    data.popleft()
                    sub_message[f'p{player_id}'] = SKIN_MAP[val]
            elif broadcast_type == '07':
                sub_message['type'] = 'health'

                hp = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
                hp = HP_MAP[hp] if hp in HP_MAP else 100
                
                sub_message['health'] = hp
            elif broadcast_type == '09':
                sub_message['type'] = 'timer_update'
                if len(data) == 2:
                    sub_message['time'] = hex_to_int_little(''.join([data.popleft() for i in range(2)]))
                else:
                    sub_message['time'] = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
            elif broadcast_type == '0D':
                sub_message['type'] = 'unk_0D'
                sub_message['unk2'] = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
            # elif broadcast_type == '0A':
            #     sub_message['type'] = 'unk0A'
            #     sub_message['unk1'] = ''.join([data.popleft() for i in range(21)])
            #     packet[f'msg{i}'] = sub_message
            #     break
            # elif broadcast_type == '00':
            #     if len(data) == 3:
            #         sub_message['type'] = 'unk00'
            #         sub_message['unk1'] = ''.join([data.popleft() for i in range(3)])
            #     else:
            #         sub_message['type'] = 'settings_update'
            #         sub_message['unk1'] = ''.join([data.popleft() for i in range(283)])
            #     packet[f'msg{i}'] = sub_message
                break
            elif broadcast_type == '08':
                sub_message['type'] = 'weapon_changed'
                weap_changed_to = data.popleft()
                if weap_changed_to not in WEAPON_MAP:
                    sub_message['weapon_changed_to'] = 'NA'
                else:
                    sub_message['weapon_changed_to'] = WEAPON_MAP[weap_changed_to]

                sub_message['unk1'] = ''.join([data.popleft() for i in range(3)])
            else:
                # raise Exception(f'{broadcast_type} not known!')
                pass

            # packet[f'msg{i}'] = sub_message
            messages.append(sub_message)
        packet['messages'] = messages
        return packet
