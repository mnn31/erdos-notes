"""Cross-check: for each n, the extremal classes found by gen.c must be pairwise
non-isomorphic, and sum_{classes} n!/|Aut(G)| must equal the number of labelled
P-free graphs with f(n) edges found by brute.c (independent enumeration)."""
import sys, math, re
sys.path.insert(0, '.')
from pcheck import g6_decode
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
byn = {}
for line in open(sys.argv[1]):
    m = re.search(r'extremal n=(\d+) e=(\d+) g6=(\S+)', line)
    if m: byn.setdefault(int(m.group(1)), []).append(m.group(3))
for n, lst in sorted(byn.items()):
    gs = []
    for s in lst:
        k, E = g6_decode(s); G = nx.Graph(); G.add_nodes_from(range(k)); G.add_edges_from(E); gs.append(G)
    noniso = all(not nx.is_isomorphic(gs[i], gs[j]) for i in range(len(gs)) for j in range(i+1, len(gs)))
    auts = [sum(1 for _ in GraphMatcher(G, G).isomorphisms_iter()) for G in gs]
    lab = sum(math.factorial(n) // a for a in auts)
    print(f"n={n} classes={len(gs)} pairwise_nonisomorphic={noniso} |Aut|={auts} labelled_total={lab}")
