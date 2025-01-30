n, k = map(int, input().split())
array = list(map(int, input().split()))


couples_sum = []
for i in range(n):
    for j in range(i + 1, n):
        couples_sum.append(array[i] + array[j])

mod = 998244353
for key in range(1, k + 1):
    res = 0
    for sum_val in couples_sum:
        res += pow(sum_val, key, mod)
        res %= mod
    print(res)
