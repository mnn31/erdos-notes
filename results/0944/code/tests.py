"""Tests for WRITEUP.md (Erdos 944, f_4(n) -> infinity, conditional chain).

Run (from this directory):
    cc -O2 -o mu mu.c && python3 -I tests.py ../out

T1  K4, W6, Groetzsch are 4-critical (Lemma 4).
T2  The gluing construction of Lemma 2 on 4-critical / 4-vertex-critical
    pieces: order formula, and the glued graph is 4-vertex-critical.
T3  The robustness half of Lemma 2: mu(glue) >= min_i mu(G_i), on pieces with
    G_i - v_i 3-colourable but mu(G_i) up to 3.
T4  The arithmetic of Lemmas 5-6: gcd = 1 and every n >= N + (5N-3)(9N-5)
    lies in N + S(N), checked exactly for N = 2..80; also prints the exact
    largest gap.
T5  Iterated toy: starting from W6 as a "(4,0)-graph" (N = 6), build glued
    graphs of orders N + g for each generator g and check 4-vertex-criticality.
All randomness is seeded; all checks are exact.
"""
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MU = os.path.join(HERE, "mu")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)


def run_mu(jobs):
    """jobs: list of (mode, n, edges). Returns list of dicts."""
    inp = []
    for mode, n, E in jobs:
        inp.append(mode)
        inp.append(f"{n} {len(E)}")
        inp.extend(f"{u} {v}" for u, v in E)
    p = subprocess.run([MU], input="\n".join(inp) + "\n", capture_output=True, text=True, check=True)
    res = []
    for line in p.stdout.strip().splitlines():
        d = {}
        for tok in line.split():
            k, v = tok.split("=")
            d[k] = int(v)
        res.append(d)
    assert len(res) == len(jobs)
    return res


# ---------------------------------------------------------------- graphs
def norm(E):
    S = set()
    for u, v in E:
        assert u != v
        S.add((min(u, v), max(u, v)))
    return sorted(S)


def K4():
    return 4, norm([(i, j) for i in range(4) for j in range(i + 1, 4)])


def wheel(h):
    """Wheel of order h: hub 0 + cycle on 1..h-1 (4-critical iff h even)."""
    c = h - 1
    E = [(0, i) for i in range(1, h)] + [(1 + i, 1 + (i + 1) % c) for i in range(c)]
    return h, norm(E)


def groetzsch():
    """Mycielskian of C5: u_i (0..4), copies w_i (5..9), apex z (10)."""
    E = []
    for i in range(5):
        j = (i + 1) % 5
        E.append((i, j))
        E.append((5 + i, j))
        E.append((5 + j, i))
        E.append((5 + i, 10))
    return 11, norm(E)


def hajos(G1, G2, e1, e2):
    """Hajos join: delete e1=(x1,y1) from G1, e2=(x2,y2) from G2, identify x1~x2, add y1y2."""
    n1, E1 = G1
    n2, E2 = G2
    x1, y1 = e1
    x2, y2 = e2
    mp = {}
    k = n1
    for v in range(n2):
        if v == x2:
            mp[v] = x1
        else:
            mp[v] = k
            k += 1
    E = [e for e in E1 if e != tuple(sorted(e1))]
    E += [(mp[u], mp[v]) for (u, v) in E2 if (u, v) != tuple(sorted(e2))]
    E.append((y1, mp[y2]))
    return k, norm(E)


def apex_tripartite(mpart):
    """v=0 joined to everything of K_{m,m,m}; G - 0 is 3-colourable."""
    n = 1 + 3 * mpart
    part = lambda x: (x - 1) // mpart
    E = [(0, x) for x in range(1, n)]
    E += [(x, y) for x in range(1, n) for y in range(x + 1, n) if part(x) != part(y)]
    return n, norm(E)


def three_colouring(n, E, removed):
    """Some proper 3-colouring of G - removed (dict) by backtracking, or None."""
    A = [set() for _ in range(n)]
    for u, v in E:
        A[u].add(v)
        A[v].add(u)
    vs = [v for v in range(n) if v not in removed]
    vs.sort(key=lambda v: -len(A[v]))
    c = {}

    def bt(i):
        if i == len(vs):
            return True
        v = vs[i]
        cols = [0, 1, 2]
        random.shuffle(cols)
        for col in cols:
            if all(c.get(w) != col for w in A[v]):
                c[v] = col
                if bt(i + 1):
                    return True
                del c[v]
        return False

    return dict(c) if bt(0) else None


def glue(H, Gs, vs, cs, rng):
    """Skottova-Steiner Lemma 2.1 construction.
    H=(h,EH); Gs[i]=(n_i,E_i); vs[i] in V(G_i); cs[i] proper 3-col of G_i - v_i
    with colours {0,1,2}; 'colour 1' of the paper is colour 0 here.
    Returns (order, edges)."""
    h, EH = H
    assert len(Gs) == len(EH)
    edges = []
    nxt = h
    EH = list(EH)
    rng.shuffle(EH)  # arbitrary enumeration
    for i, ((u, w), (ni, Ei), vi, ci) in enumerate(zip(EH, Gs, vs, cs)):
        if rng.random() < 0.5:
            u, w = w, u  # arbitrary orientation of e_i
        mp = {}
        for x in range(ni):
            if x != vi:
                mp[x] = nxt
                nxt += 1
        Nv = set()
        for a, b in Ei:
            if a == vi:
                Nv.add(b)
            elif b == vi:
                Nv.add(a)
            else:
                edges.append((mp[a], mp[b]))
        for x in Nv:
            if ci[x] == 0:
                edges.append((u, mp[x]))  # A_i
            else:
                edges.append((w, mp[x]))  # B_i
    return nxt, norm(edges)


def main():
    rng = random.Random(944)
    random.seed(944)
    log = open(os.path.join(OUT, "tests.log"), "w")

    def say(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.write(s + "\n")
        log.flush()

    # ---------------- T0
    say("== T0: cross-check of the C solver against brute force over all 3^n maps (n <= 9)")
    import itertools
    jobs, bf = [], []
    for trial in range(300):
        n = rng.randrange(3, 10)
        pr = rng.choice([0.3, 0.5, 0.7, 0.9])
        E = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < pr]
        best = min(sum(c[u] == c[v] for u, v in E) for c in itertools.product(range(3), repeat=n))
        def c3(skipv=None, skipe=None):
            EE = [e for e in E if e != skipe and skipv not in e]
            vv = [x for x in range(n) if x != skipv]
            for cc in itertools.product(range(3), repeat=len(vv)):
                d = dict(zip(vv, cc))
                if all(d[u] != d[v] for u, v in EE):
                    return 1
            return 0
        bf.append((best, c3(), int(all(c3(skipv=v) for v in range(n))), int(all(c3(skipe=e) for e in E))))
        jobs.append(("ALL", n, E))
    res = run_mu(jobs)
    for r, b in zip(res, bf):
        assert (r["mu"], r["col3"], r["allVdel3col"], r["allEdel3col"]) == b, (r, b)
    say(f"  {len(jobs)} random graphs: mu, col3, vertex-deletion and edge-deletion colourability all agree")

    # ---------------- T1
    say("== T1: 4-criticality of K4, W6, Groetzsch (exhaustive)")
    named = {"K4": K4(), "W6": wheel(6), "W8": wheel(8), "Groetzsch": groetzsch(),
             "Hajos(W6,K4)": hajos(wheel(6), K4(), (0, 1), (0, 1))}
    res = run_mu([("CRIT", n, E) for (n, E) in named.values()])
    for (nm, (n, E)), r in zip(named.items(), res):
        ok = r["col3"] == 0 and r["allVdel3col"] == 1 and r["allEdel3col"] == 1
        say(f"  {nm:14s} h={n:2d} t={len(E):2d}  {r}  4-critical={ok}")
        assert ok
    # save the H graphs used in Lemma 4
    with open(os.path.join(OUT, "H_graphs.txt"), "w") as f:
        for nm in ["K4", "W6", "Groetzsch"]:
            n, E = named[nm]
            f.write(f"{nm} {n} {len(E)}\n" + " ".join(f"{u}-{v}" for u, v in E) + "\n")

    # ---------------- T2
    say("== T2: gluing preserves 4-vertex-criticality; order = h + sum(n_i - 1)")
    pieces = [named["K4"], named["W6"], named["W8"], named["Hajos(W6,K4)"]]
    Hs = [named["K4"], named["W6"]]
    jobs, meta = [], []
    for trial in range(60):
        H = rng.choice(Hs)
        t = len(H[1])
        Gs = [rng.choice(pieces) for _ in range(t)]
        if sum(g[0] - 1 for g in Gs) + H[0] > 64:
            continue
        vs = [rng.randrange(g[0]) for g in Gs]
        cs = [three_colouring(g[0], g[1], {v: 1}) for g, v in zip(Gs, vs)]
        N, E = glue(H, Gs, vs, cs, rng)
        assert N == H[0] + sum(g[0] - 1 for g in Gs)
        jobs.append(("VCRIT", N, E))
        meta.append((H[0], t, [g[0] for g in Gs]))
    res = run_mu(jobs)
    for mt, r in zip(meta, res):
        ok = r["col3"] == 0 and r["allVdel3col"] == 1
        assert ok, (mt, r)
    say(f"  {len(jobs)} glued graphs (orders {min(j[1] for j in jobs)}..{max(j[1] for j in jobs)}): all 4-vertex-critical")

    # ---------------- T3
    say("== T3: mu(glue) >= min_i mu(G_i)")
    base = {"K4": named["K4"], "W6": named["W6"], "A1": apex_tripartite(1),
            "A2": apex_tripartite(2), "A3": apex_tripartite(3)}
    bres = run_mu([("MU", n, E) for (n, E) in base.values()])
    bmu = {nm: r["mu"] for nm, r in zip(base, bres)}
    say("  base mu:", bmu)
    # each base piece must have G - v colourable for the chosen v: use v = 0 for apex graphs
    jobs, meta = [], []
    H = named["K4"]
    names = list(base)
    for trial in range(40):
        choice = [rng.choice(names) for _ in range(6)]
        Gs = [base[c] for c in choice]
        order = H[0] + sum(g[0] - 1 for g in Gs)
        if order > 40:
            continue
        vs = [0 if c.startswith("A") else rng.randrange(base[c][0]) for c in choice]
        cs = [three_colouring(g[0], g[1], {v: 1}) for g, v in zip(Gs, vs)]
        assert all(c is not None for c in cs)
        N, E = glue(H, Gs, vs, cs, rng)
        jobs.append(("MU", N, E))
        meta.append(choice)
    res = run_mu(jobs)
    for ch, r in zip(meta, res):
        lb = min(bmu[c] for c in ch)
        assert r["mu"] >= lb, (ch, r, lb)
        say(f"  pieces={','.join(ch):24s} n={r['n']:2d}  mu(glue)={r['mu']}  min mu(G_i)={lb}")
    say(f"  {len(jobs)} cases: inequality holds in all")
    say("  T3b: all pieces with mu >= 2 (the informative case)")
    jobs, meta = [], []
    for choice in (["A2"] * 6, ["A2", "A3", "A2", "A2", "A3", "A2"], ["A3", "A2"] * 3, ["A3"] * 6):
        Gs = [base[c] for c in choice]
        vs = [0] * 6
        cs = [three_colouring(g[0], g[1], {0: 1}) for g in Gs]
        N, E = glue(H, Gs, vs, cs, rng)
        jobs.append(("MU", N, E))
        meta.append(choice)
    res = run_mu(jobs)
    for ch, r in zip(meta, res):
        lb = min(bmu[c] for c in ch)
        assert r["mu"] >= lb, (ch, r, lb)
        say(f"  pieces={','.join(ch):24s} n={r['n']:2d}  mu(glue)={r['mu']}  min mu(G_i)={lb}")

    # ---------------- T4
    say("== T4: numerical semigroup S(a) = <3+5a, 5+9a, 10+19a>, a = N-1")
    worst_ratio = 0.0
    for N in range(2, 81):
        a = N - 1
        g = [3 + 5 * a, 5 + 9 * a, 10 + 19 * a]
        assert math.gcd(math.gcd(g[0], g[1]), g[2]) == 1
        B = (5 * N - 3) * (9 * N - 5)
        L = B + max(g) + 5
        rep = bytearray(L + 1)
        rep[0] = 1
        for x in range(1, L + 1):
            for gi in g:
                if x >= gi and rep[x - gi]:
                    rep[x] = 1
                    break
        assert all(rep[x] for x in range(B, L + 1)), N  # >= B all representable (window of length > max g suffices)
        frob = max(x for x in range(L + 1) if not rep[x])
        worst_ratio = max(worst_ratio, (frob + 1) / B)
        if N in (2, 3, 4, 5, 6, 7, 10, 48, 60, 80):
            say(f"  N={N:3d} gens={g} Frobenius={frob}  bound B=(5N-3)(9N-5)={B}")
    say(f"  N=2..80: gcd=1 and all integers >= B representable; max (Frob+1)/B = {worst_ratio:.3f}")

    # ---------------- T5
    say("== T5: iterated toy from W6 (N=6, a=5): orders N + g, g in generators")
    W6 = named["W6"]
    jobs, meta = [], []
    for Hn in ["K4", "W6", "Groetzsch"]:
        H = named[Hn]
        t = len(H[1])
        Gs = [W6] * t
        vs = [rng.randrange(6) for _ in range(t)]
        cs = [three_colouring(6, W6[1], {v: 1}) for v in vs]
        N, E = glue(H, Gs, vs, cs, rng)
        assert N == 6 + (H[0] - 1) + (t - 1) * 5
        if N <= 64:
            jobs.append(("VCRIT", N, E))
            meta.append((Hn, N))
        else:
            say(f"  H={Hn}: order {N} > 64, skipped (outside solver range)")
    res = run_mu(jobs)
    for mt, r in zip(meta, res):
        say(f"  H={mt[0]:9s} order {mt[1]} = 6 + generator; {r}")
        assert r["col3"] == 0 and r["allVdel3col"] == 1
    say("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
