"""Re-solve a dumped DIMACS CNF from scratch with several different SAT solvers.
Usage: python3 -I resolve.py file.cnf [solver ...]"""
import sys
sys.path.append('~/.local/lib/python3.11/site-packages')
import time
from pysat.formula import CNF
from pysat.solvers import Solver

f = CNF(from_file=sys.argv[1])
names = sys.argv[2:] or ['glucose4', 'minisat22', 'maplechrono', 'cadical195']
for n in names:
    t = time.time()
    with Solver(name=n, bootstrap_with=f.clauses) as s:
        r = s.solve()
    print(f'{sys.argv[1].split("/")[-1]} vars={f.nv} clauses={len(f.clauses)} solver={n} '
          f'result={"SAT" if r else "UNSAT"} sec={time.time()-t:.1f}', flush=True)
