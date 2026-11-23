# Erdős #455: the GRH clauses of satorunet's Section 6, written out (2026-11-22)

**Verdict: the lead holds.** All three GRH statements (Theorem A, Theorem C, finite shifts) follow from
RH plus GRH for Dirichlet L-functions, via Lamzouri–Li–Soundararajan (LLS) Theorem 1.4. They are therefore
**unconditional if the Alpöge Lean theorems (20 Nov 2026) are accepted.** The proofs below need fewer
hypotheses than satorunet's. They do not use nondecreasing gaps, the window [Y,2Y], or any size bound on h.
The two degenerate cases (a linear or square-discriminant quadratic) and the
distinct-primes step in the CRT argument are now handled.
Nothing here is new **as a conditional statement**: satorunet's page already states all three GRH forms.
The new part is the change of status, together with the details and explicit constants.
Nothing here touches the problem itself: the main statement and the liminf constant are unchanged.

## Hypotheses used

* **(RH)** all nontrivial zeros of ζ(s) have real part 1/2.
* **(GRH-Dir)** for every primitive Dirichlet character χ̃, all nontrivial zeros of L(s,χ̃) have real part 1/2.

These are what LLS assume. I read their Section 2 (Lemmas 2.1 and 2.4 assume RH; Lemmas 2.2 and 2.3 assume
GRH for a primitive χ mod q ≥ 3) and Section 4, the proof of Thm 1.4. In Section 4, GRH is applied to the
primitive characters χ̃ that induce the non-principal characters of H̃, the group of characters trivial on H.
In every application below h = 2, so H̃ = {χ₀, χ}. **The only L-functions involved are therefore ζ(s) and one
real (quadratic) primitive Dirichlet L-function L(s,χ̃) per application.** This is the Kronecker character of
Q(√D) for a discriminant D, or χ₄. I did not re-audit the proofs of Lemmas 2.2–2.4 line by line. Whatever they
use, it lies inside RH + GRH-Dir.

**Status.** The certified statements in leanprover-community/riemann-hypothesis are `RiemannHypothesis`,
`DirichletLZerosOnLine` and `PrimitiveDirichletLZerosOnLine`. I read these in `src/Challenge.lean`. They say that
every zero of ζ, or of L(χ,s) for any (primitive) Dirichlet character of any modulus, with 0 < Re s < 1 has
Re s = 1/2. Two classical facts link these to (RH) and (GRH-Dir) as LLS use them: nontrivial zeros of a
primitive L(s,χ̃) lie in 0 < Re s < 1, and Mathlib's `DirichletCharacter.LFunction` is the classical L-function.
I did not build the Lean proof or run comparator myself. So the statements below are:
**"assume RH and GRH for Dirichlet L-functions"; unconditional if the Alpöge Lean theorems are accepted.**

## Notation

For q ≥ 3 put f(q) = (log q + 9 + (5/2)(log log q)²)². This is LLS Thm 1.4 with h = 2:
(h−1)log q + 3(h+1) = log q + 9. f is increasing on q ≥ 20000. Define

  **B(q) := max(10⁹, f(max(q, 20000)))**, which is nondecreasing in q.

Asymptotically B(q) = (1+o(1)) (log q)². Caveat: f(q) > 10⁹ only once log q > ~31346. For every realistic
size, B(q) = 10⁹ exactly. All the "≪ log² Y" statements are asymptotic in this sense.

For a sequence of primes x₀ < x₁ < … < x_L, write g_j = x_{j+1} − x_j for 0 ≤ j ≤ L−1, and
e_j = g_{j+1} − g_j for 0 ≤ j ≤ L−2.

## Lemma 1 (quadratic character for an arbitrary discriminant)

Let D ≠ 0 be an integer. Write D = ε·2^e·m with ε = ±1 and m odd and positive. Let q be a positive integer
with 8m | q. Then there is a homomorphism χ_D : (Z/qZ)* → {±1} such that χ_D(p) = (D/p) (Legendre symbol)
for every prime p ∤ q.

*Proof.* Units mod q are odd because 8 | q. For a unit n, define

  χ_D(n) = χ₄(n)^{[ε=−1]} · χ₈(n)^e · J(n | m) · χ₄(n)^{[m ≡ 3 mod 4]}.

Here χ₄ and χ₈ are the characters mod 4 and mod 8 with χ₄(n) = (−1)^{(n−1)/2} and χ₈(n) = (−1)^{(n²−1)/8}.
J is the Jacobi symbol, and [·] is 1 if the condition holds and 0 otherwise.

Each factor depends only on n mod q, because 4 | q, 8 | q and m | q. For J this is Mathlib
`jacobiSym.mod_left`. Each factor is multiplicative in n; for J this is `jacobiSym.mul_left`. So χ_D is a
homomorphism.

Now take a prime p ∤ q. Then p is odd and p ∤ D. Mathlib `legendreSym.to_jacobiSym` and `jacobiSym.mul_left`
give

  (D/p) = J(ε|p)·J(2|p)^e·J(m|p).

`jacobiSym.at_neg_one` gives J(−1|p) = χ₄(p), and `jacobiSym.at_two` gives J(2|p) = χ₈(p).
`jacobiSym.quadratic_reciprocity` applies to the odd naturals m and p. It gives
J(m|p) = (−1)^{⌊m/2⌋⌊p/2⌋}·J(p|m) = χ₄(p)^{[m≡3 mod 4]}·J(p|m).

Multiplying these gives χ_D(p). These are the Mathlib statements I read in
`Mathlib/NumberTheory/LegendreSymbol/JacobiSymbol.lean`. ∎

Numerical check: 89,964 random pairs with |D| ≤ 10⁷ and p < 5·10⁴, p ∤ 8D, gave 0 mismatches. Spot checks of
multiplicativity and periodicity mod 8|D| also passed (`check1.py`).

## Lemma 2 (a small split prime; RH + GRH-Dir)

Let q ≥ 4 with 4 | q, and let χ : (Z/qZ)* → {±1} be a homomorphism. Then some prime p ∤ q has χ(p) = 1 and
p ≤ B(q).

*Proof.* Put G = (Z/qZ)*. If χ is nontrivial, let H = ker χ. If χ is trivial, let H = ker χ₄. χ₄ is
well defined because 4 | q, and it is nontrivial because χ₄(−1) = −1. Either way [G : H] = 2.

*Case q ≥ 20000.* LLS (arXiv:1309.3595v3) Theorem 1.4 assumes GRH, q ≥ 20000 and a subgroup H of index
h > 1. It says the least prime p lying in a coset aH satisfies p ≤ 10⁹ or
p ≤ ((h−1)log q + 3(h+1) + (5/2)(log log q)²)². I read this from the rendered page 3 of the PDF, not only the
pdftotext output. Take a = 1 and h = 2. A prime lying in H is a unit mod q, so p ∤ q. Since H ⊆ ker χ,
χ(p) = 1. And p ≤ max(10⁹, f(q)) = B(q).

*Case q < 20000.* The least prime p ≡ 1 (mod q) lies in every subgroup, so χ(p) = 1, and p ∤ q.
I computed it for every 3 ≤ q < 20000 (`check1.py`). The maximum is 1,551,499, at q = 19891, which is below
10⁹ ≤ B(q). This case is unconditional. ∎

## Lemma 3 (a polynomial of degree ≤ 2 cannot be prime for long)

Let Q(t) = at² + bt + c ∈ Z[t] be nonconstant. Let n ≥ 1, and suppose Q(0), …, Q(n−1) are all prime and all
greater than n. Define q_Q = 4|b| if a = 0. If a ≠ 0, define Δ = b² − 4ac and set q_Q = 4|a| when Δ = 0 and
q_Q = 8|a||Δ| when Δ ≠ 0. Then, under RH + GRH-Dir, **n < B(q_Q)**. If moreover n ≥ 3 and every Q(t) ≤ X,
then q_Q < 64X³, so **n < B(64X³)**.

*Proof.* In each case below I find a prime p ≤ B(q_Q) and a residue r with Q(r) ≡ 0 (mod p). Suppose
n ≥ p. Then some t ∈ [0, n−1] has t ≡ r (mod p). So p | Q(t), and Q(t) is a prime greater than n ≥ p.
This is a contradiction, so n < p ≤ B(q_Q).

* *a = 0.* Here b ≠ 0. Apply Lemma 2 with q = 4|b| and χ trivial. This needs q ≥ 4, which holds since
  |b| ≥ 1. It gives a prime p ∤ 4b, and r ≡ −c·b⁻¹ (mod p) works.
* *a ≠ 0, Δ = 0.* Apply Lemma 2 with q = 4|a| and χ trivial: p ∤ 4a, so p is odd and 2a is invertible
  mod p. Since 4aQ(t) = (2at+b)² − Δ = (2at+b)², the choice r ≡ −b(2a)⁻¹ (mod p) works.
* *a ≠ 0, Δ ≠ 0.* q = 8|a||Δ| is divisible by 8m (m = odd part of |Δ|) and by 4. Apply Lemma 2 with χ = χ_Δ
  from Lemma 1. It gives p ∤ q with (Δ/p) = χ_Δ(p) = 1. So p is odd, p ∤ a, and Δ ≡ s² (mod p) for some s.
  Then r ≡ (s − b)(2a)⁻¹ (mod p) gives p | 4aQ(r), hence p | Q(r).

For the explicit bound, let Q(0), Q(1), Q(2) ∈ [1, X]. Then:
* 2a = Q(2) − 2Q(1) + Q(0), so |a| < X;
* b = (Q(1) − Q(0)) − a, so |b| < 2X;
* 1 ≤ c ≤ X, so |Δ| ≤ b² + 4|a|c < 8X².

Hence each of 4|b|, 4|a| and 8|a||Δ| is below 64X³. Since B is nondecreasing, n < B(64X³). ∎

Numerical check (`check2.py`): every quadratic x + td + t(t−1) with x < 2·10⁵, d < 3000 and values below
4·10⁷ gave n < p*(Δ), where p*(Δ) is the least odd prime with (Δ/p) ≠ −1. That is 1,016,569 runs with n ≥ 3
and no violation. The longest run, n = 40, is Euler's t² + t + 41 (x = 41, d = 2, Δ = −163), and there
p* = 41. On 1,200 random a t² + b t + c with 1 ≤ a ≤ 60 there were 0 violations.

## Theorem A (few modifications)

Let x₀ < … < x_L be primes with x₀ > L + 1, and set X = x_L. Let k = #{0 ≤ j ≤ L−2 : e_j ≠ 2}. Under
RH + GRH-Dir,

  **L ≤ (k+1)(B(8X²) − 2)**, so L ≪ (k+1) log² X.

Nondecreasing gaps are **not** needed.

*Proof.* Assume L ≥ 2; otherwise the bound is trivial, since B ≥ 10⁹.

The k indices with e_j ≠ 2 cut {0, …, L−2} into at most k+1 maximal intervals with e_j = 2, some possibly
empty. Take one of them, [s, s+m−1], with m ≥ 1. Put x = x_s and d = g_s. Then g_{s+i} = d + 2i for 0 ≤ i ≤ m,
so x_{s+t} = x + td + t(t−1) =: F(t) for 0 ≤ t ≤ m+1. That is n = m + 2 ≥ 3 consecutive prime values, each
≥ x₀ > L+1 ≥ n.

Here a = 1 and Δ = (d−1)² − 4x. Since x₀ > 2, every x_j is odd and every gap is even. So (d−1)² ≡ 1 and
4x ≡ 4 (mod 8), which gives Δ ≡ 5 (mod 8), and in particular Δ ≠ 0. Also |Δ| ≤ max((d−1)², 4x) < X² when
X ≥ 4, because d, x < X.

Lemma 3 with q_Q = 8|Δ| < 8X² gives m + 2 < B(8X²). Summing over the intervals,
L − 1 ≤ k + (k+1)(B(8X²) − 3), so L ≤ (k+1)(B(8X²) − 2). ∎

## Theorem C (equal block moments; includes periodic words)

Let x₀ < … < x_L be primes with x₀ > L + 1. Let h ≥ 1, T = ⌊L/h⌋ and X = x_L. Suppose there are integers E
and M such that, for 0 ≤ t ≤ T−1:

  (H_C) g_{th} = g₀ + tE, and x_{(t+1)h} = x_{th} + h·g_{th} + M.

Then, under RH + GRH-Dir, **L < h·B(64X³)**, so L ≪ h log² X.

*Proof.* If T ≤ 1, then L < 2h, and we are done.

Let T ≥ 2. Summing (H_C) gives x_{th} = x₀ + t(hg₀ + M) + hE·t(t−1)/2 for 0 ≤ t ≤ T. E = g_h − g₀ is even
(gaps of odd primes), so this is Q(t) ∈ Z[t] with a = h(E/2). Q is nonconstant since Q(0) = x₀ < x_h = Q(1).
Its T + 1 ≥ 3 values are primes in (L+1, X].

Lemma 3 gives T + 1 < B(64X³). So L < h(T+1) < h·B(64X³). ∎

**What implies (H_C).** Suppose every complete block (e_{th}, …, e_{th+h−1}) has the same E = Σ e_r and the
same M = Σ (h−1−r)e_r. This is satorunet's "equal block moments". Expanding g_{th+i} = g_{th} + Σ_{r<i} e_{th+r}
then gives (H_C). Only the indices up to L−2 that actually occur are used. I checked the index ranges, and
verified the identity on 2,000 random words (`check2.py`).

In particular, (H_C) holds when e_{j+h} = e_j for all j with j+h ≤ L−2. Satorunet's side conditions E ≤ Ah
and h ≤ √Y are not needed. The Thue–Morse-type words also satisfy it: any concatenation of (4,0,0,4) and
(0,4,4,0), with h = 4, E = 8 and M = 12. I checked these values.

## Theorem S (finite shifts)

Let x₀ < … < x_L be primes with x₀ > L + 1 and L ≥ 1, and X = x_L. Suppose x_j = F(j) + b_j, where F is a
real quadratic with second difference 2 and each b_j lies in a finite set S of integers with |S| = r and
max |s| = σ. Then, under RH + GRH-Dir, L < ∏_{i=1}^{r} B(q_i), where q_1, …, q_r are defined in the proof. For
fixed r and σ this gives **L ≤ (4 + o(1))^r (log X)^{2r}** as X → ∞.

*Proof.*

F has integer coefficients. Indeed F(t) = t² + βt + γ with γ = F(0) = x₀ − b₀ and
β = F(1) − F(0) − 1, both integers. Moreover |γ| ≤ X + σ and |β| ≤ X + 2σ + 1.

List S = {s₁, …, s_r}. Put F_i = F + s_i and D_i = β² − 4(γ + s_i). Then
4F_i(t) = (2t+β)² − D_i, and |D_i| ≤ (X + 2σ + 3)².

Now choose primes p₁, …, p_r one at a time:
* For each i, let q_i = 8·max(1, |D_i|)·p₁⋯p_{i−1}.
* Let χ_i be χ_{D_i} from Lemma 1 if D_i ≠ 0, and the trivial character otherwise.
* Lemma 2 gives a prime p_i ∤ q_i with χ_i(p_i) = 1 and p_i ≤ B(q_i). So p_i is odd and differs from
  p₁, …, p_{i−1}.
* F_i has a root r_i modulo p_i: r_i ≡ (u − β)/2 with u² ≡ D_i (mod p_i) if D_i ≠ 0, and r_i ≡ −β/2 if D_i = 0.

The p_i are distinct, so CRT gives j₀ ∈ [0, P−1], with P = ∏p_i, such that j₀ ≡ r_i (mod p_i) for every i.

Suppose L ≥ P − 1. Then j₀ ≤ L, and b_{j₀} = s_i for some i. So p_i | F_i(j₀) = x_{j₀}. But x_{j₀} is a prime
greater than L + 1 ≥ P ≥ p_i, a contradiction. Hence L ≤ P − 2 < ∏ B(q_i).

For the asymptotic bound, induction gives log q_i ≤ 2 log X + O_{r,σ}(log log X). Then
B(q_i) = (4 + o(1)) log² X. ∎

## Consequences inside satorunet's "Lemma L" (RH + GRH-Dir; unconditional given Alpöge)

Take a chain in [Y, 2Y] with gaps ≥ c√Y and L ≥ δ√Y. Then X ≤ 2Y and L ≤ √Y/c. So for Y > Y₀(c) we have
x₀ ≥ Y > L + 1.

* Theorem A gives k + 1 ≥ δ√Y / B(32Y²), that is, **k ≫ √Y/log² Y** modifications. The unconditional bound,
  via Pollack as quoted by satorunet, is Y^{1/4−η}.
* Theorem C gives that a periodic (or equal-block-moment) counterexample needs
  **h > δ√Y / B(512Y³) ≫ √Y/log² Y**. Satorunet's unconditional bound is Y^{1/6−ρ}.
* Theorem S gives finite-shift chains **L ≪_S (log Y)^{2|S|}**, so they cannot have length ≥ δ√Y.

In every case "≫" is asymptotic. Up to astronomically large Y (log Y ≲ 15000), the bounds read
"k + 1 ≥ δ√Y/10⁹" and so on.

## What this does and does not show

* **Problem as posed** (erdosproblems.com/455; Lean `Erdos455.erdos_455`: must q_n/n² → ∞?). **Not
  settled.** The status is OPEN, and the page was last edited 7 Oct 2025, with 0 comments and 1 proof claim.
  These results constrain the structure of a hypothetical counterexample only.
* **Lean variant `erdos_455.variants.liminf`** (> 0.352, Richter) and the higher constants (0.5434, Lin's
  0.8642, satorunet's 0.9200). **Unaffected.** Modifications at density about 1/log²Y change nothing in the
  residue / max-plus method.
* **Lemma L itself remains open.** RH/GRH strength says nothing about aperiodic second-difference words with
  many modifications. Satorunet's own "What remains" paragraph says the same.
* **Not audited:** satorunet's reduction of the problem to Lemma L. Section 5's Proposition gives a chain with
  ≥ δD/3 indices and primes ≤ 3D². The passage from that to a dyadic [Y,2Y] chain with L ≥ δ√Y is asserted on
  the page, not written out. Theorems A, C and S above are self-contained statements about prime chains and
  are valid whether or not that reduction holds. Their relevance to #455 does depend on it.
* **Not new as conditional results.** Satorunet's page (Section 6) already states "Under GRH (LLS) one gets
  L ≪ (k+1) log² Y", "L ≪ h log² Y under GRH", and "L ≪_S (log Y)^{2|S|} under GRH".
  What is added here:
  1. the **status change** (RH + Dirichlet GRH are now Lean-certified);
  2. complete proofs, including the degenerate cases and the distinct-primes step in the CRT;
  3. explicit constants;
  4. removal of the nondecreasing-gap and size hypotheses;
  5. a precise list of the L-functions used: ζ and quadratic Dirichlet L-functions only.

  Value: modest. This is a status upgrade of structural constraints inside an unrefereed, AI-produced partial
  claim.

## Prior recording check (done 2026-11-22)

* **Plasma** (plasma-ai/erdos, `wiki/problems/integer_sequences/E0455/` with `_index.md` and 4 claim files).
  I fetched these again. grep for GRH, Riemann or Lamzouri found no hits. The pages summarise only the
  Y^{1/4−η} and least-non-residue versions. The release (2026-11-16) predates Alpöge.
* **erdosproblems.com/455 and forum thread:** 0 comments, 1 proof claim (#396, satorunet). No GRH discussion.
* **formal-conjectures 455.lean:** only the main statement and the Richter liminf variant.
* **arXiv:** **not checked.** The export.arxiv.org API returned nothing (HTTP and HTTPS).
* **ryantuck/erdos-ai:** per the screener, no folder for 455. I did not re-check.

## Credit

* **Theorems A, C and S and their GRH forms:** satorunet's write-up (https://satoru.net/math/455/, Section 6).
  It was produced by Claude and Codex under satorunet's direction, and posted as claim #396 on 2026-10-06.
* **Coset bound:** Y. Lamzouri, X. Li, K. Soundararajan, *Conditional bounds for the least quadratic
  non-residue and related problems*, arXiv:1309.3595v3 (Math. Comp. 2015), Theorem 1.4.
* **RH and Dirichlet GRH:** L. Alpöge (Lean proof released 2026-11-20). Statement and certification are from
  the leanprover-community/riemann-hypothesis repository.
* **Jacobi-symbol facts:** Mathlib (`JacobiSymbol.lean`).
* **Unconditional Y^{1/4+η} versions:** satorunet via Pollack 2017 Thm 1.3, not read by me.

## Sources read / not read

**Read:**
* LLS arXiv v3: Thm 1.4 from the rendered PDF page; Section 2 lemma statements; Section 4 proof text.
* Satorunet page, full text (refs/satoru455.html).
* RH repo `README.md` and `src/Challenge.lean`.
* Mathlib `JacobiSymbol.lean` statements: `legendreSym.to_jacobiSym`, `mul_left`, `mod_left`, `at_neg_one`,
  `at_two`, `quadratic_reciprocity`.
* The erdosproblems.com 455 page and forum.
* formal-conjectures 455.lean.
* Plasma E0455 files.

**Not read:**
* The published Math. Comp. version of LLS (only arXiv v3; the constant could differ in print).
* Pollack, Proc. AMS 145 (2017).
* Alpöge's paper (alpo.ge/remark.pdf) and the Lean proof itself. I did not build or run comparator.
* Line-by-line proofs of LLS Lemmas 2.2–2.4.
* The 2026-09-24 GitHub note and Lin's erdos455-convex-primes.
* arXiv (unreachable).

**Inferred, not verified from text:** the classical facts that nontrivial zeros of primitive L(s,χ) lie in
0 < Re s < 1, and that Mathlib's `LFunction` agrees with the classical L-function.

Scripts: `grh2/455/checks/check1.py`, `grh2/455/checks/check2.py` (run with `python3 -I`).
