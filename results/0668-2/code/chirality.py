"""Orientation-preserving count: list all distance-preserving self-bijections of each class
representative and the exact sign of their orientation (via a fixed triangle).
Usage: python3 -I chirality.py <graph6>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fields import RealQ
import prove20 as P

def orient(c, a, b, d):
    x = (c["pts"][b] - c["pts"][a]) * (c["pts"][d] - c["pts"][a]).conj()
    return RealQ(x.P.b, x.Q.b, c["D"]).sign()   # sign of Im x / sqrt3

def all_bij(n, A, B):
    profA = [sorted(P.dist_key(A, x, y) for y in range(n)) for x in range(n)]
    profB = [sorted(P.dist_key(B, x, y) for y in range(n)) for x in range(n)]
    out, pi, used = [], [None]*n, [False]*n
    def rec(x):
        if x == n:
            out.append(list(pi)); return
        for y in range(n):
            if not used[y] and profA[x] == profB[y] and all(P.dist_key(A, x, x2) == P.dist_key(B, y, pi[x2]) for x2 in range(x)):
                pi[x] = y; used[y] = True; rec(x+1); used[y] = False
    rec(0); return out

code = sys.argv[1]
n, edges = P.decode_g6(code)
adj, tris, rh = P.structures(n, edges)
base = [P.rhombus_row(n, *q) for q in rh]
R0, pruned, leaves, nodes = P.dfs(n, tris, base)
info, cs = P.analyse_leaf(n, edges, tris, base, leaves[0][0], leaves[0][1], lambda s: None)
for c in cs: P.verify_candidate(n, edges, c)
a, b, d = tris[0]
for k, c in enumerate(cs):
    bij = all_bij(n, c, c)
    o0 = orient(c, a, b, d)
    signs = [orient(c, pi[a], pi[b], pi[d]) * o0 for pi in bij]
    print(f"leaf-1 candidate {k}: {len(bij)} distance-preserving self-bijections; orientation signs {signs}")
