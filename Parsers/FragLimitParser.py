

def fragLimitParser(num: int):
    '''Accepts generic_field_3 INTEGER number (which is 4 a byte long hex string)

    Returns 0 if no frag is set (time limit DM)
    '''
    num = int(num) if type(num) != 'int' else num

    binary = bin(num)[2:]
    length = len(binary)
    leftover = 32 - length
    binary_full = leftover*'0' + binary
    
    return int(binary_full[10:13],2)*5
    
