# Independent checks (networkx subgraph monomorphism, no reduction used).
# 1) every COUNTEREXAMPLE line in a given output file: hypothesis holds and tree does not embed.
# 2) random edge-minimal hosts for the Loebl edge form at n=2k: all trees with k edges embed.
import sys, random, re, networkx as nx
from networkx.algorithms import isomorphism as iso
data = sys.argv[1]
def load_trees(e):
    out = []
    for line in open(f"{data}/trees{e}.txt"):
        a = list(map(int, line.split())); nv, m = a[0], a[1]
        T = nx.Graph(); T.add_nodes_from(range(nv)); T.add_edges_from(zip(a[2::2], a[3::2])); out.append(T)
    return out
def contains(G, T):
    return iso.GraphMatcher(G, T).subgraph_is_monomorphic()
def from_masks(ms):
    G = nx.Graph(); G.add_nodes_from(range(len(ms)))
    for v, m in enumerate(ms):
        for u in range(len(ms)):
            if m >> u & 1: G.add_edge(v, u)
    return G
mode = sys.argv[2]
if mode == "cex":
    cur = None
    for line in open(sys.argv[3]):
        m = re.match(r"RESULT.*N=(\d+) J=(\d+) D=(\d+) E=(\d+)", line)
        if m: continue
    # parse blocks: a COUNTEREXAMPLE line belongs to the following RESULT line
    lines = open(sys.argv[3]).read().splitlines(); pend = []; nok = 0
    for line in lines:
        if line.startswith("COUNTEREXAMPLE"):
            pend.append(line); continue
        m = re.search(r"N=(\d+) J=(\d+) D=(\d+) E=(\d+)", line)
        if m and pend:
            N, J, D, E = map(int, m.groups()); trees = load_trees(E)
            for p in pend:
                t = int(re.search(r"tree#(\d+)", p).group(1))
                ms = [int(x, 16) for x in p.split(":")[1].split()]
                G = from_masks(ms)
                assert all((ms[v] >> v & 1) == 0 and all((ms[u] >> v & 1) == (ms[v] >> u & 1) for u in range(N)) for v in range(N))
                hyp = sum(1 for v in G if G.degree(v) >= D) >= J
                emb = contains(G, trees[t])
                print(f"N={N} J={J} D={D} E={E} tree#{t} hypothesis={hyp} tree_embeds={emb}")
                nok += (hyp and not emb)
            pend = []
    print("verified counterexamples:", nok)
elif mode == "rand":
    k = int(sys.argv[3]); J = int(sys.argv[4]); reps = int(sys.argv[5]); n = 2 * k
    trees = load_trees(k); rng = random.Random(int(sys.argv[6]))
    bad = 0
    for r in range(reps):
        p = rng.uniform(0.3, 0.9)
        G = nx.gnp_random_graph(n, p, seed=rng.randrange(10**9))
        def hyp(G): return sum(1 for v in G if G.degree(v) >= k) >= J
        if not hyp(G): continue
        es = list(G.edges()); rng.shuffle(es)
        for e in es:  # greedy edge-minimal
            G.remove_edge(*e)
            if not hyp(G): G.add_edge(*e)
        for i, T in enumerate(trees):
            if not contains(G, T):
                bad += 1; print("RANDOM COUNTEREXAMPLE", k, J, i, sorted(G.edges())); break
    print(f"random minimal hosts n={n} J={J}: reps={reps} bad={bad}")
