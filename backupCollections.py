
from mongodb import Database
import json
import os
from time import gmtime, strftime
player_stats = Database("UYA","Player_Stats")
players_online = Database("UYA","Players_Online")
game_history = Database("UYA", "Game_History")
games_active = Database("UYA","Games_Active")
players_stats_backup = Database("UYA","Player_Stats_Backup")
game_history_backup = Database("UYA", "Game_History_Backup")


date = strftime("%b-%d-%Y_", gmtime())

if not os.path.exists('backups/'):
    os.mkdir('backups/')


'''Saves passed collection to a json file in the backups dir'''
def backupToJSON(filename, mongo):
    '''Filename - name of output file
    mongo = mongodb object of collection to backup'''
    entries =[]
    filename = date+filename
    for entry in mongo.collection.find():
        e = dict(entry)
        del e['_id']
        e = json.dumps(e)
        entries.append(e)

    with open('backups/'+filename ,'w') as file:
        for e in entries:
            file.write(e+"\n")

def backupToCollection (main, backup):
    '''main = mongo object backing up
    backup = collection to backup to '''
    for doc in backup.collection.find():
        backup.collection.delete_one(doc)

    for doc in main.collection.find():
        backup.collection.insert_one(doc)



backupToJSON("player_stats_back.json", player_stats)
backupToJSON("game_history_backup.json", game_history)
#BACKUP
backupToCollection(player_stats, players_stats_backup)
backupToCollection(game_history, game_history_backup)

#RESTORE
# backupToCollection(players_stats_backup, player_stats )
# backupToCollection(game_history_backup, game_history )