
class DeathTracker():
    def __init__(self, player) -> None:
        self.deaths = 0
        self.nonPlayerDeathMap = {
            'Suicide':0,
            'Trooper':0,
            'Drones':0,
            "Shock Droids":0
        }
        self.playerDeathMap = {}
        self.player = player
    def initialize(self, lobbyItos):
        for username in lobbyItos.values():
            if username != self.player.username:
                self.playerDeathMap[username] = 0
    def die(self, killer = None, AI = None):
        if killer != None:
            self.playerDeathMap[killer.username] += 1
        if AI != None:
            self.nonPlayerDeathMap[AI] += 1

        self.deaths+=1
    def getState(self):
        return {
            'player_death_map':self.playerDeathMap,
            'nonPlayer_death_map':self.nonPlayerDeathMap
        }

