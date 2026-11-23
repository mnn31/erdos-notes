"""Independent second encoding (cross-check of cegar.py).

Differences from cegar.py, on purpose:
  * odd cycles of length < g are forbidden by EXPLICIT enumeration of every
    cycle of length 3, 5, ..., g-2 in K_N (one clause per cycle), no walk variables;
  * by default NO symmetry breaking (only the shortest odd cycle is placed on 0..g-1);
    optional 'sym' adds lex symmetry breaking encoded by brute-force forbidden pairs;
  * cardinality constraints use the totalizer encoding instead of the sequential counter;
  * D2 is computed with plain-Python bit operations instead of numpy;
  * default solver glucose4.

Usage: python3 -I cegar2.py N G0 T g [solver] [sym]
  'sym' (6th arg) adds brute-force lex symmetry breaking on the outside vertices.
  runs the single case "shortest odd cycle has length g" and prints SAT/UNSAT.
"""
import sys
sys.path.append('~/.local/lib/python3.11/site-packages')
import itertools, json, time
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def cycles(N, L):
    """All cycles of length L in K_N, each once, as vertex tuples.
    Canonical form: smallest vertex first, second vertex < last vertex."""
    out = []
    for S in itertools.combinations(range(N), L):
        m = S[0]
        for perm in itertools.permutations(S[1:]):
            if perm[0] < perm[-1]:
                out.append((m,) + perm)
    return out


def d2_python(N, edge_list):
    best = None
    for mask in range(1 << (N - 1)):
        side = mask << 1  # vertex 0 on side 0
        c = 0
        for (u, v) in edge_list:
            if ((side >> u) & 1) == ((side >> v) & 1):
                c += 1
        if best is None or c < best:
            best = c
    return best


def main():
    N, G0, T, g = map(int, sys.argv[1:5])
    solver_name = sys.argv[5] if len(sys.argv) > 5 else 'glucose4'
    pool = IDPool()
    pairs = [(u, v) for u in range(N) for v in range(u + 1, N)]
    var = {p: pool.id(p) for p in pairs}

    def e(u, v):
        return var[(min(u, v), max(u, v))]
    cls = []
    for L in range(3, g - 1, 2):
        for cyc in cycles(N, L):
            cls.append([-e(cyc[i], cyc[(i + 1) % L]) for i in range(L)])
    for i in range(g):
        cls.append([e(i, (i + 1) % g)])
    if len(sys.argv) > 6 and sys.argv[6] == 'sym':
        # optional symmetry breaking, encoded by brute force: for consecutive outside
        # vertices i, i+1 forbid every pair of 0/1 vectors (a, b) on the cycle with a >lex b
        vecs = list(itertools.product((0, 1), repeat=g))
        for i in range(g, N - 1):
            for a in vecs:
                for b in vecs:
                    if a > b:
                        cls.append([(-e(i, j) if a[j] else e(i, j)) for j in range(g)] +
                                   [(-e(i + 1, j) if b[j] else e(i + 1, j)) for j in range(g)])
    s = Solver(name=solver_name, bootstrap_with=cls)
    masks = list(range(1 << (N - 1)))
    t0 = time.time(); it = 0; ncut = 0
    while True:
        it += 1
        if not s.solve():
            print(json.dumps(dict(N=N, G0=G0, T=T, g=g, result='UNSAT', iterations=it,
                                  cuts=ncut, base_clauses=len(cls), seconds=round(time.time()-t0, 1))))
            return
        pos = set(l for l in s.get_model() if l > 0)
        el = [p for p in pairs if var[p] in pos]
        # find all bipartitions with fewer than T uncut edges (up to 30, smallest first)
        found = []
        for mask in masks:
            side = mask << 1
            c = sum(1 for (u, v) in el if ((side >> u) & 1) == ((side >> v) & 1))
            if c < T:
                found.append((c, side))
        if not found:
            print(json.dumps(dict(N=N, G0=G0, T=T, g=g, result='SAT', edges=el,
                                  D2=d2_python(N, el))))
            return
        found.sort()
        for c, side in found[:30]:
            lits = [var[(u, v)] for (u, v) in pairs if ((side >> u) & 1) == ((side >> v) & 1)]
            enc = CardEnc.atleast(lits=lits, bound=T, vpool=pool, encoding=EncType.totalizer)
            for cl in enc.clauses:
                s.add_clause(cl)
            ncut += 1


if __name__ == '__main__':
    main()
