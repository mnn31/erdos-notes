"""Independent check of witness graphs: odd girth via BFS parity (networkx-free),
D(G) via numpy enumeration of all 2^(N-1) bipartitions (exact ints)."""
import sys, json, numpy as np, itertools
def odd_girth(N, edges):
    adj = [[] for _ in range(N)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    best = None
    for s in range(N):   # shortest odd closed walk through s via BFS on (vertex, parity)
        dist = {(s, 0): 0}; q = [(s, 0)]
        for (v, p) in q:
            for u in adj[v]:
                if (u, 1-p) not in dist:
                    dist[(u, 1-p)] = dist[(v, p)] + 1; q.append((u, 1-p))
        if (s, 1) in dist:
            best = dist[(s, 1)] if best is None else min(best, dist[(s, 1)])
    return best  # shortest odd closed walk = shortest odd cycle
def D_numpy(N, edges):
    masks = np.arange(1 << (N-1), dtype=np.int64) << 1   # vertex 0 on side 0
    cnt = np.zeros(len(masks), dtype=np.int64)
    for a, b in edges:
        cnt += (((masks >> a) & 1) == ((masks >> b) & 1))
    return int(cnt.min()), len(edges)
def blowup(s):
    k = len(s); idx = []; c = 0
    for x in s: idx.append(list(range(c, c+x))); c += x
    return c, [(a, b) for i in range(k) for a in idx[i] for b in idx[(i+1) % k]]
if __name__ == "__main__":
    for f in sys.argv[1:]:
        for l in open(f):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('graph'):
                og = odd_girth(r['N'], r['graph']); D, e = D_numpy(r['N'], r['graph'])
                print(f.split('/')[-1], 'N', r['N'], 't', r['t'], 'edges', e, 'oddgirth', og, 'D', D,
                      'OK' if D >= r['t'] and og >= (7 if r['kind'] == 'og7' else 5) else 'FAIL')
