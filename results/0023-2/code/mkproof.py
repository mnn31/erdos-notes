"""Solve a DIMACS CNF with glucose4 and write its DRUP refutation.
Usage: python3 -I mkproof.py in.cnf out.drup"""
import sys
sys.path.append('~/.local/lib/python3.11/site-packages')
from pysat.formula import CNF
from pysat.solvers import Solver

f = CNF(from_file=sys.argv[1])
with Solver(name=(sys.argv[3] if len(sys.argv)>3 else 'glucose4'), bootstrap_with=f.clauses, with_proof=True) as s:
    r = s.solve()
    assert r is False, 'formula is satisfiable'
    pf = s.get_proof()
with open(sys.argv[2], 'w') as out:
    for line in pf:
        out.write(line.strip() + '\n')
print(sys.argv[1], 'UNSAT; proof lines:', len(pf))
