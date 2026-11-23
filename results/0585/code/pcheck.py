"""Independent checker (pure Python, no shared code with gen.c).
P(G): G has two edge-disjoint cycles with the same vertex set.
Method: enumerate every cycle of G explicitly, group cycles by vertex set,
and test every pair inside a group for edge-disjointness."""
from itertools import combinations
from collections import defaultdict

def g6_decode(s):
    s = s.strip()
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits.extend((v >> (5 - i)) & 1 for i in range(6))
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges

def all_cycles(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    cycles = []  # (vertex frozenset, edge frozenset)
    for s in range(n):
        # cycles whose minimum vertex is s
        stack = [(s, [s])]
        while stack:
            u, path = stack.pop()
            for w in adj[u]:
                if w == s and len(path) >= 3 and path[1] < path[-1]:
                    es = frozenset(frozenset((path[i], path[(i + 1) % len(path)])) for i in range(len(path)))
                    cycles.append((frozenset(path), es))
                elif w > s and w not in path:
                    stack.append((w, path + [w]))
    return cycles

def find_pair(n, edges):
    groups = defaultdict(list)
    for vs, es in all_cycles(n, edges):
        groups[vs].append(es)
    for vs, lst in groups.items():
        for a, b in combinations(lst, 2):
            if not (a & b):
                return vs, a, b
    return None

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        n, edges = g6_decode(line)
        p = find_pair(n, edges)
        print(line, "n=%d" % n, "e=%d" % len(edges), "ncycles=%d" % len(all_cycles(n, edges)),
              "HAS_PAIR" if p else "P-FREE")
