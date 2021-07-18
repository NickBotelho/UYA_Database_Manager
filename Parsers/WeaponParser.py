weapons = {
    0:"Lava Gun",
    1:"Morph O' Ray",
    2:"Mines",
    3:"Gravity Bomb",
    4:"Rockets",
    5:"Blitz",
    6:"N60",
    7:"Flux"
}

def weaponParser(num):
    '''Accepts PLAYER_SKILL_LEVEL named field INTEGER number (which is 2 a byte long hex string)'''
    # print("player skill number {} ".format(num))
    num = int(num) if type(num) != 'int' else num
    num = format(num, "#010b")[2:]
    res = []
    for i in range(len(num)-1, -1, -1):
        if num[i] == "0":
            res.append(weapons[i])
    return res
