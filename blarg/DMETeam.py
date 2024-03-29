

class Team():
    def __init__(self, color, players):
        '''str: color = team color
        dict: players = lobby idx --> player obj'''
        self.color = color
        self.players = [player for player in players.values() if player.teamColor == color]
        self.opponentTeams = []

        for player in self.players:
            player.setTeam(self)
    def dropFlags(self):
        pass
        # for player in self.players:
        #     player.hasFlag = False
    def addOpponentTeam(self, enemy):
        self.opponentTeams.append(enemy)
    def saveFlags(self):
        pass
        # for team in self.opponentTeams:
        #     team.dropFlags()
    def getPlayerNames(self):
        return [player.username for player in self.players]

