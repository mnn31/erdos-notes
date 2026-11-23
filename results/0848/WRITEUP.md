# Erdős 848, distinct-pairs variant: exact values of D(N) for N <= 30000

D(N) = max |A|, A ⊆ {1..N}, with ab+1 non-squarefree for all **distinct** a, b ∈ A
(the a = b condition is dropped; this is the question Dogmachine asked on the forum, 9 Mar 2026).
c(N) = floor((N+18)/25) = |{n <= N : n ≡ 7 mod 25}|. C7 / C18 are the classes 7 and 18 mod 25.

## Computed results (exact, two implementations agree where both ran)
1. **D(N) = c(N) for every 157 <= N <= 30000.** **D(N) > c(N) for every N <= 156.**
   (PLAN.md guessed 181 as the last N with D > c. That was wrong: D = 7 on [127,181], and c reaches 7 at N = 157.)
2. Values for N <= 156, from record N to record N: D = 1 (N=1..2), 2 (3..7), 3 (8..22), 4 (23..52), 5 (53..106),
   6 (107..126), 7 (127..181). Then D = c(N), with records at 182, 207, 232, ... (N ≡ 7 mod 25).
   The record witnesses are in out/r20k_records.txt. Examples: N=23 {1,7,17,23}; N=53 {19,33,35,46,53} (StijnC's set);
   N=107 {27,65,85,87,101,107}; N=127 {27,53,61,87,107,109,127}.
   The largest excess is D - c = 3, at N = 23..31 and 53..56.
3. **Are the maximum sets only the classes?** For N >= 182, every maximum set is C7∩[1,N] (or C18∩[1,N] when that class
   is equally large), except in two windows:
   - N = 157..181: D = 7 = c, but the non-class set {27,53,61,87,107,109,127} is also maximum.
   - N = 197..206: D = 8 = c, but the non-class set **{1,7,17,95,97,131,151,197}** is also maximum
     (prime-square witnesses for its pairs: 4, 9, 25, 49 and 23²).
   - Everywhere else in [182, 30000], up to the C7/C18 tie, the maximum set is unique: the only N where a non-class
     clique of size c(N) has largest element N is N = 197. ("Non-class" here means not contained in C7 and not contained in C18.)
4. Sanity check on the original diagonal problem: the same code with the a² + 1 condition put back gives D(N) = c(N)
   at every N <= 10000. This agrees with the published claims (Pitchford, Li, and the forum search).

## Method (code/d848.c)
- Graph on {1..N}, with an edge a~b iff p² | ab+1 for some prime p. Edges are built exactly: b ≡ -a⁻¹ (mod p²), computed in int64.
  200,000 random pairs were spot-checked against trial division on each run.
- Phase 1 (N <= 181): sequential exact search. D(N) = D(N-1)+1 iff nbhd(N)∩[1,N-1] contains a clique of size D(N-1).
  The test is a BBMC/Tomita branch-and-bound with greedy-colouring bounds. Every record witness is re-checked by trial division.
- Phase 2 (182 <= N <= 30000, in parallel across N, which is valid by induction because ω grows by at most 1 per vertex):
  for each N ≢ 7 (mod 25), the search refutes a clique of size c(N) in nbhd(N). No refutation failed, so D(N) <= c(N), and C7 gives D(N) >= c(N).
  Mixed test: for each N, is there a clique of size c(N) with largest element N that is neither ⊆ C7 nor ⊆ C18?
  When N is in C7 or C18, the search branches over the first element outside N's class.
- Runs: out/r20k_* (N <= 20000, 140 s CPU), out/r30k_* (20001..30000, 656 s CPU). No phase-2 test was left unfinished.

## Independent cross-checks
- code/verify.py (Python, squarefree sieve + Bron–Kerbosch, written separately) recomputes D(N) for N <= 800.
  Its records match exactly, and it finds D = c on [182,800]. It also re-checks all 33 witness sets by trial division (out/verify_800.txt).
- code/verify_mixed.py (Python, pure trial division + BK) runs the mixed test for 182 <= N <= 800 and finds only N = 197 (out/verify_mixed_800.txt).
- The earlier networkx probe (distinct_800.txt) has the same record N and D values.

## Status vs the public record (checked 2026-11-22)
- Read: the forum thread text (refs/f848.txt) and the Plasma wiki E0848 pages (out/refs/plasma_*). Neither mentions the distinct variant
  beyond Dogmachine's question, Sothanaphan's limsup <= 1 - 49/(6π²) ≈ 0.17254, and StijnC's remark with {19,33,35,46,53}.
  No file for problem 848 was found in ryantuck/erdos-ai. I did not search arXiv or OEIS myself; PLAN.md reports an OEIS search with no hit.
- So, as far as checked, the exact table and the threshold N = 156 have not been published.

## Caveats
- This is finite evidence up to N = 30000, not a proof for all N. Nothing here improves the 0.17254 bound.
- The phase-2 refutations rely on the C search code being correct. The independent Python check only covers N <= 800.
  Above 800 there is a second check only on the diagonal variant up to 10000, which matches published values. The search writes no
  refutation certificates.
