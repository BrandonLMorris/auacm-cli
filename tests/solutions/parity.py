"""Python 3 solution to 'Parity'"""

while True:
    s = raw_input()

    if s == '#': break

    ones = sum(1 for i in s if i == '1')

    result = s[:-1]
    if s[-1] == 'e':
        if ones % 2 == 1: result += '1'
        else: result += '0'
    else:
        if ones % 2 == 1: result += '0'
        else: result += '1'

    print(result)

