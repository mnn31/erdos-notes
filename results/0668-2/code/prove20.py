"""Erdos 668, exact count of congruence classes of realisations of an AMP25 extremal graph.

Usage:  python3 -I prove20.py <graph6> <outprefix>

Steps (all exact, Fractions only):
 A. decode graph6; list triangles; rhombus equations from every 4-cycle.
 B. DFS over triangle orientation signs (both signs at every triangle, no mirror reduction).
    Prune a prefix when the linear system forces p_u = p_v; record a certificate vector c with
    sum c_i row_i = e_u - e_v, re-verified by direct multiplication.  Check prefix-freeness and
    Kraft sum = 1.
 C. For every leaf: kernel basis (verified), certificate that rank >= n-3 (RREF rows re-derived
    as explicit combinations of the original rows), reduction to one unknown z on |z| = 1 and
    real-linear equations in (X, W) = (Re z, sqrt3 Im z); solve exactly.
 D. Build every candidate in Q(sqrt-3, sqrt D); verify edges = 1, injectivity, non-edges != 1.
 E. Congruence classes: exhaustive backtracking for distance-preserving bijections; multiset
    of squared distances as an invariant.
"""
import sys
import json
import itertools
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from fields import QW, QS, F, RealQ, ZERO, ONE, W, WBAR, squarefree_split


# ---------------------------------------------------------------- A. graph
def decode_g6(code):
    data = [ord(ch) - 63 for ch in code]
    assert all(0 <= x < 64 for x in data)
    assert data[0] < 63
    n = data[0]
    bits = []
    for x in data[1:]:
        for k in range(5, -1, -1):
            bits.append((x >> k) & 1)
    edges = []
    idx = 0
    for j in range(1, n):          # graph6: upper triangle, column by column
        for i in range(j):
            if bits[idx]:
                edges.append((i, j))
            idx += 1
    assert all(b == 0 for b in bits[idx:])
    return n, edges


def structures(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    tris = [t for t in itertools.combinations(range(n), 3)
            if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    rh = []      # (x, y, b, d): 4-cycle x-b-y-d-x, equation p_x + p_y - p_b - p_d = 0
    for x, y in itertools.combinations(range(n), 2):
        cn = sorted(adj[x] & adj[y])
        for b, d in itertools.combinations(cn, 2):
            rh.append((x, y, b, d))
    return adj, tris, rh


def rhombus_row(n, x, y, b, d):
    r = [ZERO] * n
    r[x] = r[x] + ONE
    r[y] = r[y] + ONE
    r[b] = r[b] - ONE
    r[d] = r[d] - ONE
    return r


def triangle_row(n, t, s):
    a, b, c = t
    ws = W if s == 1 else WBAR
    r = [ZERO] * n
    # p_c - p_a - w^s (p_b - p_a) = 0
    r[c] = r[c] + ONE
    r[b] = r[b] - ws
    r[a] = r[a] - ONE + ws
    return r


# ---------------------------------------------------------------- linear algebra over QW
class RREF:
    def __init__(self, n):
        self.n = n
        self.piv = {}   # col -> row (list), row[col] == 1, zero in other pivot cols

    def copy(self):
        o = RREF(self.n)
        o.piv = {k: list(v) for k, v in self.piv.items()}
        return o

    def reduce(self, v):
        v = list(v)
        for c, row in self.piv.items():
            if not v[c].iszero():
                f = v[c]
                v = [v[i] - f * row[i] for i in range(self.n)]
        return v

    def add(self, v):
        v = self.reduce(v)
        nz = [i for i in range(self.n) if not v[i].iszero()]
        if not nz:
            return False
        c = nz[0]
        inv = v[c].inv()
        v = [x * inv for x in v]
        for c2 in list(self.piv):
            row = self.piv[c2]
            if not row[c].iszero():
                f = row[c]
                self.piv[c2] = [row[i] - f * v[i] for i in range(self.n)]
        self.piv[c] = v
        return True

    def in_span(self, v):
        return all(x.iszero() for x in self.reduce(v))

    def coincidence(self):
        n = self.n
        for a, b in itertools.combinations(range(n), 2):
            e = [ZERO] * n
            e[a] = ONE
            e[b] = -ONE
            if self.in_span(e):
                return (a, b)
        return None


def solve_combination(rows, target):
    """Find c with sum_i c_i rows[i] == target (over QW); None if impossible.
    Independent of class RREF: plain Gauss-Jordan on the transposed augmented system."""
    m = len(rows)
    n = len(target)
    # equations: for each column j: sum_i c_i rows[i][j] = target[j]
    A = [[rows[i][j] for i in range(m)] + [target[j]] for j in range(n)]
    pivcols = []
    r = 0
    for col in range(m):
        p = None
        for k in range(r, n):
            if not A[k][col].iszero():
                p = k
                break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = A[r][col].inv()
        A[r] = [x * inv for x in A[r]]
        for k in range(n):
            if k != r and not A[k][col].iszero():
                f = A[k][col]
                A[k] = [A[k][i] - f * A[r][i] for i in range(m + 1)]
        pivcols.append(col)
        r += 1
        if r == n:
            break
    for k in range(r, n):
        if not A[k][m].iszero():
            return None
    c = [ZERO] * m
    for k, col in enumerate(pivcols):
        c[col] = A[k][m]
    return c


def check_combination(rows, c, target):
    n = len(target)
    acc = [ZERO] * n
    for ci, row in zip(c, rows):
        if ci.iszero():
            continue
        for j in range(n):
            acc[j] = acc[j] + ci * row[j]
    return all(acc[j] == target[j] for j in range(n))


# ---------------------------------------------------------------- B. DFS
def dfs(n, tris, base_rows):
    R0 = RREF(n)
    for r in base_rows:
        R0.add(r)
    pruned = []   # (prefix, (u, v))
    leaves = []   # (prefix, RREF)
    nodes = [0]

    def rec(R, prefix):
        nodes[0] += 1
        co = R.coincidence()
        if co is not None:
            pruned.append((tuple(prefix), co))
            return
        k = len(prefix)
        if k == len(tris):
            leaves.append((tuple(prefix), R))
            return
        for s in (1, -1):
            R2 = R.copy()
            R2.add(triangle_row(n, tris[k], s))
            rec(R2, prefix + [s])

    rec(R0, [])
    return R0, pruned, leaves, nodes[0]


def rows_for(n, tris, base_rows, prefix):
    return list(base_rows) + [triangle_row(n, tris[k], s) for k, s in enumerate(prefix)]


# ---------------------------------------------------------------- C. leaf analysis
def leaf_kernel(n, R):
    free = [c for c in range(n) if c not in R.piv]
    # kernel vector determined by values on free columns: p_piv = - sum_f row[f] p_f
    K = [[ZERO] * len(free) for _ in range(n)]
    for j, f in enumerate(free):
        K[f][j] = ONE
    for c, row in R.piv.items():
        for j, f in enumerate(free):
            K[c][j] = -row[f]
    return free, K


def mat_vec_zero(rows, vec):
    for row in rows:
        acc = ZERO
        for a, b in zip(row, vec):
            if not a.iszero() and not b.iszero():
                acc = acc + a * b
        if not acc.iszero():
            return False
    return True


def solve2(l1, l2, target):
    """target (vector in QW^k) = alpha*l1 + beta*l2 ; exact, verified; None if no solution."""
    k = len(l1)
    # find 2x2 nonsingular minor
    for i, j in itertools.combinations(range(k), 2):
        det = l1[i] * l2[j] - l1[j] * l2[i]
        if not det.iszero():
            alpha = (target[i] * l2[j] - target[j] * l2[i]) / det
            beta = (l1[i] * target[j] - l1[j] * target[i]) / det
            ok = all((alpha * l1[t] + beta * l2[t]) == target[t] for t in range(k))
            return (alpha, beta) if ok else None
    raise ValueError("l1, l2 dependent")


def analyse_leaf(n, edges, tris, base_rows, prefix, R, log):
    rows = rows_for(n, tris, base_rows, prefix)
    free, K = leaf_kernel(n, R)
    d = len(free)
    info = {"prefix": "".join("+" if s == 1 else "-" for s in prefix), "dim": d, "free": free}
    # (i) basis vectors are in the kernel
    for j in range(d):
        assert mat_vec_zero(rows, [K[x][j] for x in range(n)]), "basis vector not in kernel"
    # (ii) rank certificate: every RREF row is an explicit combination of the original rows
    for c, rrow in R.piv.items():
        assert rrow[c] == ONE and all(rrow[c2].iszero() for c2 in R.piv if c2 != c)
        cc = solve_combination(rows, rrow)
        assert cc is not None and check_combination(rows, cc, rrow), "rank certificate failed"
    info["rank"] = len(R.piv)
    if d == 2:
        # kernel = constants + C k ; p = c + lam k.  Normalise p_{f0} = 0 and edge e0 vector = 1:
        # every realisation in this leaf is a rotation+translation of q = (k - k_{f0}) / (k_b0 - k_a0).
        for x in range(n):
            assert (K[x][0] + K[x][1]) == ONE
        kvec = [K[x][1] for x in range(n)]
        a0, b0 = edges[0]
        den = kvec[b0] - kvec[a0]
        assert not den.iszero()
        f0 = free[0]
        q = [(kvec[x] - kvec[f0]) / den for x in range(n)]
        Dk = 2
        pts = [F.from_qw(v, Dk) for v in q]
        info["status"] = "dim 2: one candidate up to rotation/translation"
        log(f"  leaf {info['prefix']}: rank {info['rank']}, kernel dim 2 -> 1 candidate")
        return info, [{"leaf": info["prefix"], "z": ("dim2",), "pts": pts, "D": Dk}]
    if d != 3:
        info["status"] = f"kernel dim {d} != 3: not handled by this solver"
        log(f"  leaf {info['prefix']}: kernel dim {d} (not handled)")
        return info, []
    # constants in kernel: K . (1,1,1) == all ones
    for x in range(n):
        assert (K[x][0] + K[x][1] + K[x][2]) == ONE
    # edge functionals on t-space (C^3)
    lf = {}
    for (a, b) in edges:
        lf[(a, b)] = [K[b][j] - K[a][j] for j in range(3)]
    e1 = edges[0]
    e2 = None
    for e in edges[1:]:
        l1, l2 = lf[e1], lf[e]
        if any(not (l1[i] * l2[j] - l1[j] * l2[i]).iszero() for i, j in itertools.combinations(range(3), 2)):
            e2 = e
            break
    assert e2 is not None
    l1, l2 = lf[e1], lf[e2]
    # every functional vanishing on constants is a combination of l1, l2
    coef = {}
    for e in edges:
        ab = solve2(l1, l2, lf[e])
        assert ab is not None
        coef[e] = ab
    pos = {}
    f0 = free[0]
    for x in range(n):
        tx = [K[x][j] - K[f0][j] for j in range(3)]
        ab = solve2(l1, l2, tx)
        assert ab is not None
        pos[x] = ab   # p_x - p_{f0} = gamma l1(p) + delta l2(p)
    # normalise: p_{f0} = 0, l1(p) = 1, l2(p) = z, |z| = 1.
    # edge e: |alpha + beta z|^2 = 1  <=>  N(a)+N(b) + 2 Re(conj(a) b z) = 1
    # with c = conj(a) b = c1 + c2 w, z = X + iY, W = sqrt3 Y:
    #   (2 c1 + c2) X - c2 W = 1 - N(a) - N(b)
    lin = []
    for e in edges:
        a, b = coef[e]
        c = a.conj() * b
        lin.append((2 * c.a + c.b, -c.b, 1 - a.norm() - b.norm()))
    info["e1"], info["e2"] = e1, e2
    # distinct nontrivial equations (up to rational scaling)
    eqs = []
    for A, B, C in lin:
        if A == 0 and B == 0:
            if C != 0:
                info["status"] = "inconsistent constant equation"
                log(f"  leaf {info['prefix']}: constant equation 0 = {C}: no realisation")
                return info, []
            continue
        # normalise
        lead = A if A != 0 else B
        t = (A / lead, B / lead, C / lead)
        if t not in eqs:
            eqs.append(t)
    info["equations"] = [f"{A}*X + {B}*W = {C}" for A, B, C in eqs]
    sols = []   # list of (x0, x1, w0, w1, D): X = x0 + x1 sqrt D, W = w0 + w1 sqrt D
    if not eqs:
        info["status"] = "no nontrivial equation: continuum (flexible)"
        log(f"  leaf {info['prefix']}: FLEXIBLE (no equation on z)")
        return info, []
    A, B, C = eqs[0]
    if len(eqs) >= 2:
        # rank 2 or inconsistent: solve first two independent equations, check the rest
        found = None
        for (A2, B2, C2) in eqs[1:]:
            det = A * B2 - A2 * B
            if det != 0:
                found = ((C * B2 - C2 * B) / det, (A * C2 - A2 * C) / det)
                break
        if found is None:
            info["status"] = "parallel inconsistent equations"
            log(f"  leaf {info['prefix']}: parallel inconsistent equations: none")
            return info, []
        X, Wv = found
        if all(A_ * X + B_ * Wv == C_ for A_, B_, C_ in eqs) and X * X + Wv * Wv / 3 == 1:
            sols.append((X, Fr(0), Wv, Fr(0), 1))
    else:
        if B != 0:
            # W = (C - A X)/B ; (3B^2 + A^2) X^2 - 2AC X + C^2 - 3B^2 = 0
            den = 3 * B * B + A * A
            E = 3 * (3 * B * B + A * A - C * C)
            if E < 0:
                pass
            elif E == 0:
                X = A * C / den
                sols.append((X, Fr(0), (C - A * X) / B, Fr(0), 1))
            else:
                q, D = squarefree_split(E)
                for sg in (1, -1):
                    # X = (AC + sg*B*sqrt(E))/den, sqrt(E) = q sqrt(D)
                    x0, x1 = A * C / den, sg * B * q / den
                    w0, w1 = (C - A * x0) / B, (-A * x1) / B
                    if D == 1:
                        sols.append((x0 + x1, Fr(0), w0 + w1, Fr(0), 1))
                    else:
                        sols.append((x0, x1, w0, w1, D))
        else:
            X = C / A
            E = 3 * (1 - X * X)
            if E == 0:
                sols.append((X, Fr(0), Fr(0), Fr(0), 1))
            elif E > 0:
                q, D = squarefree_split(E)
                for sg in (1, -1):
                    if D == 1:
                        sols.append((X, Fr(0), sg * q, Fr(0), 1))
                    else:
                        sols.append((X, Fr(0), Fr(0), sg * q, D))
    info["status"] = f"{len(sols)} solution(s) for z"
    cands = []
    for (x0, x1, w0, w1, D) in sols:
        Dk = D if D != 1 else 2  # D = 1 means purely rational; use any field, r-part stays 0
        # z = X + i W/sqrt3 = X + W s/3
        z = F(QS(x0, w0 / 3), QS(x1, w1 / 3), Dk)
        pts = []
        for x in range(n):
            g, dl = pos[x]
            pts.append(F.from_qw(g, Dk) + F.from_qw(dl, Dk) * z)
        cands.append({"leaf": info["prefix"], "z": (x0, x1, w0, w1, D), "pts": pts, "D": Dk})
    log(f"  leaf {info['prefix']}: rank {info['rank']}, e1={e1}, e2={e2}, equations {info['equations']}, "
        f"{len(sols)} z-solution(s)")
    return info, cands


# ---------------------------------------------------------------- D. verification
def verify_candidate(n, edges, cand):
    pts = cand["pts"]
    eset = set(edges)
    d2 = {}
    for a, b in itertools.combinations(range(n), 2):
        d2[(a, b)] = (pts[a] - pts[b]).abs2()
    one = RealQ(1, 0, cand["D"])
    zero = RealQ(0, 0, cand["D"])
    edges_unit = all(d2[e] == one for e in edges)
    injective = all(d2[p].sign() > 0 for p in d2)
    nonedge_not_unit = all(not (d2[p] == one) for p in d2 if p not in eset)
    unit_count = sum(1 for p in d2 if d2[p] == one)
    # exact max / min
    keys = list(d2)
    mx = keys[0]
    mn = keys[0]
    for p in keys[1:]:
        if (d2[p] - d2[mx]).sign() > 0:
            mx = p
        if (d2[p] - d2[mn]).sign() < 0:
            mn = p
    cand["d2"] = d2
    return {"edges_unit": edges_unit, "injective": injective, "nonedge_not_unit": nonedge_not_unit,
            "unit_count": unit_count, "diam2": repr(d2[mx]), "minsep2": repr(d2[mn]),
            "diam2_float": float(d2[mx]), "minsep2_float": float(d2[mn])}


# ---------------------------------------------------------------- E. congruence
def dist_key(cand, a, b):
    if a == b:
        return (Fr(0), Fr(0), 0)
    if a > b:
        a, b = b, a
    return cand["d2"][(a, b)].key()


def find_bijection(n, P, Q):
    """Exhaustive search for a bijection pi with d_P(x,y) = d_Q(pi x, pi y) for all x, y."""
    profP = [sorted(dist_key(P, x, y) for y in range(n)) for x in range(n)]
    profQ = [sorted(dist_key(Q, x, y) for y in range(n)) for x in range(n)]
    pi = [None] * n
    used = [False] * n

    def rec(x):
        if x == n:
            return True
        for y in range(n):
            if used[y] or profP[x] != profQ[y]:
                continue
            if all(dist_key(P, x, x2) == dist_key(Q, y, pi[x2]) for x2 in range(x)):
                pi[x] = y
                used[y] = True
                if rec(x + 1):
                    return True
                used[y] = False
                pi[x] = None
        return False

    return list(pi) if rec(0) else None


def main():
    code, outprefix = sys.argv[1], sys.argv[2]
    lines = []

    def log(s):
        print(s)
        lines.append(s)

    n, edges = decode_g6(code)
    adj, tris, rh = structures(n, edges)
    log(f"graph6 {code}: n={n}, |E|={len(edges)}, triangles={len(tris)}, rhombus equations={len(rh)} "
        f"(4-cycles={len(rh)//2})")
    log(f"degree sequence: {sorted(len(a) for a in adj)}")
    base_rows = [rhombus_row(n, *q) for q in rh]
    R0, pruned, leaves, nodes = dfs(n, tris, base_rows)
    log(f"rank of rhombus system: {len(R0.piv)}; DFS nodes {nodes}; pruned {len(pruned)}; leaves {len(leaves)}")
    # completeness: prefix-free + Kraft sum 1
    words = [p for p, _ in pruned] + [p for p, _ in leaves]
    kraft = sum(Fr(1, 2 ** len(w)) for w in words)
    prefix_free = all(not (len(u) <= len(v) and v[:len(u)] == u)
                      for u, v in itertools.permutations(words, 2))
    log(f"prefix-free: {prefix_free}; Kraft sum: {kraft}")
    assert prefix_free and kraft == 1
    # pruning certificates
    ok = 0
    for prefix, (u, v) in pruned:
        rows = rows_for(n, tris, base_rows, prefix)
        tgt = [ZERO] * n
        tgt[u] = ONE
        tgt[v] = -ONE
        c = solve_combination(rows, tgt)
        assert c is not None and check_combination(rows, c, tgt), f"cert failed {prefix}"
        ok += 1
    log(f"pruning certificates verified: {ok}/{len(pruned)}")
    cands = []
    leafinfo = []
    for prefix, R in leaves:
        info, cs = analyse_leaf(n, edges, tris, base_rows, prefix, R, log)
        leafinfo.append(info)
        cands.extend(cs)
    log(f"candidates: {len(cands)}")
    results = []
    for i, c in enumerate(cands):
        r = verify_candidate(n, edges, c)
        results.append(r)
        log(f"  cand {i} (leaf {c['leaf']}, z={tuple(str(t) for t in c['z'])}): {r}")
    good = [i for i, r in enumerate(results) if r["edges_unit"] and r["injective"]]
    log(f"genuine realisations: {len(good)} of {len(cands)}")
    # congruence classes
    classes = []
    for i in good:
        placed = False
        for cl in classes:
            pi = find_bijection(n, cands[cl[0]], cands[i])
            if pi is not None:
                cl.append(i)
                log(f"  cand {i} ~ cand {cl[0]} via pi = {pi}")
                placed = True
                break
        if not placed:
            classes.append([i])
    log(f"congruence classes: {len(classes)}: {classes}")
    # multiset invariant
    for cl in classes:
        c = cands[cl[0]]
        ms = sorted(dist_key(c, a, b) for a, b in itertools.combinations(range(n), 2))
        c["ms"] = ms
    for a, b in itertools.combinations(range(len(classes)), 2):
        same = cands[classes[a][0]]["ms"] == cands[classes[b][0]]["ms"]
        log(f"  classes {a},{b}: squared-distance multisets equal? {same}")
    for k, cl in enumerate(classes):
        r = results[cl[0]]
        log(f"  class {k}: rep cand {cl[0]}, diam^2 = {r['diam2']} ({r['diam2_float']:.12f}), "
            f"minsep^2 = {r['minsep2']} ({r['minsep2_float']:.12f}), unit pairs {r['unit_count']}")
    with open(outprefix + ".txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    out = {"graph6": code, "n": n, "edges": edges, "triangles": tris,
           "pruned": [["".join("+" if s == 1 else "-" for s in p), list(co)] for p, co in pruned],
           "leaves": leafinfo,
           "candidates": [{"leaf": c["leaf"], "z": [str(t) for t in c["z"]],
                           "points_40digits": [[str(v) for v in p.to_mp(40)] for p in c["pts"]],
                           "points_exact": [[str(p.P.a), str(p.P.b), str(p.Q.a), str(p.Q.b), c["D"]] for p in c["pts"]],
                           "verify": results[i]} for i, c in enumerate(cands)],
           "classes": classes}
    with open(outprefix + ".json", "w") as f:
        json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()
