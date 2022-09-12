
class DeathTracker():
    def __init__(self, player) -> None:
        self.deaths = 0
        self.deathStreak = 0,
        self.bestDeathStreak = 0
        self.nonPlayerDeathMap = {
            'Suicide':0,
            'Trooper':0,
            'Drones':0,
            "Shock Droids":0
        }
        self.playerDeathMap = {}
        self.player = player
        self.playerDeathHeatMap = []
        self.nonPlayerDeathHeatMap = []
    def initialize(self, lobbyItos):
        for username in lobbyItos.values():
            if username != self.player.username:
                self.playerDeathMap[username] = 0
    def resetStreak(self):
        self.deathStreak=0
    def die(self, killer = None, AI = None):
        if killer != None:
            self.playerDeathMap[killer.username] += 1
            self.playerDeathHeatMap.append(self.player.getLastCoords())
        if AI != None:
            self.nonPlayerDeathMap[AI] += 1
            self.nonPlayerDeathHeatMap.append(self.player.getLastCoords())

        self.deaths+=1
        self.deathStreak+=1
        self.bestDeathStreak = max(self.deathStreak, self.bestDeathStreak)
    def getState(self):
        return {
            'player_death_map':self.playerDeathMap,
            'nonPlayer_death_map':self.nonPlayerDeathMap,
            'current_deathstreak':self.deathStreak,
            'best_deathstreak':self.bestDeathStreak
        }

