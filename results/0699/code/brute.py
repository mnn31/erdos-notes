# Independent brute force: exact gcd of binomials, strip primes <= i.
import sys
from math import comb, gcd
def nm(n, i):
    a = comb(n, i); out = []
    for j in range(i + 1, n // 2 + 1):
        g = gcd(a, comb(n, j))
        for p in range(2, i + 1):
            while g % p == 0: g //= p
        if g == 1: out.append(j)
    return out
for k in range(2, 14): print('2^%d' % k, nm(2**k, 2))
for m in range(1, 8): print('3^%d+1' % m, nm(3**m + 1, 3))
