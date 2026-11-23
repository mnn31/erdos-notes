"""CEGAR SAT search for graphs on N vertices with odd girth >= G0 and D2 >= T.

D2(G) = min over bipartitions (A, V\\A) of the number of edges with both ends on
the same side (= min number of edges whose deletion leaves G bipartite).

Usage:  python3 -I cegar.py N G0 T [solver] [dumpdir]
  N   number of vertices
  G0  required odd girth lower bound (5 = triangle-free, 7 = no C3, no C5)
  T   target: search for a graph with D2 >= T
Output: for every odd g in [G0, N] (g = length of a shortest odd cycle), either
  SAT with a witness graph (whose D2 is recomputed exactly), or UNSAT.
If every case is UNSAT, no graph on N vertices with odd girth >= G0 has D2 >= T.
"""
import sys
sys.path.append('~/.local/lib/python3.11/site-packages')
import itertools, json, os, time
import numpy as np
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def all_sides(N):
    # rows: bipartitions with vertex 0 on side 0; entry = side of vertex
    M = 1 << (N - 1)
    idx = np.arange(M, dtype=np.int64)
    S = np.zeros((M, N), dtype=np.int8)
    for v in range(1, N):
        S[:, v] = (idx >> (v - 1)) & 1
    return S


def exact_D2(N, edges):
    """Exact D2 by exhaustive enumeration over all 2^(N-1) bipartitions."""
    S = all_sides(N)
    if not edges:
        return 0
    u = np.array([a for a, b in edges]); v = np.array([b for a, b in edges])
    same = (S[:, u] == S[:, v])
    return int(same.sum(1).min())


def build_base(N, g, pool):
    """Clauses: cycle 0..g-1 present, no odd closed walk of length <= g-2,
    lex symmetry breaking on vertices g..N-1 (adjacency vectors to 0..g-1)."""
    E = {}
    for u in range(N):
        for v in range(u + 1, N):
            E[(u, v)] = pool.id(('e', u, v))

    def e(u, v):
        return E[(u, v)] if u < v else E[(v, u)]
    cls = []
    # walk variables: W[k][(u,v)] is forced true whenever a walk of length k u->v exists
    Wprev = {(u, v): e(u, v) for u in range(N) for v in range(N) if u != v}  # k = 1
    for k in range(2, g - 1):
        Wk = {(u, v): pool.id(('w', k, u, v)) for u in range(N) for v in range(N)}
        for (u, w), lit in Wprev.items():
            for v in range(N):
                if v != w:
                    cls.append([-lit, -e(w, v), Wk[(u, v)]])
        if k % 2 == 1:
            for u in range(N):
                cls.append([-Wk[(u, u)]])
        Wprev = Wk
    # fixed shortest odd cycle
    for i in range(g):
        cls.append([e(i, (i + 1) % g)])
    # lex symmetry breaking: vec(i) <=_lex vec(i+1) for i = g..N-2
    for i in range(g, N - 1):
        a = [e(i, j) for j in range(g)]
        b = [e(i + 1, j) for j in range(g)]
        eq_prev = None  # None means "true"
        for j in range(g):
            pre = [] if eq_prev is None else [-eq_prev]
            cls.append(pre + [-a[j], b[j]])          # prefix equal -> a_j <= b_j
            if j < g - 1:
                eq = pool.id(('lex', i, j))
                cls.append(pre + [a[j], b[j], eq])
                cls.append(pre + [-a[j], -b[j], eq])
                eq_prev = eq
    return E, cls


def run_case(N, g, T, solver_name='cadical153', dumpdir=None, batch=30):
    pool = IDPool()
    E, cls = build_base(N, g, pool)
    edges = sorted(E)
    eu = np.array([a for a, b in edges]); ev = np.array([b for a, b in edges])
    S = all_sides(N)
    same = (S[:, eu] == S[:, ev]).astype(np.int16)  # (2^(N-1), #pairs)
    s = Solver(name=solver_name, bootstrap_with=cls)
    allcls = list(cls)
    cuts = []
    it = 0
    t0 = time.time()
    while True:
        it += 1
        if not s.solve():
            res = ('UNSAT', None)
            break
        model = s.get_model()
        pos = set(l for l in model if l > 0)
        x = np.array([1 if E[p] in pos else 0 for p in edges], dtype=np.int16)
        unc = same @ x
        m = int(unc.min())
        if m >= T:
            res = ('SAT', [p for p in edges if E[p] in pos])
            break
        bad = np.where(unc < T)[0]
        bad = bad[np.argsort(unc[bad], kind='stable')][:batch]
        for r in bad:
            r = int(r)
            lits = [E[edges[j]] for j in np.nonzero(same[r])[0]]
            if len(lits) < T:
                new = [[]]
            else:
                enc = CardEnc.atleast(lits=lits, bound=T, vpool=pool, encoding=EncType.seqcounter)
                new = enc.clauses
            for c in new:
                s.add_clause(c)
            allcls.extend(new)
            cuts.append(r)
    s.delete()
    info = dict(N=N, g=g, T=T, result=res[0], iterations=it, cuts=len(cuts),
                seconds=round(time.time() - t0, 2))
    if dumpdir is not None:
        os.makedirs(dumpdir, exist_ok=True)
        nv = max(abs(l) for c in allcls for l in c) if allcls else 0
        with open(os.path.join(dumpdir, f'N{N}_g{g}_T{T}.cnf'), 'w') as f:
            f.write(f'c N={N} g={g} T={T}; edge var of pair (u,v) listed below\n')
            for p in edges:
                f.write(f'c e {p[0]} {p[1]} {E[p]}\n')
            f.write(f'p cnf {nv} {len(allcls)}\n')
            for c in allcls:
                f.write(' '.join(map(str, c)) + ' 0\n')
        with open(os.path.join(dumpdir, f'N{N}_g{g}_T{T}_cuts.json'), 'w') as f:
            json.dump(dict(info, cut_rows=cuts), f)
    return info, res[1]


def main():
    N, G0, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    solver_name = sys.argv[4] if len(sys.argv) > 4 else 'cadical153'
    dumpdir = sys.argv[5] if len(sys.argv) > 5 else None
    overall = 'UNSAT'
    for g in range(G0, N + 1, 2):
        info, wit = run_case(N, g, T, solver_name, dumpdir)
        if wit is not None:
            d2 = exact_D2(N, wit)
            info['witness_edges'] = wit
            info['witness_exact_D2'] = d2
            overall = 'SAT'
        print(json.dumps(info), flush=True)
        if wit is not None:
            break
    print(f'OVERALL N={N} G0={G0} T={T}: {overall}', flush=True)


if __name__ == '__main__':
    main()
