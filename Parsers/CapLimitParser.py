

def capLimitParser(num: int):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)

    Returns 0 if cap limit is None (Timed CTF no limit)
    '''
    num = int(num) if type(num) != 'int' else num

    binary = bin(num)[2:]
    length = len(binary)
    leftover = 32 - length
    binary_full = leftover*'0' + binary
    
    return int(binary_full[5:9],2)
    
