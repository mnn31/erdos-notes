# Probe: is there a C10-free graph on n vertices with min degree >=7 and >= 6n-5 edges?
# Lazy CEGAR: SAT model w/o cycle constraints; forbid each found 10-cycle; repeat.
import sys, time, itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

def find_c10s(n, adj, maxc=400):
    # adj: list of sets. return list of cycles (tuples of vertices), one per edge where possible
    cycles = []
    seen_edges = set()
    edges = [(u,v) for u in range(n) for v in adj[u] if u < v]
    for (u,v) in edges:
        if (u,v) in seen_edges: continue
        # path from v to u of length 9 not using edge uv directly, simple
        path = [u, v]; used = {u, v}
        found = None
        def dfs(x, depth):
            nonlocal found
            if found: return
            if depth == 9:
                if u in adj[x]: found = list(path)
                return
            for y in adj[x]:
                if y in used: continue
                used.add(y); path.append(y)
                dfs(y, depth+1)
                path.pop(); used.discard(y)
                if found: return
        dfs(v, 1)
        if found:
            cyc = found
            cycles.append(tuple(cyc))
            for i in range(10):
                a, b = cyc[i], cyc[(i+1)%10]
                seen_edges.add((min(a,b), max(a,b)))
            if len(cycles) >= maxc: break
    return cycles

def run(n, emin, dmin=7, solver='cadical195', tlimit=1e9):
    pool = IDPool()
    X = {}
    for i in range(n):
        for j in range(i+1, n):
            X[(i,j)] = pool.id(('x', i, j))
    def x(i,j): return X[(min(i,j), max(i,j))]
    S = Solver(name=solver)
    allv = list(X.values())
    cnf = CardEnc.atleast(lits=allv, bound=emin, vpool=pool, encoding=EncType.seqcounter if len(allv)<200 else EncType.totalizer)
    S.append_formula(cnf.clauses)
    for i in range(n):
        lits = [x(i,j) for j in range(n) if j != i]
        c = CardEnc.atleast(lits=lits, bound=dmin, vpool=pool, encoding=EncType.seqcounter)
        S.append_formula(c.clauses)
    it = 0; ncl = 0; t0 = time.time()
    while True:
        it += 1
        ok = S.solve()
        if not ok:
            print(f'n={n} emin={emin}: UNSAT after {it} iters, {ncl} cycle clauses, {time.time()-t0:.1f}s', flush=True)
            return False
        m = set(l for l in S.get_model() if l > 0)
        adj = [set() for _ in range(n)]
        for (i,j), v in X.items():
            if v in m: adj[i].add(j); adj[j].add(i)
        cyc = find_c10s(n, adj)
        if not cyc:
            print(f'n={n}: FOUND C10-free graph with {sum(len(a) for a in adj)//2} edges', flush=True)
            return adj
        for c in cyc:
            S.add_clause([-x(c[k], c[(k+1)%10]) for k in range(10)])
            ncl += 1
        if it % 50 == 0:
            print(f'  it {it} clauses {ncl} t={time.time()-t0:.1f}', flush=True)
        if time.time()-t0 > tlimit:
            print('timeout'); return None

if __name__ == '__main__':
    n = int(sys.argv[1]); emin = int(sys.argv[2]) if len(sys.argv) > 2 else 6*n-5
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    run(n, emin, tlimit=tl)
