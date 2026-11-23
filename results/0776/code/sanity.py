#!/usr/bin/env python3
"""Sanity tests (exact integers).

(1) kk(k,m) equals the brute-force minimum (k-1)-shadow over ALL families of m k-subsets of [p]
    for (p,k) in {(5,2),(5,3),(6,2),(6,3),(6,4),(7,3)} (all m <= C(p,k)); for (7,3) m <= 5 only.
(2) kk(k,m) equals the actual shadow size of the first m k-sets in colex order, k <= 9, m < 600.
(3) Python kk agrees with the C implementation (code/check k) on a grid (k <= 40, 1 <= m <= C(85,k)).
(4) Pipeline test vs. brute force: for n = 6 and every r in 2..20, "some 3-set M of missing levels
    passes the recurrence" agrees with a brute-force determination of g(6,r) >= 2
    (exists antichain with >= r sets on each of two levels in {1..5}).
"""
import sys, os, itertools, subprocess, random
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from search import kk, recurrence, colex_unrank

HERE = os.path.dirname(os.path.abspath(__file__))


def shadow(fam):
    sh = set()
    for S in fam:
        for x in S:
            sh.add(S - {x})
    return sh


def test1():
    ok = True
    for (p, k) in [(5, 2), (5, 3), (6, 2), (6, 3), (6, 4), (7, 3)]:
        sets = [frozenset(c) for c in itertools.combinations(range(p), k)]
        mmax = len(sets) if (p, k) != (7, 3) else 5
        for m in range(1, mmax + 1):
            best = min(len(shadow(f)) for f in itertools.combinations(sets, m))
            if best != kk(k, m):
                ok = False
                print("  (1) mismatch", p, k, m, best, kk(k, m))
    print("(1) brute-force min shadow == kk:", ok)
    return ok


def test2():
    ok = True
    for k in range(1, 10):
        fam = []
        for m in range(1, 600):
            fam.append(frozenset(colex_unrank(m - 1, k)))
            if len(shadow(fam)) != kk(k, m):
                ok = False
                print("  (2) mismatch", k, m)
                break
    print("(2) colex initial-segment shadow == kk:", ok)
    return ok


def test3():
    ok = True
    rng = random.Random(1)
    pts = [(k, m) for k in range(1, 41) for m in list(range(1, 60)) + [rng.randrange(1, comb(85, k) + 1) for _ in range(20)] if m <= comb(85, k)]
    for k, m in pts:
        out = subprocess.run([os.path.join(HERE, "check"), "k", str(k), str(m)], capture_output=True, text=True).stdout.strip()
        if int(out) != kk(k, m):
            ok = False
            print("  (3) mismatch", k, m, out, kk(k, m))
    print(f"(3) Python kk == C kk on {len(pts)} points:", ok)
    return ok


def recurrence_feasible(n, r, nlev):
    """some set of exactly nlev levels in 1..n-1 passes the recurrence"""
    for L in itertools.combinations(range(1, n), nlev):
        if recurrence(n, set(L), r)[0]:
            return True
    return False


def brute_feasible_2lev(n, r):
    """exact: exists antichain on [n] with >= r (wlog exactly r) sets on each of two levels
    i < j in 1..n-1.  Enumerates every r-family B on level j; the i-sets usable are exactly the
    i-sets not contained in any member of B (an i-set cannot contain a j-set)."""
    for i, j in itertools.combinations(range(1, n), 2):
        top = [frozenset(c) for c in itertools.combinations(range(n), j)]
        if len(top) < r or comb(n, i) < r:
            continue
        for Bf in itertools.combinations(top, r):
            down = set()
            for S in Bf:
                for c in itertools.combinations(sorted(S), i):
                    down.add(c)
            if comb(n, i) - len(down) >= r:
                return True
    return False


def test45():
    ok = True
    n = 6
    res = []
    for r in range(2, 21):
        a = recurrence_feasible(n, r, 2)
        b = brute_feasible_2lev(n, r)
        res.append((r, a, b))
        ok &= (a == b)
    print("(4) n=6: (r, recurrence-feasible, brute-force-feasible) =", res)
    print("(4) recurrence criterion == brute force at n=6:", ok)
    return ok


if __name__ == "__main__":
    sel = sys.argv[1:] or ["1", "2", "3", "45"]
    allok = True
    for s in sel:
        allok &= {"1": test1, "2": test2, "3": test3, "45": test45}[s]()
    print("ALL SANITY OK" if allok else "SANITY FAILURE")
