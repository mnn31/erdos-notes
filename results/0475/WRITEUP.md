# Erdős 475 (Graham rearrangement, ADMS Conj. 1.2): small-modulus exhaustive check

Run 2026-11-22, Apple M3 Pro, 11 threads. Code: `code/g475.c` (C, -O2, pthreads), `code/brute.py`
(independent brute force), `code/resolve_n30.py`. Raw outputs: `out/`.

## Statement checked
Mode 0 (Erdős 475 / Graham / ADMS Conjecture 1.2): for A ⊆ Z_n \ {0}, |A| = t, there is an
ordering whose partial sums s_1..s_t (s_0 NOT included) are pairwise distinct.
Mode 1 (Alspach, side variant): A with sum(A) ≠ 0; s_0 = 0, s_1, ..., s_t pairwise distinct.

## Result (VERIFIED by this computation)
No counterexample. Every set listed below has an ordering with distinct partial sums.

| n | sizes t | λ-orbits solved | subsets covered | time |
|---|---|---|---|---|
| every n with 2 ≤ n ≤ 32 (prime and composite) | all 1..n-1 | 2^(n-1)-1 total, e.g. n=29: 9,587,579; n=31: 35,792,567; n=32: 134,755,007 | all 2^(n-1)-1 | ≤ 33 s each |
| 37 | all 1..36 (in chunks, files `out/p37_*_m0.txt`) | 1,908,881,899 (= Burnside count) | all 2^36-1 = 68,719,476,735 | ≈ 23 min total |

Open-range content for primes (beyond what is recorded publicly):
- p = 29, t = 13..25: 6,847,424 orbits = 191,717,781 subsets, all OK.
- p = 31, t = 13..27: 29,321,201 orbits = 879,611,731 subsets, all OK.
- p = 37, t = 21..33: 386,579,662 orbits = 13,916,801,341 subsets, all OK.
- p = 37, t = 13..20: 1,460,028,724 orbits, all OK (so p = 37 does not rely on the preprint).
- p = 37, all t: 1,908,881,899 orbits = 68,719,476,735 subsets, all OK.

Combined with the recorded n ≤ 25 (ADMS16, as quoted in HOS19 p.2), the computation gives:
Graham's conjecture holds for every prime p ≤ 37 by direct computation over all t (no reliance
on 2603.20961 or on the small-t/large-t theorems). Also all cyclic Z_n, n ≤ 32, satisfy ADMS
Conj. 1.2. n = 33..36 were not run. p = 41 (2^40 subsets) was not attempted.

Alspach side variant (mode 1): all non-zero-sum A ⊆ Z_n \ {0}, 2 ≤ n ≤ 31, all t: OK.
One set hit the DFS node budget (2e9) instead of being solved: n = 30, A = Z_30 \ {0}, t = 29.
That case is the statement "Z_30 is sequenceable", settled by Gordon's construction; the explicit
ordering 1, 28, 3, 26, ... was checked by `code/resolve_n30.py` (`out/resolve_n30.txt`).
It is not a counterexample.

## How correctness is ensured
- Orbit reduction: A ↦ λA, λ ∈ Z_n^*. Only the numerically least bitmask of each orbit is solved.
  Completeness check per t: Σ over canonical A of φ(n)/|Stab(A)| = C(n-1,t) exactly (column
  `complete` in every output). Total orbit counts for p = 29, 31 match Burnside
  ((1/(p-1)) Σ_{d|p-1} φ(d) 2^{(p-1)/d} − 1 = 9,587,579, 35,792,567 and 1,908,881,899 for p = 37).
- Every ordering found is re-checked by a separate O(t) routine using plain integer arithmetic
  (permutation of A, mod-n sums, distinctness). Column `verified` = column `canon_orbits` everywhere.
- Cross-check vs independent Python brute force (all subsets, all permutations, n ≤ 10):
  orbit counts per t identical; zero failures in modes 0 and 1 (`out/brute_small.txt`).
- Negative control (mode 3 = Alspach without skipping zero-sum sets, which are impossible since
  s_t = 0 = s_0): for n ≤ 10 the solver reported exactly the zero-sum orbits as EXHAUSTED and
  nothing else, matching brute-force orbit counts. So the search does detect failures.
- Solver: randomized greedy over a bitset of free sums (≤ 2000 restarts), then exhaustive DFS.
  In mode 0 every set in every run was solved by the greedy stage (dfs_nodes = 0); max restarts
  used = 1603 (p = 37, t = 34..36); `out/hard_m0.txt` is empty.
- Not stored: the ~2e9 individual certificates (too large); they are regenerated and checked
  in-run. Rerun: `cc -O2 -o g475 g475.c -lpthread; ./g475 n tmin tmax mode threads hardfile`.

## Literature status (what was read vs inferred)
- READ: HOS19 (arXiv 1809.02684) p.2 says ADMS verified Conj. 1.2 by computer for n ≤ 25;
  2603.20961 p.3 says p ≤ 25 already solved, and its Thm 1.4 covers |A| ≤ 20; CoPe20 (2003.05939)
  item (5): cyclic G with |G| ≤ 25. Plasma E0475 _index.md: p_0 unspecified, no small-prime
  computation found.
- arXiv phrase search (2026-11-22, `refs/arxiv_dps.xml`) found two further papers, read at
  ABSTRACT level only: Pham–Sauermann 2602.15797 (all sufficiently large p; no explicit p_0 in
  abstract) and Costa–Della Fiore–Feng–Liu 2608.10015 (composite moduli, sufficiently large primes).
  Neither abstract mentions a small-modulus computation. Full texts NOT read.
- NOT accessed: ADMS16 itself, CMPP18, CDFOR22, the zenodo code 10.5281/zenodo.18997904,
  Ollis' sequenceability survey. A larger computation (n > 25) could exist there; this run
  should not be called new until those are checked.

## Honest scope
This is a finite verification for small moduli. It does not touch the open part of Erdős 475
in general: the gap is the unstated p_0 of the large-p chain. Closing it would need an explicit
p_0 from the asymptotic papers, which is likely astronomically larger than 37.
