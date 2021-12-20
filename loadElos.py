
def loadElos(dir):
    elo = {}
    with open(dir, 'r') as file:
        for line in file:
            line = line.split(',')
            name = ''
            for i in range(len(line)-1):
                if i > 0:
                    name = name + ','+line[i]
                else:
                    name+=line[i]
                
            curr_elo = int(line[-1][:len(line[-1])-1])

            elo[name] = curr_elo
    return elo
