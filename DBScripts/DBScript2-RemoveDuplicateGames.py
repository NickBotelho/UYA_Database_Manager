from mongodb import Database

def checkForDupes():
    games = Database("UYA", "Game_History")
    ids = set()
    numDupes = 0
    for game in games.collection.find().sort([("entry_number",1)]):
        if game["game_id"] not in ids:
            ids.add(game['game_id'])

        else:
            print(f"Duplicate found at {game['game_id']} entry # {game['entry_number']}")
            numDupes+=1
    print(f"{numDupes} Dupes")
def run():
    games = Database("UYA", "Game_History")
    ids = set()
    for game in games.collection.find().sort([("entry_number",1)]):
        if game["game_id"] not in ids:
            ids.add(game['game_id'])
            games.collection.find_one_and_update(
                {
                    "game_id":game['game_id']
                },
                {
                    "$set":{
                        "entry_number":len(ids)
                    }
                }
            )
        else:
            print(f"deleting game {game['_id']}")
            games.collection.find_one_and_delete({"_id":game['_id']})
def confirmSuccess():
    games = Database("UYA", "Game_History_Backup")
    ids = set()
    for game in games.collection.find().sort([("entry_number",1)]):
        print(game['entry_number'])

# checkForDupes()
# run()
# checkForDupes()
