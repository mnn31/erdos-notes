"""Exact-integer sanity checks for the counterexample to AcRi26 Question 16.9.

Construction (see WRITEUP.md):
  A_alpha = union_k [k^2, k^2 + m_k - 1],  m_k = ceil(alpha*(2k+1))
  N_1 = 1, N_{s+1} = (s+2)^3 N_s^2,  W_s = {n : N_s/(s+1) < n <= N_s},  B = union_s W_s
  M_s = (s+2)^2 N_s^2 = N_{s+1}/(s+2)
All arithmetic is with Python ints / Fractions (exact).
"""
from fractions import Fraction
from math import isqrt
import random, sys

def ceil_frac(x):
    return -((-x.numerator) // x.denominator)

def A_blocks(alpha, M):
    """blocks [lo, hi] of A_alpha with lo <= M"""
    out = []
    k = 1
    while k * k <= M:
        m = ceil_frac(alpha * (2 * k + 1))
        assert 1 <= m <= 2 * k + 1
        out.append((k * k, k * k + m - 1))
        k += 1
    return out

def N_seq(S):
    N = [None, 1]
    for s in range(1, S):
        N.append((s + 2) ** 3 * N[s] ** 2)
    return N

def W(N, s):
    return (N[s] // (s + 1) + 1, N[s])

def count_union(intervals, M):
    """exact |union of integer intervals cap [1,M]|"""
    iv = sorted((max(lo, 1), min(hi, M)) for lo, hi in intervals if lo <= M and hi >= 1)
    tot, cur_lo, cur_hi = 0, None, None
    for lo, hi in iv:
        if lo > hi:
            continue
        if cur_hi is None or lo > cur_hi + 1:
            if cur_hi is not None:
                tot += cur_hi - cur_lo + 1
            cur_lo, cur_hi = lo, hi
        else:
            cur_hi = max(cur_hi, hi)
    if cur_hi is not None:
        tot += cur_hi - cur_lo + 1
    return tot

def count_A(alpha, M):
    return count_union(A_blocks(alpha, M), M)

def count_AplusB(alpha, N, S_windows, M):
    """|(A + union_{t<=S_windows} W_t) cap [1,M]|, exact (sum of integer intervals is an interval)"""
    Ab = A_blocks(alpha, M)
    ivs = []
    for t in range(1, S_windows + 1):
        wl, wh = W(N, t)
        for lo, hi in Ab:
            ivs.append((lo + wl, hi + wh))
    return count_union(ivs, M)

def brute_check_small(alpha, N, s, M):
    """brute-force (A+B) cap [1,M] with ALL of B cap [1,M] (not only windows <= s)"""
    A = set()
    for lo, hi in A_blocks(alpha, M):
        A.update(range(lo, min(hi, M) + 1))
    Bset = set()
    t = 1
    while t < len(N) and N[t] // (t + 1) + 1 <= M:
        wl, wh = W(N, t)
        Bset.update(range(wl, min(wh, M) + 1))
        t += 1
    S = set()
    Al = sorted(A)
    for b in Bset:
        for a in Al:
            if a + b > M:
                break
            S.add(a + b)
    return len(S), len(A)

def lemma2_random_test(trials=300, seed=1):
    rng = random.Random(seed)
    for _ in range(trials):
        M = rng.randint(1, 400)
        L = rng.randint(0, 30)
        # random disjoint-or-not integer intervals
        ivs = []
        x = rng.randint(1, 5)
        while x <= M + 40:
            ln = rng.randint(0, 8)
            ivs.append((x, x + ln))
            x += ln + rng.randint(0, 10)
        A = set()
        for lo, hi in ivs:
            A.update(range(lo, hi + 1))
        thick = {a + i for a in A for i in range(L + 1)}
        lhs = sum(1 for v in thick if 1 <= v <= M)
        r = sum(1 for lo, hi in ivs if lo <= M)
        rhs = sum(1 for v in A if v <= M) + L * r
        assert lhs <= rhs, (M, L, ivs)
    return trials

def main():
    print("Lemma 2 random brute-force tests passed:", lemma2_random_test())
    S = 4
    N = N_seq(S + 1)
    for s in range(1, S + 1):
        print(f"N_{s} = {N[s]},  W_{s} = {W(N, s)}")
    # Lemma 3(c): B cap [1,M_s] subset [1,N_s]  <=>  min W_{s+1} > M_s and windows increasing
    for s in range(1, S):
        Ms = (s + 2) ** 2 * N[s] ** 2
        assert Ms * (s + 2) == N[s + 1]
        assert W(N, s + 1)[0] == Ms + 1, (s, W(N, s + 1), Ms)
        assert W(N, s + 1)[0] > N[s]
        print(f"s={s}: M_s={Ms}, min W_(s+1)={W(N, s+1)[0]} = M_s+1, |W_s|/N_s = {Fraction(W(N,s)[1]-W(N,s)[0]+1, N[s])}")
    for alpha in [Fraction(1, 2), Fraction(1, 3), Fraction(9, 10), Fraction(1, 100)]:
        print(f"\nalpha = {alpha}")
        for s in range(1, S):
            Ms = (s + 2) ** 2 * N[s] ** 2
            if Ms > 10 ** 12:
                break
            cA = count_A(alpha, Ms)
            cAB = count_AplusB(alpha, N, s, Ms)
            bound = cA + N[s] * isqrt(Ms)
            assert isqrt(Ms) ** 2 == Ms
            assert count_A(alpha, Ms - 1) <= cAB <= bound, (cA, cAB, bound)  # 1+A subset A+B
            line = (f"  s={s} M_s={Ms}: |A∩[M]|/M={float(Fraction(cA, Ms)):.6f}  "
                    f"|(A+B)∩[M]|/M={float(Fraction(cAB, Ms)):.6f}  bound/M={float(Fraction(bound, Ms)):.6f}")
            if Ms <= 20000:
                bAB, bA = brute_check_small(alpha, N, s, Ms)
                assert bAB == cAB and bA == cA, (bAB, cAB, bA, cA)
                line += "  [brute force with all of B agrees]"
            print(line)
    print("\nALL CHECKS PASSED")

if __name__ == "__main__":
    main()
