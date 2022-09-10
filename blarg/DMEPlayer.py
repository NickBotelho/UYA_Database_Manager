from blarg.DMEWeapon import DMEWeapon
from blarg.DeathTracker import DeathTracker
from blarg.KillTracker import KillTracker
from blarg.Pedometer import Pedometer
class Player():
    def __init__(self, username, lobby_idx, team, lobbyItos):
        self.username = username
        self.lobby_idx = lobby_idx
        self.team = team
        self.isBot = self.checkBotStatus(username)
        self.kills = 0
        self.hp = 100
        self.deaths = 0
        self.killTracker = KillTracker(self)
        self.deathTracker = DeathTracker(self)
        self.caps = 0
        self.weapons = { #weaponNameToObject
            'Wrench':DMEWeapon('Wrench'),
            'Hypershot':DMEWeapon("Hypershot"),
            'Holo Shield':DMEWeapon("Holo Shield"),
        }
        self.pedometer = Pedometer()
        self.x, self.y, self.rotation = -1, -1, -1
        self.isPlaced = False
        self.lastX, self.lastY = -1, -1
        self.distanceTravelled = 0
        self.disconnected = False
        self.fluxShots,self.fluxHits, self.fluxAccuracy = 0,0,0
        self.hasFlag = False
        self.flagPickups, self.flagDrops = 0, 0
        self.healthBoxesGrabbed = 0

        self.stagedNick = False
        self.nicker = None
        self.nicksReceived, self.nicksGiven = 0, 0
        self.damageTaken = 0
        self.killstreak = 0
        self.bestKillstreak = 0

        self.killHeatMap = [] #list of coords where player kill
        self.deathHeatMap = [] #list of coords where player kill
        self.deathTracker.initialize(lobbyItos)
        self.killTracker.initialize(lobbyItos)

    def __str__(self):
        return "{} HP = {}, Kills = {}, Deaths = {}, Caps = {}".format(self.username, self.hp, self.kills, self.deaths, self.caps)
    def adjustHP(self, hp):
        self.damageTaken += abs(self.hp - hp)
        self.hp = hp
    def kill(self, enemy = None, weapon = "Wrench"):
        self.killTracker.kill(enemy)
        self.killstreak+=1
        self.bestKillstreak = self.killstreak if self.killstreak > self.bestKillstreak else self.bestKillstreak
        self.weapons[weapon].kill()
        self.killHeatMap.append((self.lastX, self.lastY))
        enemy.death(self)
    def death(self, killer = None, AI = None):
        self.deathTracker.die(killer = killer, AI = AI)
        self.deaths+=1
        self.bestKillstreak = self.killstreak if self.killstreak > self.bestKillstreak else self.bestKillstreak
        self.killstreak=0
        self.hasFlag = False
        self.hp = 0
        self.deathHeatMap.append((self.lastX, self.lastY))
        for weapon in self.weapons.values():
            weapon.die()
    def cap(self):
        self.caps+=1
        self.hasFlag=False
    def respawn(self):
        self.hp = 100
        self.hasFlag = False
    def heal(self):
        self.hp = 100
        self.healthBoxesGrabbed+=1
    def addWeapon(self, weapon):
        self.weapons[weapon] = DMEWeapon(weapon)
    def getState(self):
        state = {
            'name':self.username,
            'hp':self.hp,
            'kills':self.killTracker.kills,
            'deaths':self.deathTracker.deaths,
            'caps':self.caps,
            'team':self.team,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'hasFlag':self.hasFlag,
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getState() for w in self.weapons.values()},
            'damage_taken':self.damageTaken,
            'killHeatMap':self.killHeatMap,
            'deathHeatMap':self.deathHeatMap,
            'killstreak':self.killstreak,
            'bestKillstreak':self.bestKillstreak,
            'death_info':self.deathTracker.getState(),
            'kill_info':self.killTracker.getState(),

        }
        return state
    def place(self, coords, rotation):
        self.pedometer.walk(self.lastX, coords[0], self.hasFlag)
        self.x = coords[0]
        self.y = coords[1]
        self.rotation = rotation
        self.isPlaced = True
    def unPlace(self):
        self.lastX, self.lastY = self.x, self.y
        self.x, self.y, self.rotation = -1, -1, -1
        self.isPlaced = False
    def pickupFlag(self):
        self.hasFlag = True
        self.flagPickups+=1
    def dropFlag(self):
        self.hasFlag = False
        self.flagDrops+=1
    def fire(self, weapon, player_hit):
        self.weapons[weapon].fire(player_hit)
    def quit(self):
        self.disconnected = True
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
    def checkBotStatus(self, username):
        if len(username) > 3:
            if username[:3].lower() == "cpu":
                return True
        return False
    def getResult(self):
        '''Goes into the game history document'''
        return {
            'kills':self.killTracker.kills,
            'deaths':self.deathTracker.deaths,
            'caps':self.caps,
            'team':self.team,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getResult() for w in self.weapons.values()},
            'killHeatMap':self.killHeatMap,
            'deathHeatMap':self.deathHeatMap,
            'disconnected':self.disconnected,
            'bestKillstreak':self.bestKillstreak,
            'death_info':self.deathTracker.getState(),
            'kill_info':self.killTracker.getState(),
        }
    def getStore(self):
        '''goes into the player stats document for a player'''
        return {
            'kills':self.killTracker.kills,
            'deaths':self.deathTracker.deaths,
            'caps':self.caps,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getStore() for w in self.weapons.values()},
        }
