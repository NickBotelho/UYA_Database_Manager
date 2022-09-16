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
    "nuke":f"{MERCILESS_KILLS} Kill streak",
    'undying': f"{UNDYING_KILLS} Kill streak",

    'distributor':f"{DISTRIBUTOR_KILLS} Death streak",
    'thickskull': f"{THICKSKULL_KILLS} Death streak",
    'bloodfilled':f"{BLOODFILLED_KILLS} Death streak",
    'brutalized':f"{BRUTALIZED_KILLS} Death streak",

    'radioactive':"A single kill after dropping a nuke on the same life",
    'shifty':"Getting back to back caps without dying"

}
class Medal():
    def __init__(self, name, threshold = None) -> None:
        self.name = name
        self.description = DESCRIPTIONS[name]
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
        super().__init__("Thickskull", 15)
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


class MedalTracker():
    def __init__(self, player):
        self.player = player
        self.onCapStreak = False
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


    def kill(self, weapon = "Wrench"):
        streak = self.player.getKillstreak()
        self.nuke.track(streak)
        self.brutal.track(streak)
        self.relentless.track(streak)
        self.undying.track(streak)
        self.merciless.track(streak)
        self.bloodthirsty.track(streak)
        self.radioactive.track(streak)

    def death(self):
        streak = self.player.getDeathstreak()
        self.distributor.track(streak)
        self.brutalized.track(streak)
        self.thickskull.track(streak)
        self.bloodfilled.track(streak)

        self.onCapStreak = False
    
    def cap(self):
        self.shifty.track(self.onCapStreak)
        self.onCapStreak = True

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
        }

