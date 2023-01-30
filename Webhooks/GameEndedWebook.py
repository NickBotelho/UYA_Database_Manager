from BaseWebhook import BaseWebook, Field
global BASES
BASES = False
class GameEndedWebhook(BaseWebook):
    def __init__(self, description, fields, color=None):
        title = "Game Results"
        super().__init__(title, description, fields, color)

def BroadcastGame(game):
    global BASES
    try:
        game.map = game.map.replace("_", " ")
        description = f"{game.game_mode} on {game.map}\n"
        fields = []
        for result, team in game.game_results.items():
            if type(team) != int:
                fields.append(getField(result, team, game.game_mode))
        fields.append(Field("View on UYATracker", uyaTrackerLink(game.id)))
        description+= getHeader(game.game_mode, BASES)
        hook = GameEndedWebhook(description=description, fields=fields)
        hook.broadcast()
    except:
        print("Error broadcasting game to GameEndedWebhook")
    
def getField(key, team, mode):
    global BASES
    value = ""
    for player in team:
        if BASES == False:
            BASES = True if "base_dmg" in player else False
        value+= getStatLine(mode, player)
    return Field(key, value)

def getStatLine(mode, player):
    if mode == "CTF":
        if "base_dmg" in player:
            return f"{player['username']}: {player['kills']} / {player['deaths']} / {player['caps']} / {player['saves']} / {player['base_dmg']}\n"
        return f"{player['username']}: {player['kills']} / {player['deaths']} / {player['caps']} / {player['saves']}\n"
    elif mode == "Siege":
        return f"{player['username']}: {player['kills']} / {player['deaths']} / {player['base_dmg']} / {player['nodes']}\n"
    else:
        return f"{player['username']}: {player['kills']} / {player['deaths']}\n"
def getHeader(mode, bd = False):
    if mode == "CTF":
        if bd:
            return f"K / D / C / S / BD\n"
        return f"K / D / C / S\n"
    elif mode == "Siege":
        return f"K / D/ BD / N\n"
    else:
        return f"K / D\n"

def uyaTrackerLink(id):
    return f"https://www.uyatracker.net/detailedgame?id={id}"