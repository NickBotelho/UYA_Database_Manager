from Webhooks.BaseWebhook import BaseWebook, Field

class PlayerLoginWebhook(BaseWebook):
    def __init__(self, username, clan, numPlayers, color=None):
        title = "Player Login"
        name = Field("Username", username)
        clanInfo = Field("Clan", clan)
        players = Field("Players Online", numPlayers)
        super().__init__(title,"", [name, clanInfo, players], color)