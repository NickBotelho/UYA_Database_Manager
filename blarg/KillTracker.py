
class KillTracker():
    def __init__(self, player) -> None:
        self.kills = 0
        self.killStreak = 0
        self.bestKillStreak = 0
        self.playerKillMap = {}
        self.player = player
        self.killHeatMap = []
    def initialize(self, lobbyItos):
        for username in lobbyItos.values():
            if username != self.player.username:
                self.playerKillMap[username] = 0
    def resetStreak(self):
        self.killStreak=0
    def kill(self, killed = None):
        self.kills+=1
        self.killStreak+=1
        self.bestKillStreak = max(self.bestKillStreak, self.killStreak)
        self.playerKillMap[killed.username] += 1
        self.killHeatMap.append(self.player.getLastCoords())
    def getState(self):
        return {
            'player_kill_map':self.playerKillMap,
            'current_killstreak':self.killStreak,
            'best_killstreak':self.bestKillStreak
        }

