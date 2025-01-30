n, x, y, z = map(int, input().split())
array = list(map(int, input().split()))
xyz = [x, y, z]
xyz.sort()
res = 0


def find_min_dif(array, xyz):
    min_dif = 1000000000
    index_xyz = 0
    index_array = 0
    for i in range(len(array)):
        for j in range(len(xyz)):
            if 0 <= (xyz[j] - (array[i] % xyz[j])) < min_dif:
                min_dif = (xyz[j] - (array[i] % xyz[j]))
                index_xyz = j
                index_array = i
            if min_dif <= 1:
                return min_dif, index_xyz, index_array
    return min_dif, index_xyz, index_array


while xyz:
    for i in array:
        if i in xyz:
            xyz.remove(i)
    if not xyz:
        break
    min_diff, index_xyz_min, index_array_i = find_min_dif(array, xyz)
    res += min_diff

    for i in range(len(xyz) - 1, -1, -1):  # Обратный цикл
        if (array[index_array_i] + min_diff) % xyz[i] == 0:
            xyz.pop(i)

print(res)