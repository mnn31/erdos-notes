# Erdős 420, lead A: almost-all divergence of F at scale g(n)(log n)^2

Written 22 Nov 2026. Verdict: **the lead survives, with one correction.** The almost-all divergence
statement is proved below assuming RH for ζ (only ζ is used). The quantitative bound "log F ≫ g(n) log n"
holds only after g is capped at log n. The corrected form is Theorem A(ii).
This is a routine corollary of Selberg's classical conditional theorem. It is **not** progress on
Erdős's question as posed, which asks about the limit over all n (see "What this does and does not show").

Notation: log is the natural log, as in the Lean file (`Real.log`). τ is the divisor function,
F(f,n) = τ((n+⌊f(n)⌋)!)/τ(n!). θ(x) = Σ_{p≤x} log p, π is the prime-counting function, and v_p is the p-adic valuation.
"Density" means natural (asymptotic) density.

## Final statement

**Theorem A.** Assume RH, the Riemann Hypothesis for ζ. Let g : ℕ → ℝ satisfy g(n) → ∞, and put
g*(n) = min(g(n), log n). Then there is a set E ⊂ ℕ of natural density 0 such that, for all n ∉ E with
n ≥ n₀(g):

 (i) π(n + ⌊g*(n)(log n)²⌋) − π(n) ≥ g*(n) log n / 64 − 1;

 (ii) log F(g(n)(log n)², n) ≥ log F(g*(n)(log n)², n) ≥ (log 2)·(g*(n) log n / 64 − 1).

In particular F(g(n)(log n)², n) → ∞ as n → ∞ through ℕ \ E, a set of density 1.

- Hypothesis used: **RH for ζ only**. In the "GRH for Dirichlet L-functions" framing this is the trivial
  character mod 1 and nothing more. No other L-function, no pair correlation, no Cramér.
- **Unconditional if the Alpöge Lean theorems are accepted.** Part (a) of the brief, Mathlib's
  `RiemannHypothesis`, is classical RH for ζ, the only hypothesis of Lemma 2 below. I did NOT inspect
  the Alpöge repository myself. This relies on the brief's verification note.
- Weaker than the brief's claim: the brief said "log F ≫ g(n) log n" with no cap. I prove it only with
  g* = min(g, log n), so with g itself when g(n) ≤ log n. For larger g the bound saturates at
  ≫ (log n)². That is enough for divergence. I did not try to remove the cap.

## Lemmas

**Lemma 1 (prime factor of 2; monotonicity).** Let n ≥ 1 and 0 ≤ f ≤ f′ be integers.
(a) τ((n+f)!) ≤ τ((n+f′)!).
(b) If f < n, then τ((n+f)!)/τ(n!) ≥ 2^{π(n+f)−π(n)}.

*Proof.* (a) (n+f)! divides (n+f′)!, so every divisor of the first divides the second.
(b) For m ≥ 1, τ(m!) = ∏_{p≤m}(v_p(m!)+1), because τ(∏ p^{a_p}) = ∏(a_p+1). Legendre's formula
v_p(m!) = Σ_{j≥1}⌊m/p^j⌋ is nondecreasing in m, and v_p(n!) = 0 for p > n. Hence
τ((n+f)!)/τ(n!) = ∏_{p≤n+f}(v_p((n+f)!)+1)/(v_p(n!)+1), and every factor is ≥ 1.
Now take a prime p with n < p ≤ n+f. Then v_p(n!) = 0. Since f < n we have n+f < 2n < 2p, so
⌊(n+f)/p⌋ = 1. Also p² ≥ 2p > n+f, so the higher terms vanish and v_p((n+f)!) = 1. That factor is
exactly 2/1, and the product is ≥ 2^{#{p : n<p≤n+f}}. ∎
(The fact that a prime p doubles τ from (p−1)! to p! is also used in EGIP96, Theorem 6, p. 14, as
"d(p!) = 2d((p−1)!)".)

**Lemma 2 (Selberg's mean value, explicit form; cited).** Assume RH. For all x ≥ 10⁸ and every
δ ∈ (0, 10⁻⁸],
 ∫₁ˣ |θ(y+δy) − θ(y) − δy|² dy < 202 δ x² log² x.

*Source.* M. Cully-Hugill and A. W. Dudek, "An explicit mean-value estimate for the PNT in intervals",
arXiv:2206.00433v2 (21 Aug 2023), **Theorem 1**, p. 2.
- VERIFIED by reading the text: the statement, its hypotheses ("Assuming RH", x ≥ 10⁸, δ ∈ (0,10⁻⁸]),
  and the end of the proof in §2.2, pp. 9–11 (eq. (21), A₇ = 202, T₀ = 10⁸).
- RH enters through their Lemmas 3 and 4 ("Assume RH"). The other inputs are unconditional: Perron,
  Plancherel, Delange's bound for −ζ′/ζ(σ) with σ > 1, and Karatsuba–Korolëv's Lemma 1. Only ζ appears.
- I did not re-derive their constants. The argument below needs only *some* constant, so a correct
  O-form would do. That O-form is Selberg 1943, eq. (1) in their introduction (p. 2, "δ ∈ [1/x,1]").
  I did NOT read Selberg's paper and do not rely on it.

**Lemma 3 (exceptional set at one scale).** Assume RH. Let X ≥ 5·10⁷ and Δ ∈ (0, 10⁻⁸]. Put
B = B(X,Δ) = {y ∈ [X,2X] : |θ(y+Δy) − θ(y) − Δy| > Δy/2}. Then B is a finite union of intervals and
 |B| < 3232 log²(2X)/Δ.

*Proof.* On [X,2X], y ↦ θ(y+Δy) − θ(y) − Δy is a step function minus a linear function. It has
finitely many jumps, at the y with y or (1+Δ)y prime. So B is a finite union of intervals. On B,
|·|² > Δ²y²/4 ≥ Δ²X²/4. So
|B|·Δ²X²/4 ≤ ∫_B|·|² ≤ ∫₁^{2X}|·|² < 202·Δ·(2X)²·log²(2X),
using Lemma 2 with x = 2X ≥ 10⁸. Dividing gives |B| < 3232 log²(2X)/Δ. ∎

**Lemma 4 (good points carry primes).** If X ≥ 1, 0 < Δ ≤ 1/2 and y ∈ [X,2X] \ B(X,Δ), then
 #{p prime : y < p ≤ y+Δy} ≥ ΔX / (2 log 3X).

*Proof.* Since y ∉ B, θ(y+Δy) − θ(y) ≥ Δy − Δy/2 = Δy/2 ≥ ΔX/2. Also
θ(y+Δy) − θ(y) = Σ_{y<p≤y+Δy} log p, and each term is ≤ log(y+Δy) ≤ log 3X. ∎

## Proof of Theorem A

**Step 0 (reduction to g\*).** g*(n) = min(g(n), log n) → ∞, and g*(n) ≤ g(n). Floor is
monotone, so f*(n) := ⌊g*(n) log² n⌋ ≤ ⌊g(n) log² n⌋. By Lemma 1(a), F(g log², n) ≥ F(g* log², n),
which is the first inequality in (ii). Also f*(n) ≤ log³ n < n for n ≥ 100, because log³x/x is
decreasing for x > e³ and log³100 ≈ 97.7 < 100.

Let G(X) = inf_{m ≥ X} g*(m) for real X ≥ 2. G is nondecreasing and G(X) → ∞. Also G(X) ≤ g*(n) for
every integer n ≥ X, and g*(n) ≤ log n.

**Step 1 (blocks and levels).** For j ≥ 1 put X = 2^j, L = log X, and let block j be the integers n with
2^j < n ≤ 2^{j+1}. Then [n−1,n] ⊂ [X,2X], the blocks partition {n ≥ 3}, and the intervals [n−1,n] for
different n in a block overlap only at endpoints. Choose j₀ so that for all j ≥ j₀ we have G(2^j) ≥ 4,
2^j ≥ 5·10⁷, log(2X)·L²/(4X) ≤ 10⁻⁸, and (log 2X)² ≤ 2L². All of these hold for large j.

For n in block j ≥ j₀, let k(n) = ⌊log₂ g*(n)⌋ ≥ 2. Then 2^{k(n)} ≤ g*(n) < 2^{k(n)+1}. Since
g*(n) ≥ G(X) and g*(n) ≤ log n ≤ log 2X, the level k = k(n) lies in
K_j = {k ≥ 0 : 2^{k+1} > G(X), 2^k ≤ log 2X}. For k ∈ K_j put Δ_k = 2^k L²/(4X). Then
0 < Δ_k ≤ log(2X)L²/(4X) ≤ 10⁻⁸, so Lemmas 3 and 4 apply.

**Step 2 (the exceptional set has density 0).** Let
E_j = {n in block j : [n−1,n] ⊂ B(X, Δ_{k(n)})}, and E = {n ≤ 2^{j₀}} ∪ ⋃_{j≥j₀} E_j.
For fixed k, the unit intervals [n−1,n] ⊂ B(X,Δ_k) have disjoint interiors inside B, so there are at
most |B(X,Δ_k)| of them. By Lemma 3,
#E_j ≤ Σ_{k∈K_j} |B(X,Δ_k)| < Σ_{k: 2^k > G/2} 3232 log²(2X)·4X/(2^k L²) ≤ 12928·2X·Σ_{2^k>G/2} 2^{−k} < 103424·X/G(X).
For large N, split the blocks with 2^j < N at 2^j = √N:
#(E ∩ [1,N]) ≤ 2^{j₀} + Σ_{2^j ≤ √N} 103424·2^j/G(2^{j₀}) + Σ_{√N < 2^j < N} 103424·2^j/G(√N)
 ≤ 2^{j₀} + 206848·√N + 206848·N/G(√N) = o(N),
because G(√N) → ∞ and G is nondecreasing. So E has density 0.

**Step 3 (good n carry many primes).** Let n be in block j ≥ j₀ with n ∉ E_j, and let k = k(n).
Some y ∈ [n−1,n] is not in B(X,Δ_k). By Lemma 4, (y, y+Δ_k y] contains at least
Δ_k X/(2 log 3X) = 2^k L²/(8 log 3X) primes. Since log 3X ≤ 2L, this is ≥ 2^k L/16. Since
2^k > g*(n)/2, it is > g*(n)L/32. Since log n ≤ log 2X ≤ 2L, it is ≥ g*(n) log n/64.
Containment: y ≥ n−1 and y ≤ n ≤ 2X, so (y, y+Δ_k y] ⊂ (n−1, n + 2XΔ_k]. Moreover
2XΔ_k = 2^k L²/2 ≤ g*(n) log²n/2 ≤ ⌊g*(n) log² n⌋ = f*(n). The last step uses ⌊t⌋ ≥ t/2 for t ≥ 2,
and here t = g*(n) log² n ≥ 4.
The interval (n−1,n] contains at most one prime, namely n itself. Therefore
π(n+f*(n)) − π(n) ≥ g*(n) log n/64 − 1, which is (i).

**Step 4.** By Step 0, f*(n) < n, so Lemma 1(b) together with (i) gives (ii). The right side of (ii)
tends to ∞ because g*(n) log n → ∞. ∎

## Numerical sanity check (only a consistency check, not evidence)

`python3 -I` with a sieve to 3·10⁷ (script: scratchpad `chk/check420.py`):
- On 6 random n ∈ [10⁵,10⁶] with f = ⌊log² n⌋, I computed log F exactly from Legendre's formula.
  In every case log₂F was at least the prime count in (n,n+f] (e.g. 13 primes, log₂F = 26.2).
- For X ∈ {10⁵,10⁶,10⁷} and n ∈ [X,2X) sampled with step 7, the fraction of n with no prime in
  (n, n+g log² n] was 0 for g ≥ 1. It was 2·10⁻⁵ to 2·10⁻⁴ at g = 1/2. The mean count was ≈ g log X.
  At this height these numbers say nothing beyond agreement with Cramér's model.

## What this does and does not show

- **Problem as posed (Q1):** it asks whether lim_{n→∞} F((log n)^C, n) = ∞ over **all** n, for large C.
  Theorem A is an almost-all statement. It says nothing about the density-zero set E, so it does not
  touch Q1. Lean target `Erdos420.erdos_420.parts.i` in formal-conjectures (origin/main, read) is the
  all-n `Tendsto … atTop atTop`. It is untouched.
- Under RH alone, the all-n route through primes needs intervals of length ≳ √n log n, which is worse
  than EGIP's unconditional n^{4/9} (EGIP96 Lemma 3 / Corollary 3). So RH gives nothing for Q1 by this
  route (INFERRED, not proved here).
- Q2 and Q3 (density) are already settled by Plasma's accepted Lean formalization and are not affected.
- **Lean:** the formal-conjectures file 420.lean has no almost-all variant. I did not formalize
  Theorem A. Even with RH available in Lean, that would also need Lemma 2 (Selberg's mean-value
  theorem) formalized, which is a substantial job.
- **Relation to the recorded almost-all statements:**
  - The erdosproblems.com page (read via curl, last edited 3 Dec 2025) repeats EGIP's manuscript claim
    (p. 5) that f = o((log n)²) gives F ~ 1 for almost all n.
  - Plasma's E0420 page and EGIP card (read) record that this claim is false: by Mastrostefano, at
    f ~ c log n a positive proportion of n have F ≥ 2^m. They prove the replacement: f = o(log n) gives
    F → 1 almost always. These are author-recorded, not independently reviewed. I did not re-check
    Mastrostefano.
  - Theorem A is the complementary side: once f/(log n)² → ∞, F → ∞ almost always. So the almost-all
    transition lies between f ≍ log n and f = g(n)(log n)². Had EGIP's o((log n)²) claim been true,
    Theorem A would have shown it sharp.
- **Closing the gap** (for example, F → ∞ a.a. for f = g(n) log n) needs prime counts in intervals of
  length o(log² n). Selberg's variance bound under RH gives only mean-square deviation ≪ h for
  counts in windows of length h. Per the P⁺ reduction on Plasma's page, averaging over m = a·p does
  not help (INFERRED heuristic, not proved). Pair correlation or Hardy–Littlewood/Gallagher would be
  needed, and neither is covered by the Alpöge results.
- **Value:** modest. It is a short corollary of a classical 1943 conditional theorem plus Lemma 1.
  Its only novelty is that, as far as checked, nobody has recorded it for #420. If the Alpöge RH is
  accepted, it becomes unconditional, and I found no unconditional polylog almost-all divergence
  result for F. Best unconditional almost-all primes input per CHD p. 2: Jia, x^{1/20+ε}.

## Prior-recording check (done for this write-up)

- erdosproblems.com/420 and forum thread 420 (curl, read, 22 Nov 2026): no RH or almost-all divergence
  statement. The forum has one comment, Woett's (on EGIP's results; no RH).
- erdosproblems database `data/problems.yaml` (origin/main): status open; no notes on this.
- formal-conjectures `420.lean` (origin/main): parts i–iii plus EGIP Corollary 2/3 variants. No almost-all variant.
- Plasma `wiki/problems/arithmetic_functions/E0420/{_index, claims/*}` and
  `library/factorials_binomials/erdos_1996_number_divisors/*` (all 12 cards fetched; grep for
  Selberg/Riemann/almost all/normal order): the almost-all side is recorded only as F → 1. RH appears only
  in the Theorem 6 card (champs).
- ryantuck/erdos-ai: `conjectures/420.lean`, `deepmind/reviews/420.md`, `deepmind/ai-review/420.md`
  (fetched and grepped): only the EGIP o(log²) claim is repeated. Nothing on almost-all divergence or RH.
- Literature: OpenAlex citing-works list for EGIP96 (17 works). The only recent hit on topic is
  T. Freiberg, arXiv:2609.15597 (Sept 2026): large values of K(n), Rankin-type. Abstract and grep of the
  full text read: no RH, no almost-all divergence. Targeted arXiv API search was rate-limited and not done.

## Credit

- A. Selberg (1943): the conditional mean-value estimate and the corollary that almost all intervals of
  length h with h/log² → ∞ contain primes.
- Cully-Hugill and Dudek: the explicit Theorem 1 used here.
- Erdős, Graham, Ivić, Pomerance (EGIP96): the problem setting. Theorem 6 uses the same Selberg input
  for a different (champs) statement.
- W. van Doorn (erdosproblems remarks): the analogous all-n statement under Cramér's conjecture.
- Plasma AI: the almost-all F → 1 side and the normal-order correction.
- The deduction (Lemmas 1, 3, 4 and Steps 0–4) is routine and was written here. It has not been
  independently reviewed.

## Sources not read

- Selberg 1943 (Arch. Math. Naturvid. 47), the original paper. Lemma 2 is cited from CHD instead.
- The Alpöge Lean RH/GRH repository: taken from the brief's verification note only.
- The internal inputs to CHD's proof (Delange; Karatsuba–Korolëv; their Lemmas 3–4 constants): I read
  the statements and the shape of the proof, not every estimate.
- Mastrostefano arXiv:1812.11784 (relied on only through Plasma's record, in the context section).
- R. Li arXiv:2407.05651; Jia; Wolke [29, Cor. 2 of CHD]; the published (1996) version of EGIP.
  The manuscript at math.dartmouth.edu/~carlp/factorial.pdf was read.
- No targeted arXiv search, because the API was rate-limited.

refs/ (untrusted data): factorial.pdf/.txt (EGIP manuscript), cully_2206.00433.pdf,
runs_2609.15597.pdf/runs.txt (Freiberg), site/ (erdosproblems page and forum HTML),
plasma/ (Plasma pages and EGIP cards), ryantuck/ (420 files).
