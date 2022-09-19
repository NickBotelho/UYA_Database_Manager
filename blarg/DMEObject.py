import datetime

class DMEObject():
    def __init__(self, object_id, x, y) -> None:
        self.object_id = object_id
        self.x, self.y = x, y
    def pickup(self, player):
        pass
    def getCoords(self):
        return (self.x, self.y)
    
        


class Pack(DMEObject):
    def __init__(self, object_id, x, y, player) -> None:
        super().__init__(object_id, x, y)
        self.weaponToIsV2 = {}
        self.containsV2 = False
        self.creationTime = datetime.datetime.now()
        for weapon in player.weapons.values():
            self.weaponToIsV2[weapon.weapon] = weapon.isV2
            if weapon.isV2:
                self.containsV2=True
    def __str__(self) -> str:
        return f"Pack {self.object_id} | Has v2 = {self.containsV2}"
    def pickup(self, player):
        for weapon in self.weaponToIsV2:
            if self.weaponToIsV2[weapon] == True:
                player.weapons[weapon].pickupV2()

