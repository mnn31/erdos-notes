# For each A060355 b-file term n (n, n+1 both powerful, terms < 1e22), report which of n, n+1 is 3-full.
import sys
from sympy import factorint
def kfull(m, k): return all(e >= k for e in factorint(m).values())
for line in open(sys.argv[1]):
    s = line.split()
    if len(s) != 2: continue
    n = int(s[1])
    a, b = kfull(n, 3), kfull(n + 1, 3)
    assert kfull(n, 2) and kfull(n + 1, 2)
    if a or b: print("bfile index", s[0], "n =", n, "n 3-full:", a, "n+1 3-full:", b)
