# Enumerate all graphs with exactly e edges and no isolated vertices, up to isomorphism,
# for e = 1..E, by adding one edge to every graph with e-1 edges in every possible way
# (between two existing non-adjacent vertices, from an existing vertex to a new one,
# or a new disjoint edge). Every graph with e edges and no isolated vertices arises this way
# (delete any edge, then delete the vertices that became isolated).
# Isomorph rejection: bucket by Weisfeiler-Lehman hash (an isomorphism invariant) plus
# sorted degree sequence, then exact VF2 isomorphism test inside a bucket.
# Output: out_dir/g{e}.txt, one graph per line: "u-v u-v ...".
import sys, os
from multiprocessing import Pool
import networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash as wl

def children(edges):
    G = nx.Graph(edges)
    V = sorted(G.nodes()); nv = len(V)
    cands = []
    for i in range(nv):
        for j in range(i+1, nv):
            if not G.has_edge(V[i], V[j]): cands.append((V[i], V[j]))
        cands.append((V[i], nv))
    cands.append((nv, nv+1))
    out = []
    for (a, b) in cands:
        H = G.copy(); H.add_edge(a, b)
        H = nx.convert_node_labels_to_integers(H)
        key = (wl(H, iterations=4), tuple(sorted(d for _, d in H.degree())))
        out.append((key, tuple(sorted(H.edges()))))
    return out

if __name__ == '__main__':
    E = int(sys.argv[1]); od = sys.argv[2]
    os.makedirs(od, exist_ok=True)
    gs = [((0, 1),)]
    with open(f'{od}/g1.txt', 'w') as f: f.write('0-1\n')
    print(1, 1, flush=True)
    with Pool(10) as pool:
        for e in range(2, E+1):
            buckets = {}
            res = []
            for ch in pool.imap(children, gs, chunksize=64):
                for key, ed in ch:
                    buckets.setdefault(key, []).append(ed)
            # dedupe inside buckets
            def dedup(lst):
                reps = []
                for ed in lst:
                    H = nx.Graph(ed)
                    if any(nx.is_isomorphic(H, K) for K in reps): continue
                    reps.append(H)
                return [tuple(sorted(H.edges())) for H in reps]
            newgs = []
            for key, lst in buckets.items():
                # quick exact duplicate removal first
                lst = list(dict.fromkeys(lst))
                newgs.extend(dedup(lst))
            gs = newgs
            with open(f'{od}/g{e}.txt', 'w') as f:
                for ed in gs: f.write(' '.join(f'{a}-{b}' for a, b in ed) + '\n')
            print(e, len(gs), flush=True)
