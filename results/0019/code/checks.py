"""Exact checks for Erdos #19, m_5(3) = 12.  Run: python3 -I checks.py
All arithmetic is integer/combinatorial; chromatic numbers by exhaustive backtracking."""
import itertools, json, os, sys
import networkx as nx

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')

def colorable(n, adj, k):
    """exact: is the graph on 0..n-1 (adjacency sets) properly k-colourable?"""
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    col = {}
    def rec(i, used):
        if i == n: return True
        v = order[i]
        forb = {col[u] for u in adj[v] if u in col}
        for c in range(min(k, used + 1)):          # symmetry: new colour only = used
            if c not in forb:
                col[v] = c
                if rec(i + 1, max(used, c + 1)): return True
                del col[v]
        return False
    return rec(0, 0)

def chi(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    if n == 0: return 0
    k = 1
    while not colorable(n, adj, k): k += 1
    return k

def check_decomposition(tris):
    """triangles pairwise edge-disjoint? return the union edge set"""
    E = set()
    for t in tris:
        assert len(set(t)) == 3
        for e in itertools.combinations(sorted(t), 2):
            assert e not in E, ('edge reused', e)
            E.add(e)
    return E

log = []
def say(s):
    print(s); log.append(s)

# ---- C1: STS(9) = affine plane AG(2,3) decomposes K_9 into 12 triangles; chi(K_9)=9
pts = [(x, y) for x in range(3) for y in range(3)]
idx = {p: i for i, p in enumerate(pts)}
lines = set()
for p in pts:
    for d in [(1, 0), (0, 1), (1, 1), (1, 2)]:
        L = tuple(sorted(idx[((p[0] + s * d[0]) % 3, (p[1] + s * d[1]) % 3)] for s in range(3)))
        lines.add(L)
sts9 = sorted(lines)
E = check_decomposition(sts9)
assert len(sts9) == 12 and E == set(itertools.combinations(range(9), 2))
say(f"C1: STS(9) has {len(sts9)} pairwise edge-disjoint triangles, union = K_9 ({len(E)} edges), chi = {chi(9, E)}")

# ---- C2: 12 triangles whose union has chi exactly 8 (K_8 + four pendant triangles)
M = [(0, 1), (2, 3), (4, 5), (6, 7)]
target = set(itertools.combinations(range(8), 2)) - set(M)       # K_8 minus a perfect matching
cands = [t for t in itertools.combinations(range(8), 3)
         if all(e in target for e in itertools.combinations(t, 2))]
def decompose(rem, chosen):
    if not rem: return list(chosen)
    e = min(rem)
    for t in cands:
        es = set(itertools.combinations(t, 2))
        if e in es and es <= rem:
            r = decompose(rem - es, chosen + [t])
            if r: return r
    return None
dec = decompose(set(target), [])
assert dec is not None and len(dec) == 8
tris2 = dec + [(0, 1, 8), (2, 3, 9), (4, 5, 10), (6, 7, 11)]
E2 = check_decomposition(tris2)
assert E2 >= set(itertools.combinations(range(8), 2))              # contains K_8
c2 = chi(12, E2)
say(f"C2: {len(tris2)} edge-disjoint triangles {tris2}; union has {len(E2)} edges, contains K_8, chi = {c2}")
assert c2 == 8

# ---- C3: Lemma 1 input: an 8-vertex graph with chi >= 8 is K_8 (chi(K_8 - e) = 7)
K8e = set(itertools.combinations(range(8), 2)) - {(0, 1)}
say(f"C3: chi(K_8) = {chi(8, set(itertools.combinations(range(8), 2)))}, chi(K_8 - e) = {chi(8, K8e)}")

# ---- C4: every graph on 9 vertices with min degree >= 7 and <= 33 edges has chi <= 6
#      exhaustive over all complements with 3 or 4 edges (graphs with 33 or 32 edges);
#      fewer than 32 edges is impossible with min degree >= 7 (63/2 > 31).
allE = list(itertools.combinations(range(9), 2))
cnt = 0; worst = 0; tested = 0
for r in (3, 4):
    for comp in itertools.combinations(allE, r):
        tested += 1
        deg = [8] * 9
        for u, v in comp: deg[u] -= 1; deg[v] -= 1
        if min(deg) < 7: continue
        cnt += 1
        Eg = set(allE) - set(comp)
        worst = max(worst, chi(9, Eg))
say(f"C4: complements tested = {tested}; graphs on 9 vertices with 32-33 edges and min degree >= 7: {cnt}; max chi among them = {worst}")
assert worst <= 7

# ---- C5: analogue of Lemma 2 at c=6 and c=4, exhaustive over the graph atlas (all graphs <= 7 vertices):
#      chi >= c and at most C(c,2)+c-3 edges  ==>  contains K_c.
for c in (4, 6):
    bound = c * (c - 1) // 2 + c - 3
    bad = 0; seen = 0
    for G in nx.graph_atlas_g():
        if G.number_of_edges() > bound or G.number_of_nodes() < c: continue
        n = G.number_of_nodes(); Eg = [tuple(sorted(e)) for e in G.edges()]
        if chi(n, Eg) >= c:
            seen += 1
            has = any(all(G.has_edge(a, b) for a, b in itertools.combinations(S, 2))
                      for S in itertools.combinations(G.nodes(), c))
            if not has: bad += 1
    say(f"C5: c={c}: atlas graphs with <= {bound} edges and chi >= {c}: {seen}; without K_{c}: {bad}")
    assert bad == 0

json.dump({'sts9': sts9, 'chi_exactly_8_example': tris2}, open(os.path.join(OUT, 'objects.json'), 'w'))
open(os.path.join(OUT, 'checks.txt'), 'w').write('\n'.join(log) + '\n')
print('ALL CHECKS PASSED')
