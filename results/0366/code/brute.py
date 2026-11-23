# Independent brute force: enumerate 3-full u <= N by DFS over prime powers (no B^4C^5t^3
# parametrisation), test u+d 2-full with sympy.factorint. Prints "HIT d u".
import sys
from sympy import primerange, factorint
N = int(float(sys.argv[1])); D = [int(x) for x in sys.argv[2:]]
ps = list(primerange(2, int(round(N ** (1/3))) + 2))
out = []
def dfs(i, v):
    out.append(v)
    for j in range(i, len(ps)):
        p = ps[j]
        if v * p**3 > N: break
        w = v * p**3
        while w <= N:
            dfs(j + 1, w); w *= p
dfs(0, 1)
us = sorted(x for x in out if x > 1)
print("# count", len(us))
for u in us:
    for d in D:
        m = u + d
        if m <= 0: continue
        if all(e >= 2 for e in factorint(m).values()):
            print("HIT", d, u)
