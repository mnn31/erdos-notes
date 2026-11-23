#!/usr/bin/env python3
"""Exact search for n_0^{(4)}(r), 2 <= r <= RMAX (exact Python integers).

For each r and each n = 2r+5, 2r+4, ..., 5 (downwards) we look for a 3-set M of
missing levels in {1..n-1} such that the profile f_i = r (i in L = {1..n-1}\\M),
f_i = 0 otherwise passes the prescribed-profile recurrence
    m_T = r (T = max L),  m_i = f_i + KK_{i+1}(m_{i+1}),  m_i <= C(n,i) for 0 <= i <= T.
The first n (from the top) for which NO M passes is N(r); every M then gets an
overflow certificate line (M, i, m_i, C(n,i)).  If every n in [5, 2r+5] has a passing M,
N(r) = 0.  For every n in (N(r), 2r+5], n >= 5, the passing profile is written out as an
explicit colex witness (sets as hex bitmasks) -- the witness is what certifies g(n,r) >= n-4;
the recurrence is only used to *find* it.

Also writes, for every r, the base core on q = r+5 points (levels 2..r+2, r sets each, colex)
plus r free (r+1)-sets obtained by puncturing one top-level core member.

Usage: python3 -I code/search.py RMIN RMAX OUTDIR
"""
import sys, os, itertools
from math import comb
from functools import lru_cache


@lru_cache(maxsize=None)
def kk(k, m):
    """Kruskal-Katona lower bound for the (k-1)-shadow of m distinct k-sets."""
    if m <= 0:
        return 0
    res = 0
    j = k
    while m > 0 and j >= 1:
        a = j
        while comb(a + 1, j) <= m:
            a += 1
        # a = max{a : C(a,j) <= m}
        res += comb(a, j - 1)
        m -= comb(a, j)
        j -= 1
    assert m == 0
    return res


def recurrence(n, levels, r):
    """levels: set of occupied levels. Returns (ok, m dict, first overflow (i, m_i))."""
    T = max(levels)
    m = {}
    cur = 0
    for i in range(T, -1, -1):
        f = r if i in levels else 0
        cur = f + (kk(i + 1, cur) if i < T else 0)
        m[i] = cur
        if cur > comb(n, i):
            return False, m, (i, cur)
    return True, m, None


def colex_unrank(R, k):
    """k-subset of {0,1,2,...} with 0-based colex rank R."""
    s = []
    for j in range(k, 0, -1):
        c = j - 1
        while comb(c + 1, j) <= R:
            c += 1
        s.append(c)
        R -= comb(c, j)
    assert R == 0
    return s


def colex_family(n, levels, r):
    ok, m, _ = recurrence(n, levels, r)
    assert ok
    T = max(levels)
    fam = []
    for i in sorted(levels):
        lo = kk(i + 1, m[i + 1]) if i < T else 0
        hi = m[i]
        assert hi - lo == r
        for R in range(lo, hi):
            S = colex_unrank(R, i)
            assert len(S) == i and max(S) < n
            fam.append(S)
    return fam


def mask(S):
    x = 0
    for e in S:
        x |= 1 << e
    return x


def triples_in_order(n):
    """All 3-subsets of {1..n-1}; a few natural candidates first, then the rest."""
    first = [(1, 2, n - 1), (1, n - 2, n - 1), (1, 3, n - 1)]
    seen = set()
    for t in first:
        t = tuple(sorted(t))
        if len(set(t)) == 3 and all(1 <= x <= n - 1 for x in t) and t not in seen:
            seen.add(t)
            yield t
    for t in itertools.combinations(range(1, n), 3):
        if t not in seen:
            yield t


def main():
    rmin, rmax, outdir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    os.makedirs(os.path.join(outdir, "witnesses"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "certs"), exist_ok=True)
    summary = []
    for r in range(rmin, rmax + 1):
        N = 0
        wit = []  # (n, levels)
        for n in range(2 * r + 5, 4, -1):
            found = None
            for M in triples_in_order(n):
                L = set(range(1, n)) - set(M)
                ok, _, _ = recurrence(n, L, r)
                if ok:
                    found = (M, L)
                    break
            if found is None:
                N = n
                with open(os.path.join(outdir, "certs", f"cert_r{r}_n{n}.txt"), "w") as fh:
                    fh.write(f"# r={r} N={n}: for every 3-set M of missing levels in 1..{n-1},\n")
                    fh.write("# the recurrence overflows: M1 M2 M3 i m_i C(N,i)\n")
                    fh.write(f"C {r} {n} {comb(n - 1, 3)}\n")
                    for M in itertools.combinations(range(1, n), 3):
                        L = set(range(1, n)) - set(M)
                        ok, m, ov = recurrence(n, L, r)
                        assert not ok
                        i, mi = ov
                        fh.write(f"{M[0]} {M[1]} {M[2]} {i} {mi} {comb(n, i)}\n")
                break
            wit.append((n, found[0], found[1]))
        # witnesses
        with open(os.path.join(outdir, "witnesses", f"wit_r{r}.txt"), "w") as fh:
            for (n, M, L) in sorted(wit):
                fam = colex_family(n, L, r)
                fh.write(f"W {n} {r} {n - 4} {len(fam)} missing {M[0]} {M[1]} {M[2]}\n")
                for S in fam:
                    fh.write(f"{mask(S):x}\n")
            # base core
            q = r + 5
            Lc = set(range(2, r + 3))
            okc, _, ov = recurrence(q, Lc, r)
            if not okc:
                print(f"r={r}: CORE PROFILE INFEASIBLE {ov}", flush=True)
            else:
                fam = colex_family(q, Lc, r)
                top = [S for S in fam if len(S) == r + 2][0]
                free = [sorted(set(top) - {x}) for x in top][:r]
                fh.write(f"K {q} {r} {r + 2} {len(fam)} {len(free)}\n")
                for S in fam:
                    fh.write(f"{mask(S):x}\n")
                for S in free:
                    fh.write(f"{mask(S):x}\n")
        mis = sorted(set((w[1][0], w[1][1], w[1][2] - w[0]) for w in wit))
        print(f"r={r} N={N} witness n range=({N},{2*r+5}] count={len(wit)} "
              f"missing levels used, as (m1, m2, m3-n): {mis}", flush=True)
        summary.append((r, N))
    with open(os.path.join(outdir, f"summary_{rmin}_{rmax}.txt"), "w") as fh:
        for r, N in summary:
            fh.write(f"{r} {N}\n")


if __name__ == "__main__":
    main()
