from collections import deque
from blarg.utils.utils import *
from blarg.constants.constants import WEAPON_MAP

subtype_map = {
    '10401F00': '?_crate_destroyed',
    # '41401F00': 'weapon_pickup',
    '41401F00': 'weapon_pickup_unk?_p0',
    '41441F00': 'weapon_pickup_unk?_p1',
    '41481F00': 'weapon_pickup_unk?_p2',
    '414C1F00': 'weapon_pickup_unk?_p3',
    '41501F00': 'weapon_pickup_unk?_p4',
    '41541F00': 'weapon_pickup_unk?_p5',
    '41581F00': 'weapon_pickup_unk?_p6',
    '415C1F00': 'weapon_pickup_unk?_p7',
    '00401F00': 'crate_destroyed',
    '02401F00': 'crate_respawn',
    '02441F00': 'crate_respawn_p1?',
    '00000000': 'crate_destroyed_and_pickup',
    '10000000': '?_crate_destroyed_and_pickup',
    '80421F00': 'pack_spawned',

    #drops (5)
    '02411F00': 'p0_flag_drop',
    '02451F00': 'p1_flag_drop',
    '02491F00': 'p2_flag_drop',
    '024D1F00': 'p3_flag_drop',
    '02511F00': 'p4_flag_drop',
    '02551F00': 'p5_flag_drop',
    '02591F00': 'p6_flag_drop',
    '025D1F00': 'p7_flag_drop',

    '61000000': 'p0_confirm',
    '61040000': 'p1_confirm',
    '61080000': 'p2_confirm',
    '610C0000': 'p3_confirm',
    '61100000': 'p4_confirm',
    '61140000': 'p5_confirm',
    '61180000': 'p6_confirm',
    '611C0000': 'p7_confirm',

    '73000000': 'p0_req_confirmation',
    '73040000': 'p1_req_confirmation',
    '73080000': 'p2_req_confirmation',
    '730C0000': 'p3_req_confirmation',
    '73100000': 'p4_req_confirmation',
    '73140000': 'p5_req_confirmation',
    '73180000': 'p6_req_confirmation',
    '731C0000': 'p7_req_confirmation',

    
    '40401F00': 'p0_object_update',
    '40441F00': 'p1_object_update',
    '40481F00': 'p2_object_update',
    '404C1F00': 'p3_object_update',
    '40501F00': 'p4_object_update',
    '40541F00': 'p5_object_update',
    '40581F00': 'p6_object_update',
    '405C1F00': 'p7_object_update',

    #pickup (2)
    '21000000': 'p0_flag_update',
    '21040000': 'p1_flag_update',
    '21080000': 'p2_flag_update',
    '210C0000': 'p3_flag_update',
    '21100000': 'p4_flag_update',
    '21140000': 'p5_flag_update',
    '21180000': 'p6_flag_update',
    '211C0000': 'p7_flag_update',

}
#5
flag_drop_map = {
    '0100': 'p0_capture',
    '0101': 'p1_capture',
    '0102': 'p2_capture',
    '0103': 'p3_capture',
    '0104': 'p4_capture',
    '0105': 'p5_capture',
    '0106': 'p6_capture',
    '0107': 'p7_capture',
    '00FF': 'flag_return',
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
        if subtype not in subtype_map: return {}
        subtype = subtype_map[subtype]
        timestamp = hex_to_int_little(''.join([data.popleft() for i in range(4)]))
        object_id = ''.join([data.popleft() for i in range(4)])

        packet = {
            "subtype":subtype
        }

        if subtype in ['?_crate_destroyed_and_pickup', '?_crate_destroyed']:
            packet['object_id'] = object_id
            packet['event'] = 4
            # packet['weapon_spawned'] = WEAPON_MAP[data.popleft()]
        elif 'weapon_pickup' in subtype:
            packet['weapon_pickup_unk'] =  ''.join([data.popleft() for i in range(4)])
            packet['object_id'] = object_id
            packet['event'] = 4
        elif 'object_update' in subtype:
            packet['object_update_unk'] =  ''.join([data.popleft() for i in range(4)])
            packet['object_id'] = object_id
            packet['event'] = 2
        elif 'flag_update' in subtype:
            packet['object_id'] = object_id
            flagDropKey = ''.join([data.popleft() for i in range(2)])
            packet['flag_update_type'] =  flag_drop_map[flagDropKey] if flagDropKey in flag_drop_map else flagDropKey
            packet['event'] = 1 if flagDropKey not in flag_drop_map or packet['flag_update_type'] == 'flag_return' else 0
        elif 'flag_drop' in subtype:
            packet['object_id'] = object_id
            packet['event'] = 5
            packet['flag_drop_unk'] =  ''.join([data.popleft() for i in range(16)])
        elif 'crate_destroyed_and_pickup' in subtype:
            packet['object_id'] = object_id
            packet['event'] = 4
        elif 'crate_destroyed' in subtype:
            packet['object_id'] = object_id

        # elif subtype in ['p0_confirm', 'p1_confirm', 'p2_confirm', 'p3_confirm', 'p4_confirm', 'p5_confirm', 'p6_confirm', 'p7_confirm']:
        #     packet['object_id'] = ''.join([data.popleft() for i in range(4)])
        #     packet['unk'] = ''.join([data.popleft() for i in range(2)])
        # elif subtype in ['p0_req_confirmation', 'p1_req_confirmation', 'p2_req_confirmation', 'p3_req_confirmation', 'p4_req_confirmation', 'p5_req_confirmation', 'p6_req_confirmation', 'p7_req_confirmation']:
        #     packet['object_id'] = ''.join([data.popleft() for i in range(4)])
        #     packet['buf'] = ''.join([data.popleft() for i in range(1)])
        #     packet['unk'] = ''.join([data.popleft() for i in range(2)])
        elif subtype == 'crate_respawn?':
            packet['object_id'] = object_id
            
        # elif subtype == 'weapon_pickup_unk?_p1':
        #     packet['unk'] =  ''.join([data.popleft() for i in range(4)])
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


