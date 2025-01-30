s = input()
M_was = False
for i in s:
    if i == 'M':
        M_was = True
    elif i == 'R':
        if M_was:
            print('No')
            break
        else:
            print('Yes')
            break
