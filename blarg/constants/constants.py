TEAM_MAP = {
    '00': 'blue',
    '01': 'red',
    '02': 'green',
    '03': 'orange',
    '04': 'yellow',
    '05': 'purple',
    '06': 'aqua',
    '07': 'pink',
    'FF': 'NA'
}

SKIN_MAP = {
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
    '15': 'dan',
    'FF': 'NA'
}

KILL_MSG_MAP = {
    '00': 'butchered',
    '01': 'liquidated',
    '02': 'extirpated',
    '03': 'exterminated',
    '04': 'mousetrapped',
    '05': 'kervorked',
    '06': 'flatlined',
    '07': 'abolished',
    '08': 'eviscerated',
    '09': 'cremated',
    '0A': 'dismembered',
    '0B': 'euthanized',
    '0C': 'tomahawked',
    '0D': 'expunged',
    '0E': 'devastated',
    '0F': 'smoked',
}

WEAPON_MAP = {
    '01':"N60",
    '02': "Blitz",
    '03': "Flux",
    '04':"Rockets",
    '05': "Gravity Bomb",
    '06':"Mines",
    '07':"Lava Gun",
    '09':"Morph O' Ray",
    '0A':'Wrench',
    '0C':"Holo Shield",
    '0B':"Hypershot",
    'FF':'NA'
}


# FLUSH: 16
ANIMATION_MAP = {
    'forward': '4B',
    'backward': '6A',
    'left': '7A',
    'right': '5B',
    'forward-left': '43D6',
    'forward-right': '42D2',
    'backward-left': '63DE',
    'backward-right': '535A',
    'jump': 'EF',
    'crouch': '9C', # side flip: use flush = 148, spam crouch: 32
    'shoot': 'BD',
    'forward-shoot': '45D2',
    'jump-shoot': 'B77B'
}

HP_MAP ={
    1097859072:100,
    1096810496:93,
    1095761920:86,
    1094713344:80,
    1093664768:73,
    1092616192:66,
    1091567616:60,
    1090519040:53,
    1088421888:46,
    1086324736:40,
    1084227584:33,
    1082130432:26,
    1077936128:20,
    1073741824:13,
    1065353216:6,
    0:0
}
EVENTS = {
    0:"Flag Captured",
    1:"Flag Saved",
    2:"Flag Picked Up",
    3:"Turret Shields Closing",
    4:"Ammo Picked Up",
    5:"Flag Dropped",
    6:"Respawning",
    7:"Killed",
    8:"Firing",
    9:"Game Starting",
    10:"Game Created",
    11:"Player Joined",
    12:"Taking Damage",
    13:"Time",
    14:"Player Left",
}

TIMES = {
    'no_time_limit':None,
    '5_minutes':5,
    '10_minutes':10,
    '15_minutes':15,
    '20_minutes':20,
    '25_minutes':25,
    '30_minutes':30,
    '35_minutes':35,
}

BUTTONS = {
    '0':"Select",
    '1':"???",
    "2":"???",
    "3":'Start',
    '4':"Up",
    '5':"Right",
    '6':"Down",
    '7':"Left",
    '8':'L2',
    '9':'R2',
    'A':'L1',
    'B':'R1',
    'C':'Triangle',
    'D':'Circle',
    'E':'X',
    'F':'Square',
}

STREAK_CONTRACT = {
    'current_winstreak':0,
    'best_winstreak':0,
    'current_losingstreak':0,
    'best_losingstreak':0,
    'bestKillstreak':0,
    'bestDeathstreak':0,
}

LIVE_CONTRACT =  {
    "live_games":0,
    "kills": 0,
    "deaths": 0,
    "saves": 0,
    "caps": 0,
    "distance_travelled": 0,
    "flag_distance": 0,
    "noFlag_distance": 0,
    "flag_pickups": 0,
    "flag_drops": 0,
    "health_boxes": 0,
    "packs_grabbed":0,
    "nicks_given": 0,
    "nicks_received": 0,
    "weapons": {
        "Wrench": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Hypershot": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Holo Shield": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Flux": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Blitz": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Gravity Bomb": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Lava Gun": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Rockets": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Morph O' Ray": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "Mines": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        },
        "N60": {
            "kills": 0,
            "shots": 0,
            "hits": 0
        }
    },
    'medals':{
        "nuke":0,
        "brutal":0,
        "relentless":0,
        "bloodthirsty":0,
        "merciless":0,
        'undying': 0,
        'distributor':0,
        'thickskull': 0,
        'bloodfilled':0,
        'brutalized':0,
        'radioactive':0,
        'shifty':0,
        'lockon':0,
        'juggernaut':0,
        'olympiad':0,
        'dropper':0,
        'ratfuck':0,
        'healthrunner':0,
        }
}    