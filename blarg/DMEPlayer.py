class Player():
    def __init__(self, username, lobby_idx, team):
        self.username = username
        self.lobby_idx = lobby_idx
        self.team = team
        self.kills = 0
        self.hp = 0
        self.deaths = 0
        self.caps = 0
        self.x, self.y = -1, -1
        self.isPlaced = False
        self.lastX = -1
        self.distanceTravelled = 0
        self.fluxShots,self.fluxHits, self.fluxAccuracy = 0,0,0
        self.blitzShots,self.blitzHits, self.blitzAccuracy = 0,0,0
        self.hasFlag = False
        self.flagPickups, self.flagDrops = 0, 0
        self.healthBoxesGrabbed = 0
    def __str__(self):
        return "{} HP = {}, Kills = {}, Deaths = {}, Caps = {}".format(self.username, self.hp, self.kills, self.deaths, self.caps)
    def adjustHP(self, hp):
        self.hp = hp
    def kill(self):
        self.kills+=1
    def death(self):
        self.deaths+=1
        self.hp = 0
    def cap(self):
        self.caps+=1
        self.hasFlag=False
    def respawn(self):
        self.hp = 100
    def heal(self):
        self.hp = 100
        self.healthBoxesGrabbed+=1
    def getState(self):
        state = {
            'name':self.username,
            'hp':self.hp,
            'kills':self.kills,
            'deaths':self.deaths,
            'caps':self.caps,
            'team':self.team,
            'distance_travelled':self.distanceTravelled,
            'hasFlag':self.hasFlag,
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'flux_shots':self.fluxShots,
            'flux_hits':self.fluxHits,
            'flux_accuracy':self.fluxAccuracy,
            'blitz_shots':self.blitzShots,
            'blitz_hits':self.blitzHits,
            'blitz_accuracy':self.blitzAccuracy,
            'health_boxes':self.healthBoxesGrabbed
        }
        return state
    def place(self, coords):
        self.distanceTravelled = abs(self.distanceTravelled - coords[0]) if self.lastX != -1 else self.distanceTravelled
        self.x = coords[0]
        self.y = coords[1]
        self.isPlaced = True
    def unPlace(self):
        self.lastX = self.x
        self.x, self.y = -1, -1
        self.isPlaced = False
    def pickupFlag(self):
        self.hasFlag = True
        self.flagPickups+=1
    def dropFlag(self):
        self.hasFlag = False
        self.flagDrops+=1
    def fire(self, serialized):
        weapon = serialized['weapon'].lower()
        if weapon == "flux":
            self.fluxShots+=1
            self.fluxHits = self.fluxHits + 1 if serialized['player_hit'] != "FF" else self.fluxHits
            self.fluxAccuracy = round(self.fluxHits/self.fluxShots, 1)
        if weapon == "blitz":
            self.blitzShots+=1
            self.blitzHits = self.blitzHits + 1 if serialized['player_hit'] != "FF" else self.blitzHits
            self.blitzAccuracy = round((self.blitzHits/self.blitzShots)*100, 1)
        

