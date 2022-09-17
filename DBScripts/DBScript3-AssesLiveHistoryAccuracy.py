from mongodb import Database

games = Database("UYA", "Game_History")
live = Database("UYA", "LiveGame_History")

total, good = 0, 0
for game in games.collection.find().sort("entry_number", -1).limit(20):
    id = game['game_id']
    liveG = live.collection.find_one({"game_id":id})
    if liveG != None:
        good+=1
    else:
        print(id)
    total+=1

print(f"{good}/{total}")
