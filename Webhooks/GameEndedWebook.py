from Webhooks.BaseWebhook import BaseWebook, Field
class GameEndedWebhook(BaseWebook):
    def __init__(self, description, fields, color=None):
        title = "Game Results"
        super().__init__(title, description, fields, color)

def BroadcastGame(game):
    try:
        description = f"{game.game_mode} on {game.map}"
        fields = []
        for result, team in game.game_results.items():
            if type(team) != int:
                fields.append(getField(result, team))
        fields.append(Field("View on UYATracker", uyaTrackerLink(game.id)))
        hook = GameEndedWebhook(description=description, fields=fields)
        hook.send()
    except:
        print("Error broadcasting game to GameEndedWebhook")
    
def getField(key, team):
    value = ""
    for player in team:
        value+= f"{player['username']}: {player['kills']} / {player['deaths']}\n"
    return Field(key, value)

def uyaTrackerLink(id):
    return f"https://www.uyatracker.net/detailedgame?id={id}"
