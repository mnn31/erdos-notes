# Erdős 820: golden-ratio lower bound for H(n) under Dirichlet GRH

Written 2026-11-22. Verdict: **the lead survives as stated.** It is a small constant improvement on a
lower bound. It does not solve any open part of Problem 820.

## Final statement

Notation. phi = (1+sqrt5)/2, so log phi = 0.4812118250... . omega*(n) = #{p prime : p-1 | n}.
H(n) is the least l such that some k with 2 <= k < l has gcd(k^n - 1, l^n - 1) = 1. This is the
formal-conjectures definition `Erdos820.H`, which requires k >= 2.

Hypothesis (GRH-D), "GRH for Dirichlet L-functions": for every modulus q >= 1 and every Dirichlet
character chi mod q, L(s, chi) != 0 for Re s > 1/2 (the pole of the trivial character at s = 1 excepted).

**Theorem A.** Assume GRH-D. Then for every eps > 0 there are infinitely many n with

    H(n) > exp( n^{(log phi - eps)/log log n} ).

Equivalently, c_H := limsup_{n->oo} (log log H(n)) (log log n) / log n >= log phi.

**Status of the hypothesis.** RH (zeta alone) does NOT suffice. The proof needs GRH-D for the
characters mod d, with d running over moduli of size about x^{1/2}. Theorem A is **unconditional if the
Alpöge Lean theorem `LFunction_ne_zero_of_half_lt_re` (20 Nov 2026) is accepted**. Lemma 5 shows that
this theorem states exactly GRH-D.

**Corollary B (conditional on Price's unreviewed claim).** Liam Price's proof claim of 16 Jul 2026 says
that H(n) < exp(n^{(log 2 + eps)/log log n}) for every eps > 0 and all large n. If it is correct, then
log phi <= c_H <= log 2, and the formal variant `erdos_820.variants.log_log_exponent` holds with
c = c_H. That variant's answer was already observed by Plasma using the lower constant 0.6736 log 2;
the only new part here is the lower end log phi.

Improvement over the recorded constant: 0.6736 log 2 = 0.46690... (Fan–Pollack (1.4) plus the Fermat
transfer) becomes log phi = 0.48121... .

## Lemmas

**Lemma 1 (Fermat transfer).** Let n >= 1 and 2 <= k < l with gcd(k^n - 1, l^n - 1) = 1. Then
P(n) := prod_{p prime, p-1 | n} p divides kl.

*Proof.* Let p be prime with p - 1 | n. Suppose p divides neither k nor l. Fermat's little theorem gives
k^{p-1} ≡ 1 and l^{p-1} ≡ 1 (mod p). Since p - 1 | n, also k^n ≡ 1 ≡ l^n (mod p). So p divides both
k^n - 1 and l^n - 1. Both are >= 1 because k, l >= 2 and n >= 1. That contradicts the gcd being 1. So
p | k or p | l, and hence p | kl. The primes involved are distinct, hence pairwise coprime, so their
product P(n) divides kl. ∎

**Lemma 2.** For n >= 1, H(n)^2 > P(n).

*Proof.* The defining set is nonempty. For n = 1 take k = 2, l = 3. For n >= 2 take k = 2,
l = 2^n - 1: then l^n ≡ 0 (mod 2^n - 1), so gcd(2^n - 1, l^n - 1) = gcd(2^n - 1, -1) = 1. (This is
`Erdos820.H_spec` in formal-conjectures, which is proved there.) So the least element l = H(n) has a
partner k with 2 <= k < l and gcd(k^n - 1, l^n - 1) = 1. By Lemma 1, P(n) | kl, and kl > 0, so
P(n) <= kl. Since k < l, kl < l^2 = H(n)^2. ∎

**Lemma 3.** If s := omega*(n) >= 32, then log H(n) > s.

*Proof.* P(n) is a product of s distinct primes. The primes up to e^4 = 54.598... are the 16 primes
2, ..., 53. So at least s - 16 of the factors exceed e^4, and the rest are >= 1. Hence
log P(n) >= 4(s - 16). By Lemma 2, 2 log H(n) > log P(n) >= 4s - 64. So log H(n) > 2s - 32 >= s when
s >= 32. ∎

**Lemma 4 (Fan–Pollack, Theorem 1.1, eq. (1.5)).** Assume GRH-D. Then
omega*(n) > exp((log phi + o(1)) log n / log log n) for infinitely many n.

*Citation.* K. Fan and P. Pollack, "The maximal order of the shifted-prime divisor function",
arXiv:2510.14167v1 (15 Oct 2025; v1 is the only arXiv version), p. 3, Theorem 1.1, (1.5). Plasma
records the journal version as Integers 26A (2026) #A9; I did not read that version.

*Hypothesis check (VERIFIED in the text).* The theorem says "if GRH is true". On p. 1 (the abstract,
and again in the introduction) "GRH" is defined as "the Generalized Riemann Hypothesis for Dirichlet
L-functions".

*Audit of the GRH branch (Section 3, pp. 4–7; VERIFIED by reading; checks are mine).*
- The only analytic input is the estimate quoted on p. 3 and p. 5 from [13] = Montgomery–Vaughan,
  Corollary 13.8: pi(x; d, 1) = Li(x)/phi(d) + O(sqrt(x) log x). It is applied only to squarefree
  d | k with d <= x^{1/2}/(log x)^3, and only in the lower-bound form
  pi(x; d, 1) >> x/(phi(d) log x). The moduli d vary with x, so characters to many moduli are needed,
  and zeta alone is not enough.
- Range check. d ∈ D means |log d - (1/2 - eps) log x| < 2L/(log L)^2, where L = (u - eps) log x and
  eps = (log log x)^{-1/2}. The saving is eps log x = log x/(log log x)^{1/2}. It beats both
  2L/(log L)^2 ≍ log x/(log log x)^2 and 3 log log x, so d <= x^{1/2}/(log x)^3 for large x.
- Counting m. Write m = (k/d) m' with gcd(m', d) = 1. Since k is squarefree, gcd(m, k) = k/d.
  Different d therefore give disjoint sets of pairs. The count of m' is
  (phi(d)/d)(x^u/k) + O(tau(d)). Here x^u/k = exp(eps log x + O(L/(log L)^3)), and
  tau(d) <= 2^{pi(L)} = exp(O(log x/log log x)). So the main term dominates.
- Pigeonhole. Each pair (m, p) gives a multiple n = m(p-1) of k with n <= N := x^{u+1}/min_{d∈D} d. For a
  fixed n, distinct pairs have distinct p, each with p - 1 | n. So some n <= N has
  omega*(n) >= (sum_d A_d)/(N/k) = #D · exp(O(log x/(log log x)^2))/log x. Also n >= k → oo as x → oo,
  which gives infinitely many distinct n.
- Entropy count, (3.7)–(3.10). Chebyshev gives P(|log d - E log d| > L^{2/3}) << L^{-1/3} log L and
  P(|Omega(d) - rho R| > R^{2/3}) <= R^{-1/3}. Each surviving d has mass
  rho^{rho R}(1-rho)^{(1-rho)R} e^{O(R^{2/3})}, since log(rho/(1-rho)) is bounded. So
  #D >= exp(R·h(rho) - O(R^{2/3})), where h is the binary entropy, rho → 1/(2u) and
  R = (u + o(1)) log x/log log x. Then R h(rho) = (u h(1/(2u)) + o(1)) log x/log log x, and
  u h(1/(2u)) = (1/2) log 2u + (u - 1/2) log(2u/(2u-1)) = C. With u = (3+sqrt5)/4 we have
  2u = phi^2 and 2u/(2u-1) = phi, so C = (u + 1/2) log phi. I checked this algebra by hand and
  numerically (below).
- Final step. log X = (u + 1/2) log x and N = X^{1+o(1)}. Since t/log t is increasing for t >= e,
  this gives omega*(n) >= exp((log phi + o(1)) log n/log log n).
- Plasma flags one printed issue in this paper: the L^{2/3} window in (3.17) of the *unconditional*
  branch. In the GRH branch, (3.7) explicitly adds the O(L/(log L)^3) expectation error and states a
  window of 2L/(log L)^2. That is consistent with the PNT error, so the flag does not affect (1.5).

**Lemma 5 (the hypothesis is exactly what the Alpöge theorem states).** VERIFIED from
leanprover-community/riemann-hypothesis, main at c592e91 (2026-11-23T04:24Z), file `src/Challenge.lean`.
`LFunction_ne_zero_of_half_lt_re : DirichletLNonvanishingRightOfHalf`, where the latter is defined as:
for all N with NeZero N, every `χ : DirichletCharacter ℂ N` and every s, if 1/2 < s.re and
(χ ≠ 1 or s ≠ 1), then `DirichletCharacter.LFunction χ s ≠ 0`. The Mathlib docstring
(`Mathlib/NumberTheory/LSeries/DirichletContinuation.lean`) describes `LFunction χ` as the unique
meromorphic function agreeing with sum χ(n) n^{-s} where that converges (`LFunction_eq_LSeries` for
Re s > 1). It is defined for every character mod N, imprimitive ones included. So the theorem is GRH-D
word for word. The same file also states `LFunction_eq_zero_re` (all zeros with 0 < Re s < 1 lie on
Re s = 1/2) and its primitive version. So the "nontrivial zeros on the line" form of GRH is covered too.
The README says Comparator checks these statements, the three standard axioms, and acceptance by both
Lean's kernel and nanoda. I did NOT build or run it myself.

## Proof of Theorem A

Fix eps > 0. By Lemma 4 (under GRH-D) there are infinitely many n with
omega*(n) > exp((log phi - eps/2) log n/log log n) = n^{(log phi - eps/2)/log log n}. Along these n,
omega*(n) → oo, so omega*(n) >= 32 for all but finitely many of them. For those n, Lemma 3 gives
log H(n) > omega*(n) > n^{(log phi - eps/2)/log log n} > n^{(log phi - eps)/log log n}. Hence
H(n) > exp(n^{(log phi - eps)/log log n}). ∎

Corollary B: by Theorem A, for every eps there are infinitely many n with
(log log H(n))(log log n)/log n > log phi - eps, so c_H >= log phi. Price's claim gives c_H <= log 2.
If c_H is finite and positive, the definition of limsup gives both halves of `log_log_exponent` with
c = c_H. (The same limsup argument is Plasma's "growth_constant" page.)

## Numerical checks (checks/num.py, checks/fermat.py; Python -I)
- max over t > 1/2 of f_{1/2}(t) (the paper's (3.12)) is 0.481211825 at t ≈ 1.3090 = (3+sqrt5)/4. It
  equals log phi to 1e-16. f_{0.4736} has max 0.46694 at t ≈ 1.2694, which reproduces the paper's
  0.4669. Also 0.6736 log 2 = 0.466904.
- C = (u + 1/2) log phi = u·h(1/(2u)) = 0.8705203694. Also 2u = phi^2 and 2u/(2u-1) = phi exactly.
  f_{1/2}(t) = t h(1/(2t))/(t + 1/2) at four test points.
- Brute force over 1 <= n <= 36: H(n) matches the listed values 3,3,3,6,3,18,3,6,3,12 for n <= 10.
  H(n)^2 > P(n) always (for example n = 36: H = 1406, sqrt P = 1385.35). Among all coprime pairs with
  l <= H(n) + 5 there is no case where P(n) fails to divide kl.

## What this does and does not show
- It improves only the infinitely-often lower bound in the "estimate H(n)" part. It says nothing about
  the main question `erdos_820` (H(n) = 3 infinitely often, i.e. gcd(2^n - 1, 3^n - 1) = 1 infinitely
  often), nothing about K(n) (`two_pow_upper`), and gives no upper bound.
- Lean statement `log_log_exponent` asks only whether some c exists. That question was already
  answerable (yes, if Price is right) from 0.6736 log 2 > 0. This result only narrows c = c_H to
  [log phi, log 2]. It does not determine c_H. The formal-conjectures file (origin/main 2207c54,
  21 Nov 2026) has no variant for any Fan–Pollack or van Doorn lower bound, and I did not formalize
  this.
- INFERRED, not load-bearing: log phi is the best constant this method gets from GRH-D. Fan–Pollack
  Section 4 gives the exponent max_{t>=theta} f_theta(t) when (4.1) holds at level theta. GRH-D gives
  level theta = 1/2, and the maximum at theta = 1/2 is log phi. Pushing the level for individual moduli
  past 1/2 is not known even under GRH. My guess that average results (Bombieri–Vinogradov type) do not
  help, because D has only x^{o(1)} members, was not checked against the literature.
- Significance: modest. It is a two-line corollary of a published conditional theorem whose GRH branch
  Plasma already catalogs. What is new is only the H(n) consequence of that branch and the fact that it
  is now unconditional. Whether it is unconditional depends on the community's acceptance of the Alpöge
  proof.
- Prior recording (checked 22 Nov 2026). erdosproblems.com/820 page, forum (comments frozen) and the
  proof-claims page: only van Doorn's c > 0 and "0.67 log 2", no GRH. Plasma E0820 index: c_H in
  [0.6736 log 2, log 2], with "the GRH-conditional theorem is kept separate". The Plasma Fan–Pollack card
  has the GRH branch for omega* only; its H(n) corollary uses 0.6736 log 2. No mention of Alpöge.
  arXiv: v1 is the only version of 2510.14167. An arXiv search for "shifted-prime divisor" shows nothing
  newer on the maximal order (the only later hit, 2607.08985, is about sums of two prime squares). The
  arXiv API was rate-limited, so this used the web search page. The erdosproblems database entry
  (8e3d61b) lists the problem as open, last updated 2025-08-31.

## Credit
- Fermat transfer omega*(n) → H(n): Erdős [Er74b] (per Plasma's reading); W. van Doorn, forum comment,
  15 Oct 2025 (with Adleman–Pomerance–Rumely); van Doorn, 17 Jul 2026 (with the Fan–Pollack constant).
- omega* lower bound under GRH: K. Fan and P. Pollack, Theorem 1.1 (1.5), building on Prachar (1955).
- GRH-D: L. Alpöge (Lean 4, 20 Nov 2026, found with Claude); Comparator setup by the
  leanprover-community riemann-hypothesis project.
- The c_H limsup framing: Plasma AI wiki (growth_constant page). Upper bound: Liam Price's claim (proof
  credited to GPT 5.6 Sol Pro, Lean to Claude Fable 5).
- The combination written here (Lemma 4 GRH branch + transfer + Lemma 5) is this note's only
  contribution.

## Sources not read
- Montgomery–Vaughan, *Multiplicative Number Theory I*, Corollary 13.8: not accessed. Its statement and
  uniformity in d are taken from Fan–Pollack's quotation (pp. 3, 5). From memory (UNVERIFIED), MV's
  standing hypothesis there is GRH for all characters mod q. By Lemma 5 both standard forms are covered.
- Alpöge's proof itself (alpo.ge/remark.pdf, the `original` branch): not read. I read only the repo
  README and the statements in `src/Challenge.lean`, and did not build or run Comparator.
- Price's manuscript and its Lean file: not read. I read only the forum claim summary and Plasma's
  description.
- Integers 26A #A9 (the published version of Fan–Pollack), Erdős [Er74b], Adleman–Pomerance–Rumely
  Prop. 10, and Plasma's growth_constant and full h_n_corollary pages: not read, or read only in part.
- Sutherland's GRH page: not consulted (not relevant).
