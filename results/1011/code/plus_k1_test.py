"""Exploration (not load-bearing): compare chi(H), chi(G*(H)), chi(G*(H+K1)) for small triangle-free H."""
import sys, time
sys.path.insert(0, sys.path[0])
import networkx as nx
from gstar import gstar, triangle_free
from pysat.solvers import Cadical153
def colourable(G, k):
    V = list(G.nodes()); idx = {v: i for i, v in enumerate(V)}
    var = lambda v, c: idx[v]*k + c + 1
    s = Cadical153()
    for v in V: s.add_clause([var(v, c) for c in range(k)])
    for u, w in G.edges():
        for c in range(k): s.add_clause([-var(u, c), -var(w, c)])
    u, w = next(iter(G.edges())); s.add_clause([var(u, 0)]); s.add_clause([var(w, 1)])
    r = s.solve(); s.delete(); return r
def chi(G, lo=1):
    k = lo
    while not colourable(G, k): k += 1
    return k
def plusK1(H):
    H2 = nx.convert_node_labels_to_integers(H); H2.add_node(H2.number_of_nodes()); return H2
tests = {'K1': nx.empty_graph(1), 'K2': nx.complete_graph(2), 'P3': nx.path_graph(3), 'C4': nx.cycle_graph(4),
         'C5': nx.cycle_graph(5), 'C7': nx.cycle_graph(7), 'C9': nx.cycle_graph(9), 'Petersen': nx.petersen_graph(),
         'K33': nx.complete_bipartite_graph(3, 3), 'C5+C5': nx.disjoint_union(nx.cycle_graph(5), nx.cycle_graph(5)),
         'Moebius8': nx.circulant_graph(8, [1, 4]), 'C8(1,3)': nx.circulant_graph(8, [1, 3])}
for nm, H in tests.items():
    H = nx.convert_node_labels_to_integers(H); assert triangle_free(H)
    t = time.time()
    ch = chi(H) if H.number_of_edges() else 1
    G1 = gstar(H); G2 = gstar(plusK1(H))
    c1 = chi(G1, 2); c2 = chi(G2, 2)
    print(f'{nm:10s} |H|={H.number_of_nodes():2d} chi(H)={ch} chi(G*(H))={c1} chi(G*(H+K1))={c2} '
          f'|G*(H+K1)|={G2.number_of_nodes()} t={time.time()-t:.1f}', flush=True)
