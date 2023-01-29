from Webhooks.BaseWebhook import BaseWebook, Field

class PlayerLoginWebhook(BaseWebook):
    def __init__(self, username, clan, color=None):
        title = "Player Login"
        name = Field("Username", username)
        clanInfo = Field("Clan", clan)
        super().__init__(title,"", [name, clanInfo], color)