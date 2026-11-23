# Erdős Problem 770, third question: h(n) = P(n) once P(n) > n^ε, from RH + GRH for Dirichlet L-functions

Written 22 Nov 2026. The deduction is complete. The only open point is non-mathematical: whether
Alpöge's Lean theorems are accepted (§6).

## 0. Notation

For integers n ≥ 1 and M ≥ 2:

* D_n(M) = gcd{ m^n − 1 : 2 ≤ m ≤ M }. This is a positive integer, because each m^n − 1 ≥ 1.
* h(n) = min{ M > 2 : D_n(M) = 1 }. This is the collective-gcd reading. Lemma 1(d) shows the set
  is nonempty.
* P(n) = max{ p prime : p − 1 | n }. This is well defined: 2 qualifies, and p − 1 | n forces p ≤ n + 1.
* π(x) is the prime-counting function, and log is the natural logarithm.

## 1. Final statement

**Theorem A.** Assume
  (RH) the Riemann Hypothesis, and
  (GRH-D) GRH for Dirichlet L-functions. Only this case is used: for every prime q ≥ 3000 and every
  nonprincipal character χ mod q, every nontrivial zero of L(s, χ) has real part 1/2.
Then for every real A > 4 there is n_0(A) such that, for all n ≥ n_0(A),

    P(n) ≤ h(n) ≤ max{ P(n), ⌊A (log n)^2⌋ }.

**Corollary B (third question of #770).** Assume (RH) and (GRH-D). For every ε > 0 there is n_1(ε)
such that, for all n ≥ n_1(ε), P(n) > n^ε implies h(n) = P(n). This is exactly the mathematical
content of `Erdos770.erdos_770.parts.iii` in formal-conjectures (§7).

**Unconditional form.** Suppose the Alpöge Lean theorems of 20 Nov 2026 are accepted: `riemannHypothesis`
together with `LFunction_ne_zero_of_half_lt_re` (or `LFunction_eq_zero_re_of_isPrimitive`), or the
formal-conjectures `GRH.generalized_riemann_hypothesis`. Then (RH) and (GRH-D) hold, and Theorem A and
Corollary B are unconditional (§6). Without that acceptance, they are theorems under RH + GRH for
Dirichlet L-functions.

## 2. Elementary lemmas

**Lemma 1.** Let n ≥ 1.

(a) If M ≥ 2 and q is a prime dividing D_n(M), then q > M.
(b) If 2 ≤ M ≤ M', then D_n(M') | D_n(M).
(c) If p is prime, p − 1 | n and 2 ≤ M < p, then p | D_n(M).
(d) The set {M > 2 : D_n(M) = 1} is nonempty and upward closed, and h(n) ≥ max(3, P(n)).

*Proof.*
(a) Suppose q ≤ M. Then m = q is one of the indices, and q^n − 1 ≡ −1 (mod q). So q does not divide
D_n(M).
(b) D_n(M') is the gcd over a superset of the numbers used for D_n(M).
(c) Each m with 2 ≤ m ≤ M < p is coprime to p. Fermat's little theorem gives m^{p−1} ≡ 1 (mod p).
Since p − 1 | n, this gives m^n ≡ 1 (mod p).
(d) Take M_* = max(3, 2^n). By (a), any prime q | D_n(M_*) satisfies q > M_* ≥ 2^n. But q also divides
2^n − 1 ≥ 1, so q ≤ 2^n − 1. This is a contradiction, so the positive integer D_n(M_*) equals 1. The
set is upward closed by (b). Now suppose P(n) > 2 and 2 < M < P(n). Then (c) gives P(n) | D_n(M),
so D_n(M) ≠ 1. Hence h(n) ≥ P(n). The bound h(n) ≥ 3 holds by definition. ∎

**Lemma 2 (Chebyshev-type bound, proved here).**
(i) For every real x ≥ 2, π(x) ≥ ((x − 2) log 2 − log(x + 1)) / log x.
(ii) For x ≥ 40, π(x) ≥ x / (2 log x).

*Proof.*
(i) Let m = ⌊x/2⌋ ≥ 1, so 2 ≤ 2m ≤ x and 2m > x − 2.

First, 4^m = Σ_k C(2m, k) ≤ (2m + 1) C(2m, m).

Next, by Legendre's formula, v_p(C(2m, m)) = Σ_{k≥1} (⌊2m/p^k⌋ − 2⌊m/p^k⌋). Each summand is 0 or 1,
and it vanishes once p^k > 2m. So p^{v_p} ≤ 2m. Also no prime p > 2m divides C(2m, m). Hence
C(2m, m) ≤ (2m)^{π(2m)}.

Combining the two bounds:

    π(x) log(2m) ≥ π(2m) log(2m) ≥ 2m log 2 − log(2m + 1) ≥ (x − 2) log 2 − log(x + 1).

If the right side is ≤ 0, (i) is trivial. Otherwise use 0 < log(2m) ≤ log x.

(ii) Set g(x) = x(log 2 − 1/2) − 2 log 2 − log(x + 1). Then g'(x) = log 2 − 1/2 − 1/(x + 1) > 0 for
x ≥ 40, and g(40) = 7.7259… − 1.3863… − 3.7136… > 2.6. So for x ≥ 40,
(x − 2) log 2 − log(x + 1) ≥ x/2 > 0. Now apply (i). ∎

Lemma 2 was also checked numerically for every integer 2 ≤ x ≤ 200000 (§8).

**Lemma 2′.** For 1 ≤ r ≤ N, C(N, r) ≥ (N/r)^r.

*Proof.* C(N, r) = Π_{i=0}^{r−1} (N − i)/(r − i). Each factor is ≥ N/r, because
r(N − i) ≥ N(r − i) is equivalent to iN ≥ ir, which holds since N ≥ r. ∎

## 3. The analytic input (cited; hypotheses checked against the source text)

**Lemma 3 (Lamzouri–Li–Soundararajan, arXiv:1309.3595v3, Theorem 1.1(2)).** Assume (RH) and (GRH-D).
Let q ≥ 3000 be prime and let H be a proper subgroup of G = (Z/qZ)^*. Then some prime ℓ ≤ (log q)^2
does not lie in H.

*Source and hypothesis check.* I read refs/lls.txt, text extracted from refs/lls.pdf, which is v3,
8 Dec 2016.

* Theorem 1.1 opens "Assume GRH. Let q ≥ 3000 be an integer, and let H be a proper subgroup of G".
* Part (2) adds one hypothesis: q is not divisible by any prime below (log q)^2. It concludes that
  some prime ℓ ≤ (log q)^2 lies outside H.
* For prime q, the only prime factor is q itself. And q > (log q)^2, because e^t > t^2 for all t ≥ 0:
  f(t) = 1 + t − t^2/2 + t^3/6 satisfies f(0) = 1 and f'(t) = ((t − 1)^2 + 1)/2 > 0, and
  e^t ≥ 1 + t + t^2/2 + t^3/6.
* Since ℓ ≤ (log q)^2 < q, ℓ is a unit mod q, so "ℓ ∉ H" is meaningful.

*Exactly which L-functions are used.* I read the proof of Part 2 in LLS §3.2 and the lemmas it calls.

* Let H̃ be the group of characters trivial on H. Because H is proper, H̃ contains a nonprincipal
  character χ.
* Lemma 2.1 and Lemma 2.4 are stated under "Assume RH". They are used for Σ Λ(n) log(X/n) and
  Σ (Λ(n)/n)(1 − n/X).
* Lemma 2.2 and Lemma 2.3 are stated under "Assume GRH. Let q ≥ 3 and let χ (mod q) be a primitive
  Dirichlet character". They are applied to the primitive character χ̃ inducing χ.
* For prime q, every nonprincipal χ mod q is primitive of conductor q. So χ̃ = χ, and §3.2 itself notes
  S(X, χ) = S(X, χ̃) in this case.
* Inside these lemmas, GRH is used in the form that every zero ρ_χ of ξ(s, χ), that is, every
  nontrivial zero of L(s, χ), equals 1/2 + iγ_χ. LLS §2 says this: "The zeros of ξ(s, χ) are
  precisely the non-trivial zeros of L(s, χ)". Lemma 2.3 also uses the functional equation, which
  relates the value at 1 to the value at 0 for χ̄. That step is not a GRH input.

So Lemma 3 needs RH for ζ, plus the critical-line statement for the nontrivial zeros of L(s, χ) for one
nonprincipal (hence primitive) character χ mod the prime q. It uses no Dedekind, Hecke, Artin or
automorphic L-function, no Kummer-field GRH, no zero-simplicity and no pair-correlation input.

## 4. The key proposition (after Korsky, Prop. 2.3; proved here with an explicit constant)

**Lemma 4.** Assume (RH) and (GRH-D). Fix A > 4. There is n_0(A) such that for every n ≥ n_0(A),
with M = ⌊A (log n)^2⌋, every prime q dividing D_n(M) satisfies q > M and (q − 1) | n.

*Choice of n_0(A).* Put r = r(M) = ⌊√M / log M⌋. Choose n_0(A) so that every n ≥ n_0(A) satisfies:

  (C1) M ≥ 3000;
  (C2) r · log(√M / 2) > log n.

(C1) clearly holds for large n. For (C2), with M ≥ 3000 we have r ≥ 6 and (1/2)log M − log 2 > 0, so

    r log(√M/2) ≥ (√M/log M − 1)((1/2) log M − log 2)
                = (1/2)√M − (log 2)√M/log M − (1/2) log M + log 2
                ≥ (1/2)√M · (1 − 2 log 2/log M − log M/√M).

Since M ≥ A(log n)^2 − 1, we get √M ≥ log n · √(A − (log n)^{−2}). Therefore

    r log(√M/2) / log n ≥ (1/2) √(A − (log n)^{−2}) · (1 − 2 log 2/log M − log M/√M) → √A / 2 > 1

as n → ∞, because M → ∞. So (C2) holds for all large n.

*Proof of Lemma 4.* Let n ≥ n_0(A), and let q be a prime dividing D_n(M).

1. By Lemma 1(a), q > M ≥ 3000.
2. Let H = { x ∈ (Z/qZ)^* : x^n = 1 }. This is a subgroup. Every integer 1 ≤ m ≤ M is a unit mod q
   (since m < q) and satisfies m^n ≡ 1 (mod q): for m ≥ 2 because q | m^n − 1, and trivially for
   m = 1. So H contains the residues of 1, …, M. Since (Z/qZ)^* is cyclic of order q − 1,
   |H| = gcd(n, q − 1) ≤ n.
3. Suppose (q − 1) ∤ n. Then gcd(n, q − 1) < q − 1, so H is proper. Lemma 3 applies, since q ≥ 3000
   is prime. It gives a prime ℓ ≤ (log q)^2 with ℓ ∉ H. If ℓ ≤ M, then ℓ ∈ H by step 2. So
   M < ℓ ≤ (log q)^2, that is, log q > √M.
4. Let S be the set of products of r distinct primes ≤ M. Lemma 2(ii) applies since M ≥ 40, giving
   π(M) ≥ M/(2 log M) ≥ √M/log M ≥ r ≥ 1. Each s ∈ S satisfies 2 ≤ s ≤ M^r ≤ M^{√M/log M} = e^{√M} < q.
   Each s ∈ S lies in H, since H is closed under multiplication and contains every prime ≤ M.
   Distinct elements of S are distinct integers in [2, q − 1], so their residues mod q are distinct.
   Hence |H| ≥ |S| = C(π(M), r).
5. By Lemma 2′ and Lemma 2(ii),

       |S| ≥ (π(M)/r)^r ≥ ( (M/(2 log M)) / (√M/log M) )^r = (√M/2)^r.

   By (C2), log |S| ≥ r log(√M/2) > log n, so |H| > n. This contradicts step 2.

Hence (q − 1) | n. ∎

*Remark.* The constant 4 comes from log q > √M (Lemma 3 with constant 1) and the count
log|S| ≈ (1/2)√M. It is not claimed to be optimal. LLS Theorems 1.2 and 1.3 give smaller constants
for the least prime outside a subgroup of index ≥ 2; this was not pursued. Korsky's Prop. 2.3 states
only "an absolute constant A". The explicit A > 4 here is my own derivation from LLS Thm 1.1(2).

## 5. Proof of Theorem A and Corollary B

*Theorem A.* Let n ≥ n_0(A), M = ⌊A (log n)^2⌋ and M' = max(P(n), M) ≥ 3000.

* Suppose a prime q divides D_n(M'). By Lemma 1(b), q | D_n(M). By Lemma 4, q − 1 | n, so q ≤ P(n) ≤ M'.
* But Lemma 1(a) gives q > M'. This is a contradiction.
* So the positive integer D_n(M') has no prime factor, and D_n(M') = 1. Since M' > 2, h(n) ≤ M'.

The lower bound h(n) ≥ P(n) is Lemma 1(d). ∎

*Corollary B.* Fix ε > 0 and take A = 5.

* Since (log n)^2 / n^ε → 0, there is n_1 ≥ n_0(5) such that n^ε > 5 (log n)^2 and n^ε > 2 for all
  n ≥ n_1.
* Let n ≥ n_1 with P(n) > n^ε. Then P(n) > ⌊5 (log n)^2⌋, so the maximum in Theorem A is P(n), and
  h(n) ≤ P(n).
* Lemma 1(d) gives h(n) ≥ P(n). Hence h(n) = P(n). ∎

## 6. Where the hypotheses come from now (Alpöge, 20 Nov 2026)

**Verified by reading** github.com/leanprover-community/riemann-hypothesis on 22 Nov 2026 (latest main
commit 2026-11-23T04:24Z UTC):

* src/Challenge.lean states five theorems, which Main.lean is to be judged against. Among them:
  * `riemannHypothesis : RiemannHypothesis` (Mathlib's).
  * `LFunction_ne_zero_of_half_lt_re`: for every N ≥ 1, every χ : DirichletCharacter ℂ N and every s
    with 1/2 < Re s, if χ ≠ 1 or s ≠ 1, then LFunction χ s ≠ 0.
  * `LFunction_eq_zero_re_of_isPrimitive`: for primitive χ, any zero of LFunction χ with 0 < Re s < 1
    has Re s = 1/2.
* The second setup, comparator/, judges the proof against formal-conjectures' earlier statements.
  These are Mathlib's `RiemannHypothesis` and `GRH.generalized_riemann_hypothesis`: for primitive χ
  mod q, every zero of χ.LFunction outside `GRH.trivialZeros χ` has Re s = 1/2. I read that statement
  in formal-conjectures (FormalConjectures/Millennium/RiemannHypothesis.lean, origin/main).

**How the hypotheses follow from the Lean statements.**

* (RH) is Mathlib's `RiemannHypothesis`: every zero of ζ other than −2(n+1), with s ≠ 1, has real
  part 1/2. Those are exactly the classical nontrivial zeros.
* (GRH-D) for nonprincipal χ mod a prime q ≥ 3000 follows by either of two routes:
  * Route A: `GRH.generalized_riemann_hypothesis`, since such χ is primitive. For q ≠ 1, its
    `trivialZeros` are the classical trivial zeros: −2n−1 for odd χ, and −2n for even χ.
  * Route B: `LFunction_ne_zero_of_half_lt_re`, applied to χ and to χ̄, both ≠ 1. Let ρ be a zero of
    ξ(s, χ) = (q/π)^{(s+a)/2} Γ((s+a)/2) L(s, χ). If Re ρ > 1/2, the Gamma factor is finite and
    nonzero, so L(ρ, χ) = 0, which is excluded. If Re ρ < 1/2, the functional equation
    ξ(s, χ) = ε_χ ξ(1 − s, χ̄) (as recalled in LLS §2) gives ξ(1 − ρ, χ̄) = 0 with Re(1 − ρ) > 1/2,
    which is excluded the same way. So Re ρ = 1/2.
  * Both routes identify Mathlib's `DirichletCharacter.LFunction` with the classical L(s, χ), its
    analytic continuation. That identification is standard and was INFERRED, not re-checked against
    Mathlib source here. The repository's NOTES.md also says the statements "were read by hand".

**Certification status, as I read it (this is the one non-mathematical gap).**

* README.md says Comparator checks that Main.lean proves exactly the five Challenge statements, with
  only `propext`, `Quot.sound` and `Classical.choice`, and that Lean's kernel and nanoda accept.
* verification/NOTES.md, at the version I read, still ends with "Results: The build is in progress".
  It says Comparator's output "will be added".
* NOTES.md does record an independent run (ishaan2006, earlier pins). In it, `con-leche --compare`
  reports `RiemannHypothesis.riemannHypothesis` and `GRH.generalized_riemann_hypothesis` as "justified
  by the solution". NOTES.md also says `lake comparator` had not been run on that export.
* The task brief states that the communities certified the RH statement and proof. I did not see a
  completed Comparator verdict recorded in the repository files I read, and I cannot confirm it from
  them.

Hence the wording: unconditional *if the Alpöge Lean theorems are accepted*.

## 7. What this does and does not show

**The problem as posed.** erdosproblems.com/770 (page last edited 24 Sep 2025; fetched 22 Nov 2026)
asks three questions:
  (Q1) does the density δ_p of {n : h(n) = p} exist for every prime p?
  (Q2) is liminf h(n) = ∞?
  (Q3) is it true that if p = P(n) and p > n^ε, then h(n) = p?

* The site says "mutually coprime". As Plasma's page notes, the intended and only nontrivial reading is
  the collective gcd. That reading matches the site's own remark that h(n) = n + 1 iff n + 1 is prime.
  I did not read Erdős 1974 myself.
* Q3 carries no quantifiers. With a fixed ε and all n it is false at small n: h(86) = 5 while
  P(86) = 3, and h(3) = 3 while P(3) = 2. The meaningful reading is "for every ε > 0 and all
  sufficiently large n". Corollary B answers Q3 **yes** in that reading, under RH + GRH-D, and
  unconditionally if the Alpöge theorems are accepted.
* Q1, Q2 and the remark "h(n) = 3 for infinitely many n" are **not** addressed. Q2 is not implied
  either way, because h(n) ≥ P(n) gives nothing for odd n, where P(n) = 2.
* The problem as a whole would move from "open" to at most "partially solved". It would not be solved.

**The Lean statement.** formal-conjectures origin/main (2207c54d, 21 Nov 2026), theorem
`Erdos770.erdos_770.parts.iii`:

    ∀ ε > 0, ∀ᶠ n in atTop, let p := sSup {m : ℕ | m.Prime ∧ m - 1 ∣ n};
      p > (n:ℝ)^(ε:ℝ) → h n = p

Here h n = sInf {m : ℕ∞ | 2 < m ∧ gcd over Icc 2 m.toNat of (i^n − 1) = 1}. Corollary B implies this
statement mathematically. The checks:

* For n ≥ 1, the set {m prime : m − 1 | n} is finite and nonempty, so its ℕ-sSup is the maximum P(n).
* m = ⊤ is excluded from the h-set, because toNat ⊤ = 0 and the gcd over the empty set is 0 ≠ 1.
* For 2 ≤ i and n ≥ 1, the truncated subtraction i^n − 1 is exact.
* So `h n` equals h(n) as defined in §0.
* Whether ε is real or natural in the binder, Corollary B covers it.

**No Lean proof was attempted.** A formal proof would need LLS Thm 1.1(2), which is not in Mathlib.

**Which hypotheses are NOT needed:** no Elliott–Halberstam, pair correlation, simple zeros, Kummer or
Artin GRH, or Hecke or Dedekind L-functions.

## 8. Numerical sanity checks (not load-bearing)

Script: check/check770.py (run with `python3 -I check770.py 3000`). Output: check/out3000.txt.

* Lemma 2(i) holds for every integer 2 ≤ x ≤ 200000, and Lemma 2(ii) for 40 ≤ x ≤ 200000. The
  inequality behind (ii) first holds from x ≈ 23.8 onward, on a grid to x = 200.
* For 1 ≤ n ≤ 3000:
  * h(n) ≥ P(n) always.
  * 1530 values have h(n) ≠ P(n); the largest h among them is h(2855) = 19, with P = 2.
  * The only n with h(n) ≠ P(n) and h(n) > 4 log^2 n is n = 1 (h = 3, P = 2, log 1 = 0).
* h(86) = 5 with P(86) = 3, and h(4044) = 17 with P(4044) = 13. These match the forum (StijnC, 21 Sep
  2025) and the Zeng claim.
* The core of Lemma 4 at small scale: for 3 ≤ n ≤ 3000 and M = max(3, ⌊A log^2 n⌋), with
  A ∈ {4.01, 2, 1}, every prime factor q of D_n(M) has q − 1 | n. This is far below the range where
  Lemma 4 is proved (M ≥ 3000), so it is only a consistency check.
* A grid check of (C1)–(C2), not a proof, suggests n_0(8) ≈ e^{19.4}, and n_0(5) ≈ e^{606}.

## 9. Credit

* **Samuel Korsky**, "Improved Bounds for Cubical Decompositions" (manuscript, 5 Aug 2026; written
  with GPT-5.6 Pro per his post). His Prop. 2.3 (§2.3, "Assume GRH") and the proof of Thm 1.1(ii)
  contain the argument of Lemma 4 and Theorem A, with an unspecified absolute constant.
  * His erdosproblems.com proof-claim notes on #769, submitted 2026-08-05 and read 22 Nov 2026, state
    the #770 consequence explicitly. They say that under GRH, h(n) ≤ max{P(n), C(log n)^2}, so h(n) =
    P(n) "for every fixed positive-power threshold".
  * **The mathematical deduction here is his. What is new in this note:**
    * the observation that its hypothesis is now covered by Alpöge's Dirichlet theorems;
    * a precise list of the L-functions used;
    * an explicit constant A > 4;
    * a self-contained proof of the counting step with an elementary Chebyshev bound.
* **Lamzouri, Li, Soundararajan**: Theorem 1.1(2), which is the analytic input. Ankeny and Bach are the
  classical sources for O((log q)^2); I did not read them.
* **Jeffrey Zeng** (proof claim, 24 Jul 2026, OpenAI internal model): the subgroup observation and
  the unconditional range ε > 1/2. **StijnC** (forum, Sep 2025): the heuristic and the n = 4044 example.
* **Levent Alpöge** (with Claude): the Lean proofs of RH and of GRH for Dirichlet L-functions. The
  leanprover-community riemann-hypothesis maintainers, Comparator, and the independent checkers
  ran the verification.
* Plasma AI's E0770 page (wiki/problems/integer_sequences/E0770/_index.md, last changed in the
  2026-10-19 release) records the Korsky consequence as GRH-conditional only, and leaves the standing
  open.

## 10. Prior-recording check (done 22 Nov 2026)

* **erdosproblems.com/770**: open. The page was last edited 24 Sep 2025. There are 6 comments, all
  StijnC, Sep 2025, all read. They say nothing about GRH. There is 1 proof claim (Zeng, ε > 1/2), and
  the forum is closed to new comments.
* **erdosproblems.com/769 proof claims**: Korsky, GRH-conditional, as quoted above.
* **erdosproblems repository** data/problems.yaml (origin/main 8e3d61bf, 22 Nov 2026): status "open",
  last_update 2025-08-31.
* **formal-conjectures**: `erdos_770.parts.iii` is still tagged `research open`, with a `sorry`.
* **Plasma AI** plasma-ai/erdos: the E0770 page records only the GRH-conditional form. It was last
  changed 2026-10-19, and the latest repository release is 2026-11-16, before Alpöge.
* **ryantuck/erdos-ai**: conjectures/770.lean contains only the statement, last changed 2026-03-09.
  Code search found no other 770 material.
* **arXiv**: NOT CHECKED. The API returned "Rate exceeded" on every query.
* I found no record anywhere of the upgrade from GRH-conditional to unconditional.

## 11. Sources read and not read

**Read (text):**
* Korsky manuscript: ../769/refs/korsky.txt, extracted from korsky.pdf, §§1–2.
* LLS arXiv v3: refs/lls.txt, §§1–3.
* erdosproblems.com: pages 770, the 770 forum, 770 proof claims and 769 proof claims (saved in
  refs/web/).
* Plasma E0770 _index.md: refs/web/plasma_E0770.md.
* formal-conjectures: 770.lean and Millennium/RiemannHypothesis.lean.
* riemann-hypothesis repository: README.md, src/Challenge.lean, verification/NOTES.md.
* ryantuck 770.lean.

**Not read:**
* the arXiv listings (rate-limited), including any arXiv version of Korsky;
* the published Math. Comp. version of LLS;
* Ankeny and Bach;
* Davenport or any textbook (the functional equation is taken as recalled in LLS §2);
* Alpöge's remark.pdf and the Lean proof itself (Main.lean and its 175k files);
* Comparator's final output (not yet posted, per NOTES.md);
* Mathlib's source for `DirichletCharacter.LFunction` (its identification with classical L(s, χ) is
  inferred);
* Erdős 1974 [Er74b] (known only through Plasma's quotation);
* OEIS A263647;
* Ailon–Rudnick;
* Zeng's Lean formalization;
* Plasma's claim subpages for E0770 and its library cards.
