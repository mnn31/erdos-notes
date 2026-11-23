"""Case-split version. G non-bipartite => G has a shortest odd cycle C, length L.
C is induced; we relabel so C = 0-1-...-(L-1)-0. Case L: fix C, forbid every odd
cycle of length < L (C3,C5 by clauses; odd closed walks of length 7..L-2 by a
walk-reachability encoding). Remaining vertices L..N-1 ordered by degree (sound:
relabelling outside C). Also every vertex degree >= dmin (sound, see RESULT.md).
Feasible(N,t) <=> some case L in {7,9,...,N} (for og7) is feasible.
For kind 'tri' the cases are L in {5,7,...}.
"""
import sys, itertools, json
from ortools.sat.python import cp_model
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bsat import cycles, D_brute

def feasible_case(N, t, L, short, dmin=0, tlimit=None, seed=0, b2=None):
    m = cp_model.CpModel()
    x = {}
    for i in range(N):
        for j in range(i+1, N):
            x[(i, j)] = m.NewBoolVar(f"x{i}_{j}")
    E = lambda a, b: x[(min(a, b), max(a, b))]
    # fixed induced cycle
    for i in range(L):
        for j in range(i+1, L):
            m.Add(x[(i, j)] == (1 if (j - i == 1 or (i == 0 and j == L-1)) else 0))
    for l in short:            # explicit clauses for C3 (and C5)
        if N >= l:
            for cyc in cycles(N, l):
                m.AddBoolOr([x[e].Not() for e in cyc])
    # forbid odd closed walks of length k, max(short)+2 <= k <= L-2
    kmax = L - 2
    kmin = max(short) + 2
    if kmax >= kmin:
        w = {(u, v): E(u, v) for u in range(N) for v in range(N) if u != v}
        for k in range(2, kmax + 1):
            nw = {}
            for u in range(N):
                for v in range(N):
                    b = m.NewBoolVar("")
                    for z in range(N):
                        if z != v and (u, z) in w:
                            # w(u,z) & x(z,v) -> b
                            m.AddBoolOr([w[(u, z)].Not(), E(z, v).Not(), b])
                    nw[(u, v)] = b
            w = nw
            if k % 2 == 1 and k >= kmin:
                for u in range(N):
                    m.Add(w[(u, u)] == 0)
    deg = [sum(E(i, j) for j in range(N) if j != i) for i in range(N)]
    for i in range(N):
        if dmin > 0:
            m.Add(deg[i] >= dmin)
    for i in range(L, N-1):
        m.Add(deg[i] >= deg[i+1])
    if b2 is not None and t - b2 > 0:
        # D(G) <= b(N-2) + floor(d_i/2) + floor(d_j/2)   (any pair i,j)
        # D(G) <= b(N-2) + floor((d_i+d_j-2)/2)          (adjacent i,j)
        r = t - b2
        h = [m.NewIntVar(0, N, f"h{i}") for i in range(N)]
        for i in range(N):
            m.Add(2*h[i] <= deg[i]); m.Add(deg[i] <= 2*h[i] + 1)
        for i in range(N):
            for j in range(i+1, N):
                m.Add(h[i] + h[j] >= r)
                m.Add(deg[i] + deg[j] >= 2*r + 2).OnlyEnforceIf(E(i, j))
    pairs = list(x.keys())
    for mask in range(1 << (N-1)):
        side = [0] + [(mask >> (k-1)) & 1 for k in range(1, N)]
        m.Add(sum(x[(i, j)] for (i, j) in pairs if side[i] == side[j]) >= t)
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    s.parameters.random_seed = seed
    if tlimit:
        s.parameters.max_time_in_seconds = tlimit
    st = s.Solve(m)
    G = [e for e in pairs if s.Value(x[e])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return s.StatusName(st), G, s.WallTime()

if __name__ == "__main__":
    kind, N, t, L, dmin = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    tl = float(sys.argv[6]) if len(sys.argv) > 6 else None
    short = [3] if kind == 'tri' else [3, 5]
    st, G, wt = feasible_case(N, t, L, short, dmin, tl)
    rec = dict(kind=kind, N=N, t=t, L=L, dmin=dmin, status=st, wall=round(wt, 2), graph=G)
    if G is not None:
        rec['D_check'] = D_brute(N, G)
    print(json.dumps(rec), flush=True)
