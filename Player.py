from Parsers.PlayerClanParser import getClanId
from Parsers.ClanStatsParser import getClanTag
import requests
CLANS_API = 'https://uya.raconline.gg/tapi/robo/clans/id' #/clanId
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
        self.clan_id = getClanId(self.packet['stats'])['clan_id']
        self.clan_name = None
        if self.clan_id != -1:
            try:
                res = requests.get(f"{CLANS_API}/{self.clan_id}").json()
            except:
                res = {}
            self.clan_name = res['clan_name']
            self.clan_tag = getClanTag(res['clan_stats']) if len(res) > 0 else ""
            self.clan_tag = "".join([char for char in self.clan_tag if len(char)==1])
        else:
            self.clan_tag = ""
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
