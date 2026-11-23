# Lemma G check: t(v) = 4v^2(v^2-1).  Symbolic identities for t+a, a in {1,2,4,5}, and a numeric check
# that t(v) is a 7-shift for v = 21k, 1 <= k <= 300 (and records where it fails at a = 8).
# run: python3 -I code/family7.py
import sympy as sp
from sympy import factorint
v = sp.symbols('v'); t = 4*v**2*(v**2-1)
ids = {1: ((2*v**2-1), 0), 2: ((2*v**2-1), 1), 4: ((2-2*v**2), 2*v), 5: ((2*v**2-1), 2)}
for a, (X, Y) in ids.items():
    assert sp.expand(t + a - X**2 - Y**2) == 0, a
print("identities t+a = X^2+Y^2 verified for a = 1,2,4,5")
def inE(m): return m >= 1 and all(e % 2 == 0 for p, e in factorint(m).items() if p % 4 == 3)
def L(T, cap=40):
    for a in range(1, cap+1):
        if inE(a) != inE(a+T): return a-1
    return cap
Ls = []
for k in range(1, 301):
    T = int(t.subs(v, 21*k)); l = L(T); assert l >= 7, (k, l); Ls.append(l)
from collections import Counter
print("v=21k, k<=300: all are 7-shifts; distribution of L(t):", sorted(Counter(Ls).items()))
