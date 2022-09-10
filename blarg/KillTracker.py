
class KillTracker():
    def __init__(self, player) -> None:
        self.kills = 0
        self.playerKillMap = {}
        self.player = player
    def initialize(self, lobbyItos):
        for username in lobbyItos.values():
            if username != self.player.username:
                self.playerKillMap[username] = 0
    def kill(self, killed = None):
        self.kills+=1
        self.playerKillMap[killed.username] += 1

    def getState(self):
        return {
            'player_kill_map':self.playerKillMap,
        }

