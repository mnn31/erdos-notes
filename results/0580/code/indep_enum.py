# Independent re-implementation (Python + networkx) of the reduced enumeration:
# H from the atlas file, S-side = multisets of N-J columns (itertools.combinations_with_replacement
# over all subsets of L), filtered by row sums; embedding by networkx monomorphism.
import sys, itertools, networkx as nx
from networkx.algorithms import isomorphism as iso
data, N, J, D, E = sys.argv[1], *map(int, sys.argv[2:6])
NS = N - J
def rd(fn):
    for line in open(fn):
        a = list(map(int, line.split())); yield a[0], list(zip(a[2::2], a[3::2]))
trees = []
for nv, es in rd(f"{data}/trees{E}.txt"):
    T = nx.Graph(); T.add_nodes_from(range(nv)); T.add_edges_from(es); trees.append(T)
hosts = bad = 0
subsets = range(1 << J)
for nv, es in rd(f"{data}/graphs{J}.txt"):
    deg = [0] * J
    for a, b in es: deg[a] += 1; deg[b] += 1
    r = [max(0, D - d) for d in deg]
    for cols in itertools.combinations_with_replacement(subsets, NS):
        if any(sum(c >> u & 1 for c in cols) != r[u] for u in range(J)): continue
        G = nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(es)
        for s, c in enumerate(cols):
            for u in range(J):
                if c >> u & 1: G.add_edge(u, J + s)
        hosts += 1
        if any(not iso.GraphMatcher(G, T).subgraph_is_monomorphic() for T in trees): bad += 1
print(f"INDEP N={N} J={J} D={D} E={E} reduced_hosts={hosts} hosts_with_missing_tree={bad}")
