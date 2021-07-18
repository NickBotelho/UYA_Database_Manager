


account_name = '00000000000000003400000000000000D0000070A00100700000000000000000000000000000000070020070001A0000BCFC1F00001A0000D0000070FFFFFF00'
for i in range(0, len(account_name), 2):
    char = account_name[i:i+2]
    c = chr((int(char, 16)))
    i = int(char, 16)
    print(c, i)