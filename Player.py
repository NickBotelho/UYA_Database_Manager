from Parsers.PlayerClanParser import getClanId
from Parsers.ClanStatsParser import getClanTag
import requests
CLANS_API = 'http://107.155.81.113:8281/robo/clans/name' #/clanName
CACHE_LIMIT = 20
class Player():
    def __init__(self, packet) -> None:
        self.packet = packet
        self.cached_ticks = 0 #one tick = 30 seconds.
        self.parse()
    def parse(self):
        self.id = self.packet['account_id']
        self.username = self.packet['username']
        self.status = self.packet['status']
        self.ladderstatswide = self.packet['ladderstatswide']
        # self.clan_id = getClanId(self.packet['stats'])['clan_id']
        self.clan_name = self.packet['clan']
        self.clan_tag = self.packet['clan_tag']
        self.isBot = isBot(self.username)
        if self.clan_name != "" and not self.isBot:
            try:
                res = requests.get(f"{CLANS_API}/{self.clan_name}").json()
            except:
                res = {}
            self.clan_id = res['clan_id']
        else:
            self.clan_id = -1
    def updateCache(self):
        '''if player is in the cache. 
        this will increment ticks by 1 until threshold is met and is resets.
        
        Returns true if it is time to update the player'''
        self.cached_ticks+=1
        return self.cached_ticks >= CACHE_LIMIT
    def softUpdate(self, packet):
        self.id = packet['account_id']
        self.username = packet['username']
        self.status = packet['status']
        self.ladderstatswide = packet['ladderstatswide']
def isBot(username):
    '''bot names have prefixes of cpu so return false if the prefix is not cpu'''
    if len(username) <3: return False

    return username[:3].lower() == 'cpu' 