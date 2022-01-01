from Parsers.symbols import CLANTAG_ALLOWED_CHARACTERS
# from symbols import CLANTAG_ALLOWED_CHARACTERS #DEBUG

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
    for i, char in enumerate(tag):
        if len(char) > 1:
            continue
        else:
            if char.isalpha():
                if char.islower():
                    tag[i] = char.upper()
                else:
                    tag[i] = char.lower()
    return tag


# stats = '46464646464646464646464646464646354130433435304200FFFFFFFFFFFFFF00003D0000000000AC696800000000000040B9010000000001000000000000000040B90100000000C8A1670000000000D05F6D00000000006CA1670000000000505E1A00000000000100000000000000A0AB6D000000000010AB6D00000000003100000000000000BC57680000000000000000000038454636454545394145383332314241000000000000000B450C5A00C0C50100000000B047680000000000C87CD501000000000000000000000000C049680000000000000000000000000000C0C50100000000D05E1A000000000000C0C50100000000D05E1A0000000000'
# print(getClanTag(stats))
