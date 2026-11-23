# Erdős #366 — computer search result (2026-11-22)

## Result (computed, exact integer arithmetic)
Examined every 3-full u with 1 < u <= 10^24 (460,160,082 of them) and decided exactly whether u-1 and
u+1 are 2-full.
- Main question (n 2-full, n+1 3-full): **no n with n+1 <= 10^24.**
- Reverse order (n 3-full, n+1 2-full): **exactly n = 8 and n = 12167 for n <= 10^24.**
- Weaker question (n, n+1 both 3-full): **none with n <= 10^24** (any such pair would appear in the
  reverse list; 9 = 3^2 and 12168 = 2^3·3^2·13^2 are not 3-full).
Output: out/run_1e24.txt (307 s wall, 993 s CPU, 11 threads, 1.7 GB). No counterexample.

## Method (code/s366.c)
u = B^4 C^5 t^3, B,C squarefree coprime. Per family (B,C) sieve f(t)=c t^3+d over t, d=±1, with all
primes p <= P = 63095, where (P+1)^5 > 10^24+1. p=2,3: exact residue classes mod p^2 + full stripping
at test time. Other p not dividing c: roots via per-prime discrete-log tables, unique Hensel lift to
p^2; t ≡ root (mod p) is rejected unless t ≡ lifted root (mod p^2), in which case p is recorded.
Survivor: strip 2,3 (reject on exponent 1) and recorded primes; the cofactor has all primes > P and
is < (P+1)^5, so it is 2-full iff it is 1, a square or a cube (exact integer isqrt/icbrt).

## Validation (all passed)
1. Per-position check vs an independent trial-division 2-full test, 16 shifts
   d in {±1,±2,±3,±4,±8,±9,±16,±27}, U=10^13, small chunk sizes: 1,449,881 decisions, 0 mismatches,
   39 positive hits (out/check_1e13_multid.txt).
2. Independent Python brute force (3-full numbers by DFS over prime powers, sympy.factorint), same
   16 shifts, U=10^11: identical hit set, 39 hits; 3-full count 18,588 agrees (out/*_1e11_multid.txt).
3. A060355 b-file (39 terms < 10^22, refs/b060355.txt): its only pairs with a 3-full member are
   n = 8 and 12167 (out/bfile_3full_members.txt); the sieve reproduces exactly these at 10^18, 10^20,
   10^22 and 10^24.
4. Mutation test: with the Hensel lift disabled the checker reports 24 mismatches (39 -> 15 hits),
   so the check does detect a broken sieve (out/mutant_nolift_1e12.txt).

## What this does and does not show
- VERIFIED (by this computation): the three statements above up to 10^24.
- Prior public bound: 10^22 via the uncertified A060355 b-file (coverage of #366 INFERRED, see PLAN.md).
  Rechecked 2026-11-22: problem page, forum thread and Plasma E0366 page record nothing beyond 10^22.
  So 10^24 is a x100 extension that is likely, but not certainly, new (INFERRED: absence of evidence).
- Not attempted: 10^25+ (est. ~15 min at 10^25 with 3.6 GB tables; 10^26 needs ~8.6 GB tables).
  Time cap reached. This is a finite check, not a resolution; heuristically no solutions are expected.
