#!/usr/bin/env python3
"""Build the Lemma 7 (padding) + Lemma 8 (core-to-full) antichains explicitly from the stored base
core of each r, for n = 2r+6, ..., 2r+6+EXTRA-1, and print them as W-blocks (k = n-3) for
`code/check w`.  This is a sanity test of the proofs of Lemmas 7-8 on many instances; the
theorem's tail (n >= 2r+6, all n) rests on the lemmas, not on this test.

Usage: python3 -I code/tail_demo.py OUTDIR RMIN RMAX EXTRA > FILE
"""
import sys, os


def read_core(path):
    lines = open(path).read().split("\n")
    for k, l in enumerate(lines):
        if l.startswith("K "):
            q, r, s, cnt, nf = map(int, l.split()[1:6])
            core = [int(x, 16) for x in lines[k + 1:k + 1 + cnt]]
            free = [int(x, 16) for x in lines[k + 1 + cnt:k + 1 + cnt + nf]]
            return q, r, s, core, free
    raise SystemExit("no core")


def pc(x):
    return bin(x).count("1")


def main():
    outdir, rmin, rmax, extra = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    for r in range(rmin, rmax + 1):
        q, r_, s, core, free = read_core(os.path.join(outdir, "witnesses", f"wit_r{r}.txt"))
        assert r_ == r and q == r + 5 and s == r + 2 and len(free) == r
        for n in range(2 * r + 6, 2 * r + 6 + extra):
            t = (n - (2 * r + 6)) // 2
            # Lemma 7: pad by 2t points x_j = q+2(j-1), y_j = q+2(j-1)+1
            C = list(core)
            X = 0
            for j in range(1, t + 1):
                xj, yj = q + 2 * (j - 1), q + 2 * (j - 1) + 1
                for G in free:
                    C.append(G | X | (1 << xj) | (1 << yj))
                X |= 1 << xj
            qq = q + 2 * t
            h = n // 2
            assert qq <= n - 1 - r
            a = qq
            P = [qq + 1 + j for j in range(r)]
            Lam = [(1 << a) | (1 << p) for p in P]
            for ell in range(2, h):
                mem = [E for E in C if pc(E) == ell]
                assert len(mem) >= r, (r, n, ell, len(mem))
                Lam += [E | (1 << a) for E in mem[:r]]
            full = (1 << n) - 1
            F = Lam + [full ^ L for L in Lam]
            print(f"W {n} {r} {n - 3} {len(F)} tail-demo t={t}")
            for S in F:
                print(f"{S:x}")


if __name__ == "__main__":
    main()
