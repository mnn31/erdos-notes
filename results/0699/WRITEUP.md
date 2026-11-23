# Erdős 699, side question (Erdős–Szekeres "p > i" strengthening): family search beyond 64 bits

Run 2026-11-22, about 45 min wall clock, 11 cores, Python 3.11 + gmpy2 + sympy. Exact big-integer arithmetic throughout.

## Scope
- n = 2^k, i = 2, k = 63..300 (238 values), all j with 2 < j <= n/2.
- n = 3^m + 1, i = 3, m = 40..150 (111 values), all j with 3 < j <= n/2.
- Only these (n, i) pairs. Other i for these n were NOT checked.
- A near-miss means no prime p > i divides gcd(C(n,i), C(n,j)).

## Result
**Five new near-misses for n = 2^k, i = 2.** In each, 2^k − 1 = p·q with p and q prime, and the gcd is a pure power of 2, so p = i = 2 divides both binomials. None is a counterexample to the main question.

| k | j | 2^k − 1 | gcd(C(n,2), C(n,j)) |
|---|---|---|---|
| 67 | 23206563898901803639 | 193707721 · 761838257287 | 2^66 |
| 101 | 137177249633792241973877360183 | 7432339208719 · 341117531003194129 | 2^100 |
| 137 | 16141961986503368055107762054812561012816 | 32032215596496435569 · 5439042183600204290159 | 2^133 |
| 149 | 128187607486771957240347442690809417317798185 | 86656268566282183151 · 8235109336690846723986161 | 2^148 |
| 227 | 101300084359891653057791615262224317072042311693978602118916606877065 | 26986333437777017 · 7992177738205979626491506950867720953545660121688631 | 2^226 |

Each of these k has exactly one such j (the search enumerates all j <= n/2).
- **Other k in 63..300: none**, except k = 277 and k = 293, which are **undecided**. Their cofactors stayed unfactored: a c78 cofactor of 2^277 − 1 after removing 1121297, and all of 2^293 − 1 (c89, no factor found). With only partial factors the search could not narrow the candidates.
- **n = 3^m + 1, i = 3, m = 40..150: no near-miss.** All 111 values are decided. For m = 119, 131, 133, 146 and 149 a composite cofactor was left unfactored, but the known primes plus a necessary-condition test on that cofactor (see Method) already ruled out every candidate.

If these are counted as new terms of A399402, they would be 2^67, 2^101, 2^137, 2^149 and 2^227 (a(9) <= 2^41 remains). Terms between 10^12 and 2^62 are still excluded only for these families, not for all n.

## What is verified vs inferred
VERIFIED (computation, this run):
- Validation: the same code on k = 2..62 and m = 1..39 gives exactly k = 4, 9, 11, 41 with j = 6, 147, 713, 285920731515, and m = 2, 3, 5, 7, 13 with j = 5, 14, 122, 1094, 797162 (n/2). These match Cong Lu's list (forum) and Lee's README / OEIS A399402. `code/brute.py` uses exact math.comb gcds for k <= 13 and m <= 7 and agrees (out/brute_small.txt).
- Each hit was checked two more ways:
  - Legendre's formula, inside search.py, gives v_p(C(n,j)) = 0 for every odd p | 2^k − 1.
  - `code/verify_hits.py` is a separate script using Kummer carry counting. It checks that the factorization multiplies back to 2^k − 1; for k <= 101 the factors come from sympy factorint. It confirms v_p(C(n,j)) = 0 for both odd primes, v_2 > 0 and j <= n/2. Output: out/verify_hits.txt.
- Primality: every prime used passed gmpy2 Miller–Rabin (40 rounds) and sympy isprime (BPSW). Below 2^64 that is deterministic. The larger primes are BPSW **probable primes, not certified**: in the hits, the factors of 2^137 − 1, 2^149 − 1 and the p52 of 2^227 − 1.
- Source check of the saved refs (page, forum, OEIS entry, Lee README and fam2/README.txt, Plasma E0699 pages):
  - The largest recorded family range is k <= 62, m <= 39 (Lee fam2: "2^50..2^62 and 3^32+1..3^39+1: none").
  - None of 2^67, 2^101, 2^137, 2^149, 2^227 or these j appears in those texts.
  - A path grep of ryantuck/erdos-ai found no 699 folder.
  - arXiv was NOT searched.
INFERRED (not proved):
- Novelty: these are not recorded in the sources above. That is not proof that nobody has them.
- Erdős–Szekeres already tied the i = 2 cases to 2^r − 1 = pq (OEIS comment). The hits fit that pattern: in all known cases 2^k − 1 is a semiprime. Not every semiprime 2^k − 1 qualifies: k = 23, 37, 49, 59 have semiprime 2^k − 1 and give no near-miss in validation. If infinitely many suitable k existed, the finiteness strengthening would be false. This run shows nothing either way about that; it only adds data.

## Method (short)
- Factoring: 2^k − 1 = prod Φ_d(2) and 3^{2m} − 1 = prod Φ_d(3). Each Φ_d (d <= 300) was split along its Aurifeuillian factorization where one exists, then factored with gmpy2 p−1, rho and ECM (code/fac.py).
- Digit conditions (Lucas): for a prime p > i dividing n − t (t < i), the low base-p digits of n give necessary residue conditions on j mod p^s. Each digit position is an item with d+1 choices. CRT weights turn the allowed residues into a modular subset sum, which is solved by meet-in-the-middle over [i+1, n/2]. Extra digits are added greedily until the expected number of candidates is below 1. Every candidate then gets the full Lucas check for all known primes.
- Unfactored cofactor C | n − t: every prime q | C needs j mod q in {0..t}. Check pow(prod_{s<=t}(j−s), bits(C), C) == 0. A candidate that fails is excluded rigorously. For t = 0 (3^m + 1 part), C | j is a valid CRT modulus. A candidate that passes would be reported as unresolved; none did.

## Files
- code/: fac.py, run_factor.py, refactor.py (factoring); search.py (search); brute.py; verify_hits.py; run_all.sh
- out/:
  - factors_final.jsonl: all Φ_d pieces with primes and leftover composites
  - fam2_final.jsonl, fam3_final.jsonl: per-k/m status, candidate counts, hits
  - val_fam2.jsonl, val_fam3.jsonl: validation runs
  - verify_hits.txt, brute_small.txt
