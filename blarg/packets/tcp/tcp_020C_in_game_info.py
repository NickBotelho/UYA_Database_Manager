from collections import deque
from blarg.utils.utils import *
from blarg.constants.constants import WEAPON_MAP

subtype_map = {
    '10401F00': '?_crate_destroyed',
    '41401F00': 'weapon_pickup',
    '00401F00': 'crate_destroyed',
    '02401F00': 'crate_respawn',
    '00000000': 'crate_destroyed_and_pickup', #
    '10000000': '?_crate_destroyed_and_pickup',
    '40401F00': 'object_update',
    '21000000': 'flag_update', #
    '02411F00': 'flag_drop',
    '80421F00': 'pack_spawned',
    'C2803E00':"damaging_base_turret"
}
player_map = {
    '00' : 0,
    '04' : 1,
    '08' : 2,
    '0C' : 3,
    '10' : 4,
    '14' : 5,
    '18' : 6,
    '1C' : 7,

}
player_focused = {
    '21' : "player_flag_interaction",
    # '00' : "player_crate_interaction"
}
object_focused = {

}
class tcp_020C_in_game_info:
    def __init__(self):
        pass

    def serialize(self, data: deque):

        subtype = ''.join([data.popleft() for i in range(4)])
        # subtype = subtype_map[subtype]
        timestamp = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
        object_id = ''.join([data.popleft() for i in range(4)])

        packet = {
            "subtype":subtype
        }

        subtypeFocus = subtype[:2]
        if subtypeFocus in player_focused:
            focus = player_focused[subtypeFocus]
            # print(subtype)
            player_mapped = player_map[subtype[2:4]]
            if focus == 'player_flag_interaction':
                code = data.popleft()
                player_idx = data.popleft()
                updateType = 'cap' if code == '01' else 'save'
                packet['player_idx'] = player_idx
                packet['updateType'] = updateType
                packet['event'] = 0 if updateType == 'cap' else 1
            elif focus == 'player_crate_interaction':
                pass

        else:                
            if subtype in subtype_map:
                subtype = subtype_map[subtype]
                if subtype in ['?_crate_destroyed_and_pickup', '?_crate_destroyed']:
                    packet['weapon_spawned'] = WEAPON_MAP[data.popleft()]
                elif subtype == 'weapon_pickup':
                    packet['weapon_pickup_unk'] =  ''.join([data.popleft() for i in range(4)])
                    packet['item_picked_up_id'] = object_id
                    packet['event'] = 4
                elif subtype == 'object_update':
                    packet['event'] = 2
                    packet['object_update_unk'] =  ''.join([data.popleft() for i in range(4)])    
                    packet['object_id'] = object_id
                elif subtype == 'flag_drop':
                    packet['event'] = 5 #flag dropped
                    packet['flag_drop_unk'] =  ''.join([data.popleft() for i in range(16)])
                elif subtype == 'pack_spawned':
                    packet['object id'] = object_id
                    packet['pack_id'] = "".join([data.popleft() for i in range(4)])
                    packet['pack_info'] = "".join([data.popleft() for i in range(36)])
        return packet
















# class tcp_020C_in_game_info:
#     def __init__(self):
#         pass

#     def serialize(self, data: deque):

#         teams = {
#             '6110' : "Blue", #kisi
#             '4B10' : "Blue", #hoven
#             '6410' : "Blue", #x12      0100110000000000
#             '5A10' : "Blue", #metro
#             '5110' : "Blue", #bwc      0101000100000000
#             '1310' : "Blue", #marc, cc 0001001100000000
#             '4410' : "Red", #kisi``
#             '5010' : "Red", #hoven
#             '4D10' : "Red", #x12       0100110100000000

#             '5210' : "Red", #bwc       0101001000000000
#             '1410' : "Red", #marc, cc  0001010000000000

#         }



#         weapon_keys = {
#             '0710':'blitz',
#             '0610':'blitz',
#             '0210':'grav',
#             '0110':'grav',
#             '1B10':'grav',
#             '1110':'chargeboots',
#             '1210':'chargeboots',
#             '0410':'flux',
#             '0510':'flux',
#             '0C10':'mines',
#             '0D10':'mines',
#             '0810':'lava gun',
#             '0910':'lava gun',
#             '2910':'lava gun',
#             '3210':'morph',
#             '0B10':'holos',
#             '0A10':'holos',
#             '0310':'rockets',
#             '1E10':'rockets',

#             '0F10':'health',
#             '0E10':'health',

#         }
#         # EVENTS = {
#         #     0:"Flag Captured",
#         #     1:"Flag Saved",
#         #     2:"Flag Picked Up",
#         #     3:"Turret Shields Closing",
#         #     4:"Ammo Picked Up",
#         #     5:"Flag Dropped"
#         # }
        
#         messages = []
#         result = {}
#         broadcast_type = data.popleft() + (data.popleft())[:-1]
#         result['broadcast'] = broadcast_type
#         # print(f"BROADCAST TYPE = {broadcast_type}")
#         # print(data)


#         if broadcast_type == '210': #2100
#             player_idx = data.pop()
#             code = data.pop()
#             for i in range(3):data.pop()
#             team = data.pop()
#             if code == '01':
#                 result['event'] = 0 #cap
#             elif code == '00':    
#                 result['event'] = 1 #Returns opposite team of the saved flag

#             result['player'] = player_idx
#             result['team'] = team

            

#         elif broadcast_type =='404': #4040
#             code = None
#             if len(data) == 14:
#                 code = data[len(data)-4] + data[len(data)-3] + data[len(data)-2] + data[-1]
#             team = teams[data[6]+ data[7]] if data[6]+data[7] in teams else "unknown"
#             if code == 'FFFFFFFF':
#                 result['event'] = 3 #shield close
#             elif code == '00000000':
#                 result['event'] = 2 #flag pickup
#                 # print(data[6]+ data[7], team)

#                 result['team'] = team
#             elif code == '01000000':
#                 result['event'] = 4 #ammo pickup




#         elif broadcast_type == '024': #0241
#             result['event'] = 5 #flag drop
#             team = teams[data[6]+ data[7]] if data[6]+data[7] in teams else "unknown"
#             result['team'] = team
#         # elif broadcast_type == '004': #004
#         #     result['type'] = 'box broken'
#         #     # weapon = weapon_keys[data[6] + data[7]]
#         #     # result['event'] = f"{weapon} box broken"
#         # elif broadcast_type == '0040':
#         #     result['type'] = 'mystery box broken'
#         #     # weapon = weapon_keys[data[6] + data[7]]
#         #     # result['event'] = f"{weapon} box broken"
#         # elif broadcast_type == '4140':
#         #     result['type'] = 'item pickup'
#         #     # weapon = weapon_keys[data[6] + data[7]]
#         #     # result['event'] = f"{weapon} picked up"
#         # elif broadcast_type == '0240':
#         #     result['type'] = 'box spawned'
#         #     # weapon = weapon_keys[data[6] + data[7]]
#         #     # result['event'] = f"{weapon} box spawned"
#         # elif broadcast_type == '0000':
#         #     result['type'] = 'box broken and gun picked up'
#         #     # weapon = weapon_keys[data[6] + data[7]]
#         #     # result['event'] = f"{weapon} opened and taken"
#         # # elif broadcast_type == '0140':
#         # #     result['type'] = 'turret destroyed'
#         # elif broadcast_type == '8100':
#         #     result['type'] = 'player began spinning node'
#         # elif broadcast_type == 'D040':
#         #     result['type'] = 'player spinning node'
#         # elif broadcast_type == '8040':
#         #     result['type'] = 'node captured'
#         # elif broadcast_type == '4200':
#         #     result['type'] = 'player entered vehicle'
#         # elif broadcast_type == '4F00':
#         #     result['type'] = 'player exited vehicle'
#         # elif broadcast_type == 'C280':
#         #     result['type'] = 'Base turret being damaged'
#         return result


