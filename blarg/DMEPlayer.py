from blarg.DMEWeapon import DMEWeapon
from blarg.DeathTracker import DeathTracker
from blarg.KillTracker import KillTracker
from blarg.Pedometer import Pedometer
from blarg.Medals import MedalTracker
from blarg.DMEController import Controller
class Player():
    def __init__(self, username, lobby_idx, team, lobbyItos):
        self.username = username
        self.lobby_idx = lobby_idx
        self.teamColor = team #str
        self.team = None #will be Team object
        self.isBot = self.checkBotStatus(username)
        self.kills = 0
        self.hp = 100
        self.deaths = 0
        self.killTracker = KillTracker(self)
        self.deathTracker = DeathTracker(self)
        self.medals = MedalTracker(self)
        self.caps, self.saves = 0, 0
        self.weapons = { #weaponNameToObject
            'Wrench':DMEWeapon('Wrench'),
            'Hypershot':DMEWeapon("Hypershot"),
            'Holo Shield':DMEWeapon("Holo Shield"),
        }
        self.controller = Controller(self)
        self.pedometer = Pedometer(self)
        self.x, self.y, self.rotation = -1, -1, -1
        self.isPlaced = False
        self.lastX, self.lastY = -1, -1
        self.disconnected = False
        self.fluxShots,self.fluxHits, self.fluxAccuracy = 0,0,0
        self.hasFlag = False
        self.flagPickups, self.flagDrops = 0, 0
        self.healthBoxesGrabbed = 0
        self.packsGrabbed = 0

        self.stagedNick = False
        self.nicker = None
        self.nicksReceived, self.nicksGiven = 0, 0
        self.damageTaken = 0

        self.deathTracker.initialize(lobbyItos)
        self.killTracker.initialize(lobbyItos)

    def __str__(self):
        # return "{} HP = {}, Kills = {}, Deaths = {}, Caps = {}".format(self.username, self.hp, self.kills, self.deaths, self.caps)
        return f"({self.lobby_idx} {self.username} [{self.teamColor}])"
    def setTeam (self, team):
        self.team = team
    def adjustHP(self, hp):
        self.damageTaken += abs(self.hp - hp)
        self.hp = hp
    def kill(self, enemy = None, weapon = "Wrench"):
        self.killTracker.kill(enemy)
        if weapon in self.weapons:
            self.weapons[weapon].kill()
        self.deathTracker.resetStreak()
        self.medals.kill(weapon)
        enemy.death(self)
    def death(self, killer = None, AI = None):
        self.deathTracker.die(killer = killer, AI = AI)
        self.deaths+=1
        self.killTracker.resetStreak()
        self.hasFlag = False
        self.hp = 0
        self.medals.death()
    def cap(self):
        self.caps+=1
        self.hasFlag=False
        self.team.dropFlags()
        self.medals.cap()
    def save(self):
        self.saves+=1
        self.team.saveFlags()
    def respawn(self):
        self.hp = 100
        self.hasFlag = False
        for weapon in self.weapons.values():
            weapon.die()
    def getKillstreak(self):
        return self.killTracker.killStreak
    def getDeathstreak(self):
        return self.deathTracker.deathStreak
    def heal(self):
        self.hp = 100
        self.healthBoxesGrabbed+=1
        self.medals.heal()

    def getLastCoords(self):
        return (self.lastX, self.lastY)
    def addWeapon(self, weapon):
        self.weapons[weapon] = DMEWeapon(weapon)
    def getState(self):
        state = {
            'name':self.username,
            'hp':self.hp,
            'kills':self.killTracker.kills,
            'deaths':self.deathTracker.deaths,
            'caps':self.caps,
            'saves':self.saves,
            'team':self.teamColor,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'hasFlag':self.hasFlag,
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'packs_grabbed':self.packsGrabbed,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getState() for w in self.weapons.values()},
            'damage_taken':self.damageTaken,
            'killHeatMap':self.killTracker.killHeatMap,
            'deathHeatMap':self.deathTracker.playerDeathHeatMap,
            'nonPlayerDeathHeatMap':self.deathTracker.nonPlayerDeathHeatMap,
            'killstreak':self.killTracker.killStreak,
            'bestKillstreak':self.killTracker.bestKillStreak,
            'death_info':self.deathTracker.getState(),
            'kill_info':self.killTracker.getState(),
            # 'controller':self.controller.getState(),

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
        self.medals.dropFlag()
    def fire(self, weapon, player_hit):
        if weapon != 'Wrench' or weapon != "Hypershot": self.hasFlag = False

        self.weapons[weapon].fire(player_hit)
        self.medals.fire(weapon, player_hit)
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
            'saves':self.saves,
            'team':self.teamColor,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'packs_grabbed':self.packsGrabbed,
            'health_boxes':self.healthBoxesGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getResult() for w in self.weapons.values()},
            'killHeatMap':self.killTracker.killHeatMap,
            'deathHeatMap':self.deathTracker.playerDeathHeatMap,
            'nonPlayerDeathHeatMap':self.deathTracker.nonPlayerDeathHeatMap,
            'disconnected':self.disconnected,
            'bestKillstreak':self.killTracker.bestKillStreak,
            'death_info':self.deathTracker.getState(),
            'kill_info':self.killTracker.getState(),
            # 'controller':self.controller.getState(),
            'medals':self.medals.getState(),
        }
    def getStore(self):
        '''goes into the player stats document for a player'''
        return {
            'live_games':1,
            'kills':self.killTracker.kills,
            'deaths':self.deathTracker.deaths,
            'saves':self.saves,
            'caps':self.caps,
            'distance_travelled':self.pedometer.getTotalDistance(),
            'flag_distance':self.pedometer.getFlagDistance(),
            'noFlag_distance':self.pedometer.getNoFlagDistance(),
            'flag_pickups':self.flagPickups,
            'flag_drops':self.flagDrops,
            'health_boxes':self.healthBoxesGrabbed,
            'packs_grabbed':self.packsGrabbed,
            'nicks_given':self.nicksGiven,
            'nicks_received':self.nicksReceived,
            'weapons':{w.weapon:w.getStore() for w in self.weapons.values()},
            'controller':self.controller.getState(),
            'medals':self.medals.getState(),
        }
    def hasJug(self):
        if "Flux" in self.weapons \
            and "Blitz" in self.weapons \
                and "Gravity Bomb" in self.weapons:
                return self.weapons['Flux'].createdV2 == True and self.weapons['Blitz'].createdV2 == True and self.weapons['Gravity Bomb'].createdV2 == True
    def pickupPack(self, pack):
        pack.pickup(self)
        self.packsGrabbed+=1
        self.medals.pack(pack)
    def pressButton(self, event):
        '''event is 0209['button'] which is a 2 or 4 digit string'''
        self.controller.track(event)

