# Erdős Problem 451: what RH adds to the van Doorn–Tang bound

Written 22 Nov 2026. The lead was "under RH, θ can be any constant in (1/2, 21/40), and c stays 1/20". That lead holds, but it is a one-line corollary. While checking Sec. 6 of the paper step by step, I found that its large-n accounting wastes constant factors. With those factors removed, the admissible constant is any c < (1−θ)/3. That gives c < 19/120 from the same input the paper uses, and c < 1/6 under RH. The proof follows.

Notation: L = log k, ℓ = log log k, I = I_k = (k, k+k^θ), ‖x‖ = distance to the nearest integer, and
K = K(k,n,θ) = #{ m ∈ ℤ ∩ I : ‖n/m‖ < k^{θ−1} }.

## Exact final statement

**Hypothesis P(θ).** There are κ > 0 and k₀ such that for all k ≥ k₀ the interval (k, k+k^θ) contains at least κ k^θ / log k primes. This is the hypothesis of vDTa26, p. 1, verbatim.

**Theorem 1 (master).** Let θ ∈ (2/5, 3/5) satisfy P(θ), and let 0 < c < (1−θ)/3. Then for all sufficiently large k and all integers n with
  2k < n ≤ exp(c log²k / log log k),
some prime p ∈ (k, k + 3k^θ) divides (n−k)(n−k+1)···(n−1). Since 3k^θ < k for large k, it follows that n_k > exp(c log²k / log log k) for all large k.

**Corollary 2 (RH).** Assume RH for ζ only. No Dirichlet L-function, Dedekind zeta or other L-function is used, so GRH for Dirichlet L-functions is not needed.
 (a) For every θ ∈ (1/2, 3/5) and every c < (1−θ)/3, the conclusion of Theorem 1 holds.
 (b) For every c < 1/6: n_k > exp(c log²k / log log k) for all large k.
 (c) This is the lead's claim. For every ε ∈ (0, 1/10), the paper's own c = 1/20 holds with θ = 1/2 + ε. That is, some prime p ∈ (k, k + 3k^{1/2+ε}) divides the product for all large k and all 2k < n ≤ exp(log²k/(20 log log k)).
 This is unconditional if the Alpöge Lean proof of Mathlib's `RiemannHypothesis` is accepted. The step from RH to the prime-count bound (Lemma R) is classical literature, not Lean (see below).

**Corollary 3 (same input as the paper, BHP).** Assume P(21/40). The paper takes it from Baker–Harman–Pintz [vDTa26 ref. 2], and the authors' Lean file states it as `axiom bhp`. Then for every c < 19/120 (≈ 0.158), the conclusion of Theorem 1 holds with θ = 21/40. In particular n_k > exp(c log²k/log log k) for large k. The published constant is c = 1/20 = 0.05.

## Sources and what each was checked for

- **[vDT]** W. van Doorn, Q. Tang, arXiv:2606.19863v2 (17 Nov 2026). Local copy at `../refs424/vDTa26.pdf` and `.txt`. I read the full text and checked pp. 3–5 against the rendered PDF pages.
  - Theorem 1.1 and hypothesis P(θ): p. 1.
  - Small n: Sec. 2.
  - Medium n: Sec. 3.
  - Theorem 4.1 (eq. (1)): p. 3.
  - Medium-large n: Sec. 5.
  - Large n: Sec. 6, with c = 1/20 and r₀ = ⌈2c log k / log log k⌉.
- **Theorem 4.1 of [vDT]** (VERIFIED wording, p. 3). Let r be an integer with 2 ≤ r ≤ ½k^{1−θ} and λ ≥ 1. Then
  K ≪ k^θ [ (n r! λ^r / k^{r+1})^{1/(2r−1)} + (k^{r+θ}/(n r! λ^r))^{1/(r−1)} + ((r+1)λ/k)^{1/(2r)} ] + rλ.
  - The proof (pp. 3–4) applies Konyagin's [8, Theorem 2] with N = k^θ, W = 1, f(x) = (−1)^r n/(k+x), D_r = n r!/k^{r+1}, δ = k^{θ−1}.
  - It uses no property of θ beyond 0 < θ < 1 and r ≤ ½k^{1−θ}. In particular it does not use P(θ).
  - Cross-check: the authors' Lean file `refs/ErdosProblem451.lean` (Woett/Lean-files, last changed 19 Jun 2026) states `konyagin_thm` for arbitrary r ≥ 2, N > 0, W ≥ 1, δ > 0, λ ≥ 1 and f satisfying derivative bounds. Its bound is c₆·N·[(D_rλ^rW²)^{1/(2r−1)} + (δW²/(D_rλ^r))^{1/(r−1)} + (D_{r+1}λW²/D_r)^{1/(2r)}] + 2rλ.
  - With D_{r+1}/D_r = (r+1)/k and δ/(D_rλ^r) = k^{r+θ}/(n r! λ^r), this is eq. (1). I read the statement. I did not build the file.
  - The file has one axiom (`bhp`, with θ fixed to 21/40) and grep finds no `sorry`.
- **[Sch76]** L. Schoenfeld, Math. Comp. 30 (1976), Theorem 10: under RH, |ϑ(x) − x| < (1/(8π)) √x log²x for all x ≥ 599. Here ϑ(x) = Σ_{p≤x} log p.
  - VERIFIED as restated, with the same hypothesis (RH) and range (x ≥ 599), in two independent secondary sources held locally:
    - Axler, arXiv:1703.08032, eq. (2.6), p. 2–3 (`../../grh/428/refs/referee-source/axler_1703.08032.txt`).
    - Broadbent–Kadiri–Lumley–Ng–Wilk, arXiv:2002.11068, eq. (1.5) and the following sentence (`../../grh/428/refs/referee-source/bklnw_2002.11068.txt`).
  - Both call it an effective form of von Koch's theorem.
  - I could not read the primary paper: ams.org returned a bot-check page, and I did not try to get around it.

## Lemmas and proofs

### Lemma R (RH ⇒ P(θ), uniformly in shifted windows)
Assume RH and fix θ ∈ (1/2, 1). There is x₀ such that for all x ≥ x₀ and all h with x^θ/4 ≤ h ≤ x, the interval (x, x+h) contains at least h/(8 log x) primes.

*Proof.* The primes in (x, x+h) include those in (x, x+h/2]. By [Sch76] at both endpoints (x ≥ 599, and x + h/2 ≤ 2x):
ϑ(x+h/2) − ϑ(x) ≥ h/2 − (1/(8π))(√(x+h/2) log²(x+h/2) + √x log²x) ≥ h/2 − (1/(4π))√(2x) log²(2x).
Since θ > 1/2, √(2x) log²(2x)/(4π) ≤ x^θ/16 ≤ h/4 for x large. So ϑ(x+h/2) − ϑ(x) ≥ h/4.
Each prime in (x, x+h/2] contributes log p ≤ log(2x) ≤ 2 log x. So there are at least h/(8 log x) of them. ∎

Consequences:
- Under RH, P(θ) holds with κ = 1/8 (take x = k, h = k^θ).
- Lemma W below also holds directly. For a ∈ [k, k+2k^θ] we have a ≤ 2k, so h = k^θ ≥ a^θ/4 (since 2^θ < 4) and h ≤ a.

### Lemma W (shifted window from P(θ))
Let θ ∈ (0,1) satisfy P(θ). For all large k and every real a with k ≤ a ≤ k + 2k^θ, the interval (a, a+k^θ) contains a prime.

*Proof.*
1. Let N = ⌈a⌉. Then a ≤ N ≤ k + 2k^θ + 1, and by P(θ) the interval (N, N+N^θ) has ≥ κN^θ/log N ≥ κk^θ/(2L) primes (large k).
2. Since N ≥ a, (N, N+N^θ) \ (a, a+k^θ) ⊂ [a+k^θ, N+N^θ). This set has length ≤ 1 + (N^θ − k^θ).
3. By the mean value theorem, N^θ − k^θ ≤ θk^{θ−1}(N−k) ≤ k^{θ−1}(2k^θ+1) ≤ 2k^{2θ−1} + 1. So it contains at most 2k^{2θ−1} + 3 integers.
4. Since 2θ−1 < θ, κk^θ/(2L) − 2k^{2θ−1} − 3 > 0 for large k. ∎

The authors' Lean file proves the same thing as `exists_prime_in_window`. The paper's Sec. 2 needs this step but does not state it.

### Lemma F (far prime divides the product; [vDT] Sec. 3, first paragraph)
Let n > 2k, and let p ∈ I be prime with ‖n/p‖ ≥ k^{θ−1}. Then p | (n−k)···(n−1).

*Proof.*
1. Let j = n mod p ∈ {0, …, p−1}. Then ‖n/p‖ = min(j, p−j)/p, so min(j, p−j) ≥ p k^{θ−1} > k^θ ≥ 1.
2. Hence j ≥ 1 and j < p − k^θ < k, using p < k + k^θ.
3. So 1 ≤ j ≤ k and p | n − j, which is a factor of the product. ∎

Corollary: if P(θ) holds and K < κk^θ/L, then some prime p ∈ I has ‖n/p‖ ≥ k^{θ−1}, so p | product, and p ∈ (k, k+3k^θ). So in Lemmas M, ML and L it suffices to show K = o(k^θ/L) uniformly in n in the range.

### Lemma S (small n: 2k < n ≤ ½k^{2−θ}; [vDT] Sec. 2)
*Proof.*
1. Let m = ⌈n/k⌉ − 1. Then mk < n ≤ (m+1)k, m ≥ 2, and m < n/k ≤ ½k^{1−θ}. So (2m−1)k^θ < 2m k^θ < k.
2. **Case n < mk + mk^θ.** Lemma W with a = k + (m/(m−1))k^θ (valid since m/(m−1) ≤ 2) gives a prime p with k + (m/(m−1))k^θ < p < k + ((2m−1)/(m−1))k^θ ≤ k + 3k^θ. Then:
   - (m−1)p > (m−1)k + mk^θ > n − k.
   - (m−1)p < (m−1)k + (2m−1)k^θ < mk < n.
   - So (m−1)p is one of n−k, …, n−1, and p divides the product.
3. **Case mk + mk^θ ≤ n ≤ (m+1)k.** P(θ) gives a prime p ∈ I (there is at least one for large k). Then n − k ≤ mk < mp < mk + mk^θ ≤ n, so mp is one of the factors. ∎

### Lemma M (medium n: ½k^{2−θ} < n ≤ k²/L²; [vDT] Sec. 3)
Here K ≤ 3 + 28k^{2θ−1} + k^θ/L² = o(k^θ/L).

*Proof.*
1. For m ∈ I, n/m ∈ (n/(k+k^θ), n/k). If ‖n/m‖ < k^{θ−1} < 1/2, the nearest integer h to n/m lies in J = [⌊n/(k+k^θ)⌋, ⌈n/k⌉].
2. Also |J ∩ ℤ| ≤ 3 + n/k − n/(k+k^θ) < 3 + n/k^{2−θ}.
3. Fix h ∈ J ∩ ℤ. Write u = n/k ≥ ½k^{1−θ} and ε = k^{θ−1} ≤ 1/10 (large k).
   - We have m < (1+ε)k and h > u/(1+ε) − 1/2.
   - So m/h ≤ 2k/u = 2k²/n, because u(2/(1+ε) − (1+ε)) ≥ 0.71u ≥ 1.
   - This is the paper's inequality m/h < 2k/(n/k). The paper does not spell out this check.
4. So |m − n/h| = (m/h)|n/m − h| < 2k^{1+θ}/n, which leaves at most 1 + 4k^{1+θ}/n choices of m for each h.
5. Therefore K ≤ (1 + 4k^{1+θ}/n)(3 + n/k^{2−θ}) = 3 + n/k^{2−θ} + 12k^{1+θ}/n + 4k^{2θ−1} ≤ 3 + k^θ/L² + 28k^{2θ−1}, using n > ½k^{2−θ} and n ≤ k²/L².
6. Since 2θ − 1 < θ, this is o(k^θ/L). ∎

### Lemma ML (medium-large n: k²/L² < n ≤ ½k^{2+θ}; [vDT] Sec. 5)
*Proof.*
1. Apply Theorem 4.1 with r = 2 (≤ ½k^{1−θ} for large k) and λ = √(k^{2+θ}/(2n))·L. Then λ ≥ L ≥ 1, since n ≤ ½k^{2+θ}.
2. Directly:
   - first term = (k^{θ−1}L²)^{1/3};
   - second term = 1/L²;
   - λ ≤ k^{θ/2}L²/√2 (using n > k²/L²), so third term = (3λ/k)^{1/4} ≤ 2k^{(θ−2)/8}√L;
   - rλ ≤ √2 k^{θ/2}L².
3. Hence K ≪ k^θ(k^{(θ−1)/3}L^{2/3} + L^{−2} + k^{(θ−2)/8}√L) + k^{θ/2}L² = o(k^θ/L), for any fixed θ ∈ (0,1). ∎

### Lemma G (the exponent function)
For θ ∈ (0,1) and real r ≥ 3, let g(r) = [2 − θ − (1−θ)(2r−1)/(3r−2)]/r. Then g is strictly decreasing on [3, ∞), and g(3) = (9−2θ)/21 ≤ 3/7.

*Proof.*
1. g(r) = (ar − b)/(3r² − 2r), with a = 4−θ and b = 3−θ. This uses (2−θ)(3r−2) − (1−θ)(2r−1) = (4−θ)r − (3−θ).
2. The numerator of g′ is a(3r²−2r) − (ar−b)(6r−2) = −3ar² + 6br − 2b.
3. For r ≥ 3, this is ≤ r(6b − 9a) − 2b = r(3θ − 18) − 2b < 0.
4. g(3) = (3a−b)/21 = (9−2θ)/21. ∎

I checked this numerically for θ ∈ {0.401, 0.5, 0.501, 0.525, 0.599} and r ∈ [3, 5000).

### Lemma L (large n: ½k^{2+θ} < n ≤ exp(cL²/ℓ), with 0 < c < (1−θ)/3 and θ ∈ (9/23, 1)). New accounting.
Then K = o(k^θ/L) uniformly in n in this range.

*Proof.*
**Choosing r.**
1. Fix η > 0 with a := (1−θ)/(3(1+η)c) > 1. Then (1+η)c < (1−θ)/3 < 14/69, since θ > 9/23.
2. Let r₁ = ⌈(1+η)cL/ℓ⌉. For large k, r₁ ≤ L/ℓ, so log r₁ ≤ ℓ and log(r₁!) ≤ r₁ℓ.
3. For n in range: log n + log(r₁!) ≤ cL²/ℓ + r₁ℓ ≤ r₁(L − ℓ) + r₁ℓ ≤ (r₁+θ)L. The middle step uses cL²/ℓ ≤ (1+η)(cL/ℓ)(L−ℓ) ≤ r₁(L−ℓ), which holds once (1+η)(1 − ℓ/L) ≥ 1.
4. So n·r₁! ≤ k^{r₁+θ}, and the least positive integer r with n r! ≤ k^{r+θ} exists and satisfies r ≤ r₁.
5. r ≥ 3: r = 1 would need n ≤ k^{1+θ}, and r = 2 would need 2n ≤ k^{2+θ}; both contradict n > ½k^{2+θ} (k > 2).
6. Also r ≤ r₁ ≤ ½k^{1−θ}.

**Choosing λ.**
7. Let λ = (k^{r+1−(1−θ)(2r−1)/(3r−2)}/(n r!))^{1/r}, as in [vDT] Sec. 6. Since n r! ≤ k^{r+θ}, λ^r ≥ k^{(1−θ)(r−1)/(3r−2)} ≥ 1. So Theorem 4.1 applies.

**First two terms.**
8. Substituting λ^r, the first term is (k^{−(1−θ)(2r−1)/(3r−2)})^{1/(2r−1)} = k^{(θ−1)/(3r−2)}.
9. The second term is k^{(1−θ)[(2r−1)/(3r−2) − 1]/(r−1)} = k^{(θ−1)/(3r−2)}. (Also checked numerically on 1000 random cases.)
10. Since 3r − 2 ≤ 3r₁ − 2 < 3(1+η)cL/ℓ + 1:
    k^{(θ−1)/(3r−2)} ≤ exp(−(1−θ)ℓ/(3(1+η)c + ℓ/L)) ≤ L^{−(1+a)/2} for large k.
11. This is o(1/L).

**Third term.**
12. By minimality of r (r−1 ≥ 2 is a positive integer below r), n(r−1)! > k^{r−1+θ}, so n r! > k^{r−1+θ}.
13. Hence λ^r < k^{r·g(r)}, so λ < k^{g(3)} ≤ k^{3/7} by Lemma G.
14. Then ((r+1)λ/k)^{1/(2r)} < (r+1)^{1/(2r)} k^{−2/(7r)} ≤ 2k^{−2/(7r₁)}, using r+1 ≤ 4^r.
15. Also k^{−2/(7r₁)} ≤ exp(−2ℓ/(7(1+η)c + 7ℓ/L)) ≤ L^{−6/5} for large k, since 7(1+η)c < 98/69 < 1.43 and 2/1.43 > 6/5. This is o(1/L).

**Additive term.**
16. rλ < r₁k^{g(3)} = r₁ k^{(9−2θ)/21} with r₁ = O(L).
17. (9−2θ)/21 < θ is exactly θ > 9/23, so rλ = o(k^θ/L).

**Conclusion.**
18. With the implied constant C_θ of eq. (1): K ≤ C_θ[k^θ(2k^{(θ−1)/(3r−2)} + ((r+1)λ/k)^{1/(2r)}) + rλ] = o(k^θ/L).
19. The bounds depend only on k, so this is uniform in n. ∎

Where the paper loses constants:
- It uses r ≤ r₀ = ⌈2cL/ℓ⌉. That is about twice the true size cL/ℓ.
- It uses 3r₀ − 2 < 7cL/ℓ instead of ≈ 6cL/ℓ.
- For the third term it uses r ≥ 3 to get k^{−1/(6r)}.

These lead to c < min((1−θ)/7, 1/13). That is 19/280 at θ = 21/40 and 1/14 as θ → 1/2, as the lead's argument said. The rewrite above needs only c < (1−θ)/3.

### Proof of Theorem 1
For large k, the four ranges (2k, ½k^{2−θ}], (½k^{2−θ}, k²/L²], (k²/L², ½k^{2+θ}] and (½k^{2+θ}, exp(cL²/ℓ)] cover (2k, exp(cL²/ℓ)]. The last range may be empty.
- On the first range, Lemma S gives the prime directly.
- On the other three, Lemmas M, ML and L give K = o(k^θ/L) uniformly. With P(θ), some prime p ∈ I is outside the K-set, and Lemma F applies.

Every prime found lies in (k, k+3k^θ) ⊂ (k, 2k) once 3k^θ < k. So every such n fails the defining property of n_k, and n_k > exp(cL²/ℓ). ∎

### Proofs of the corollaries
- **2(a).** Lemma R gives P(θ), and Lemma W, for every θ ∈ (1/2, 3/5) ⊂ (2/5, 3/5).
- **2(b).** Given c < 1/6, pick θ ∈ (1/2, min(3/5, 1−3c)). Then c < (1−θ)/3.
- **2(c).** θ = 1/2 + ε with ε < 1/10, and 1/20 < (1/2 − ε)/3 ⟺ ε < 7/20.
- **3.** θ = 21/40 ∈ (2/5, 3/5), and (1 − 21/40)/3 = 19/120.

## Numerical sanity checks
These were run with python3 -I. The script is in the scratchpad at `451/check2.py`.

- (1 + 1/(2r))^{r+1} < 2 for r ≥ 2 (max 1.953 at r = 2). This is the [vDT] Thm 4.1 derivative check.
- Lemma G was checked numerically (see above).
- The first two Konyagin terms are equal (checked numerically).
- In log space for L = log k ∈ {10³, …, 10¹⁶}, I computed the least r and r₁ for:
  - (c, θ) = (1/20, 21/40), (0.15, 21/40), (0.155, 21/40), (0.16, 0.505), (0.165, 0.5001).
  - In every case r ≤ r₁, and log(L·T₁) < 0 and decreasing (slowly, as L^{−(a−1)/2} predicts).
  - The third and additive terms are far smaller.
  - Above the threshold, with c = 0.18 and θ = 0.5, log(L·T₁) increases with L. So (1−θ)/3 is the true limit of this accounting.
- Schoenfeld's ϑ-bound holds for 599 ≤ x ≤ 2·10⁶ (max ratio 0.92). This is consistent with the unconditional verification Axler cites to 1.4·10²⁵.
- Prime counts in (x, x + x^θ/4) for x ≤ 10⁶ are not informative. The window there is shorter than Schoenfeld's error term, and Lemma R is asymptotic.

## What this does and does not show
- **The problem as posed** ("estimate n_k") stays OPEN. Nothing here touches the upper bound e^{(1+o(1))k}, Erdős's e^{εk} expectation, or the k/log k heuristic. The lower-bound shape exp(c log²k/log log k) from Konyagin's method is unchanged. Only the constant improves.
- **Constant c:**
  - from the same input as the paper: 1/20 → any c < 19/120;
  - under RH: any c < 1/6.
- **RH's contribution:**
  - the constant goes from 19/120 to 1/6;
  - the dividing prime is localized in (k, k + 3k^{1/2+ε}) instead of (k, k + 3k^{21/40}).
- **The lead's own claim** (Cor. 2(c), and "within the paper's accounting c < 1/14") is correct. But it is superseded by Cor. 3, which needs no RH and beats it. As the screener predicted, re-optimizing without RH moves c more than RH does.
- **Lean / databases:**
  - google-deepmind/formal-conjectures has no `ErdosProblems/451.lean` on origin/main.
  - teorth/erdosproblems lists 451 as open/unformalized (last update 2025-08-31).
  - The unofficial draft in ryantuck/erdos-ai `conjectures/451.lean` states (n_k > k^d for all d, for large k) ∧ (n_k < e^{εk} for all ε). The first conjunct already follows from vDT. The second is untouched.
  - The authors' Lean file fixes θ = 21/40 and c = 1/20. Formalizing Cor. 3 would mean changing only the large-n part (`case_large` and its helper lemmas). Formalizing Cor. 2 would also need RH ⇒ Schoenfeld/von Koch, which is not in Mathlib.
- **Not shown (remark, INFERRED only):** under RH one could probably take k^θ replaced by H = A√k log²k, giving p ∈ (k, k + 3A√k log²k). That would need Theorem 4.1 with a k-dependent θ and an absolute implied constant. The Lean `konyagin_thm` has an absolute c₆ and arbitrary N, δ, but I did not write this version out, so it is not claimed.

## Credit
- **The method and every lemma except Lemma L's new accounting and Lemma R:** van Doorn–Tang [vDT]. Its declaration says the core idea came from ChatGPT 5.5 Pro, and the Lean file was made with Aristotle.
- **The underlying method:** Konyagin (1999).
- **RH ⇒ ϑ-bound:** von Koch (1901) and Schoenfeld (1976).
- **RH:** Alpöge (Lean, 20 Nov 2026), per the brief. I did not re-check this.
- **The re-optimized large-n accounting (c < (1−θ)/3) and the RH substitution:** this note, prepared with Claude.

**Prior-recording check:**
- [vDT] v2 has c = 1/20 and no RH remark.
- The erdosproblems.com page (last edited 21 Jun 2026) and the forum thread (6 comments, last 19 Jun 2026; refetched 22 Nov 2026) have no RH remark and no improved constant.
- Plasma's E0451 page (updated 2026-10-15) and its claim page record only θ = 21/40, BHP and c = 1/20.
- ryantuck/erdos-ai has only statement and review files for 451.
- The authors' repos (Woett/Lean-files, last 451 change 19 Jun 2026; QuanyuTang/Notes-on-Erdos-Problem-451, last commit 26 Apr 2026) have nothing newer.

## Sources not read
- **Konyagin**, Mathematika 46 (1999), Theorem 2. I relied on [vDT] Thm 4.1 and on the Lean statement `konyagin_thm`. The Lean file was not built.
- **Baker–Harman–Pintz** (2001). P(21/40) is taken as [vDT] states it.
- **Schoenfeld** (1976), primary text: AMS returned a bot-check page. I used the Axler and BKLNW restatements instead.
- **von Koch** (1901).
- **Sutherland's GRH page.**
- **A fresh arXiv search after v2:** the arXiv API answered "Rate exceeded".
- **The model write-up in Woett/ChatGPT-s-note-on-Erdos451.**
