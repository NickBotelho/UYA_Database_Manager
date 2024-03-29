class DMEWeapon():
    def __init__(self, gun):
        self.weapon = gun
        self.isV2 = False
        self.kills = 0
        self.shots = 0
        self.hits = 0
        self.streak = 0
        self.bestStreak = 0
        self.createdV2 = False
        self.v2sMade = 0
        self.foundV2 = False
    def kill(self):
        self.streak+=1
        self.bestStreak = self.streak if self.streak > self.bestStreak else self.bestStreak
        self.kills+=1
        if self.streak == 3 and self.isV2 == False:
            self.createdV2 = True
            self.v2sMade+=1
            self.isV2=True
    def isUpgrade(self):
        return self.isV2
    def die(self):
        self.bestStreak = self.streak if self.streak > self.bestStreak else self.bestStreak
        self.streak=0
        self.isV2 = False
        self.createdV2 = False
        self.foundV2 = False
    def fire(self, player_hit):
        self.shots+=1
        self.hits = self.hits + 1 if player_hit != "FF" else self.hits
    def getState(self):
        return {
            "weapon":self.weapon,
            'kills':self.kills,
            'isV2':self.isV2,
            'shots':self.shots//3 if self.weapon != "Flux" else self.shots,
            'hits':self.hits,
            'accuracy':round((self.hits/self.shots)*100, 1) if self.shots > 0 else 0,
            'killstreak':self.streak,
            'bestStreak': self.bestStreak,
            'made_v2s':self.v2sMade,
        }
    def getResult(self):
        return {
            "weapon":self.weapon,
            'kills':self.kills,
            'shots':self.shots//3 if self.weapon != "Flux" else self.shots,
            'hits':self.hits,
            'accuracy':round((self.hits/self.shots)*100, 1) if self.shots > 0 else 0,
            'made_v2s':self.v2sMade,
            'bestStreak': self.bestStreak,
        }
    def getStore(self):
        return {
            'kills':self.kills,
            'shots':self.shots//3 if self.weapon != "Flux" else self.shots,
            'hits':self.hits,
            'made_v2s':self.v2sMade,
        }
    def pickupV2(self):
        if self.isV2 == False:
            self.foundV2 = True
            self.isV2 = True
