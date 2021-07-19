def hash_id(packet):
    '''In theory 2 games could be made at the same time, so combining the creation date
    and the dme world id will give a unique game id impossible to be duplicated'''
    id = str(round(packet['created_date'], 2))
    dme_id = str(packet["dme_world_id"])
    return float(id + dme_id)
