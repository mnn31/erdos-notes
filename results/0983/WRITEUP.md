# Erdős #983 — f(π(n)+1, n) = 2π(√n) + O(n^{1/4} log n) under RH

Status: **proved, conditional on RH for ζ only** (no Dirichlet L-function, no GRH for number fields).
Unconditional if the Alpöge Lean theorem `riemannHypothesis` (Mathlib's `RiemannHypothesis`,
leanprover-community/riemann-hypothesis, 20 Nov 2026) is accepted. Value: modest. This is the
"PNT with an error term" step that Erdős already points to on p.140 of [Er70b], with RH plugged in
(details under Credit).

## Final statement

Notation: p_k is the k-th prime (p_1 = 2). π is the usual prime-counting function. x = √n, and
N = π(x) = π(⌊√n⌋). f is the function of the Lean file (`Erdos983.f`): the least r such that
*every* A ⊆ {1,…,n} with |A| = k has a set S of exactly r primes with more than r elements of A
whose prime factors all lie in S. Set D(n) := 2π(√n) + 1 − f(π(n)+1, n).

**Theorem.** Assume RH. Then there is n_0 such that for all n ≥ n_0

    0 ≤ D(n) ≤ c·n^{1/4}·(log n + 2 log 3) + 10,    c = (3+√3)/(8π) ≈ 0.1883.

In particular f(π(n)+1, n) = 2π(n^{1/2}) + O(n^{1/4} log n).
As a Lean statement: `RiemannHypothesis → (fun n : ℕ ↦ (f (π n + 1) n : ℝ) - 2 * π (Nat.sqrt n)) =O[atTop] (fun n ↦ (n:ℝ)^(1/4:ℝ) * Real.log n)`.

Both inequalities also hold for the Hall form f'(k,n) = max_A min{|S| : |A[S]| > |S|} used by
Sothanaphan on the forum (see the remarks after Lemmas 1 and 3).

The leading constant in the upper bound is explicit. n_0 is effective but I did not compute it.
It is fixed by the three "eventually" facts in Lemma 5.

## Lemmas

**Lemma 1 (Erdős–Straus (14), in exact-cardinality form).** If π(n) ≥ 2π(√n) + 1, then
f(π(n)+1, n) ≤ 2π(√n) + 1.

*Proof.* (This is my own proof, written for the exact-|S| definition. Erdős's proof on p.139 picks a
set of s+v primes that depends on A. The Lean `sInf` needs a single r that works for every A, so I
prove directly that r = 2s+1 works.) Let s = π(√n). Call a prime *small* if it is ≤ √n and *large*
if it lies in (√n, n]. Let L be the set of large primes, so |L| = π(n) − s ≥ s + 1. Fix
A ⊆ [1,n] with |A| = π(n)+1. An element a ≤ n has at most one large prime factor, and it appears
to the first power, because q² > n for large q. Let c_0 be the number of a ∈ A with no large prime
factor (this includes a = 1). For q ∈ L let c_q be the number of a ∈ A whose large prime factor is q.
If a = q·b, then b ≤ n/q < √n, so every prime factor of b is small. Hence for any S that contains
all small primes, such an a is S-smooth iff q ∈ S. Also c_0 + Σ_{q∈L} c_q = |A| = s + |L| + 1, so
Σ_{q∈L}(c_q − 1) = s + 1 − c_0. Let Q ⊆ L be s+1 primes with the largest c_q, and let
S = {small primes} ∪ Q, so |S| = 2s+1. Then

numSmooth(A,S) − |S| = c_0 + Σ_Q c_q − (2s+1) = c_0 − s + Σ_Q (c_q − 1).

- If every q ∈ Q has c_q ≥ 2, the sum is ≥ s+1, and the excess is ≥ c_0 + 1 ≥ 1.
- Otherwise some q ∈ Q has c_q ≤ 1. Because Q holds the largest values, every q ∈ L∖Q has
  c_q ≤ 1. So Σ_{L∖Q}(c_q−1) ≤ 0, which gives Σ_Q(c_q−1) ≥ s+1−c_0, and the excess is ≥ 1.

So every A has a set of exactly 2s+1 primes with more than 2s+1 smooth elements, and
f ≤ 2s+1 by `f_le`. ∎
(Hall form: min_S ≤ 2s+1 for every A, so f' ≤ 2s+1. Brute-force check for n ≤ 18 with both
definitions: checks/brute.py; f_lean = f_hall ≤ 2s+1 in every case.)

**Lemma 2 (path count).** Let v_0, …, v_L be a path, and let T be a set of vertices with
T ≠ {all vertices}. Let e(T) be the number of path edges with both ends in T, and let ε(T) be
|T ∩ {v_0, v_L}|. If L ≥ 1, then e(T) + ε(T) ≤ |T|.

*Proof.* If T = ∅ both sides are 0. Otherwise T splits into k ≥ 1 maximal runs of consecutive
indices. A run of ℓ vertices contains exactly ℓ−1 path edges, and every path edge inside T lies in
one run, so e(T) = |T| − k. If ε(T) ≤ 1, then e + ε ≤ |T| − 1 + 1. If ε(T) = 2, then v_0, v_L ∈ T,
and because T misses some vertex, v_0 and v_L lie in different runs. So k ≥ 2 and
e + ε ≤ |T| − 2 + 2. ∎

**Lemma 3 (generalized Price path, lower bound).** Let N = π(√n), and let d be an integer with
0 ≤ d ≤ N−1. Put m = N−d ≥ 1 and r_j = p_{N+1+j} for 0 ≤ j ≤ m. Suppose p_{2N+1} ≤ n and

(★) p_i · r_{m+1−i} ≤ n for i = 1, …, m.

Then f(π(n)+1, n) ≥ 2m+1 = 2π(√n) + 1 − 2d.

*Proof.* Take the path r_m, p_1, r_{m−1}, p_2, …, r_1, p_m, r_0. Its vertices are v_{2i−1} = p_i and
v_{2i} = r_{m−i}, and it has 2m+1 distinct primes: the p_i are ≤ √n and the r_j are > √n. Its edges
are p_i r_{m+1−i} and p_i r_{m−i} for i = 1..m. Let C be the 2m edge products together with the two
endpoint primes r_m and r_0. Unique factorization makes these 2m+2 numbers distinct. Let A be C
together with all primes ≤ n that are not on the path. All path primes are ≤ r_m ≤ p_{2N+1} ≤ n,
so |A| = 2m+2 + π(n) − (2m+1) = π(n)+1. By (★), and since p_i r_{m−i} < p_i r_{m+1−i}, we have
A ⊆ [1,n].

Now let S be any set of r ≤ 2m primes, and let T = S ∩ path. Then T is not the whole path. An
element of A is S-smooth only in one of three ways: it is a non-path prime in S (there are at most
|S∖T| of these); it is an edge product with both ends in T; or it is an endpoint prime in T. By
Lemma 2, numSmooth(A,S) ≤ |S∖T| + |T| = r. So no r ≤ 2m is admissible for this A. The admissible
set is nonempty, since π(n) is admissible by the Lean `le_primeCounting`, so its `sInf` is ≥ 2m+1. ∎
(Hall form: the same A has min_S ≥ 2m+1. Brute force: checks/cover.py checked all 61 valid
(n,d) with 30 ≤ n ≤ 61 exhaustively over all prime sets, and found the minimal admissible r = 2m+1
every time. It also checked 4 larger cases over all subsets of path primes.)

This is the construction of Price (forum, 30 Apr 2026) and Sothanaphan (19 May 2026). Their version
is the case n = p_{N+1}²−1, d = 0. The case of general (n,d) is my extension.

**Lemma 4 (reduction to π).** Let M(n) := max_{N+1 ≤ j ≤ 2N+1} [2N − j − π(n/p_j)]. If
d ≥ max(0, 2 + M(n)), then (★) holds.

*Proof.* For i = 1..m, r_{m+1−i} = p_j with j = 2N−d+2−i, and j runs over [N+2, 2N−d+1], which is
contained in [N+1, 2N+1]. For real y ≥ 0, p_i ≤ y iff π(y) ≥ i. So (★) for this i is equivalent to
π(n/p_j) ≥ 2N−d+2−j, that is, to d ≥ 2 + [2N − j − π(n/p_j)]. ∎

**Lemma 5 (analytic input, RH).** Under RH, for n large, M(n) ≤ c·√x·log(3x) + 2, with
c = (3+√3)/(8π) and x = √n.

Cited input (VERIFIED by reading the text): Büthe, *Estimating π(x) and related functions under
partial RH assumptions*, Math. Comp. 85 (2016); arXiv:1410.7015v4, **Theorem 2, (7.2)**. If RH
holds for zeros with 0 < Im ρ ≤ T and 4.92·√(x/log x) ≤ T, then |π(x) − li(x)| ≤ √x·log x/(8π) for
x > 2657. Büthe's introduction says this is Schoenfeld's bound "implied by the Riemann hypothesis
[Sch76]". Under full RH, which is Mathlib's `RiemannHypothesis` (every zero with s ≠ 1 that is not
a trivial zero −2(k+1) has Re s = 1/2), the hypothesis holds for every T, so the bound holds for
all x > 2657. Büthe's π is normalized: a prime at the endpoint counts 1/2. So for the usual π,
|E(y)| ≤ B(y) := √y·log y/(8π) + 1/2 for y > 2657, where E := π − li. I did not find where Büthe
defines li. The argument below uses only li′(u) = 1/log u on (1,∞), plus differences of li, so any
additive normalization works.

*Eventual facts.* From (7.2), π(y) = li(y) + O(√y log y). L'Hôpital gives li(y) ~ y/log y, so
π(y) ~ y/log y. Hence for all large n: (a) π(3x) ≥ 2π(x)+1, so p_{2N+1} ≤ 3x ≤ n;
(b) π(n) ≥ 2π(√n)+1; (c) x > 7971 and log x ≥ 3; (d) c√x log(3x) + 5 ≤ N − 1, because N ~ x/log x.

*Proof.* Fix j ∈ [N+1, 2N+1] and put t = p_j/x. Then 1 < t ≤ 3 by (a), since p_{N+1} > x.
π(p_j) = j, and n/p_j = x/t. With E = π − li:

2N − j − π(n/p_j) = 2π(x) − π(xt) − π(x/t) = −Λ(t) + [2E(x) − E(xt) − E(x/t)],

where Λ(t) = [li(xt) − li(x)] − [li(x) − li(x/t)]. Substitute u = xs in the first integral and
u = x/s in the second:

Λ(t) = x ∫_1^t [1/log(xs) − 1/(s² log(x/s))] ds.

Both logarithms are positive, because x > 3 ≥ s. So the integrand is ≥ 0 iff
(s²−1)·log x ≥ (s²+1)·log s. For 1 ≤ s ≤ 3, log s ≤ s−1 gives
(s²+1)·log s ≤ (s²−1)·(s²+1)/(s+1) ≤ (s²−1)·s ≤ 3(s²−1) ≤ (s²−1)·log x, using (c). So Λ(t) ≥ 0.

The points x/t, x, xt all lie in (2657, 3x] by (c), and B is increasing. So
2E(x) − E(xt) − E(x/t) ≤ 2B(x) + B(3x) + B(x) ≤ (3+√3)·√x·log(3x)/(8π) + 2. ∎

**Proof of the Theorem.** Take n large enough that (a)–(d) hold. The lower bound D ≥ 0 is Lemma 1
with (b). For the upper bound, let d = ⌈4 + c√x log(3x)⌉. Lemma 5 gives d ≥ 2 + M(n), (d) gives
d ≤ N−1, and (a) gives p_{2N+1} ≤ n. So Lemmas 4 and 3 give D(n) ≤ 2d ≤ 10 + 2c√x log(3x)
= 10 + c·n^{1/4}(log n + 2 log 3). ∎

## Numerical sanity checks (checks/, run with python3 -I)

- `main.py`: 280 random n in [10^6, 10^12] (40 per decade). For each n it computes the exact minimal
  d satisfying (★) and the sufficient d from Lemma 4 (the second is always ≥ the first). It builds
  the set A and checks that the elements are ≤ n, distinct, and that the path has 2m+1 primes. It
  also checks that the Lemma 4 d is ≤ the RH-derived value 4 + c√x log 3x. Worst ratio found:
  d/(n^{1/4} log n) ≤ 0.0112. The bound 2d is therefore far from tight in practice.
- `cover.py` and `brute.py`: described after Lemmas 1 and 3.

## What this does and does not show

- **Part (i)** (whether 2π(√n) − f → ∞) is already answered no, unconditionally, by Pomerance 1979
  and by Price 2026 (see Credit). This note does not touch it.
- **Part (ii)** (estimate f(k,n) for π(n)+1 < k = o(n)) remains open. This note is only about
  k = π(n)+1.
- What it adds: under RH, the Erdős–Straus error o_A(n^{1/2}/(log n)^A) (website; Lean
  `erdos_983.variants.erdos_straus`, currently `sorry`) improves to O(n^{1/4} log n). Under RH this
  implies the Lean `erdos_straus` variant. That variant follows unconditionally from the classical
  PNT error term anyway (Erdős's p.140 remark), so the gain is the exponent, not the existence of
  the bound.
- No lower bound: nothing here says D(n) is unbounded or how large it gets. Pomerance conjectured
  that 2π(√x) − f(π(x)+1,x) is unbounded (Po79 §5) and could not prove it. D(n) = 0 infinitely
  often (Pomerance 1979 / Price). The numerics suggest the true size of the minimal admissible d
  is far smaller than the bound.
- Unconditional variant (stated in the brief): using the Vinogradov–Korobov PNT error in Lemma 5
  would give D(n) ≪ √n·exp(−c(log n)^{3/5}(log log n)^{−1/5}). This is **not verified**: I did not
  read a source for the VK error term. It is a remark only and not part of the Theorem.
- Which L-functions are used: only ζ (RH), through Büthe Thm 2. GRH for Dirichlet L-functions is
  not used.

## Credit

- The upper bound (14) and the lower-bound method are due to Erdős–Straus [Er70b, pp.139–140]
  (read on page images and in OCR text). On p.140 Erdős says that the PNT *with an error term*
  turns this proof into f = 2π(x^{1/2}) + o(x^{1/2}/(log x)^k). The present result is that remark
  with RH as the error term.
- **Pomerance 1979** (Math. Comp. 33, 399–408, §5; read via OCR of the scanned PDF,
  refs/pomerance79_ocr.txt) already disproved part (i). He shows that equality holds in (5.6) =
  (14) for an unbounded set of x, using f(π(x)+1,x) ≥ t+1, which he quotes from [Er70b]. The same
  §5 also has RH-conditional remarks on the closely related quantity
  M(n) = max_{i<n} p_{n−i}p_{n+i}: under RH, |p_n² − M(n)| = O(p_n^{3/2} log² n), stated without
  proof. This is essentially the same input as (★). Neither the forum nor the Lean docstring
  credits Pomerance with the disproof itself (the Lean docstring cites Po79 only for the lemma).
  Someone should flag this.
- The path construction for general n is the Price/GPT-5.5 Pro construction (forum 30 Apr 2026),
  in the form expounded by Sothanaphan (19 May 2026). The extension to every n with a shift d, and
  the RH bookkeeping, are mine. They are routine.
- The explicit RH bound is due to Schoenfeld 1976, reproved by Büthe (Thm 2).
- Prior-recording check: I found no RH or error-term statement for f in any of these: the forum
  thread (read in full), the website page, the Lean file, Plasma E0983 (_index, claims index, claim
  page; none mention RH), or Pomerance 1979 (which has RH remarks on M(n) but not on f). This
  search is not exhaustive.

## Sources not read

- Schoenfeld 1976 (Math. Comp. 30, 337–360): the AMS PDF is behind a bot check. I used Büthe
  Thm 2 instead, which I read.
- von Koch 1901: not read and not needed.
- Price's Overleaf write-up: a JS-only link.
- Any Vinogradov–Korobov source (only the unverified remark above depends on it).
- The ryantuck/erdos-ai review files and the arXiv/OpenAlex searches: I am relying on the screener
  (SCREEN.md) for these and did not redo them.
- The Alpöge Lean proof itself. I read only the README of leanprover-community/riemann-hypothesis
  (it lists `riemannHypothesis : RiemannHypothesis`). Its correctness is taken from the brief, not
  checked by me.

Local refs: refs/er70b.{pdf,txt}, refs/pomerance79.pdf (+ _ocr.txt), refs/arxiv/buthe1410.7015.pdf,
refs/web/ (forum and page), refs/plasma/.
