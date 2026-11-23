# Erdős #137: anchor search result (2026-11-22)

## Result (VERIFIED by running)
For every k in {3, 4, 5, 6, 7, 10, 11}: no n >= 1 with n + k - 1 <= 10^19 makes
n(n+1)...(n+k-1) powerful.

Run: `code/anchor137 1e19 11 0 out/run1e19`. 469 s wall on 11 processes. Totals are in `out/run1e19/summary.txt`.
- 2,537,872,835 odd powerful anchors T <= 1e19 were enumerated. The count predicted by 0.80*sqrt(X) is 2.53e9.
- Candidate windows that survived the sieve and got an exact check: k3 184.8M, k4 38.0M, k5 7.67M, k6 2.95M,
  k7 610k, k10 18.7k, k11 3.2k.
- Windows where every term's k-rough part is powerful: only n=1 for k=4, 6, 10 (1·2·...·k with k+1 prime).
  The product of each of those fails at prime 2, 3 or 5. hits = 0. errs = 0 (internal consistency counter).
- Self-check: the run found exactly 33 consecutive powerful pairs, which is exactly the A060355 b-file
  entries whose odd member is <= 1e19. No extras and none missing.

## Method (code/anchor137.c, C, -O2, __int128)
Fix k in the set. Jacobsthal values j(2)=2, j(6)=4, j(30)=6, j(210)=10 mean every length-k window contains a
term T coprime to all primes < k. Primes >= k divide at most one term of the window, so T is powerful and
every other term has no prime >= k to the first power. Enumerate T = a^2 b^3 (b squarefree, a and b odd).
For each b, sieve over a the neighbours N = b^3 a^2 + d (|d| <= 10) by every odd prime p <= Y with
Y^5 > X+10 (Y = 6310 here). The roots of b^3 a^2 = -d mod p come from Tonelli-Shanks. They are Hensel-lifted
to p^2 so that p^2 | N is recorded and never killed. Large b uses direct residues instead. Surviving windows
get an exact check: strip 2, 3, 5, 7 and the recorded p^2 primes. The Y-rough cofactor c < Y^5 is powerful
iff c is 1, a square or a cube (any powerful c with all primes > Y and fewer than 5 prime factors counted
with multiplicity is p^2, p^3, p^4 or p^2 q^2). Then the exponents of primes < k are summed over the window.
Every window with n + k - 1 <= X has its anchor <= X, so it is covered.

## Validation (VERIFIED)
- The sieve flags (kill class by p = 3 / 5 / 7 / >=11, and the p^2 flag) for 141,240 (anchor, d) pairs at
  X = 1e10 match independent trial division (`code/check_s.py`): 0 mismatches. They include 9,740 p^2 flags.
  The root-sieve path and the direct-residue path give byte-identical flags.
- Brute force (`code/brute_rp.py`, `code/brute_nm.py`, independent spf sieve in Python) agrees with C's
  rough-powerful window list to 3e6 and with a looser near-miss list to 2e6.
- The pair lists match the A060355 b-file exactly at 1e10 (14), 1e16 (26) and 1e19 (33).

## What is and is not new (INFERRED / caveats)
- k=3: this run is unconditional but reaches only 1e19. The b-file reduction (`code/k3_from_pairs.py`) already
  gives 1e22 for k=3, but that is conditional on the b-file being complete. The 7.38e28 figure for #364 is
  unverified and covers only the odd-n case.
- k in {4..7, 10, 11} to 1e19: I found no recorded search range on the problem page, the forum, Plasma E0137
  or OEIS (see PLAN.md). I did NOT check Shorey-Tijdeman (2016 survey), de Weger-van de Woestijne (1999) or
  general literature on k=4 (n(n+1)(n+2)(n+3) = m^2 - 1). Do not call this new before checking those.
- k = 8, 9 and k >= 12 are not covered (they have no anchor lemma).
- This is a finite check. It says nothing about the conjecture itself.
- Planned target 1e22 not reached: measured cost was ~0.15 CPU-s per 1e6 anchors (sieve-dominated), so 1e22
  (8e10 anchors) would be ~3-4 h on this machine. 1e20-1e21 is feasible in ~20-60 min.
