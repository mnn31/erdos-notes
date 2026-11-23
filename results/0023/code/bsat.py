"""Exact b(N) = max over graphs G on N vertices (forbidden odd cycles) of
D(G) = |E| - maxcut(G), via CP-SAT feasibility of "D(G) >= t".

kind 'tri' : forbid C3            (should reproduce OEIS A389646)
kind 'og7' : forbid C3 and C5     (odd girth >= 7, Erdos [Er92b] k=3)

Model: x_ij boolean edges. For every bipartition (vertex 0 fixed on side A),
#edges inside the parts >= t  (all 2^(N-1) cuts, exact integer constraints).
Sound reductions used (each proved in RESULT.md):
  * degrees nonincreasing in vertex order (relabelling; symmetry breaking only)
  * if t > b(N-1): every vertex has degree >= 2(t - b(N-1)), since
    D(G) <= D(G-v) + floor(deg v / 2).
"""
import sys, itertools, time, json
from ortools.sat.python import cp_model

def cycles(N, L):
    """all L-cycles in K_N as tuples of edges (i<j)"""
    out = []
    for S in itertools.combinations(range(N), L):
        a = S[0]
        for perm in itertools.permutations(S[1:]):
            if perm[0] > perm[-1]:
                continue  # each cycle once (fix start a, orientation)
            seq = (a,) + perm
            out.append([tuple(sorted((seq[k], seq[(k+1) % L]))) for k in range(L)])
    return out

def feasible(N, t, kind, dmin=0, workers=1, tlimit=None, extra_lex=True):
    m = cp_model.CpModel()
    x = {}
    for i in range(N):
        for j in range(i+1, N):
            x[(i, j)] = m.NewBoolVar(f"x{i}_{j}")
    L = [3] if kind == 'tri' else [3, 5]
    for l in L:
        if N >= l:
            for cyc in cycles(N, l):
                m.AddBoolOr([x[e].Not() for e in cyc])
    deg = [sum(x[tuple(sorted((i, j)))] for j in range(N) if j != i) for i in range(N)]
    for i in range(N):
        if dmin > 0:
            m.Add(deg[i] >= dmin)
        if i + 1 < N:
            m.Add(deg[i] >= deg[i+1])
    pairs = list(x.keys())
    for mask in range(1 << (N-1)):
        side = [0] + [(mask >> (k-1)) & 1 for k in range(1, N)]
        same = [x[(i, j)] for (i, j) in pairs if side[i] == side[j]]
        m.Add(sum(same) >= t)
    s = cp_model.CpSolver()
    s.parameters.num_workers = workers
    if tlimit:
        s.parameters.max_time_in_seconds = tlimit
    st = s.Solve(m)
    G = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        G = [e for e in pairs if s.Value(x[e])]
    return s.StatusName(st), G, s.WallTime()

def D_brute(N, edges):
    best = None
    for mask in range(1 << (N-1)):
        side = [0] + [(mask >> (k-1)) & 1 for k in range(1, N)]
        c = sum(1 for (i, j) in edges if side[i] == side[j])
        best = c if best is None else min(best, c)
    return best

if __name__ == "__main__":
    kind = sys.argv[1]; Nmax = int(sys.argv[2]); N0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    bprev = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    tl = float(sys.argv[5]) if len(sys.argv) > 5 else None
    b = bprev
    for N in range(N0, Nmax+1):
        t = b + 1
        while True:
            dmin = 2*(t - b)  # b = b(N-1) still
            st, G, wt = feasible(N, t, kind, dmin=dmin, tlimit=tl)
            rec = dict(kind=kind, N=N, t=t, dmin=dmin, status=st, wall=round(wt, 2), graph=G)
            if G is not None:
                rec['D_check'] = D_brute(N, G)
            print(json.dumps(rec), flush=True)
            if st == 'FEASIBLE' or st == 'OPTIMAL':
                t += 1
                continue
            break
        if st != 'INFEASIBLE':
            print(json.dumps(dict(kind=kind, N=N, note="UNKNOWN (time limit) -- stop", lower=t-1)), flush=True)
            break
        bN = t - 1
        print(json.dumps(dict(kind=kind, N=N, b=bN)), flush=True)
        b = bN
