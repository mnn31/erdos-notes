#!/usr/bin/env python3
"""KK-free cross-check with OR-tools CP-SAT: decide whether there is an r-multiplicity antichain
on [n] with >= n-4 distinct sizes.  (Independent of Kruskal-Katona and of the recurrence.)

Model: x_S (S in F), u_S ("S is contained in some member of F"), y_i (level i used).
  u_S >= x_S;  u_S >= u_T for every T = S + one element;   x_S + u_T <= 1 for such T
  (so no member of F is properly contained in a set contained in a member: antichain);
  sum_{|S|=i} x_S >= r*y_i;  sum_i y_i >= n-4.
Every r-multiplicity antichain with >= n-4 sizes gives a solution (u_S = [S below some member]),
and every solution's x is such an antichain.  So INFEASIBLE <=> g(n,r) <= n-5.

Usage: python3 -I code/cpsat_cross.py r n [timelimit_s] [workers]
"""
import sys
from ortools.sat.python import cp_model


def main():
    r, n = int(sys.argv[1]), int(sys.argv[2])
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600.0
    m = cp_model.CpModel()
    N = 1 << n
    x = [m.NewBoolVar(f"x{S}") for S in range(N)]
    u = [m.NewBoolVar(f"u{S}") for S in range(N)]
    y = [m.NewBoolVar(f"y{i}") for i in range(n + 1)]
    for S in range(N):
        m.AddImplication(x[S], u[S])
        for e in range(n):
            if not (S >> e) & 1:
                T = S | (1 << e)
                m.AddImplication(u[T], u[S])
                m.AddBoolOr([x[S].Not(), u[T].Not()])
    lev = [[] for _ in range(n + 1)]
    for S in range(N):
        lev[bin(S).count("1")].append(x[S])
    for i in range(n + 1):
        m.Add(sum(lev[i]) >= r * y[i])
    m.Add(sum(y) >= n - 4)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    st = s.Solve(m)
    name = s.StatusName(st)
    extra = ""
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        F = [S for S in range(N) if s.Value(x[S])]
        # direct verification of the found family
        sizes = {}
        for S in F:
            sizes.setdefault(bin(S).count("1"), []).append(S)
        ac = all(not ((A & B) == A) for A in F for B in F if A != B)
        good = [k for k, v in sizes.items() if len(v) >= r]
        extra = f" family_antichain={ac} levels_with>=r={sorted(good)}"
    print(f"r={r} n={n} status={name} wall={s.WallTime():.1f}s{extra}", flush=True)


if __name__ == "__main__":
    main()
