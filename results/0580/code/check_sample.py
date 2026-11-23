# networkx re-check of sampled reduced hosts: hypothesis and all trees with E edges embed
import sys, networkx as nx
from networkx.algorithms import isomorphism as iso
data, fn, J, D, E = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:6])
trees = []
for line in open(f"{data}/trees{E}.txt"):
    a = list(map(int, line.split())); T = nx.Graph(); T.add_nodes_from(range(a[0])); T.add_edges_from(zip(a[2::2], a[3::2])); trees.append(T)
n = bad = 0
for line in open(fn):
    if not line.startswith("HOST"): continue
    ms = [int(x, 16) for x in line.split()[1:]]; N = len(ms)
    G = nx.Graph(); G.add_nodes_from(range(N))
    for v in range(N):
        for u in range(N):
            if ms[v] >> u & 1: G.add_edge(v, u)
    assert sum(G.degree(v) >= D for v in G) >= J
    n += 1
    if any(not iso.GraphMatcher(G, T).subgraph_is_monomorphic() for T in trees): bad += 1
print(f"sampled hosts={n} missing_tree={bad}")
