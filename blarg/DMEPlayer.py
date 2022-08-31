from blarg.DMEWeapon import DMEWeapon
X12_UNIT = 35162
class Player():
    def __init__(self, username, lobby_idx, team):
        self.username = username
        self.lobby_idx = lobby_idx
        self.team = team
        self.kills = 0
        self.hp = 100
        self.deaths = 0
        self.caps = 0
        self.weapons = { #weaponNameToObject
            'Wrench':DMEWeapon('Wrench'),
            'Hypershot':DMEWeapon("Hypershot")
        }
        self.enemyNameToKills = {}
        self.x, self.y = -1, -1
        self.isPlaced = False
        self.lastX, self.lastY = -1, -1
        self.distanceTravelled = 0
        self.fluxShots,self.fluxHits, self.fluxAccuracy = 0,0,0
        self.blitzShots,self.gravityBombShots= 0,0
        self.hasFlag = False
        self.flagPickups, self.flagDrops = 0, 0
        self.healthBoxesGrabbed = 0

        self.stagedNick = False
        self.nicker = None
        self.nicksReceived, self.nicksGiven = 0, 0

        self.killHeatMap = [] #list of coords where player kill
        self.deathHeatMap = [] #list of coords where player kill

    def __str__(self):
        return "{} HP = {}, Kills = {}, Deaths = {}, Caps = {} (isPlaced = {})".format(self.username, self.hp, self.kills, self.deaths, self.caps, self.isPlaced)
    def adjustHP(self, hp):
        self.hp = hp
    def kill(self, enemy = None, weapon = "Wrench"):
        self.kills+=1
        self.enemyNameToKills[enemy.username] = 1 if enemy.username not in self.enemyNameToKills else self.enemyNameToKills[enemy.username] + 1
        self.weapons[weapon].kill()
        self.killHeatMap.append((self.lastX, self.lastY))
    def death(self):
        self.deaths+=1
        self.hp = 0
        self.deathHeatMap.append((self.lastX, self.lastY))
    def cap(self):
        self.caps+=1
        self.hasFlag=False
    def respawn(self):
        self.hp = 100
    def heal(self):
        self.hp = 100
        self.healthBoxesGrabbed+=1
    def addWeapon(self, weapon):
        self.weapons[weapon] = DMEWeapon(weapon)
    def getState(self):
        state = {
            'name':self.username,
            'hp':self.hp,
            'kills':self.kills,
            'deaths':self.deaths,
            'caps':self.caps,
            'team':self.team,
            'distance_travelled':round(self.distanceTravelled/X12_UNIT, 2),
            'hasFlag':self.hasFlag,
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.toJson() for w in self.weapons.values()},
            'killHeatMap':self.killHeatMap,
            'deathHeatMap':self.deathHeatMap

        }
        return state
    def place(self, coords):
        self.distanceTravelled = self.distanceTravelled + abs(self.lastX - coords[0]) if self.lastX != -1 else self.distanceTravelled
        self.x = coords[0]
        self.y = coords[1]
        self.isPlaced = True
    def unPlace(self):
        self.lastX, self.lastY = self.x, self.y
        self.x, self.y = -1, -1
        self.isPlaced = False
    def pickupFlag(self):
        self.hasFlag = True
        self.flagPickups+=1
    def dropFlag(self):
        self.hasFlag = False
        self.flagDrops+=1
    def fire(self, weapon, player_hit):
        self.weapons[weapon].fire(player_hit)
    def stageNick(self, nicker):
        '''Nicker is the player object that shot the nickee'''
        self.stagedNick = True
        self.nicker = nicker
    def checkNick(self, hp):
        if self.stagedNick:
            if self.hp > 20 and abs(self.hp - hp) < 87:
                self.nicker.addNick()
                self.nicksReceived+=1
            self.nicker = None
            self.stagedNick = False
    def addNick(self):
        self.nicksGiven+=1
