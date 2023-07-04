from Webhooks.BaseWebhook import BaseWebook, Field

class GameStartedWebhook(BaseWebook):
    def __init__(self, description, fields, color=None):
        title = "Game Starting"
        super().__init__(title, description, fields, color)


def BroadcastGameStart(uyatrackerId, colorToTeam, map, mode):
    fields = []
    map = map.replace("_", " ")
    desc = f"{mode} on {map}"
    for color, team in colorToTeam.items():
        fields.append(Field(f"{team.color} Team", "  ".join(team.getPlayerNames())))
    fields.append(Field("Watch live", uyaTrackerLink(uyatrackerId)))
    hook = GameStartedWebhook(desc, fields)
    hook.broadcast()


def uyaTrackerLink(id):
    return f"https://www.uyatracker.net/game?id={id}"