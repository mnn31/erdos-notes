# verify_py.py -- independent Python re-implementation of the classification
# (different code path from classify.c):
#   * avoidance is tested straight from the definition (group disjoint pairs of
#     members by their union; a union reached by two different unordered pairs
#     is a forbidden configuration);
#   * the conflict relation between link pairs is computed by brute-force
#     avoidance tests of H + {w,p} + {w,q}, NOT by the 5-set rule of Lemma 3;
#   * isomorphism rejection uses a different canonical form: minimum of the
#     sorted image triple list over all permutations that respect the
#     (degree, sorted codegree-multiset) vertex invariant.
# Usage: python3 -I verify_py.py N THR
import sys, itertools
from math import comb

def avoiding(F):
    """F: iterable of 3-tuples. True iff no four distinct members A,B,C,D with
    A|B = C|D and A&B = C&D = empty."""
    F = [frozenset(t) for t in F]
    seen = {}
    for i in range(len(F)):
        for j in range(i + 1, len(F)):
            if not (F[i] & F[j]):
                U = F[i] | F[j]
                if U in seen:
                    return False
                seen[U] = (i, j)
    return True

def invariant(F, n):
    deg = [0] * n
    cod = [[0] * n for _ in range(n)]
    for t in F:
        for v in t: deg[v] += 1
        for a, b in itertools.combinations(t, 2):
            cod[a][b] += 1; cod[b][a] += 1
    return [(deg[v], tuple(sorted(cod[v][u] for u in range(n) if u != v))) for v in range(n)]

def canon(F, n):
    inv = invariant(F, n)
    keys = sorted(set(inv))
    cells = [[v for v in range(n) if inv[v] == k] for k in keys]
    best = None
    for choice in itertools.product(*[itertools.permutations(c) for c in cells]):
        order = [v for c in choice for v in c]        # order[pos] = vertex
        pos = {v: p for p, v in enumerate(order)}
        img = tuple(sorted(tuple(sorted(pos[v] for v in t)) for t in F))
        if best is None or img < best:
            best = img
    return best

def extend(H, n, need):
    """All avoiding G = H + {w}*L on [n+1] (w = n) with |L| >= need, in which w
    has minimum degree."""
    w = n
    pairs = list(itertools.combinations(range(n), 2))
    Hs = list(H)
    # single additions are always fine (checked anyway)
    ok = [p for p in pairs if avoiding(Hs + [p + (w,)])]
    conf = {p: set() for p in ok}
    for p, q in itertools.combinations(ok, 2):
        if not avoiding(Hs + [p + (w,), q + (w,)]):
            conf[p].add(q); conf[q].add(p)
    degH = [sum(1 for t in H if v in t) for v in range(n)]
    out = []
    def rec(i, L, banned):
        rem = sum(1 for q in ok[i:] if q not in banned)
        if len(L) + rem < need: return
        if i == len(ok):
            dl = [0] * n
            for p in L:
                for v in p: dl[v] += 1
            if all(degH[v] + dl[v] >= len(L) for v in range(n)):
                out.append(tuple(sorted(Hs + [p + (w,) for p in L])))
            return
        p = ok[i]
        if p not in banned:
            rec(i + 1, L + [p], banned | conf[p])
        rec(i + 1, L, banned)
    rec(0, [], frozenset())
    return out

def main():
    N, THR = int(sys.argv[1]), int(sys.argv[2])
    thr = {N: THR}
    for n in range(N - 1, 2, -1):
        thr[n] = max(0, thr[n + 1] - (3 * thr[n + 1]) // (n + 1))
    level = set()
    if thr[3] <= 0: level.add(())
    if thr[3] <= 1: level.add(((0, 1, 2),))
    for n in range(3, N):
        nxt = set(); raw = 0
        for H in level:
            for G in extend(H, n, thr[n + 1] - len(H)):
                raw += 1
                assert avoiding(G)
                nxt.add(canon(G, n + 1))
        hist = {}
        for G in nxt: hist[len(G)] = hist.get(len(G), 0) + 1
        print(f"level {n+1} (thr {thr[n+1]}): {len(nxt)} classes, raw {raw}, sizes {dict(sorted(hist.items()))}", flush=True)
        level = nxt
    for G in sorted(level):
        print(len(G), ' '.join(''.join(map(str, t)) for t in G))

main()
