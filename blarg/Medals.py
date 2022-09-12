
#nuke = 35 kills
#distrubtor = 25
#radioactive = kills on a 25 streak
NUKE_KILLS = 35
DISTRIBUTOR_KILLS = 25
class Medal():
    def __init__(self, player):
        self.player = player
        self.distributorStreak = 0
        self.nukes = 0
        self.distributors = 0
        self.radioactives = 0
        self.undying = 0

    def kill(self, weapon = "Wrench"):
        streak = self.player.getKillstreak()
        if streak == NUKE_KILLS:
            self.nukes+=1
        elif streak > NUKE_KILLS:
            self.radioactives+=1
        elif streak == 15:
            self.undying+=1

    def death(self):
        streak = self.player.getDeathstreak()
        if streak == DISTRIBUTOR_KILLS:
            self.distributors+=1

    def getState(self):
        return {
            'nukes':self.nukes,
            'distributors':self.distributors,
            'radioactives':self.radioactives,
            'undying':self.undying,
        }

