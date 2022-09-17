from mongodb import Database

live = Database("UYA", "LiveGame_History")

for game in live.collection.find():
    first = None
    for p in game['results'].keys():
        first = p
        break

    if 'saves' not in game['results'][p]:
        print("old game")
    else:
        print("new game")

