n, m = map(int, input().split())
length = list(map(int, input().split()))

min_l = length[0]
max_l = length[1]
length.pop(0)
length.pop(0)
n -= 2
good = 0
changes = 0

i = 0
while i < n:
    if min_l <= length[i] <= max_l:
        good += 1
        length.pop(i)
        n -= 1
    else:
        i += 1


def find_min_dif(array, min_l, max_l):
    min_dif = 10000000
    index = 0
    for i in range(0, n):
        if min_dif > (min_l - array[i]) > 0:
            min_dif = min_l - array[i]
            index = i
        if min_dif > (array[i] - max_l) > 0:
            min_dif = array[i] - max_l
            index = i
    return min_dif, index


while good < m:
    minimal_diff, index_min = find_min_dif(length, min_l, max_l)
    changes += minimal_diff
    length.pop(index_min)
    n -= 1
    good += 1

print(changes)
