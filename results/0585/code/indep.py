"""Independent verification of f(9)=23 and f(10)=27 (upper bounds), using only
  * pcheck.py (explicit enumeration of all cycles; no code shared with gen.c),
  * networkx isomorphism tests,
  * labelled counts from brute.c at n=8 (m=18: 6368152, m=19: 175560),
  * Lemma 2 (min-degree vertex deletion) and Lemma 1 (monotonicity).
The 8-vertex class lists are taken from gen.c's dump but are *certified* here:
each listed graph is checked P-free, the list is checked pairwise non-isomorphic,
and the orbit sizes 8!/|Aut| are checked to sum to brute.c's labelled count, which
forces the list to be complete.
Usage: python3 -I indep.py ../out/dump_n8_ge18.txt
"""
import sys, math, re, itertools
from multiprocessing import Pool
sys.path.insert(0, '.')
from pcheck import g6_decode, find_pair
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

BRUTE = {18: 6368152, 19: 175560}

def mk(n, E):
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E); return G

def haspair(arg):
    n, E = arg
    return find_pair(n, E) is not None

def dedupe(graphs):
    buckets = {}
    out = []
    for G in graphs:
        h = nx.weisfeiler_lehman_graph_hash(G, iterations=4)
        lst = buckets.setdefault(h, [])
        if any(nx.is_isomorphic(G, H) for H in lst):
            continue
        lst.append(G); out.append(G)
    return out

def extensions(G, d):
    n = G.number_of_nodes()
    for N in itertools.combinations(range(n), d):
        E = list(G.edges()) + [(x, n) for x in N]
        yield (n + 1, E)

def main():
    cls = {18: [], 19: []}
    for line in open(sys.argv[1]):
        m = re.search(r'class n=8 e=(\d+) g6=(\S+)', line)
        if m and int(m.group(1)) in cls:
            n, E = g6_decode(m.group(2)); cls[int(m.group(1))].append(mk(n, E))
    pool = Pool(8)
    for e in (18, 19):
        L = cls[e]
        pf = pool.map(haspair, [(8, list(G.edges())) for G in L])
        assert not any(pf), "listed graph not P-free"
        assert len(dedupe(L)) == len(L), "duplicates in list"
        lab = sum(math.factorial(8) // sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter()) for G in L)
        print(f"n=8 e={e}: {len(L)} classes, all P-free, pairwise non-isomorphic, orbit sum {lab}, brute {BRUTE[e]}, match={lab==BRUTE[e]}")
        assert lab == BRUTE[e]
    # f(9) <= 23: a P-free 24-edge graph on 9 vertices = 19-edge 8-vertex class + degree-5 vertex
    cand = [x for G in cls[19] for x in extensions(G, 5)]
    res = pool.map(haspair, cand)
    print(f"n=9 e=24 candidates: {len(cand)}, P-free among them: {res.count(False)}")
    # 23-edge P-free graphs on 9 vertices: 19-class + deg-4 vertex, or 18-class + deg-5 vertex
    cand = [x for G in cls[19] for x in extensions(G, 4)] + [x for G in cls[18] for x in extensions(G, 5)]
    res = pool.map(haspair, cand)
    free23 = dedupe([mk(n, E) for (n, E), r in zip(cand, res) if not r])
    print(f"n=9 e=23 candidates: {len(cand)}, P-free iso classes: {len(free23)}")
    for G in free23:
        print("   ", nx.to_graph6_bytes(G, header=False).decode().strip(), sorted(d for _, d in G.degree()))
    # f(10) <= 27: P-free 28-edge graph on 10 vertices = 23-edge 9-vertex class + degree-5 vertex
    cand = [x for G in free23 for x in extensions(G, 5)]
    res = pool.map(haspair, cand)
    print(f"n=10 e=28 candidates: {len(cand)}, P-free among them: {res.count(False)}")

if __name__ == "__main__":
    main()
