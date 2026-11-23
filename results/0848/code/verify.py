"""Independent checker for Erdos 848 distinct variant (written separately from d848.c).
1. Verifies witness sets directly (pairwise a*b+1 non-squarefree via sympy-free factor search).
2. Recomputes D(N) for N <= NB by a plain Bron-Kerbosch (pivot) max clique on the graph,
   built with a squarefree sieve (different method from the C modular-inverse construction).
Usage: python3 -I verify.py records_file mixed_file NB
"""
import sys
from itertools import combinations


def nonsqfree(x):
    d = 2
    while d * d <= x:
        if x % (d * d) == 0:
            return True
        d += 1
    return False


def check_set(S):
    return all(nonsqfree(a * b + 1) for a, b in combinations(S, 2)) and len(set(S)) == len(S)


def bk_max(adj, R, P, X, best):
    if not P and not X:
        if len(R) > len(best[0]):
            best[0] = list(R)
        return
    if len(R) + len(P) <= len(best[0]):
        return
    u = max(P | X, key=lambda w: len(adj[w] & P))
    for v in list(P - adj[u]):
        bk_max(adj, R + [v], P & adj[v], X & adj[v], best)
        P = P - {v}
        X = X | {v}


def main():
    rec, mixed, NB = sys.argv[1], sys.argv[2], int(sys.argv[3])
    bad = 0
    n = 0
    for fn in (rec, mixed):
        for line in open(fn):
            parts = line.split()
            S = [int(t) for t in parts[-1].split(",")]
            n += 1
            if not check_set(S):
                bad += 1
                print("BAD witness", line.strip()[:80])
    print(f"witness sets checked: {n}, bad: {bad}")
    # independent recomputation of D(N) for N <= NB
    M = NB * NB + 2
    sf = bytearray([1]) * (M + 1)
    p = 2
    while p * p <= M:
        for q in range(p * p, M + 1, p * p):
            sf[q] = 0
        p += 1
    adj = {v: set() for v in range(1, NB + 1)}
    D = 0
    out = []
    for N in range(1, NB + 1):
        for a in range(1, N):
            if not sf[a * N + 1]:
                adj[a].add(N)
                adj[N].add(a)
        best = [[]]
        nb = set(adj[N])
        # need clique of size D in nb
        if D == 0:
            found = True
        else:
            best = [[]]
            bk_max(adj, [], nb, set(), best)
            found = len(best[0]) >= D
        if found:
            D += 1
            out.append((N, D))
    print("records (N, D):", out[:12], "...", out[-1])
    c = lambda N: (N + 18) // 25
    print("N in [182,NB] with D(N)!=floor((N+18)/25):",
          [N for N in range(182, NB + 1) if max([d for (m, d) in out if m <= N]) != c(N)][:10])


main()
