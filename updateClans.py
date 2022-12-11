
from mongodb import Database
import json
import requests


clans = Database("UYA","Clans")
players = Database("UYA","Player_Stats")

CLANS_API = 'http://103.214.110.220:8281/robo/clans/id/{}' #/id

def updateAllClans():
    for clan in clans.collection.find():
        idx = clan['clan_id']
        try:
            res = requests.get(CLANS_API.format(idx)).json()
            if len(res) == 0:
                print("{} Deleted".format(clan['clan_name']))
                clans.collection.find_one_and_delete({'clan_id':idx})
            else:
                member_names = res['members']
                member_ids = []
                for name in member_names:
                    p_id = players.collection.find_one({'username_lowercase':name.lower()})['account_id']
                    member_ids.append(p_id)
                clans.collection.find_one_and_update({
                    'clan_id' : idx
                },
                {
                    '$set':{
                        'member_names':member_names,
                        'member_ids':member_ids
                    }
                })
        except:
            print("Problem fetching clan")


# updateAllClans()


    