# One step of the enumeration in gen.py, sharded to disk so it scales to e = 13, 14:
# read every graph with e-1 edges (no isolated vertices, one per iso class) from g{e-1}.txt,
# form every one-edge extension (same three kinds as gen.py), compute the invariant key
# (WL hash with 4 iterations, sorted degree sequence), write each child to shard
# hash(key) mod S, then deduplicate every shard independently by exact VF2 isomorphism
# inside each key bucket. Isomorphic graphs have equal keys, hence land in the same shard
# and bucket, so no class is lost and no class is kept twice.
# Usage: python3 -I gen_next.py graphsdir e workdir
import sys, os, hashlib
from multiprocessing import Pool
import networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash as wl
S = 200

def parse(line):
    return [tuple(map(int, t.split('-'))) for t in line.split()]

def children(line):
    G = nx.Graph(parse(line))
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
        key = wl(H, iterations=4) + ':' + ','.join(map(str, sorted(d for _, d in H.degree())))
        sh = int(hashlib.md5(key.encode()).hexdigest(), 16) % S
        out.append((sh, key + '\t' + ' '.join(f'{x}-{y}' for x, y in sorted(H.edges()))))
    return out

def dedup_shard(path):
    buckets = {}
    for line in open(path):
        key, ed = line.rstrip('\n').split('\t')
        buckets.setdefault(key, set()).add(ed)
    res = []
    for key, lst in buckets.items():
        reps = []
        for ed in sorted(lst):
            H = nx.Graph(parse(ed))
            if any(nx.is_isomorphic(H, K) for K in reps): continue
            reps.append(H)
        res += [' '.join(f'{x}-{y}' for x, y in sorted(H.edges())) for H in reps]
    os.remove(path)
    return res

if __name__ == '__main__':
    gd, e, wd = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    os.makedirs(wd, exist_ok=True)
    fs = [open(f'{wd}/shard{i}.txt', 'w') for i in range(S)]
    lines = [l for l in open(f'{gd}/g{e-1}.txt') if l.strip()]
    nch = 0
    with Pool(10) as pool:
        for ch in pool.imap_unordered(children, lines, chunksize=32):
            for sh, txt in ch:
                fs[sh].write(txt + '\n'); nch += 1
        for f in fs: f.close()
        print('children', nch, flush=True)
        total = 0
        with open(f'{gd}/g{e}.txt.tmp', 'w') as out:
            for res in pool.imap_unordered(dedup_shard, [f'{wd}/shard{i}.txt' for i in range(S)]):
                for ed in res: out.write(ed + '\n')
                total += len(res)
    os.rename(f'{gd}/g{e}.txt.tmp', f'{gd}/g{e}.txt')
    print(e, total, flush=True)
