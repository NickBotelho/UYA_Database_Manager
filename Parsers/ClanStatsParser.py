from symbols import CLANTAG_ALLOWED_CHARACTERS
tag_indices = [32, 36, 40, 44]

def getClanTag(packet):
    '''packet is the clans stat packet
    (not clanstatswide)
    
    returns list of the 4 characters in the clan tag'''
    tag = []
    for char in tag_indices:
        tag.append(packet[char:char+4])
    tag.reverse()
    tag=[CLANTAG_ALLOWED_CHARACTERS[char] for char in tag]
    return tag


# stats = '303030303030313130303030303030313237324432443044000000000000000050F9FF010000000050F9FF01000000006C69B901000000000100000000000000020000000000000000003700000000000442B90100000000020000000000000090976D000000000064976D0000000000434330303030303030412D30303030303031310000313237464143423130354130324145330000000100000001000000433030303030303061596F757220636C006E20686173206265656E206368616C6C656E67656420627920536D6F6B65728A000000020000000A00000011000000000000002000000000F9FF010000000011000000000000000100000000000000'
