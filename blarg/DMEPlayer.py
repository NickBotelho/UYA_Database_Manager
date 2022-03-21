class Player():
    def __init__(self, username, lobby_idx, team):
        self.username = username
        self.lobby_idx = lobby_idx
        self.team = team
        self.kills = 0
        self.hp = 0
        self.deaths = 0
        self.caps = 0
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
    def respawn(self):
        self.hp = 100
    def heal(self):
        self.hp = 100
    def getState(self):
        state = {
            'name':self.username,
            'hp':self.hp,
            'kills':self.kills,
            'deaths':self.deaths,
            'caps':self.caps,
            'team':self.team
        }
        return state
        

