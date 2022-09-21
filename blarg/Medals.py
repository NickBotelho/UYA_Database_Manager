import datetime

NUKE_KILLS = 35
BRUTAL_KILLS = 25
RELENTLESS_KILLS = 20
UNDYING_KILLS = 15
MERCILESS_KILLS = 10
BLOODTHIRSTY_KILLS = 5

DISTRIBUTOR_KILLS = 35
BRUTALIZED_KILLS = 25
THICKSKULL_KILLS = 15
BLOODFILLED_KILLS = 5


DESCRIPTIONS = {
    "nuke":f"{NUKE_KILLS} Kill streak",
    "brutal":f"{BRUTAL_KILLS} Kill streak",
    "relentless":f"{RELENTLESS_KILLS} Kill streak",
    "bloodthirsty":f"{BLOODTHIRSTY_KILLS} Kill streak",
    "merciless":f"{MERCILESS_KILLS} Kill streak",
    'undying': f"{UNDYING_KILLS} Kill streak",

    'distributor':f"{DISTRIBUTOR_KILLS} Death streak",
    'thickskull': f"{THICKSKULL_KILLS} Death streak",
    'bloodfilled':f"{BLOODFILLED_KILLS} Death streak",
    'brutalized':f"{BRUTALIZED_KILLS} Death streak",

    'radioactive':"A single kill after dropping a nuke on the same life",
    'shifty':"Getting back to back caps without dying",
    'lockon':"Hit 5 flux shots on players in a row without missing",
    'juggernaut':'Make a jug in a single life',
    'olympiad':"Travel 5 miles in a single life",
    'dropper':"Drop the flag and kill someone within 10 seconds",
    'ratfuck':'Consume 5 v2 contained packs in one life'
}
class Medal():
    def __init__(self, name, threshold = None) -> None:
        self.name = name
        self.description = DESCRIPTIONS[name] if name in DESCRIPTIONS else "Description not found"
        self.threshold = threshold
        self.numAchieved = 0
    def track(self, streak):
        if streak == self.threshold:
            self.numAchieved+=1

class Shifty(Medal):
    def __init__(self) -> None:
        super().__init__("shifty", None)
        self.onStreak = False
    def track(self, onCapStreak = False):
        if onCapStreak:
            self.numAchieved+=1

class Radioactive(Medal):
    def __init__(self) -> None:
        super().__init__("radioactive", 35)
    def track(self, streak):
        if streak > self.threshold:
            self.numAchieved+=1
class Distributor(Medal):
    def __init__(self) -> None:
        super().__init__("distributor", 35)
class Brutalized(Medal):
    def __init__(self) -> None:
        super().__init__("brutalized", 25)
class Thickskull(Medal):
    def __init__(self) -> None:
        super().__init__("thickskull", 15)
class Bloodfilled(Medal):
    def __init__(self) -> None:
        super().__init__("distributor", 5)
class Nuke(Medal):
    def __init__(self) -> None:
        super().__init__("nuke", 35)
class Brutal(Medal):
    def __init__(self) -> None:
        super().__init__("brutal", 25)
class Relentless(Medal):
    def __init__(self) -> None:
        super().__init__("relentless", 20)
class Undying(Medal):
    def __init__(self) -> None:
        super().__init__("undying", 15)
class Merciless(Medal):
    def __init__(self) -> None:
        super().__init__("merciless", 10)
class Bloodthirsty(Medal):
    def __init__(self) -> None:
        super().__init__("bloodthirsty", 5)
class LockOn(Medal):
    def __init__(self) -> None:
        super().__init__("lockon", 5)
        self.hits = 0 #shots in a row
    def track(self, player_hit):
        self.hits = self.hits + 1 if player_hit != "FF" else 0
        if self.hits == self.threshold:
            self.numAchieved+=1
            self.hits = 0
class HeatingUp(Medal):
    def __init__(self) -> None:
        super().__init__("heatingup", 3)
        self.hits = 0 #shots in a row
    def track(self, player_hit):
        self.hits = self.hits + 1 if player_hit != "FF" else 0
        if self.hits == self.threshold:
            self.numAchieved+=1
            self.hits = 0
class HealthRunner(Medal):
    def __init__(self) -> None:
        super().__init__("healthrunner", 5)

class Juggernaut(Medal):
    def __init__(self) -> None:
        super().__init__("juggernaut", 1)
        self.madeJug = False
    def track(self, hasJug):
        if not self.madeJug:
            if hasJug:
                self.numAchieved+=1
                self.madeJug = True

class Olympiad(Medal):
    def __init__(self) -> None:
        super().__init__("olympiad", 5)
        self.eligible = True
    def track(self, distance):
        if self.eligible and int(distance) == self.threshold:
            self.eligible = False
            self.numAchieved+=1
    def reset(self):
        self.eligible = True

class Dropper(Medal):
    def __init__(self) -> None:
        super().__init__("dropper", 1)
        self.dropTime = None
    def setDropTime(self):
        self.dropTime = datetime.datetime.now()
    def reset(self):
        self.dropTime = None
    def track(self):
        if self.dropTime != None:
            currentTime = datetime.datetime.now()
            timeDiff = currentTime - self.dropTime
            if timeDiff.seconds <= 10:
                self.numAchieved+=1
            else:
                self.dropTime = None
class Untouchable(Medal):
    def __init__(self) -> None:
        super().__init__("untouchable", 1)
        self.damageTaken = 0
        self.hasFlag = False
        self.distance = 0
    def pickupFlag(self):
        self.hasFlag = True
        self.damageTaken = 0
        self.distance = 0
    def damage(self, dmg):
        self.damage+=dmg
    def move(self, dist):
        if self.hasFlag:
            self.distance+=dist
    def dropFlag(self):
        self.hasFlag = False
        self.distance = 0
    def track(self):
        if self.damageTaken == 0 and self.distance > 0.25:
            self.numAchieved+=1

class MachineGun(Medal):
    def __init__(self, name="machinegun", threshold=4) -> None:
        super().__init__(name, threshold)
        self.startTime = datetime.datetime.now()
        self.streak = 0
    def track(self):
        currentTime = datetime.datetime.now()
        timeDiff = currentTime - self.startTime
        if timeDiff.seconds <= 15:
            self.streak+=1
        else:
            self.dropTime = datetime.datetime.now()
            self.streak = 1

        if self.streak == self.threshold:
            self.numAchieved+=1


class RatFuck(Medal):
    def __init__(self, name='ratfuck', threshold=5) -> None:
        super().__init__(name, threshold)


class MedalTracker():
    def __init__(self, player):
        self.player = player
        self.onCapStreak = False
        self.hpStreak = 0
        self.distance = 0
        self.packsConsumed = 0

        self.nuke = Nuke()
        self.brutal = Brutal()
        self.relentless = Relentless()
        self.undying = Undying()
        self.merciless = Merciless()
        self.bloodthirsty = Bloodthirsty()

        self.distributor = Distributor()
        self.brutalized = Brutalized()
        self.thickskull = Thickskull()
        self.bloodfilled = Bloodfilled()

        self.radioactive = Radioactive()

        self.shifty=Shifty()
        self.healthrunner = HealthRunner()
        self.lockon = LockOn()
        self.heatingup = HeatingUp()
        self.juggernaut = Juggernaut()
        self.olympiad = Olympiad()
        self.dropper = Dropper()
        self.ratfuck = RatFuck()
        self.untouchable = Untouchable()
        self.machinegun = MachineGun()



    def kill(self, weapon = "Wrench"):
        streak = self.player.getKillstreak()
        self.nuke.track(streak)
        self.brutal.track(streak)
        self.relentless.track(streak)
        self.undying.track(streak)
        self.merciless.track(streak)
        self.bloodthirsty.track(streak)
        self.radioactive.track(streak)

        self.juggernaut.track(self.player.hasJug())
        self.dropper.track()
        self.machinegun.track()

    def death(self):
        streak = self.player.getDeathstreak()
        self.distributor.track(streak)
        self.brutalized.track(streak)
        self.thickskull.track(streak)
        self.bloodfilled.track(streak)


        self.onCapStreak = False
        self.hpStreak = 0
        self.juggernaut.madeJug = False
        self.distance=0
        self.dropper.reset()
        self.olympiad.reset()
        self.packsConsumed=0
    def cap(self):
        self.shifty.track(self.onCapStreak)
        self.onCapStreak = True
        self.untouchable.track()

    def fire(self, weapon, player_hit):
        if weapon == "Flux":
            self.lockon.track(player_hit)

    def heal(self):
        self.hpStreak+=1
        self.healthrunner.track(self.hpStreak)

    def move(self, distance):
        self.distance+=distance
        self.olympiad.track(self.distance)
        self.untouchable.move(distance)

    def dropFlag(self):
        self.dropper.setDropTime()
        self.untouchable.dropFlag()

    def pickupFlag(self):
        self.untouchable.pickupFlag()

    def damage(self, dmg):
        self.untouchable.damage(dmg)

    def pack(self, pack):
        if pack.containsV2:
            self.packsConsumed+=1
            self.ratfuck.track(self.packsConsumed)

    def getState(self):
        return {
            self.nuke.name:self.nuke.numAchieved,
            self.brutal.name:self.brutal.numAchieved,
            self.relentless.name:self.relentless.numAchieved,
            self.undying.name:self.undying.numAchieved,
            self.merciless.name:self.merciless.numAchieved,
            self.bloodthirsty.name:self.bloodthirsty.numAchieved,
            self.radioactive.name:self.radioactive.numAchieved,
            self.distributor.name:self.distributor.numAchieved,
            self.brutalized.name:self.brutalized.numAchieved,
            self.thickskull.name:self.thickskull.numAchieved,
            self.shifty.name:self.shifty.numAchieved,
            self.juggernaut.name:self.juggernaut.numAchieved,
            self.olympiad.name:self.olympiad.numAchieved,
            self.dropper.name:self.dropper.numAchieved,
            self.ratfuck.name:self.ratfuck.numAchieved,
            self.lockon.name:self.lockon.numAchieved,
            self.healthrunner.name:self.healthrunner.numAchieved,
            self.heatingup.name:self.heatingup.numAchieved,
            self.machinegun.name:self.machinegun.numAchieved,
        }
    

