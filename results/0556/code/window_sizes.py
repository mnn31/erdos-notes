# For a cycle C of length L that is a shortest cycle of length >= 11 in a C10-free graph,
# every cycle of the graph has length <= 9 or >= L.  A vertex x off C adjacent to v_i, v_j
# (cyclic distance d) lies on cycles of lengths d+2 and L-d+2.  This script lists, for each L,
# the allowed distances d (both lengths outside [10, L-1]) and the maximum number of
# C-neighbours an off-C vertex can have (exhaustive over subsets of Z_L containing 0).
import itertools
def allowed(L):
    bad = set(range(10, L))
    return [d for d in range(1, L//2+1) if (d+2) not in bad and (L-d+2) not in bad]
for L in range(11, 38):
    A = set(allowed(L))
    best = 1
    # exhaustive: subsets of {1..L-1} added to {0}; prune via clique search
    verts = [v for v in range(1, L) if min(v, L-v) in A]
    def ok(a, b): return min((a-b) % L, (b-a) % L) in A
    def rec(cur, cand):
        global best
        best = max(best, len(cur))
        for k, v in enumerate(cand):
            if len(cur) + len(cand) - k <= best: return
            rec(cur+[v], [w for w in cand[k+1:] if ok(v, w)])
    rec([0], verts)
    print(f"L={L:2d} allowed d={sorted(A)} max C-neighbours of an off-C vertex = {best}")
