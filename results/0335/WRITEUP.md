# Erdős #335, target T1: Question 16.9 of Ackelsberg–Richter [AcRi26]. DISPROVED, as stated

## Outcome

**DISPROVED.** The answer to the question as written in the arXiv v1 LaTeX source is **No**.

**Statement established (Theorem).** Let N = {1,2,3,...} and [M] = {1,...,M}. There is a set B ⊆ N with
d̄(B) = 1 (in fact d̲(B) = 0 and B contains arbitrarily long intervals) such that for **every** α ∈ (0,1)
there is a set A ⊆ N with natural density d(A) = α and

  d̲(A+B) = α = d(A)   (and d̄(A+B) = 1).

So B is not a d-essential component in the sense of [AcRi26, Question 16.9], because the required strict
inequality d̲(A+B) > d(A) fails for every α. Explicitly:

- N_1 = 1, N_{s+1} = (s+2)^3 · N_s^2 (so N_2 = 27, N_3 = 46656, N_4 = 272097792000, ...);
- W_s = { n ∈ Z : N_s/(s+1) < n ≤ N_s }, B = ⋃_{s≥1} W_s;
- m_k = ⌈α(2k+1)⌉, I_k = [k^2, k^2 + m_k − 1] ∩ Z, A = A_α = ⋃_{k≥1} I_k.

## The question, as checked in the source (VERIFIED)

From `../../refs/acri26_v1.tex` (arXiv:2604.12864 v1):

- Line 400–408: N = {1,2,3,...}, [N] = {1,...,N}, d̲ and d̄ are the liminf/limsup of |A∩[N]|/N, and d(A) is the limit when it exists.
- Line 5853: "Say that a set B ⊆ N is a *d-essential component* if for every A ⊆ N with d(A) ∈ (0,1), one has
  \underline{d}(A+B) > d(A)."
- Line 5859 (Question `question_d-essential_component`): "Is every set with full upper density \overline{d}(B) = 1 a
  d-essential component?"

The bars are present in the .tex; this is the reading attacked here.

## Lemmas and proofs

Throughout, for integers u ≤ v, [u,v] means {n ∈ Z : u ≤ n ≤ v}. For X ⊆ Z and M ≥ 1, X(M) := |X ∩ [1,M]|.

### Lemma 1 (the set A_α). Fix α ∈ (0,1). Then
(a) 1 ≤ m_k ≤ 2k+1 and α(2k+1) ≤ m_k < α(2k+1) + 1;
(b) the I_k are pairwise disjoint and A_α ⊆ N, with min A_α = 1;
(c) d(A_α) = α;
(d) for every M ≥ 1, the number of k with min I_k = k^2 ≤ M is ⌊√M⌋ ≤ √M.

*Proof.* (a) 0 < α(2k+1) < 2k+1 and 2k+1 is an integer, so 1 ≤ ⌈α(2k+1)⌉ ≤ 2k+1; the second chain is the
definition of the ceiling. (b) By (a), I_k ⊆ [k^2, k^2+2k] = [k^2, (k+1)^2 − 1], and these ranges are disjoint for
distinct k. I_1 starts at 1 and m_1 ≥ 1, so 1 ∈ A_α, and all elements are ≥ 1. (d) k^2 ≤ M iff k ≤ ⌊√M⌋.
(c) Let M ≥ 1 and K = ⌊√M⌋ ≥ 1, so K^2 ≤ M < (K+1)^2. Blocks with k ≥ K+1 start at k^2 ≥ (K+1)^2 > M, and
blocks with k ≤ K−1 end at ≤ K^2 − 1 < M. Hence, using disjointness,

  Σ_{k=1}^{K−1} m_k ≤ A_α(M) ≤ Σ_{k=1}^{K} m_k.

By (a), Σ_{k=1}^{K−1} m_k ≥ α Σ_{k=1}^{K−1}(2k+1) = α(K^2 − 1), and Σ_{k=1}^{K} m_k ≤ α((K+1)^2 − 1) + K.
Dividing by M with K^2 ≤ M < (K+1)^2:

  α(K^2 − 1)/(K+1)^2 ≤ A_α(M)/M ≤ (α((K+1)^2 − 1) + K)/K^2.

As M → ∞, K → ∞ and both bounds tend to α. So d(A_α) exists and equals α. ∎

### Lemma 2 (thickening a union of intervals). Let A = ⋃_{j∈J} [u_j, v_j] with integers 1 ≤ u_j ≤ v_j, and for
M ≥ 1 let r(M) = #{ j : u_j ≤ M } (assumed finite). For an integer L ≥ 0 put A^{+L} = A + [0,L] = {a+i : a∈A, 0≤i≤L}.
Then for every M ≥ 1,

  A^{+L}(M) ≤ A(M) + L · r(M).

*Proof.* Let x ∈ A^{+L} ∩ [1,M], say x = a + i with a ∈ [u_j, v_j] and 0 ≤ i ≤ L. Then x ≥ a ≥ u_j, and x ≤ M,
so u_j ≤ M, i.e. j is one of the r(M) indices counted. If x ≤ v_j then x ∈ [u_j, v_j] ⊆ A, so x ∈ A ∩ [1,M].
Otherwise v_j < x ≤ v_j + L (because a ≤ v_j and i ≤ L), so x lies in the set (v_j, v_j + L] ∩ Z, which has
exactly L elements. Therefore

  A^{+L} ∩ [1,M] ⊆ (A ∩ [1,M]) ∪ ⋃_{j : u_j ≤ M} ((v_j, v_j+L] ∩ Z),

and the right side has at most A(M) + L·r(M) elements. ∎

(Lemma 2 does not need the intervals to be disjoint or maximal; it was also brute-force tested on 300 random
interval families, see code.)

### Lemma 3 (the set B). With N_s, W_s, B as above and M_s := (s+2)^2 N_s^2:
(a) every N_s is a positive integer, N_{s+1} = (s+2) M_s, and N_s/(s+1) is nondecreasing in s; N_s is strictly increasing;
(b) |W_s| ≥ s N_s/(s+1); hence d̄(B) = 1;
(c) for every s ≥ 1, B ∩ [1, M_s] ⊆ [1, N_s]; hence d̲(B) = 0;
(d) min B = 1.

*Proof.* (a) Induction gives positive integers, and (s+2)M_s = (s+2)^3 N_s^2 = N_{s+1} by definition. Also
N_{s+1}/(s+2) = (s+2)^2 N_s^2 ≥ N_s ≥ N_s/(s+1) since N_s ≥ 1; and N_{s+1} ≥ (s+2)^3 N_s > N_s.
(b) W_s = [⌊N_s/(s+1)⌋ + 1, N_s], so |W_s| = N_s − ⌊N_s/(s+1)⌋ ≥ N_s − N_s/(s+1) = s N_s/(s+1). Since W_s ⊆ [1,N_s],
B(N_s)/N_s ≥ s/(s+1) → 1; and B(N)/N ≤ 1 always, so d̄(B) = 1.
(c) Let b ∈ B, say b ∈ W_t. If t ≤ s then b ≤ N_t ≤ N_s by (a). If t ≥ s+1 then, by (a),
b > N_t/(t+1) ≥ N_{s+1}/(s+2) = M_s, so b ∉ [1, M_s]. Thus B ∩ [1,M_s] ⊆ [1,N_s], so B(M_s)/M_s ≤ N_s/M_s
= 1/((s+2)^2 N_s) → 0, giving d̲(B) = 0.
(d) W_1 = { n : 1/2 < n ≤ 1 } = {1}. ∎

### Theorem. For every α ∈ (0,1), with A = A_α: d(A) = α, d̲(A+B) = α, d̄(A+B) = 1. In particular B (which has
d̄(B) = 1) is not a d-essential component.

*Proof.* d(A) = α is Lemma 1(c).

*Upper bound on d̲(A+B).* Fix s ≥ 1 and let x ∈ (A+B) ∩ [1, M_s], x = a + b with a ∈ A, b ∈ B. Since a ≥ 1,
b ≤ x − 1 < M_s, so b ∈ B ∩ [1, M_s] ⊆ [1, N_s] by Lemma 3(c). Hence x ∈ A + [1, N_s] ⊆ A + [0, N_s] = A^{+N_s}.
Apply Lemma 2 to the representation A = ⋃_k I_k (u_k = k^2, so r(M) ≤ √M by Lemma 1(d)) with L = N_s and
M = M_s (note √M_s = (s+2)N_s is an integer):

  (A+B)(M_s) ≤ A(M_s) + N_s · (s+2) N_s = A(M_s) + M_s/(s+2).

Divide by M_s. Since M_s → ∞, A(M_s)/M_s → α by Lemma 1(c), so (A+B)(M_s)/M_s ≤ α + o(1), and
d̲(A+B) ≤ liminf_s (A+B)(M_s)/M_s ≤ α.

*Lower bound.* 1 ∈ B (Lemma 3(d)), so A + 1 ⊆ A + B and (A+B)(M) ≥ A(M−1) for M ≥ 2. Since
A(M−1)/M → α, d̲(A+B) ≥ α. Together, d̲(A+B) = α = d(A), so the strict inequality d̲(A+B) > d(A) fails.

*Upper density.* 1 ∈ A (Lemma 1(b)), so 1 + B ⊆ A + B and (A+B)(N_s + 1) ≥ |1 + W_s| ≥ s N_s/(s+1); dividing by
N_s + 1 and letting s → ∞ gives d̄(A+B) = 1. ∎

**Why it works (one line).** d̄(B) = 1 only constrains B at the sparse scales N_s; d-essentiality is a lower-density
(liminf) condition, and at the intermediate scales M_s (with N_s ≪ √M_s) the part of B seen so far is a bounded set
[1,N_s], which barely thickens a set A whose number of blocks up to M is O(√M).

## Computation (sanity checks only; the proof above does not depend on it)

Code: `code/verify.py` (exact Python integers / Fractions; no floating point in any assertion).
Output: `out/verify_output.txt`. Reproduce with

    cd attack/335/t1/prove && python3 -I code/verify.py

It checks: Lemma 2 by brute force on 300 random interval families; the identities N_{s+1} = (s+2)M_s and
min W_{s+1} = M_s + 1 (Lemma 3(c)) for s ≤ 3; that √M_s is an integer; the inequalities
A(M_s − 1) ≤ (A+B)(M_s) ≤ A(M_s) + N_s√M_s for α ∈ {1/2, 1/3, 9/10, 1/100} and s = 1,2,3 (M_3 ≈ 5.4·10^10, computed by
exact interval-union counting); and, for M_s ≤ 20000, that brute-force (A+B) ∩ [1,M_s] computed with **all** of
B ∩ [1,M_s] equals the count using only W_1..W_s. All passed. The numerics show the expected slow approach
(excess over α is at most 1/(s+2): e.g. α=1/2, s=3 gives 0.680 ≤ bound 0.700); this is a proof, not an
extrapolation from data. Faster growth of N_s would make the excess visibly small, but is unnecessary.

## What this does and does not show

Does show (rigorous): Question 16.9 of [AcRi26] **as written in the v1 .tex** has a negative answer, with an explicit
B and, for every α ∈ (0,1), an explicit A. The same B also has upper Banach density 1 (it contains the intervals
W_s of length ≥ s N_s/(s+1) → ∞), so the answer stays No if "full upper density" is read as full upper Banach density.

Does not show / caveats:
- The argument is short and elementary, which raises the possibility that the authors intended a different question.
  INFERRED (not checked with the authors) nearby readings: (i) conclusion with d̄(A+B) instead of d̲(A+B):
  then the answer is trivially Yes, since d̄(A+B) ≥ d̄(min A + B) = d̄(B) = 1 > d(A); (ii) hypothesis d̲(B) = 1: trivially
  Yes for the same reason with lower densities; (iii) more interesting variants, e.g. B with d(B) existing and
  positive, B with d̲(B) > 0, or B with positive density meeting every residue class: **not addressed here**.
  Our B has d̲(B) = 0, so it says nothing about those.
- It does not touch Erdős #335 itself (the characterisation of d(A+B) = d(A)+d(B)); it concerns the degenerate
  phenomenon d(A+B) = d(A) of [AcRi26, Prop. 15.1] only in the lower-density sense.
- Novelty: not found on the #335 page, the #335 forum thread (2 comments, both about [AcRi26] generally),
  or Plasma's E0335 pages (grep for "essential", "16.9", "upper density" found nothing). A quick arXiv API search
  for "essential component" returned nothing relevant (search was noisy). Given how short the argument is, it may be
  known to experts or folklore; do not present it as a significant result.

## Sources read
- `../../refs/acri26_v1.tex` (arXiv:2604.12864 v1), lines 395–410 (definitions) and 5800–5860 (questions).
- `refs/page335.html`, `refs/forum335.html` (erdosproblems.com, fetched 2026-11-23).
- Plasma AI `wiki/problems/additive_combinatorics/E0335/_index.md` and `claims/2026_04_14_ackelsberg_richter.md` (grep only).

## Sources not read
- I. Z. Ruzsa, *Essential components*, Proc. London Math. Soc. (3) 54 (1987). It treats Schnirelmann- and
  lower-density essential components; it may contain this or a stronger construction. The proof above is
  self-contained and does not rely on it.
- The rest of [AcRi26] beyond the lines listed (in particular the proof of Prop. 15.1).
- ryantuck/erdos-ai; any literature after a quick arXiv search.
