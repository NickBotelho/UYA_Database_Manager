X12_UNIT = 35162
class Pedometer():
    '''Tracks travelling metrics for a DMEPlayer in live game'''
    def __init__(self):
        self.totalDistance = 0
        self.flagDistance = 0
        self.noFlagDistance = 0
    def walk(self, oldPoint, newPoint, hasFlag):
        if oldPoint != -1:
            distance = abs(oldPoint - newPoint)
            self.totalDistance = self.totalDistance + distance
            if hasFlag:
                self.flagDistance+= distance
            else:
                self.noFlagDistance+=distance
    def getTotalDistance(self):
        return round(self.totalDistance/X12_UNIT, 2)
    def getFlagDistance(self):
        return round(self.flagDistance/X12_UNIT, 2)
    def getNoFlagDistance(self):
        return round(self.noFlagDistance/X12_UNIT, 2)


        