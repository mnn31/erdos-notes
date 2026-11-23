# Check: for every consecutive powerful pair (m, m+1) listed in the OEIS A060355 b-file
# (stated there as all terms < 10^22), is (m-1)m(m+1) or m(m+1)(m+2) powerful?
# Reduction (proved in PLAN.md): if n(n+1)(n+2) is powerful then (n,n+1) or (n+1,n+2)
# is a consecutive powerful pair, so this covers every n with n+1 < 10^22.
import sys
from sympy import factorint
def powerful(x):
    return all(e >= 2 for e in factorint(x).values())
pairs = []
for line in open(sys.argv[1]):
    line=line.strip()
    if not line or line.startswith('#'): continue
    i, m = line.split(); m=int(m)
    assert powerful(m) and powerful(m+1), m
    pairs.append(m)
hits = []
for m in pairs:
    for n in (m-1, m):
        if n >= 1 and powerful(n*(n+1)*(n+2)):
            hits.append(n)
print("pairs checked:", len(pairs), "max m:", max(pairs))
print("k=3 hits:", hits)
