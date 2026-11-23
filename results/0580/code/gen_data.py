# Generate (1) all graphs on j vertices up to isomorphism (networkx graph atlas, j<=7)
# and (2) all trees with e edges up to isomorphism (networkx nonisomorphic_trees).
# Output: one line per object, "nverts m a1 b1 a2 b2 ..." (edge list).
import sys, networkx as nx
out = sys.argv[1]
atlas = nx.graph_atlas_g()
for j in range(1, 8):
    gs = [g for g in atlas if g.number_of_nodes() == j]
    with open(f"{out}/graphs{j}.txt", "w") as f:
        for g in gs:
            m = {v: i for i, v in enumerate(g.nodes())}
            es = [(m[a], m[b]) for a, b in g.edges()]
            f.write(f"{j} {len(es)} " + " ".join(f"{a} {b}" for a, b in es) + "\n")
    print("graphs", j, len(gs))
for e in range(1, 15):
    ts = list(nx.nonisomorphic_trees(e + 1)) if e >= 1 else []
    with open(f"{out}/trees{e}.txt", "w") as f:
        for t in ts:
            m = {v: i for i, v in enumerate(t.nodes())}
            es = [(m[a], m[b]) for a, b in t.edges()]
            f.write(f"{e+1} {len(es)} " + " ".join(f"{a} {b}" for a, b in es) + "\n")
    print("trees_edges", e, len(ts))
