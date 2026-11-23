# Erdős Problem 879: under RH, G(n) ≥ H(n) − O(n^{5/4} log n)

Status: the lead survives as stated. Every step below is proved here, or cited to a
source whose text I read (theorem number and hypotheses checked). One external input
is used: Büthe, arXiv:1410.7015v4, Theorem 2. Schoenfeld 1976, the original
source of that bound, was **not** read; see "Sources not read".

## Final statement

Notation. `G(n)` is the maximum of `Σ_{a∈S} a` over sets `S ⊆ {1,…,n}` whose
elements are pairwise coprime. Two versions of `H` are in use:
`H_E(n) = Σ_{p≤n} p + n·π(n^{1/2})` (Erdős 1984, p.120) and
`H_W(n) = Σ_{p<n} p + n·π(n^{1/2})` (erdosproblems.com/879). Since `H_W ≤ H_E`, it is
enough to prove the bound for `H_E`.

**Theorem.** Assume RH, the Riemann Hypothesis for ζ only. No Dirichlet
L-function, no GRH, and no other L-function is used. Then there is an absolute
`n_0` such that for every `n ≥ n_0`,

    G(n) ≥ H_E(n) − 6·n^{5/4}·log n  ≥  H_W(n) − 6·n^{5/4}·log n.

**Unconditional form.** The theorem holds unconditionally if the Alpöge Lean
theorem `riemannZeta_eq_zero_re` is accepted, or equivalently Mathlib's
`RiemannHypothesis` as proved in leanprover-community/riemann-hypothesis. Its statement
(read in `src/Challenge.lean`) is that every zero `s` of `riemannZeta` that is not a
trivial zero `−2(n+1)` and is not `s = 1` has `Re s = 1/2`. That gives exactly the
hypothesis Büthe's Theorem 2 needs, for every T. I did not build or check the Lean
proof myself; the brief reports the community's certification.

If the admissible set is required to have `a_i < n` strictly, apply the
theorem to `n−1`. Here `H_E(n) − H_E(n−1) ≤ n + n(π(√n) − π(√(n−1))) + π(√(n−1)) ≤ 2n + √n`,
because `π(√n) − π(√(n−1)) ≤ 1`. So the statement changes only by `O(n)`.

## External input (read)

**Lemma R (Büthe, arXiv:1410.7015v4, Theorem 2, §7, p.13; also stated in the
Introduction, credited to Schoenfeld [Sch76]).** I read the text. Let `T > 0` be such
that RH holds for the zeros `ρ` with `0 < Im ρ ≤ T`. Then, whenever
`4.92·sqrt(x/log x) ≤ T`, one has (7.2): `|π(x) − li(x)| ≤ sqrt(x)·log(x)/(8π)` for
`x > 2657`.

*Hypotheses check.* Under full RH, for any `x > 2657` pick `T = 4.92 sqrt(x/log x)`.
The theorem then gives (7.2) at that x, so (7.2) holds for all `x > 2657`. Büthe's
π is the normalized count: §7 writes `π(x) = Σ_p χ*_{[0,x]}(p)`, where `χ*` is the
normalized characteristic function, so a prime equal to x is counted with weight 1/2.
The usual π differs from it by at most 1/2. I only use differences
`li(y) − li(z) = ∫_z^y dt/log t` with `y, z ≥ 2`, so the normalization of li does not
matter.

**Corollary R′.** Assume RH. There is an absolute constant `K ≥ 1/2` such that for
all real `y ≥ 2`,
`|π(y) − li(y)| ≤ E(y) := sqrt(y)·log(y)/(8π) + K`, where π is the standard
prime-counting function.

*Proof.* For `y > 2657` this is Lemma R plus 1/2. On the compact set `[2, 2657]`,
`0 ≤ π(y) ≤ 2657` and li is continuous, so `|π − li|` is bounded there. Take K to
be the larger of these two bounds. ∎

`E` is increasing on `[1, ∞)` because `sqrt(y) log y` is.

## Setup

Let n be large, `L = log n`, `D(x) = sqrt(x)·L²` and `D_0 = n^{1/4}·L³`.
Let `P` be the set of primes `≤ √n`. Split it into `P_2 = {p ∈ P : p > √n − D_0}` and
`P_1 = P \ P_2`. For `p ∈ P_1`, put `x_p = n/p` and define the window
`I_p = [x_p − D(x_p), x_p]`. Let `Q` be the set of primes in `(√n, n]`.

"For n ≥ n_0" below means that finitely many explicit inequalities in n hold:
`L ≥ 10`, `D_0 < √n`, `√n ≥ L⁴`, and the two final inequalities in Lemma 6.
Each holds for all large n.

## Lemma 1 (windows lie in (√n, n/2])

For `n ≥ n_0` and every `p ∈ P_1`: `√n < x_p − D(x_p)` and `x_p ≤ n/2`.

*Proof.* `p ≥ 2` gives `x_p ≤ n/2`. From `p ≤ √n − D_0` with `0 < D_0 < √n`:
`x_p ≥ n/(√n − D_0) = √n + √n·D_0/(√n − D_0) > √n + D_0`.
- If `x_p ≤ 4√n`, then `D(x_p) ≤ 2n^{1/4}L² < n^{1/4}L³ = D_0` (since L > 2). So
  `x_p − D(x_p) > √n + D_0 − D_0 = √n`.
- If `x_p > 4√n`, then `sqrt(x_p) > 2n^{1/4} ≥ 2L²` (since `√n ≥ L⁴`). So
  `D(x_p) = sqrt(x_p)L² ≤ x_p/2`, and `x_p − D(x_p) ≥ x_p/2 > 2√n`. ∎

## Lemma 2 (left ends are monotone)

`φ(x) = x − D(x)` is continuous and strictly increasing on `[√n, ∞)`.

*Proof.* `φ'(x) = 1 − L²/(2 sqrt x)`. For `x ≥ √n` we have `sqrt x ≥ n^{1/4} ≥ L² > L²/2`,
so `φ' > 0`. ∎

So for every `a > √n` there is a unique `a' > a` with `φ(a') = a`, namely `a' − a = D(a')`.
For `p ∈ P_1`, `x_p ≥ √n`, and `I_p ⊆ [a, b]` holds iff `φ(x_p) ≥ a` and `x_p ≤ b`,
which holds iff `a' ≤ x_p ≤ b`, which holds iff `n/b ≤ p ≤ n/a'`.

## Lemma 3 (Hall's theorem; proof included, so no citation is needed)

Let X and Y be finite sets, and let each `x ∈ X` have a set of neighbours
`N(x) ⊆ Y`. If `|N(Z)| ≥ |Z|` for every `Z ⊆ X`, where `N(Z) = ∪_{z∈Z} N(z)`, then
there is an injective `f : X → Y` with `f(x) ∈ N(x)` for all x.

*Proof (induction on |X|).* The case `|X| ≤ 1` is immediate. Assume `|X| ≥ 2`.
(i) Suppose `|N(Z)| ≥ |Z| + 1` for every nonempty `Z ⊊ X`. Pick any `x ∈ X` and any
`y ∈ N(x)`; one exists because `|N({x})| ≥ 1`. Delete x and y. Every nonempty
`Z ⊆ X∖{x}` still has `|N(Z)∖{y}| ≥ |Z|`. By induction, match `X∖{x}` into `Y∖{y}`,
then add `x ↦ y`.
(ii) Otherwise some nonempty `Z_0 ⊊ X` has `|N(Z_0)| = |Z_0|`. Every subset of
`Z_0` has all its neighbours inside `N(Z_0)`, so by induction `Z_0` can be matched
into `N(Z_0)`. For `Z ⊆ X∖Z_0`, in the graph with `N(Z_0)` deleted,
`|N(Z)∖N(Z_0)| = |N(Z ∪ Z_0)| − |N(Z_0)| ≥ |Z| + |Z_0| − |Z_0| = |Z|`. By induction,
match `X∖Z_0` into `Y∖N(Z_0)`. The union of the two matchings is injective. ∎

## Lemma 4 (reduction to intervals)

Suppose that for all reals `√n < a ≤ b ≤ n/2`,

    (★)  #{p ∈ P_1 : I_p ⊆ [a,b]} ≤ #{primes in [a,b]}.

Then there is an injective `f : P_1 → Q` with `f(p) ∈ I_p` for all `p ∈ P_1`.

*Proof.* Apply Lemma 3 with `X = P_1`, `Y = Q` and `N(p) = Q ∩ I_p`. By Lemma 1,
`I_p ⊆ (√n, n/2]`, so `N(p)` is exactly the set of primes in `I_p`. Fix `Z ⊆ P_1`.
`U = ∪_{p∈Z} I_p` is a finite union of closed intervals, so it is a disjoint union of
finitely many closed intervals `J_k = [a_k, b_k]`, its connected components. Each
`a_k` is the left end of some `I_p` and each `b_k` is the right end of some `I_p`, so
`√n < a_k ≤ b_k ≤ n/2`. Each `I_p` is connected, so it lies in exactly one `J_k`.
Hence `|Z| ≤ Σ_k #{p ∈ P_1 : I_p ⊆ J_k} ≤ Σ_k #{primes in J_k} = |N(Z)|`, using (★). ∎

## Lemma 5 (the main-term comparison)

Let `L ≥ 10` and `g(s) = 1/log s − n/(s² log(n/s))`.
(a) `g(s) ≥ 0` for `√n ≤ s ≤ n/2`.
(b) `g(s) ≥ 1/(2 log s) > 1/(2L)` for `2√n ≤ s ≤ n/2`.

*Proof.* Write `s = √n·e^t` with `0 ≤ t ≤ T := L/2 − log 2`. Then
`log s = L/2 + t`, `log(n/s) = L/2 − t > 0` and `n/s² = e^{−2t}`. So
`g(s) = (1 − e^{h(t)})/log s` with `h(t) = −2t + log(L/2+t) − log(L/2−t)`.
We have `h(0) = 0` and `h'(t) = −2 + L/(L²/4 − t²)`. For `t ≤ T`,
`L²/4 − t² ≥ L²/4 − T² = L·log 2 − (log 2)²`. So `h'(t) ≤ −2 + R(L)` with
`R(L) = 1/(log 2 − (log 2)²/L)`. R decreases in L, and `R(10) = 1.5502…`, so
`h' ≤ −0.449 < 0` on `[0, T]`. Therefore h is decreasing with `h ≤ h(0) = 0`, which gives (a).
For (b), `t ≥ log 2`, so `h(t) ≤ h(log 2) = −2 log 2 + log((L/2+log 2)/(L/2−log 2))`.
The ratio inside the log decreases in L, so for `L ≥ 10`,
`h(log 2) ≤ −1.3863 + 0.2791 = −1.1072`. Then `1 − e^{h} ≥ 1 − 0.3306 > 1/2`. Also
`log s < L` because `s ≤ n/2`. ∎

(Numerical check: `numerics/lem5.py` scans L ∈ [10, 500] and t ∈ (0, T]. It finds
`h(t)/t ≤ −1.39` and `min_{t≥log 2}(1 − e^{h}) = 0.6696`, consistent with the proof.)

## Lemma 6 (Hall's interval condition holds under RH)

Assume RH. For `n ≥ n_0`, (★) holds for all `√n < a ≤ b ≤ n/2`.

*Proof.* Let `a'` be as in Lemma 2. If `a' > b`, the left side of (★) is 0. Assume
`a' ≤ b`. By Lemma 2 the left side counts primes in `[n/b, n/a']`, so it is at most
`π(n/a') − π(n/b) + 1`. The right side is at least `π(b) − π(a)`. All four arguments are
`≥ 2`, because `n/b ≥ 2` and `n/a' ≥ n/b`. Also `a, b ∈ (√n, n/2]` and
`n/a', n/b ∈ [2, √n)`. Let
`Δ = [π(b) − π(a)] − [π(n/a') − π(n/b)] − 1`. By Corollary R′,

    Δ ≥ M − E(a) − E(b) − E(n/a') − E(n/b) − 1,
    M = ∫_a^b ds/log s − ∫_{n/b}^{n/a'} du/log u.

Substitute `u = n/s` in the second integral; this is valid because `log(n/s) > 0` on
`[a', b]`. It gives `∫_{a'}^{b} n/(s² log(n/s)) ds`, so

    M = ∫_a^{a'} ds/log s + ∫_{a'}^{b} g(s) ds.

By Lemma 5(a), the second term is ≥ 0, since `[a', b] ⊆ [√n, n/2]`. The first term is at
least `(a' − a)/log a' = D(a')/log a' > sqrt(a')·L`, using `log a' < L`. Since E is
increasing, `E(a) ≤ E(b)` and `E(n/a'), E(n/b) ≤ E(√n) = n^{1/4}L/(16π) + K`.

*Case A: `b ≤ 4a'`.* Here `sqrt b ≤ 2 sqrt(a')` and `log b < L`, so
`E(a) + E(b) ≤ sqrt(a')L/(2π) + 2K`. Also
`E(n/a') + E(n/b) ≤ n^{1/4}L/(8π) + 2K ≤ sqrt(a')L/(8π) + 2K`, because `a' > √n`. Hence
`Δ ≥ (1 − 5/(8π))·sqrt(a')·L − 4K − 1 ≥ 0.8·n^{1/4}·L − 4K − 1 > 0` for `n ≥ n_0`.

*Case B: `b > 4a'`.* Then `[b/2, b] ⊆ [a', b] ∩ [2√n, n/2]`. Using Lemma 5 (part (a) on
the rest of `[a', b]`, part (b) on `[b/2, b]`) and dropping the first term:
`M ≥ (b/2)/(2L) = b/(4L)`. Also `n^{1/4} < sqrt(b)/2`, because `b > 4√n`. So the error
terms total at most `(1/(4π) + 1/(16π))·sqrt(b)·L + 4K + 1 ≤ 0.1·sqrt(b)·L + 4K + 1`. Since
`b/(4L) ≥ sqrt(b)·n^{1/4}/(2L)`:
`Δ ≥ sqrt(b)·(n^{1/4}/(2L) − 0.1L) − 4K − 1 > 0` for `n ≥ n_0`, because
`sqrt b > 2n^{1/4}`.

In both cases Δ > −1. Δ is an integer, so Δ ≥ 0, which is (★). ∎

## Lemma 7 (the construction and its cost)

Assume RH and `n ≥ n_0`. Let f be the injection from Lemmas 4 and 6. Put

    S = {p·f(p) : p ∈ P_1} ∪ {p² : p ∈ P_2} ∪ (Q ∖ f(P_1)).

Then `S ⊆ {1, …, n}`, its elements are pairwise coprime, and
`H_E(n) − Σ_{a∈S} a ≤ 6·n^{5/4}·log n`.

*Proof.* **Bounds.** `p·f(p) ≤ p·x_p = n`, `p² ≤ n` for `p ≤ √n`, and `q ≤ n` for `q ∈ Q`.

**Coprimality.** The prime supports of the elements are `{p, f(p)}` for `p ∈ P_1`,
`{p}` for `p ∈ P_2`, and `{q}` for `q ∈ Q∖f(P_1)`. Here `p ≤ √n < f(p)` by Lemma 1,
f is injective, and the q's are outside `f(P_1)`. So the supports are pairwise disjoint.
In particular the elements are distinct and pairwise coprime.

**Cost.** `H_E(n) = Σ_{p∈P} p + Σ_{q∈Q} q + n|P|`, so

    H_E − ΣS = Σ_{p∈P} p + Σ_{P_1}(n − p f(p)) + Σ_{P_1} f(p) + Σ_{P_2}(n − p²).

1. `Σ_{p∈P} p ≤ √n·√n = n`.
2. `n − p f(p) = p(x_p − f(p)) ≤ p·D(x_p) = sqrt(np)·L² ≤ n^{3/4}L²`. To bound
   `|P_1| ≤ π(√n)`: by Corollary R′, `π(y) ≤ 1 + ∫_2^y dt/log t + E(y) + E(2)`. Also
   `∫_2^y dt/log t ≤ √y/log 2 + 2y/log y`, by splitting at √y. With `y = √n` this gives
   `π(√n) ≤ 4√n/L + O(n^{1/4}L) ≤ 5√n/L` for `n ≥ n_0`. So this sum is at most `5n^{5/4}L`.
3. `Σ_{P_1} f(p) ≤ Σ_{2≤m≤√n} n/m ≤ n·log √n = nL/2`.
4. For `p ∈ P_2`: `n − p² = (√n − p)(√n + p) < 2√n·D_0`, and `|P_2| ≤ D_0 + 1 ≤ 2D_0`.
   So this sum is at most `4√n·D_0² = 4nL⁶`.

Total: `n + 5n^{5/4}L + nL/2 + 4nL⁶ ≤ 6n^{5/4}L` for `n ≥ n_0`. ∎

*Proof of the Theorem.* `G(n) ≥ Σ_{a∈S} a ≥ H_E(n) − 6n^{5/4} log n ≥ H_W(n) − 6n^{5/4} log n`. ∎

## Numerical sanity check (not part of the proof)

The proof's thresholds need n far beyond what can be computed. For example, `D_0 < √n`
requires `n^{1/4} > L³`, which needs roughly `n > 10^{20}`. At `n ≤ 10^8` with the
proof's constants, `P_1` is empty (`numerics/check.py`).

With the shapes kept and the constants reduced (`D(x) = 0.5·sqrt(x)·L`,
`D_0 = 0.5·n^{1/4}·L`), `numerics/small.py` builds f greedily: it takes windows by
increasing right end and gives each the smallest free prime in it. It finds 0 failures
at `n = 10^6, 10^7, 10^8`. The ratio `(H_E − ΣS)/(n^{5/4} log n)` is
0.056, 0.047 and 0.040, while `(H_E − ΣS)/n^{3/2}` falls from 0.025 to 0.0074. This
is consistent with the `n^{5/4}`-type scaling but proves nothing.

## What this does and does not show

- **Problem as posed (erdosproblems.com/879, read):** Q1 asks whether
  `G(n) > H(n) − n^{1+o(1)}`. This result does **not** settle Q1. It gives
  exponent `5/4 + o(1)` under RH, and nothing about Q2 (elements with ≥ k prime factors).
- **Relation to the recorded bound.** erdosproblems.com records the unconditional
  Erdős–van Lint bound as `H(n) − n^{3/2−o(1)} < G(n)`. Plasma's library card for
  p.120 transcribes it as `n^{3/2−ε}` and notes that the exponent is faint and no
  quantifier is printed. My own look at the page image (`refs/erdos1984_p120.png`)
  shows `n^{3/2−c}` or `n^{3/2−ε}`, with the last glyph unreadable at scan resolution,
  no quantifier and no proof.
  - If the intended meaning is `3/2 − o(1)`, as erdosproblems.com reads it, then the
    Theorem improves the exponent from 3/2 to 5/4 under RH.
  - If Erdős meant a fixed unspecified `c > 0`, the Theorem gives the explicit value
    `c = 1/4 − o(1)` under RH. Whether it beats their c cannot be decided, because
    their proof is unpublished.
  - INFERRED, not verified: rerunning the same argument with only the unconditional
    PNT error term reproduces `n^{3/2−o(1)}`. The bottleneck is prime-count
    discrepancy near √n, where demand and supply densities coincide. This supports
    the `o(1)` reading.
- **Lean.** No `FormalConjectures/ErdosProblems/879.lean` exists on
  formal-conjectures `origin/main` (checked). The database entry `data/problems.yaml`
  lists 879 as open and unformalized. Kitamura's FC PR #5302 (forum) concerns Q2
  only. Nothing here touches a Lean statement.
- **Which L-functions are used:** only ζ, through Büthe Theorem 2. The Dirichlet
  GRH part of the Alpöge release is not used.
- **Why 5/4 is probably the limit of this method (INFERRED).** Pointwise RH
  guarantees a prime only in windows of length ≍ `sqrt(x)·log² x`. Each small prime p
  then pays about `sqrt(np)·L²`, and summing over `p ≤ √n` gives `n^{5/4}L`. A rough
  transport heuristic near √n, with surplus density ≈ 2u/L at `x = √n(1+u)` against
  pointwise error `n^{1/4}L`, also gives `n^{5/4}`. Going further would need averaged
  or short-interval information (for example Selberg-type mean values), not
  pointwise RH. This is a pointer, not a claim.

## Credit

- Problem, `G`, `H` and the recorded bounds: Erdős (1984, p.120), crediting the
  bounds to joint unpublished work with van Lint. The source is Erdős's Nieuw Archief
  problem 623 (1983).
- The construction (pair each small prime p with a prime near n/p, and use p² near √n)
  is the structure that H(n) itself suggests. Erdős–van Lint presumably used something
  similar, but their proof is unpublished, so this cannot be checked.
- The RH lead and the Hall-on-intervals argument come from the screen in
  `SCREEN.md` (this folder). This file completes it: it adds the full Lemma 1–7 proofs,
  a self-contained proof of Hall, and replaces Schoenfeld with Büthe Thm 2, which I read.
- Explicit RH bound for π: Schoenfeld (1976), as restated and re-proved in Büthe
  (arXiv:1410.7015, Math. Comp. 2016).

## Prior-work check (this session)

- erdosproblems.com/879 and forum thread 879 (2 comments, Kitamura and Zeraoulia):
  nothing on Q1's exponent or RH.
- Plasma: E0879 index, the Erdős–van Lint claim page, and the library card
  `theorem_p120`: no conditional bound.
- formal-conjectures: no 879 file. OEIS A186736 (read): data and programs only.
- arXiv: the web search worked this session (the API was rate-limited, HTTP 429).
  Queries: "pairwise coprime" (≈100 results, titles filtered), "mutually coprime
  integers", "relatively prime sets sum", "largest sum pairwise coprime", "Erdos van
  Lint", "Erdos problem 879", and others. Nothing relevant. This searches metadata
  only, not full text.

## Sources not read

- **Schoenfeld 1976** (Math. Comp. 30, 337–360). AMS returned 403
  (`refs/schoenfeld/AMS_403_response.html`). I used Büthe Thm 2 instead, which I read.
  It is a refereed restatement and independent proof under (partial) RH.
- **[Er98]** Erdős, "Some of my new and almost new problems and results in combinatorial
  number theory" (Eger 1996, pp.169–180). erdosproblems.com cites it for 879; I could
  not locate it in the Rényi archive. It might restate or sharpen the bounds.
- **Nieuw Archief problem 623 (1983)** and any published solution, and any van Lint
  write-up. Not accessed.
- **The Lean RH proof itself.** I read only the README, `comparator.json` and
  `src/Challenge.lean`. I did not build or check it.
