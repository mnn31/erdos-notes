"""Enumerate triangle-free graphs on n <= 11 vertices up to isomorphism (n <= 10),
and list all triangle-free graphs on 11 vertices with chromatic number >= 4.

Method (Lemma 5 of WRITEUP): every triangle-free graph on n vertices is isomorphic to
R + v where R is a triangle-free graph on n-1 vertices (a representative of H - v) and
N(v) is an independent set of R. Levels 1..10 are deduplicated exactly (WL hash bucket,
then networkx VF2 isomorphism test). Level 11 is NOT deduplicated: every candidate
R + v is tested for 3-colourability; only the non-3-colourable ones are kept and then
deduplicated.  Output: counts per level, and the list of non-3-colourable graphs.
"""
import sys, itertools, json, time
import networkx as nx

def to_nx(n, adj):
    G = nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1, n):
            if adj[i] >> j & 1: G.add_edge(i, j)
    return G

def indep_subsets(n, adj):
    """all independent sets of the graph (bitmasks), including empty"""
    out = [0]
    for v in range(n):
        out += [S | (1 << v) for S in out if not (adj[v] & S)]
    return out

def three_colourable(n, adj, k=3):
    """exact backtracking k-colouring; vertices in order of decreasing degree.
    A True answer is certified: the colouring found is re-checked edge by edge."""
    col = _colour(n, adj, k)
    if col is None: return False
    assert all(col[i] != col[j] and 0 <= col[i] < k for i in range(n) for j in range(n) if adj[i] >> j & 1)
    return True

def _colour(n, adj, k):
    order = sorted(range(n), key=lambda v: -bin(adj[v]).count('1'))
    col = [-1]*n
    def bt(i):
        if i == n: return True
        v = order[i]
        used = {col[u] for u in range(n) if adj[v] >> u & 1 and col[u] >= 0}
        top = max([c for c in col if c >= 0], default=-1)
        for c in range(min(k, top+2)):   # symmetry: new colour only the next unused one
            if c not in used:
                col[v] = c
                if bt(i+1): return True
                col[v] = -1
        return False
    return list(col) if bt(0) else None

def is_tf(n, adj):
    return all(not (adj[i] & adj[j]) for i in range(n) for j in range(n) if adj[i] >> j & 1)

class Dedup:
    def __init__(self): self.buckets = {}; self.reps = []
    def add(self, n, adj):
        G = to_nx(n, adj)
        h = (tuple(sorted(d for _, d in G.degree())), nx.weisfeiler_lehman_graph_hash(G, iterations=3))
        for H in self.buckets.get(h, []):
            if nx.is_isomorphic(G, H): return False
        self.buckets.setdefault(h, []).append(G); self.reps.append(tuple(adj)); return True

def extend(n, adj, S):
    new = list(adj) + [S]
    for u in range(n):
        if S >> u & 1: new[u] |= 1 << n
    return new

FULL = '--full' in sys.argv
def main(N=11):
    level = {1: [(0,)]}
    print('n=1 count 1', flush=True)
    noncol = {}
    for n in range(2, N+1):
        t = time.time()
        D = Dedup(); bad = Dedup(); cand = 0
        for adj in level[n-1]:
            for S in indep_subsets(n-1, list(adj)):
                new = extend(n-1, adj, S); cand += 1
                if n < N or FULL: D.add(n, new)
                if not three_colourable(n, new):
                    assert is_tf(n, new)
                    bad.add(n, new)
        if n < N: level[n] = D.reps
        noncol[n] = bad.reps
        print(f'n={n} candidates {cand} distinct {len(D.reps) if (n < N or FULL) else "(not deduplicated)"} '
              f'non-3-colourable distinct {len(bad.reps)} time {time.time()-t:.1f}s', flush=True)
    return level, noncol

if __name__ == '__main__':
    level, noncol = main(11)
    out = {str(n): [[[i, j] for i in range(n) for j in range(i+1, n) if adj[i] >> j & 1] for adj in L]
           for n, L in noncol.items()}
    json.dump(out, open(sys.argv[1], 'w'))
    G11 = nx.mycielski_graph(4)
    for n, L in noncol.items():
        for adj in L:
            print('non-3-colourable graph on', n, 'vertices, edges', bin(sum(1 for a in adj for _ in [0])) and sum(bin(a).count('1') for a in adj)//2,
                  'isomorphic to Groetzsch:', nx.is_isomorphic(to_nx(n, adj), G11))
