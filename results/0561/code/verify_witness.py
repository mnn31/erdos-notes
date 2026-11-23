# Independent verifier of witness colourings written by arrow.c.
# For each line "mask<TAB>edges": checks that the colouring (bit i of mask = edge i red)
# has no red F1 and no blue F2. Uses a different algorithm from arrow.c: centres of the stars
# with >= 2 leaves are enumerated, leaves are decided by bipartite b-matching (augmenting paths),
# and single-edge components are found by a maximum matching (Edmonds) in what is left.
# Usage: python3 -I verify_witness.py "n1,n2,.." "m1,m2,.." witnessfile
import sys, itertools
import networkx as nx

def contains(adj, sizes):
    """Does the graph adj (dict vertex -> set of neighbours) contain vertex-disjoint stars
    K_{1,s} for s in sizes?  Stars with s >= 2: choose distinct centres (increasing among
    equal sizes) and then decide whether their leaves can be chosen disjointly, by a bipartite
    b-matching (augmenting paths).  If there are also q single-edge components (s = 1), the
    leaf sets of the big stars are enumerated explicitly and a matching of size q is sought in
    the rest (Edmonds' blossom algorithm: networkx max_weight_matching, unit weights,
    maxcardinality=True)."""
    big = sorted([x for x in sizes if x >= 2], reverse=True)
    q = sum(1 for x in sizes if x == 1)
    V = sorted(adj)
    cand = [[v for v in V if len(adj[v]) >= s] for s in big]
    def rest_has_matching(used):
        if q == 0: return True
        H = nx.Graph()
        for u in V:
            if u in used: continue
            for w in adj[u]:
                if w not in used and u < w: H.add_edge(u, w)
        if H.number_of_edges() < q: return False
        return len(nx.max_weight_matching(H, maxcardinality=True)) >= q
    def rec(i, chosen):
        if i == len(big):
            if q == 0:
                return leaves_ok(adj, big, chosen)
            return leafsets(chosen)
        for v in cand[i]:
            if v in chosen: continue
            if i > 0 and big[i] == big[i-1] and v < chosen[-1]: continue
            if rec(i+1, chosen + [v]): return True
        return False
    def leafsets(centres):
        if not leaves_ok(adj, big, centres): return False
        C = set(centres)
        def lr(i, used):
            if i == len(centres): return rest_has_matching(used)
            nb = sorted(u for u in adj[centres[i]] if u not in used and u not in C)
            for L in itertools.combinations(nb, big[i]):
                if lr(i+1, used | set(L)): return True
            return False
        return lr(0, set(C))
    return rec(0, [])

def leaves_ok(adj, sizes, centres):
    """Can each centre c_i get sizes[i] private leaves among its neighbours, all distinct and
    avoiding all centres?  Bipartite b-matching via augmenting paths (one slot per leaf)."""
    C = set(centres)
    slots = []
    for c, s in zip(centres, sizes):
        nb = [u for u in adj[c] if u not in C]
        if len(nb) < s: return False
        slots += [nb] * s
    match = {}  # leaf -> slot index
    def aug(i, seen):
        for u in slots[i]:
            if u in seen: continue
            seen.add(u)
            if u not in match or aug(match[u], seen):
                match[u] = i; return True
        return False
    return all(aug(i, set()) for i in range(len(slots)))

if __name__ == '__main__':
    F1 = [int(x) for x in sys.argv[1].split(',')]
    F2 = [int(x) for x in sys.argv[2].split(',')]
    n = bad = 0; nonarrow = 0
    for line in open(sys.argv[3]):
        mask, edges = line.rstrip('\n').split('\t')
        mask = int(mask); n += 1
        E = [tuple(map(int, t.split('-'))) for t in edges.split()]
        if mask < 0: continue
        nonarrow += 1
        R = {}; B = {}
        for v in {x for e in E for x in e}: R[v] = set(); B[v] = set()
        for i, (a, b) in enumerate(E):
            D = R if mask >> i & 1 else B
            D[a].add(b); D[b].add(a)
        if contains(R, F1) or contains(B, F2):
            bad += 1; print('BAD WITNESS', line, end='')
    print(f'graphs {n} witnesses {nonarrow} bad {bad}')
