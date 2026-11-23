# Independent brute-force check of Lemmas 3,4 / Theorem A.
# Builds realizations of the ES family E(i,j) (i=a-2, j=b-2) with INTEGER coordinates
# satisfying (P1) all x of R exceed all x of L and (P2) every L-R slope exceeds every
# internal slope, with randomized translation parameters; then counts nonempty cups,
# caps and convex-position subsets by exhaustive DFS (convex position is hereditary),
# using exact integer orientation tests only.
import sys, random, itertools
from fractions import Fraction as F

def slope(p, q):
    return F(q[1]-p[1], q[0]-p[0])

def build(i, j, rng):
    if i == 0 or j == 0:
        return [(0, 0)]
    L = build(i-1, j, rng); R = build(i, j-1, rng)
    internal = [slope(p, q) for S in (L, R) for p, q in itertools.combinations(S, 2)]
    M = max([F(0)] + internal)
    X = max(p[0] for p in L) - min(p[0] for p in R) + rng.randint(1, 5)
    Rx = [(x+X, y) for x, y in R]
    dx = max(r[0]-l[0] for l in L for r in Rx)
    dy = max(abs(r[1]-l[1]) for l in L for r in Rx)
    Y = int(M*dx) + 1 + dy + rng.randint(0, 7)
    Rt = [(x, y+Y) for x, y in Rx]
    P = L + Rt
    # verify P1, P2 exactly
    assert max(p[0] for p in L) < min(p[0] for p in Rt)
    Mi = max([F(-10**30)] + [slope(p, q) for S in (L, Rt) for p, q in itertools.combinations(S, 2)])
    assert min(slope(l, r) for l in L for r in Rt) > Mi
    return P

def orient(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def in_convex_position(S):
    # S sorted by x. Andrew monotone chain; general position assumed (checked separately).
    if len(S) <= 2: return True
    lower = []
    for p in S:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(S):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return len(lower) + len(upper) - 2 == len(S)

def is_cup(S):  # S sorted by x; strictly increasing slopes <=> each consecutive triple turns left
    return all(orient(S[k-1], S[k], S[k+1]) > 0 for k in range(1, len(S)-1))
def is_cap(S):
    return all(orient(S[k-1], S[k], S[k+1]) < 0 for k in range(1, len(S)-1))

def count_hereditary(P, pred):
    n = len(P); cnt = 0
    stack = [((), -1)]
    while stack:
        S, last = stack.pop()
        for k in range(last+1, n):
            T = S + (P[k],)
            if pred(T):
                cnt += 1
                stack.append((T, k))
    return cnt

def rec(i, j, memo={}):
    if (i, j) in memo: return memo[i, j]
    if i == 0 or j == 0: r = (1, 1, 1, 1)
    else:
        sL, uL, vL, cL = rec(i-1, j); sR, uR, vR, cR = rec(i, j-1)
        r = (sL+sR, uL*(1+sR)+uR, vR*(1+sL)+vL, cL+cR+uL*vR)
    memo[i, j] = r
    return r

if __name__ == '__main__':
    cases = [(1,1),(1,2),(2,1),(2,2),(1,5),(5,1),(2,3),(3,2),(3,3),(2,4),(4,2),(3,4),(4,3),(2,6),(6,2),(1,8),(8,1)]
    for seed in (1, 2):
        rng = random.Random(seed)
        for (i, j) in cases:
            P = sorted(build(i, j, rng))
            assert len(set(p[0] for p in P)) == len(P)
            assert all(orient(*t) != 0 for t in itertools.combinations(P, 3)), 'collinear'
            s, u, v, c = rec(i, j)
            bu = count_hereditary(P, is_cup)
            bv = count_hereditary(P, is_cap)
            bc = count_hereditary(P, in_convex_position)
            ok = (len(P), bu, bv, bc) == (s, u, v, c)
            print(f"seed={seed} (i,j)=({i},{j}) (a,b)=({i+2},{j+2}) n={len(P)} "
                  f"cups={bu}/{u} caps={bv}/{v} convex={bc}/{c} {'OK' if ok else 'MISMATCH'}", flush=True)
            assert ok
    print("ALL OK")
