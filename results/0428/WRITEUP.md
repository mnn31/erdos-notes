# Erdős Problem 428: under RH, the liminf is at most 1/2

Written 2026-11-22. Status of this file: a complete proof of a CONDITIONAL partial bound.
It does not resolve Problem 428.

## 0. Setup and notation

- N = positive integers. For a set A ⊆ N call an integer n ≥ 2 **good for A** if n − a is prime
  for every a ∈ A with 0 < a < n. Call A **admissible** if infinitely many n are good for A.
- π(y) = number of primes ≤ y. θ(y) = Σ_{p ≤ y} log p (sum over primes).
- E(y) := √y · (log y)² / (8π) for real y ≥ 1. Both factors √y and (log y)² are non-negative and
  non-decreasing on [1, ∞), so E is non-decreasing on [1, ∞).
- **RH** means: every zero ρ of the Riemann zeta function with 0 < Re ρ < 1 has Re ρ = 1/2.
  Only RH for ζ is used. GRH for Dirichlet L-functions is not used anywhere.

## 1. Exact statement

**Theorem.** Assume RH. Let A ⊆ N be admissible. Then

    liminf_{x→∞} |A ∩ [1,x]| / π(x)  ≤  1/2.

More precisely: there is an absolute N₀ such that for every n ≥ N₀ that is good for A, with
x = x(n) := ⌈√n (log n)³⌉ and L := log n,

    |A ∩ [1,x]| / π(x)  ≤  (1 + 1/(4πL)) · (1 − (1/2 + E(x))/x)^{-1} · (L/2 + 3 log L + log 2) / (L − log 2),

and the right side tends to 1/2 as n → ∞.

The theorem says nothing about whether an admissible A with positive liminf exists.

## 2. Lemmas

**Lemma 1 (Büthe 2016, Theorem 2; this is Schoenfeld's 1976 bound).** Assume RH. For every real
y > 599 that is not a prime number,

    |θ(y) − y| ≤ E(y) = √y (log y)² / (8π).

*Citation and hypothesis check.* J. Büthe, "Estimating π(x) and related functions under partial RH
assumptions", arXiv:1410.7015v4, Theorem 2 (Section 7). I read the statement and its proof in the
arXiv v4 text (saved in refs/buthe/). The theorem says: if T > 0 is such that RH holds for all zeros
with 0 < Im ρ ≤ T, and 4.92·√(x/log x) ≤ T, then |ϑ(x) − x| ≤ (√x/(8π)) log(x)² for x > 599.
Under full RH the hypothesis holds for every T > 0, so for a given y > 599 take
T = 4.92·√(y/log y) > 0. The only mismatch with the standard θ is a normalisation: Büthe's ϑ is
Σ_p χ*_{[0,x]}(p) log p, where χ* counts the endpoint with weight 1/2 (his Section 2 and the
display at the start of Section 7). So Büthe's ϑ(y) equals the standard θ(y) exactly when y is not
a prime. That is why Lemma 1 is stated only for non-prime y; below it is applied only at
half-integers. Büthe's proof of Theorem 2 uses computer checks for x below 10^19; I did not rerun
them. Only arbitrarily large y matter for the liminf.

**Lemma 2 (injection).** Let n be good for A and let x be an integer with 1 ≤ x < n. Then

    |A ∩ [1,x]| ≤ #{primes p : n − x ≤ p ≤ n − 1}.

*Proof.* If a ∈ A ∩ [1,x] then 0 < a ≤ x < n, so n − a is prime because n is good, and
n − x ≤ n − a ≤ n − 1. The map a ↦ n − a is injective. ∎

**Lemma 3 (primes in the window, upper bound).** Assume RH. Let n, x be integers with x ≥ 1 and
n − x ≥ 601. Then

    #{primes p : n − x ≤ p ≤ n − 1} ≤ (x + 2E(n)) / log(n − x).

*Proof.* Let P be that set of primes. Each p ∈ P has log p ≥ log(n − x) > 0, so
|P| · log(n − x) ≤ Σ_{p∈P} log p. The primes in P are exactly the primes in the real interval
(n − x − 1/2, n − 1/2], so Σ_{p∈P} log p = θ(n − 1/2) − θ(n − x − 1/2). Both n − 1/2 and
n − x − 1/2 are non-integers, hence not prime, and both exceed 599 (the smaller is ≥ 600.5).
Lemma 1 gives θ(n − 1/2) ≤ n − 1/2 + E(n − 1/2) and θ(n − x − 1/2) ≥ n − x − 1/2 − E(n − x − 1/2).
Subtracting, and using that E is non-decreasing on [1,∞),

    Σ_{p∈P} log p ≤ x + E(n − 1/2) + E(n − x − 1/2) ≤ x + 2E(n).  ∎

**Lemma 4 (lower bound for π).** Assume RH. For every integer x ≥ 600,

    π(x) ≥ (x − 1/2 − E(x)) / log x.

*Proof.* Every prime p ≤ x has log p ≤ log x, so π(x) log x ≥ θ(x) ≥ θ(x − 1/2). The number
x − 1/2 is a non-integer > 599, so Lemma 1 gives θ(x − 1/2) ≥ x − 1/2 − E(x − 1/2) ≥ x − 1/2 − E(x). ∎

(Lemma 4 is far weaker than the prime number theorem; it is derived from Lemma 1 only so that the
whole proof rests on one cited estimate.)

## 3. Proof of the Theorem

Assume RH and let A be admissible. Let n be good for A, put L = log n and x = ⌈√n L³⌉, so
√n L³ ≤ x < √n L³ + 1. Since √n (log n)³ / n → 0, there is an absolute N₀ such that for all
n ≥ N₀:

  (a) 600 ≤ x ≤ n/2 (so in particular x < n and n − x ≥ n/2 ≥ 601), and
  (b) x ≤ 2√n L³, and
  (c) (1/2 + E(x))/x < 1 (true for every x ≥ 600, since E(x)/x = (log x)²/(8π√x) < 0.07 there
      and it is decreasing for x ≥ e⁴).

Take a good n ≥ N₀. By Lemma 2 and Lemma 3,

    |A ∩ [1,x]| ≤ (x + 2E(n)) / log(n − x).

By Lemma 4 and (c), π(x) ≥ (x − 1/2 − E(x))/log x > 0. Dividing,

    |A ∩ [1,x]| / π(x) ≤ [(1 + 2E(n)/x) / (1 − (1/2 + E(x))/x)] · [log x / log(n − x)].      (*)

Now bound each piece.

  (i)   2E(n)/x ≤ (√n L²/(4π)) / (√n L³) = 1/(4πL).
  (ii)  (1/2 + E(x))/x = 1/(2x) + (log x)²/(8π√x) → 0 as x → ∞, and x ≥ √n L³ → ∞ as n → ∞.
  (iii) log(n − x) ≥ log(n/2) = L − log 2, by (a).
  (iv)  log x ≤ log(2√n L³) = L/2 + 3 log L + log 2, by (b).

Putting (i), (iii), (iv) into (*) gives the displayed bound in the Theorem, and with (ii) its right
side tends to (1)(1)(1/2) = 1/2 as n → ∞.

Because A is admissible there are good n_1 < n_2 < ... → ∞. The integers x_k := x(n_k) tend to
infinity, and |A ∩ [1,x_k]|/π(x_k) ≤ 1/2 + o(1). Hence liminf_{x→∞} |A ∩ [1,x]|/π(x) ≤ 1/2.
(The liminf over real x and over integer x agree, since both |A ∩ [1,x]| and π(x) are constant on
each [m, m+1).) ∎

A numerical sanity check of Lemmas 3 and 4 against a sieve up to 2·10⁶ found no violations. This is
a check on transcription, not part of the proof.

## 4. What this does and does not show

**Shows.** Under RH for ζ: any A for which infinitely many n have all n − a (a ∈ A, 0 < a < n)
prime satisfies liminf |A ∩ [1,x]|/π(x) ≤ 1/2. So IF the answer to Problem 428 is yes, the liminf
in question lies in (0, 1/2].

**Does not show.**
- It does not answer Problem 428. The problem asks whether some admissible A has liminf > 0.
  This theorem neither constructs such an A nor rules one out. Problem 428 stays open.
- It does not show 1/2 is sharp, and it gives no lower bound of any kind.
- It is conditional on RH. The brief for this write-up says RH for ζ has been proved in Lean
  (announcement dated 20 November 2026). I did not check that proof. What I read is the saved copy
  (refs/sutherland.html) of the verification page at math.mit.edu/~drew/grh/, which reports that a
  Lean theorem `riemannHypothesis : RiemannHypothesis` (Mathlib's definition) compiles and is
  accepted by several kernels, with some checks marked as still running at 2026-11-22 16:20 UTC.
  Mathlib's `RiemannHypothesis` (every zero of ζ other than −2, −4, ... and s ≠ 1 has real part
  1/2) implies RH as defined in Section 0. If that proof stands, the Theorem is unconditional.
  I state it as conditional because that is the part I verified.

**Relation to the problem as posed.** The page (erdosproblems.com/428, read in refs/page.html) asks:
is there A ⊆ N such that for infinitely many n all n − a with a ∈ A, 0 < a < n are prime, and
liminf |A ∩ [1,x]|/π(x) > 0? The hypothesis "admissible" here is exactly the first condition.

**Relation to the Lean statement.** `Erdos428.erdos_428` (formal-conjectures origin/main) is
∃ A : Set ℕ, (∃ᶠ n in atTop, ∀ a ∈ A, 0 < a → a < n → (n − a).Prime) ∧
liminf (fun n ↦ (A ∩ Icc 1 n).ncard / primeCounting n) atTop > 0, tagged `research open`.
The first conjunct is "admissible" (elements a = 0 of A are ignored there too). The Theorem gives,
for every A satisfying the first conjunct, that the sequence f(m) = |A ∩ [1,m]|/π(m) has
f(x_k) ≤ 1/2 + o(1) along x_k → ∞. For a real sequence Mathlib's `liminf f atTop` is
sSup {a | ∀ᶠ m, a ≤ f m}. Every a in that set satisfies a ≤ f(x_k) for large k, hence a ≤ 1/2,
and the set is non-empty (it contains 0 because f ≥ 0), so the Lean liminf is ≤ 1/2 as well. This
does not prove or disprove `erdos_428`; it would be a separate lemma of the form
"first conjunct → liminf ≤ 1/2". Nothing here has been formalised or compiled in Lean.

**Relation to what was already on record.** The forum thread (refs/forum.html) has: Will Sawin
(3 Jul 2026), the argument that a short-interval prime number theorem for intervals of length n^δ,
for every δ > 0, would give a negative answer; Steve Fan (3 Jul 2026), that the same argument with
Guth–Maynard's exponent gives liminf ≤ 17/30 unconditionally. The Theorem replaces 17/30 by 1/2 at
the cost of assuming RH. It is the same argument with a different short-interval input; the only
changes are (1) the input is the RH error term, and (2) the window x = √n (log n)³ is taken just
above √n instead of n^δ with δ ↓ 1/2, which avoids a second limit.

**Why this method stops at 1/2 (remark, not a theorem).** The argument compares |A ∩ [1,x]| with the
number of primes in a window of length x below n, and gives liminf ≤ (log x / log n) · C, where
C·x/log n is an upper bound for primes in the window. RH gives C = 1 + o(1) only when
x/(√n (log n)²) → ∞ in the form used here, which forces log x/log n ≥ 1/2. To go below 1/2 one
would need an upper bound with constant close to 1 for primes in intervals of length n^{1/2 − ε},
which I do not know to follow from RH. Brun–Titchmarsh (constant 2·log n/log x) only gives the
bound 2 that Fan already noted for the limsup.

**Novelty.** I did not search the literature for this corollary. It is a two-line consequence of the
Sawin–Fan forum argument and should be described as such, not as a new method.

## 5. Credit

- Will Sawin and Steve Fan (erdosproblems.com forum thread 428, 3 July 2026): the argument
  (Lemma 2 plus comparison of a short-interval prime count with π(x)), and the 17/30 version.
- H. von Koch (1901) and L. Schoenfeld (1976): the RH error term for ψ, θ, π, in O-form and in the
  explicit form with constant 1/(8π). J. Büthe (2016): the version with a full proof that I
  actually read and cite as Lemma 1.
- L. Guth and J. Maynard: the unconditional short-interval asymptotic at exponent 17/30 behind
  Fan's bound (context only; not used in the proof).
- The RH proof itself, if it stands: its authors (announcement at alpo.ge/remark.pdf per the
  verification page; not read).
- Nothing in Sections 2–3 beyond bookkeeping is original to this write-up.

## 6. Sources

**Read (text checked):**
- erdosproblems.com/428 and forum thread 428, saved copies refs/page.html, refs/forum.html
  (fetched 2026-11-22). Problem statement, Sawin's and Fan's comments.
- formal-conjectures origin/main, FormalConjectures/ErdosProblems/428.lean. Lean statement.
- erdosproblems origin/main data/problems.yaml, entry "428": status open.
- J. Büthe, arXiv:1410.7015v4 (25 May 2022), refs/buthe/. Theorem 2 statement and proof, and the
  definition of ϑ with the half-weight endpoint convention.
- arXiv:2405.20552 abstract page (Guth–Maynard), refs/gm/gm_abs.html. Abstract only: it states
  asymptotics for primes in short intervals of length x^{17/30+o(1)}.
- refs/sutherland.html (saved copy of math.mit.edu/~drew/grh/; a live re-fetch on 2026-11-22
  returned a page of the same size with the same "last updated" line). Verification status only.

**Sources not read:**
- H. von Koch, "Sur la distribution des nombres premiers", Acta Math. 24 (1901). Not obtained.
  Not relied on; Lemma 1 is cited to Büthe instead.
- L. Schoenfeld, "Sharper bounds for the Chebyshev functions θ(x) and ψ(x). II", Math. Comp. 30
  (1976), and its corrigendum. The AMS site returned a bot-check page (HTTP 403) and I did not go
  around it. Not relied on; Büthe's Theorem 2 reproves the same bounds.
- The journal version of Büthe's paper (I believe Math. Comp. 85 (2016); bibliographic details are
  from memory and unchecked). I read the arXiv v4 only.
- The body of Guth–Maynard (which numbered result gives the short-interval asymptotic). Abstract
  only. This affects only the comparison "17/30", not the Theorem.
- Erdős–Graham 1980 [ErGr80], the original source of the problem and of the limsup result under
  the prime k-tuple conjecture. Not obtained.
- The RH/GRH Lean proof and its announcement (alpo.ge/remark.pdf). Not read, not rebuilt.
- No general literature or web search was done for prior statements of this corollary.
