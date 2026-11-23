"""Builds the explicit extremal graphs K2 v H (join of an edge ab with H) for
n=5..10 and (i) checks the hypothesis of Lemma 5 for H by brute force over all
vertex subsets T: if H[T] has minimum degree >= 2 then e(H[T]) < 2|T|-4;
(ii) checks the edge count; (iii) re-checks P-freeness with pcheck.find_pair;
(iv) prints graph6 and whether it is isomorphic to one of gen.c's extremal graphs."""
import sys, re, itertools
sys.path.insert(0, '.')
from pcheck import find_pair, g6_decode
import networkx as nx

def path(m): return [(i, i+1) for i in range(m-1)], m
def cycle(m): return [(i, (i+1) % m) for i in range(m)], m
def theta332():
    # branch vertices 0,1; paths 0-2-3-1, 0-4-5-1, 0-6-1
    return [(0,2),(2,3),(3,1),(0,4),(4,5),(5,1),(0,6),(6,1)], 7
def k4sub():
    # K4 on {0,1,2,3}; edges 01,02,13,23 subdivided by 4,5,6,7; edges 03,12 kept
    return [(0,4),(4,1),(0,5),(5,2),(1,6),(6,3),(2,7),(7,3),(0,3),(1,2)], 8

def hyp_ok(EH, m):
    adj = {v: set() for v in range(m)}
    for a, b in EH: adj[a].add(b); adj[b].add(a)
    for k in range(1, m+1):
        for T in itertools.combinations(range(m), k):
            Ts = set(T)
            if all(len(adj[t] & Ts) >= 2 for t in T):
                e = sum(1 for a, b in EH if a in Ts and b in Ts)
                if not e < 2*k - 4: return False
    return True

def join_K2(EH, m):
    a, b = m, m+1
    E = [(x+0, y+0) for x, y in EH] + [(a, b)] + [(a, v) for v in range(m)] + [(b, v) for v in range(m)]
    return E, m+2

ext = {}
for line in open(sys.argv[1]):
    r = re.search(r'extremal n=(\d+) e=(\d+) g6=(\S+)', line)
    if r:
        n, E = g6_decode(r.group(3)); G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
        ext.setdefault(n, []).append(G)
for name, (EH, m) in [("P3", path(3)), ("P4", path(4)), ("C5", cycle(5)), ("C6", cycle(6)),
                      ("theta(3,3,2)", theta332()), ("K4 with 4 edges subdivided", k4sub())]:
    E, n = join_K2(EH, m)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    iso = any(nx.is_isomorphic(G, X) for X in ext.get(n, []))
    print(f"n={n} H={name}: e(H)={len(EH)}, hypothesis of Lemma 5: {hyp_ok(EH, m)}, e(G)={len(E)}, "
          f"pcheck: {'HAS_PAIR' if find_pair(n, E) else 'P-free'}, iso to a gen.c extremal graph: {iso}, "
          f"g6={nx.to_graph6_bytes(G, header=False).decode().strip()}")
