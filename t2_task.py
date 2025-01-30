def max_stepen(num):
    test = 1
    count = 0
    while num > test*2:
        test *= 2
        count += 1
    return count


n = int(input())
for k in range(n):
    max_cost = 0
    i = int(input())
    if i - 2**max_stepen(i) >= 3:
        max_cost += 2**max_stepen(i)
        i -= 2**max_stepen(i)
        max_cost += 2**max_stepen(i)
        i -= 2**max_stepen(i)
        max_cost += 2**max_stepen(i)
        print(max_cost)
    elif i >= 7:
        print(2**(max_stepen(i)-1) + 2**(max_stepen(i)-2) + 2**(max_stepen(i)-3))
    else:
        print(-1)
