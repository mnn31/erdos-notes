"""Independent check of the 'mixed maximum clique' test for 182 <= N <= NB (Python, BK).
For each N: m(N) = largest clique with max element N that is neither inside C7 nor inside C18
(C7 = 7 mod 25, C18 = 18 mod 25). Prints N where m(N) >= floor((N+18)/25)."""
import sys
sys.setrecursionlimit(10000)
NB = int(sys.argv[1])
def nsf(x):
    d = 2
    while d * d <= x:
        if x % (d * d) == 0: return True
        d += 1
    return False
adj = {v: set() for v in range(1, NB + 1)}
for a in range(1, NB + 1):
    for b in range(a + 1, NB + 1):
        if nsf(a * b + 1): adj[a].add(b); adj[b].add(a)
def omega(P):
    best = [0]
    def bk(r, P, X):
        if not P and not X:
            best[0] = max(best[0], r); return
        if r + len(P) <= best[0]: return
        u = max(P | X, key=lambda w: len(adj[w] & P))
        for v in list(P - adj[u]):
            bk(r + 1, P & adj[v], X & adj[v]); P = P - {v}; X = X | {v}
    bk(0, set(P), set())
    return best[0]
hits = []
for N in range(182, NB + 1):
    c = (N + 18) // 25
    U = {a for a in adj[N] if a < N}
    r = N % 25
    if r not in (7, 18):
        m = 1 + omega(U)
    else:
        cls = {a for a in U if a % 25 == r}
        m = 0
        done = set()
        for x in sorted(U - cls):
            m = max(m, 2 + omega((U & adj[x]) - done))
            done.add(x)
    if m >= c: hits.append((N, c, m))
print("NB", NB, "N with mixed clique of size >= c(N) ending at N:", hits)
