"""Exact check of the closed form P_eps = R4 + rho_eps * T5 (eps = +-1), with
R4 = {0, 1, w, conj w}, T5 = {-1, 0, 1, w, w^2}, rho_eps = conj(w) * (-5 + eps*i*sqrt11)/6,
and of its congruence to the classes found by prove20.py.
Usage: python3 -I explicit.py <graph6 of G20>   (re-runs prove20 internals; ~30 s)
"""
import sys
import os
import itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from fields import QW, QS, F, RealQ, ZERO, ONE, W, WBAR
import prove20 as P

D = 33


def fqw(q):
    return F.from_qw(q, D)


def main():
    code = sys.argv[1]
    R4 = [ZERO, ONE, W, WBAR]
    T5 = [QW(-1, 0), ZERO, ONE, W, W * W]
    # i*sqrt(11) = sqrt(-3)*sqrt(33)/3  -> F(P=0, Q=s/3)
    isq11 = F(QS(0, 0), QS(0, Fr(1, 3)), D)
    sets = {}
    for eps in (1, -1):
        e = F(QS(Fr(-5, 6), 0), QS(0, 0), D) + (isq11 * F(QS(Fr(eps, 6), 0), QS(0, 0), D))
        rho = fqw(WBAR) * e
        assert rho.abs2() == RealQ(1, 0, D)
        pts = [fqw(a) + rho * fqw(b) for a in R4 for b in T5]
        d2 = {(i, j): (pts[i] - pts[j]).abs2() for i, j in itertools.combinations(range(20), 2)}
        distinct = all(v.sign() > 0 for v in d2.values())
        units = sum(1 for v in d2.values() if v == RealQ(1, 0, D))
        print(f"eps={eps:+d}: 20 distinct points: {distinct}; unit pairs: {units}")
        sets[eps] = {"pts": pts, "d2": d2, "D": D}
    # compare with classes of prove20
    n, edges = P.decode_g6(code)
    adj, tris, rh = P.structures(n, edges)
    base = [P.rhombus_row(n, *q) for q in rh]
    R0, pruned, leaves, nodes = P.dfs(n, tris, base)
    reps = []
    for prefix, R in leaves[:1]:
        info, cs = P.analyse_leaf(n, edges, tris, base, prefix, R, lambda s: None)
        for c in cs:
            P.verify_candidate(n, edges, c)
            reps.append(c)
    for eps, S in sets.items():
        for k, c in enumerate(reps):
            pi = P.find_bijection(n, S, c)
            print(f"  R4 + rho_{eps:+d} T5  vs  leaf-1 candidate {k}: distance-preserving bijection "
                  f"{'found' if pi else 'none'}")


if __name__ == "__main__":
    main()
