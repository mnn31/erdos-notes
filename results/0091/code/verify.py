"""Exact verification of the finite facts used in WRITEUP.md (Erdos #91, n = 10..15).
Triangular-lattice sets: point (a,b) <-> a + b*w, w = e^{i pi/3}; |(a,b)|^2 = a^2+ab+b^2 (exact ints).
Regular-polygon facts are proved by hand in the write-up; here they are only cross-checked with
50-digit mpmath arithmetic (NOT load-bearing)."""
import itertools
from collections import Counter

def N(a, b): return a*a + a*b + b*b
def sqd(p, q): return N(p[0]-q[0], p[1]-q[1])
def dists(P): return sorted({sqd(p, q) for p, q in itertools.combinations(P, 2)})
def mingraph_degrees(P):
    m = min(sqd(p, q) for p, q in itertools.combinations(P, 2))
    deg = Counter()
    for p, q in itertools.combinations(P, 2):
        if sqd(p, q) == m: deg[p] += 1; deg[q] += 1
    return m, sorted(deg[p] for p in P)

# L12: the 12-point 5-distance lattice set (found by code/lattice_search.py, re-checked here exactly)
L12 = [(-1,-2),(-1,-1),(-1,0),(0,-3),(0,-2),(0,-1),(0,0),(1,-3),(1,-2),(1,-1),(2,-3),(2,-2)]
# S16: lattice hexagon of side 2 (|a|,|b|,|a+b| <= 2) minus the three alternate corners (2,0),(-2,2),(0,-2)
H2 = [(a,b) for a in range(-2,3) for b in range(-2,3) if abs(a+b) <= 2]
S16 = [p for p in H2 if p not in [(2,0),(-2,2),(0,-2)]]

print("L12: |L12| =", len(L12), " squared distances", dists(L12), " (count", len(dists(L12)), ")")
print("     min-distance graph: min sq dist, degree sequence =", mingraph_degrees(L12))
for p in L12:
    Q = [q for q in L12 if q != p]
    print("  L12 -", p, ": |.|=", len(Q), " #dist =", len(dists(Q)), " degrees =", mingraph_degrees(Q)[1])
print("H2 (side-2 hexagon): |H2| =", len(H2), " #dist =", len(dists(H2)))
print("S16: |S16| =", len(S16), " squared distances", dists(S16), " (count", len(dists(S16)), ")")
for p in [(-2,0),(0,0)]:
    Q = [q for q in S16 if q != p]
    print("  S16 -", p, ": |.|=", len(Q), " #dist =", len(dists(Q)), " degrees =", mingraph_degrees(Q)[1])

# ---- cross-check (not load-bearing) of regular-polygon facts in 50-digit arithmetic
import mpmath as mp
mp.mp.dps = 50
def reg(n, drop=False, centre=False):
    P = [mp.expjpi(2*mp.mpf(k)/n) for k in range(n)]
    if drop: P = P[1:]
    if centre: P.append(mp.mpc(0))
    return P
def info(P, tol=mp.mpf(10)**-30):
    ds = sorted(abs(a-b) for a, b in itertools.combinations(P, 2))
    cl = []
    for d in ds:
        if not cl or d - cl[-1] > tol: cl.append(d)
    m = cl[0]; deg = Counter()
    for i, j in itertools.combinations(range(len(P)), 2):
        if abs(abs(P[i]-P[j]) - m) < tol: deg[i] += 1; deg[j] += 1
    return len(cl), sorted(deg[i] for i in range(len(P))), min(b-a for a, b in zip(cl, cl[1:]))
for name, P in [("R10", reg(10)), ("R11-1", reg(11, drop=True)), ("R11", reg(11)),
                ("R13", reg(13)), ("R12+", reg(12, centre=True)), ("R14", reg(14)),
                ("R15-1", reg(15, drop=True)), ("R15", reg(15)), ("R13+", reg(13, centre=True))]:
    k, degs, gap = info(P)
    print(f"{name:6s} |P|={len(P):2d} #dist={k}  min-graph degrees={degs}  smallest gap between distinct distances={mp.nstr(gap,5)}")
