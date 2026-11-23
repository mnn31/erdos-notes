# Erdős 420, lead 2: EGIP96 Theorem 6 (champs of D(n) have density zero) under RH, now unconditional

Date: 22 Nov 2026. Status: **argument complete** (every step proved here or cited with hypotheses checked against source text).
Relevance caveat up front: champs are **not** Erdős Problem 420 or a recorded variant of it. This is a status change for a
theorem in 420's main reference paper (EGIP96), nothing more. See "What this does and does not show".

## Final statement

Notation: d(m) = number of divisors of m; D(n) = d(n!) - d((n-1)!) for n >= 1 (D(1) = 0); P(n) = largest prime factor
(P(1) = 1); log = natural log. n is a **champ** if D(n) > D(m) for every natural m < n (EGIP96, p.13). C(x) = #{champs <= x}.

**Theorem.** Assume RH (the Riemann Hypothesis for zeta only; no Dirichlet L-function is used). Then
  x / log x  <<  C(x)  <<  x log log x / log x.
In particular the champs have asymptotic density zero (EGIP96 Theorem 6), and the upper bound is the same bound EGIP96
(p.15) derived only from Cramér's conjecture. The lower bound is unconditional.

**Unconditional if the Alpöge Lean theorems are accepted:** the only conditional input (Lemma 4) needs classical RH for
zeta, which is what Mathlib's `RiemannHypothesis` states (checked in a local Mathlib copy,
`Mathlib/NumberTheory/LSeries/RiemannZeta.lean`: every zero of `riemannZeta` other than s = -2(n+1) and s = 1 has real
part 1/2). Under that acceptance, EGIP's conjecture "the set of champs has asymptotic density zero" (p.14: they write that
it is "very annoying that we cannot seem to prove this") holds, with the stronger counting bound above.

## Lemmas

### Lemma 1 (ratio bound; EGIP96 Lemma 1/Theorem 2, upper half, reproved). For n >= 2^20,
  R(n) := d(n!)/d((n-1)!) <= 1 + P(n)/n + 6 n^{-1/2}.

Proof. Let w_p(k) = v_p(k!). Then w_p(n) = w_p(n-1) + v_p(n), d(k!) = prod_p (w_p(k)+1), so
R(n) = prod_{p^a || n} (1 + a/(w_p(n-1)+1)). For p | n, w_p(n-1) >= floor((n-1)/p) = n/p - 1, so w_p(n-1)+1 >= n/p and
each factor is <= 1 + ap/n <= exp(ap/n). Hence R(n) <= exp(S(n)/n), S(n) = sum of prime factors with multiplicity.
Also S(m) <= m for all m >= 1 (a+b <= ab for a,b >= 2, induct).
Case P(n) <= n^{1/2}. Let p = P(n), q = P(n/p) (n/p > 1 since n is not a prime <= n^{1/2}).
 If q <= n^{1/3}: S(n) = p + S(n/p) <= n^{1/2} + n^{1/3} log_2 n. If q > n^{1/3}: n/(pq) < n^{1/3} and
 S(n) = p + q + S(n/(pq)) <= 2n^{1/2} + n^{1/3}. For n >= 2^20, log_2 n <= 2 n^{1/6}, so S(n) <= 3n^{1/2} in both cases,
 and R(n) <= exp(3n^{-1/2}) <= 1 + 6n^{-1/2} (e^t <= 1+2t for 0 <= t <= 1).
Case p = P(n) > n^{1/2}. Then p^2 > n, so p || n; write n = mp, m < n^{1/2} < p, so p does not divide m. Since p^2 > n,
 w_p(n-1) = floor((n-1)/p) = m-1, so p contributes (m+1)/m = 1 + P(n)/n. The other primes contribute
 <= exp(S(m)/n) <= exp(m/n) = exp(1/p) <= 1 + 2n^{-1/2}. So R(n) <= (1 + 1/m)(1 + 2n^{-1/2}) <= 1 + P(n)/n + 4n^{-1/2}. QED
(Numerically: Lemma 1's inequality holds for every 2 <= n <= 3000, exact rational arithmetic.)

### Lemma 2 (unconditional non-champ criterion; EGIP96 proof of Thm 6, p.14, reproved with the strictness made explicit).
Let n >= e^25, L = log^3 n. If P(n) <= n/L and the interval (n - L/3, n] contains a prime, then n is not a champ.

Proof. Suppose n is a champ. n is not prime (a prime n has P(n) = n > n/L), so the prime p in (n - L/3, n] satisfies
p <= n-1. Let m = floor(n - L/3); then m < p, and n - 1 - m < L/3. Since m+1 <= p <= n-1, the range m < j < n is
nonempty and each D(j) < D(n) (champ), so
  d((n-1)!) = d(m!) + sum_{m<j<n} D(j) < d(m!) + (n-1-m) D(n) <= d(m!) + (L/3) D(n)   (D(n) >= 0).
By Lemma 1, D(n) = (R(n)-1) d((n-1)!) <= (1/L + 6n^{-1/2}) d((n-1)!) <= (3/2)(1/L) d((n-1)!), using
12 log^3 n <= n^{1/2} for n >= e^25. Hence d((n-1)!) < d(m!) + (1/2) d((n-1)!), i.e. d((n-1)!) < 2 d(m!).
But p! = p (p-1)! with p prime to (p-1)!, so d(p!) = 2 d((p-1)!); and k -> d(k!) is nondecreasing (k! | (k+1)!).
So d((n-1)!) >= d(p!) = 2 d((p-1)!) >= 2 d(m!). Contradiction. QED

### Lemma 3 (unconditional). #{n <= x : P(n) > n/log^3 n} = O(x log log x / log x).

Proof. Chebyshev bound: prod_{p<=N} p < 4^N (induction: for N = 2k+1 the primes in (k+1, 2k+1] divide
binom(2k+1,k) <= 4^k; even N > 2 reduce to N-1). So theta(y) < y log 4 and, for y >= 2,
pi(y) <= sqrt(y) + theta(y)/log sqrt(y) <= y/log y + 2 log 4 * y/log y <= 4y/log y.
If P(n) > n/log^3 n, write n = kp with p = P(n), k = n/p < log^3 n <= log^3 x. For fixed k there are <= pi(x/k) such n.
For large x, x/k >= x/log^3 x >= sqrt(x), so log(x/k) >= (1/2) log x and pi(x/k) <= 8x/(k log x). Summing over
k <= log^3 x gives <= (8x/log x)(1 + 3 log log x). QED
(Numerically the asymptotics are far off at small x: 88% of n <= 10^6 have P(n) > n/log^3 n. Lemma 3 is only asymptotic.)

### Lemma 4 (RH input). Assume RH. #{n <= x : no prime in (n - (1/3)log^3 n, n]} = O(x / log x).

Cited input, statement and hypotheses VERIFIED in text: Cully-Hugill & Dudek, arXiv:2206.00433v2, **Theorem 1**:
"Assuming RH, for all x >= 10^8 and any delta in (0, 10^-8]",
  J(x,delta) := int_1^x |theta(y + delta y) - theta(y) - delta y|^2 dy < 202 delta x^2 log^2 x.
(Explicit version of Selberg 1943, their eq. (1). Their proof assumes RH for zeta only; the one GRH paper in their
bibliography, Simonič [26], is cited only for comparison in the introduction. I read the statement, the hypothesis
lines, and the final step (21) with A7 = 202; I did not re-verify the whole proof.)

Proof. Fix large X and put delta = log^3 X/(12X) (so delta <= 10^-8 and X/2 >= 1 + 2 delta X for X large). For an
integer n in (X, 2X] let I_n = [n - 1 - 2 delta X, n - 2 delta X], a unit interval; distinct n give intervals with
disjoint interiors, and I_n is inside [X/2, 2X]. For y in I_n: delta y <= 2 delta X, so
(y, y + delta y] is inside (n - 1 - 2delta X, n] = (n - 1 - log^3 X/6, n], which is inside (n - (1/3)log^3 n, n] because
1 + log^3 X/6 < (1/3) log^3 X <= (1/3) log^3 n (log^3 X > 6). So if n is bad (no prime in its window), then for every
y in I_n, theta(y+delta y) - theta(y) = 0 and |theta(y+delta y) - theta(y) - delta y| = delta y >= delta X/2.
Thus #bad n in (X,2X] <= meas{y in [X/2,2X] : |...| >= delta X/2} <= (delta X/2)^{-2} J(2X, delta)
  < 4 * 202 delta (2X)^2 log^2(2X) / (delta^2 X^2) = 3232 log^2(2X)/delta <= 4 * 3232 * 12 X / log X.
Dyadic sum: cover (sqrt(x), x] by (x/2^{j+1}, x/2^j] with x/2^{j+1} >= sqrt(x)/2; on each, log X >= (1/3) log x for
large x, so the total is O(x/log x) + O(sqrt x). QED
(Selberg's own 1943 statement was NOT read; the citation above replaces it. Numerically, every n in [5, 10^6] has a prime
in (n - (1/3)log^3 n, n] (only n = 4 fails), consistent but irrelevant to the asymptotic claim.)

### Lemma 5 (lower bound; EGIP96 Theorem 5, prime case, reproved). Every prime p is a champ.
Proof. For m < p: D(m) = d(m!) - d((m-1)!) <= d(m!) - 1 < d(m!) <= d((p-1)!) = d(p!) - d((p-1)!) = D(p). QED
So C(x) >= pi(x) >> x/log x.

### Proof of the Theorem
For x large, every champ n <= x satisfies n < e^25, or P(n) > n/log^3 n, or has no prime in (n - (1/3)log^3 n, n]
(Lemma 2, contrapositive). The counts are O(1), O(x log log x/log x) (Lemma 3), O(x/log x) under RH (Lemma 4).
Lower bound by Lemma 5. QED

## Which L-functions are used
Only zeta, through Cully-Hugill–Dudek Theorem 1 (RH). No Dirichlet L-function, no GRH, no pair correlation, no
Cramér. Lemmas 1, 2, 3, 5 are unconditional and elementary.

## Numerical sanity checks (Python -I, scratch scripts not kept in this folder)
- Champs <= 3000 computed exactly: 786 champs; Lemma 1 inequality holds for all 2 <= n <= 3000; among the 20 n <= 3000
  meeting Lemma 2's hypotheses, none is a champ.
- Side observation, not load-bearing: my computation gives **31** champs <= 500 not of the form p or 2p; the manuscript
  (p.14, Deléglise's computation) lists 30. The extra one is **292 = 4 * 73**: D(292)/D(291) = 1.0136 > 1 and 291 is the
  argmax of D below 292 (checked twice, by an incremental ratio computation and by direct Legendre-formula d(n!)).
  So either the manuscript's list omits 4*73 or I misread its definition; the published version was not compared.

## What this does and does not show
- Erdős Problem 420 asks about F(f,n) = d((n + floor f(n))!)/d(n!) (whether F((log n)^C, n) -> oo for all large n, etc.).
  Champs of D(n) are **not** part of the problem as posed, not in the Lean file
  `FormalConjectures/ErdosProblems/420.lean` (origin/main: parts i-iii and variants on log/Rankin/4/9 scales, no champs),
  and not in the erdosproblems database entry or page. This result resolves none of 420's parts.
- It upgrades EGIP96 Theorem 6 (the main reference of 420) from "assuming RH" to unconditional modulo acceptance of the
  Alpöge RH theorem, and sharpens it to C(x) << x log log x/log x (EGIP only had this from Cramér's conjecture). The true
  order of C(x) between x/log x and x log log x/log x remains open (EGIP p.15 say they are unsure what to conjecture).
- Mathematically this is a routine consequence: the authors' own proof plus RH. The novelty is the status change only.

## Credit
The argument is EGIP96's (Erdős, Graham, Ivić, Pomerance, "On the number of divisors of n!", 1996, Theorem 6 and its
proof, pp.14-15 of the manuscript at math.dartmouth.edu/~carlp/factorial.pdf). The RH input is Selberg (1943), used here
via the explicit version of Cully-Hugill & Dudek (arXiv:2206.00433, Theorem 1). RH itself: Alpöge's Lean proof (20 Nov
2026). My contributions: rewriting the proof with explicit thresholds, making the strict inequality in Lemma 2 explicit
(it needs p <= n-1, which follows from n not prime), the quantitative bound O(x log log x/log x), and the 292 observation.

## Prior-recording check (22 Nov 2026)
- Plasma `library/.../erdos_1996_number_divisors/theorem_6.md` (read): records Theorem 6 as conditional on RH; says no
  problem page concerns champs. Repo code search for "champ": only the EGIP cards (theorem_5, theorem_6, _index).
- erdosproblems.com/420 page and forum thread 420 (curl, grep): no "champ"; no RH remarks of this kind. Database
  problems.yaml: no "champ".
- Web search (two queries): no later paper on the density of champs found. Freiberg arXiv:2609.15597 (read abstract/intro
  grep) concerns K(n), not champs.

## Sources not read
- Selberg 1943 (Arch. Math. Naturvid. 47) itself: not read; replaced by Cully-Hugill–Dudek Theorem 1.
- Full proof of Cully-Hugill–Dudek Theorem 1: statement and hypotheses read, proof not re-verified line by line.
- Published (Birkhäuser 1996) version of EGIP96: not compared with the manuscript.
- OEIS (no champ sequence searched for directly), ryantuck/erdos-ai (not checked for this lead), arXiv full-text search.
