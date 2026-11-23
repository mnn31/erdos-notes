# Erdős Problem 91, cases n = 10, ..., 15: which n have a unique minimiser?

Date: 2026-11-23. Folder: `attack/91/t1/prove/`. Nothing was posted, committed or sent anywhere.

## 0. Bottom line

**Statement established.** Take `UniqueMinimizer n` exactly as defined in
`FormalConjectures/ErdosProblems/91.lean` (origin/main, 2026-11-21). Then

* `¬ UniqueMinimizer 10`, `¬ UniqueMinimizer 11`, `¬ UniqueMinimizer 13`, `¬ UniqueMinimizer 14`,
  `¬ UniqueMinimizer 15`;
* `UniqueMinimizer 12`.

The minimum numbers of distinct distances are f(10)=f(11)=f(12)=5, f(13)=6 and f(14)=f(15)=7.

**The proof depends on these published theorems, used as black boxes:**

* (T-EF) Erdős–Fishburn 1996, Theorem 1;
* (T-W) Wei 2012, Theorems 18 and 19, with an independent computer proof in Szöllősi–Östergård 2020,
  Theorem 16 and Table 9;
* (T-S) Shinohara 2008. This one is needed **only for n = 12**.

Section 1 says how each statement was checked. Everything else is proved below. The
finite facts about lattice sets were checked with exact integer arithmetic.

**This is not new mathematics.** Every case is a short corollary of results already published:

* n=10 can be read off Wei 2012, Theorem 11, which classifies all 10-point 5-distance sets into
  20 classes.
* n=13 can be read off Szöllősi–Östergård 2020, Theorem 16, which gives exactly three 13-point
  6-distance sets.
* n=12 is Shinohara's uniqueness theorem.

As far as I could check, nobody has written these cases down as cases of Problem 91. They are not
in the Lean file, which stops at n=9, and not on the Plasma page. **I could not read the
erdosproblems.com page or its forum**, and either may already record them.

The one point of interest: n = 12 is a value n > 5 where the minimiser **is** unique. Erdős wrote
([Er87b] p.171, via the Plasma card) that he had thought uniqueness fails for every n > 5. The
n = 9 case had already raised the question for him. Problem 91 itself only asks about large n.

## 1. Sources and what was verified

The labels below mean:
* **VERIFIED-text**: I read the statement in the source text, in the file named.
* **VERIFIED-secondary**: I read the statement as quoted by another paper, not in the original.
* **VERIFIED-comp**: checked by the code in `code/`, with exact integers unless stated otherwise.

**(T-EF)** P. Erdős, P. Fishburn, *Maximum planar sets that determine k distances*, Discrete Math. 160
(1996) 115–125, Theorem 1: g(1)=3, g(2)=5, g(3)=7, g(4)=9, g(5)=12. Here g(k) is the largest size of a
planar set with **exactly** k distinct distances.
- VERIFIED-secondary in four places:
  - Wei 2012, p.2 (`refs/wei.txt`);
  - Balaji et al. arXiv:1911.11688, Thm 1.3 (`../../refs/b19.txt`), which uses the "at most k"
    convention;
  - Nozaki–Shinohara arXiv:2009.13111, Table 1 (`refs/ns.txt`);
  - the Plasma source card, which quotes Theorem 1 from page images
    (`../../refs/pl_library_..._theorem_1.md`). That card also notes that EF itself states
    "every planar set of 10 or 13 points determines at least 5 or 6 distances".
- The EF paper itself was not read.

**(T-W)** X. Wei, *A proof of Erdős–Fishburn's conjecture for g(6)=13*, Electron. J. Combin. 19(4)
(2012) #P38.
- VERIFIED-text (`refs/wei2012.pdf`, `refs/wei.txt`):
  - Theorem 18: "There exists no 14-point 6-distance set in the plane."
  - Theorem 19: "g(6) = 13".
  - Here k-distance means exactly k distances (Abstract, §1).
- Independent confirmation, VERIFIED-text (`refs/so2020.pdf`, `refs/so.txt`): F. Szöllősi,
  P. Östergård, *Constructions of maximum few-distance sets in Euclidean spaces*, Electron. J.
  Combin. 27(1) (2020) #P1.23.
  - Theorem 16: "The largest cardinality of a 6-distance set in R² is 13. There are exactly three
    configurations realizing this up to isometry: the regular convex 13-gon, the regular convex
    12-gon with its center point, and a regular hexagram with its center point".
  - Table 9 lists 0 candidate Gram matrices at n = 14.
  - Their search enumerates matrices with at most s distinct off-diagonal entries (§3.1).

**(T-S)** M. Shinohara, *Uniqueness of maximum planar five-distance sets*, Discrete Math. 308 (2008)
3048–3055 (doi:10.1016/j.disc.2007.08.028). Statement used: every 12-point planar set with exactly 5
distinct distances is similar to one fixed set, which is a subset of the triangular lattice.
- VERIFIED-secondary only, but in two papers, read verbatim:
  - Wei 2012, p.2: "Shinohara [5] proved that 12-point 5-distance set which realized for g(5) = 12
    is unique up to similar transformation, that is a subset of L△."
  - Balaji et al. 2019, Thm 1.3(v): "g(5) = 12, and the only 5-optimal configuration is a subset
    of L∆."
- Shinohara's paper itself was **not** read. ScienceDirect returned 403 and I found no preprint.
- Consistent with the Plasma EF card: Erdős–Fishburn proved uniqueness only in some sub-cases of
  their diameter analysis.

**Lean definitions**, VERIFIED-text (`git show origin/main:FormalConjectures/ErdosProblems/91.lean`,
`FormalConjecturesUtil`):
- `distinctDistances A = #(A.offDiag.image dist)`, so 0 is not counted.
- `minimalDistinctDistances ℝ² n = sInf {m | ∃ A, #A = n ∧ distinctDistances A = m}`.
- `IsOptimal A n ⇔ #A = n ∧ distinctDistances A = minimalDistinctDistances ℝ² n`.
- `DilationEquivSimilar A B ⇔ ∃ f : ℝ² ≃ᵈ ℝ², f '' A = B`.
- `UniqueMinimizer n ⇔ ∀ A B, IsOptimal A n → IsOptimal B n → DilationEquivSimilar A B`.

## 2. Notation

* R_n: the vertices of a regular n-gon. R_n^+: R_n together with its centre.
* R_{2m+1} − 1: R_{2m+1} with one vertex removed. By symmetry, all such sets are congruent.
* Triangular lattice point (a,b) means the complex number a + bω, ω = e^{iπ/3}. Its squared norm
  is a² + ab + b², an integer.
* L12: the 12 lattice points
  (−1,−2),(−1,−1),(−1,0),(0,−3),(0,−2),(0,−1),(0,0),(1,−3),(1,−2),(1,−1),(2,−3),(2,−2).
* S16: the lattice hexagon H2 = {(a,b): |a|,|b|,|a+b| ≤ 2} (19 points) minus the three alternate
  corners (2,0),(−2,2),(0,−2).
* For a finite set A with |A| ≥ 2, the *minimum-distance graph* M(A) has vertex set A. Its edges
  are the pairs at distance min{|x−y| : x ≠ y ∈ A}.
* G(k): the largest size of a planar set with **at most** k distinct distances.

## 3. Lemmas

**Lemma 1 (at most k vs. exactly k).** G(1),...,G(6) are 3, 5, 7, 9, 12, 13. Hence:
* every planar set of 10 points has ≥ 5 distinct distances;
* every planar set of 13 points has ≥ 6;
* every planar set of 14 or more points has ≥ 7.

*Proof.* A set X with |X| ≥ 2 and at most k distances has exactly j distances for some
1 ≤ j ≤ k. So |X| ≤ g(j), and G(k) = max_{j≤k} g(j).

By (T-EF) and (T-W), g(1..6) = 3, 5, 7, 9, 12, 13. This sequence is increasing, so G(k) = g(k).
(Wei's Theorem 18 gives g(6) ≤ 13 directly. R_13 gives ≥ 13.)

Now the three claims:
* A 10-point set with ≤ 4 distances would give 10 ≤ G(4) = 9.
* A 13-point set with ≤ 5 distances would give 13 ≤ 12.
* A set of N ≥ 14 points with ≤ 6 distances contains a 14-point subset with ≤ 6 distances, giving
  14 ≤ 13.

Each is a contradiction. ∎

**Lemma 2 (regular polygons).** Let n ≥ 3 and put R_n on a circle of radius ρ. Then:
* R_n has exactly ⌊n/2⌋ distinct distances.
* Its minimum distance 2ρ sin(π/n) is attained exactly by cyclically adjacent pairs, so M(R_n)
  is the cycle C_n.

*Proof.* Let z_j = ρe^{2πij/n}. Then |z_j − z_k| = 2ρ|sin(π(j−k)/n)| = 2ρ sin(πd/n), where
d = min(|j−k| mod n, n − (|j−k| mod n)) ∈ {1, ..., ⌊n/2⌋}. Every such d occurs (take k = 0, j = d).

For these d, πd/n ∈ (0, π/2]. On [0, π/2] the sine is strictly increasing. So distinct d give
distinct distances, and d = 1 gives the unique smallest one. The pairs with d = 1 are exactly
{j, j+1 mod n}, which form C_n. ∎

**Lemma 3 (R_{2m+1} minus a vertex).** Let m ≥ 2 and X = R_{2m+1} − 1. Then:
* X has exactly m distinct distances.
* M(X) is the path P_{2m}, so it has exactly two vertices of degree 1.

*Proof.* Remove z_0 and keep z_1, ..., z_{2m}. Every distance of X is a distance of R_{2m+1}, so
X has at most m distances by Lemma 2.

The pair (z_1, z_{1+d}) for 1 ≤ d ≤ m lies in X, since 1 + d ≤ 2m. It realises the d-th distance,
so X has exactly m distances.

The minimum is still 2ρ sin(π/(2m+1)): adjacent pairs remain in X, and nothing in X is smaller.
The pairs at that distance are the adjacent pairs inside X, namely {z_j, z_{j+1}} for
1 ≤ j ≤ 2m−1. The pairs {z_{2m}, z_0} and {z_0, z_1} are gone. These edges form the path
z_1 − z_2 − ... − z_{2m}. ∎

**Lemma 4 (R_12^+ and R_13^+).**
* R_12^+ has exactly 6 distinct distances. M(R_12^+) is C_12 plus an isolated vertex (the centre).
* R_13^+ has exactly 7 distinct distances.

*Proof.* For R_12^+: the vertex-to-vertex distances are 2ρ sin(πd/12), d = 1..6, by Lemma 2. The
centre-to-vertex distance is ρ = 2ρ sin(π/6), which is the d = 2 value. So there are exactly 6.

The minimum is 2ρ sin(π/12) < 2ρ sin(π/6) = ρ, by monotonicity of sine on [0, π/2]. So the
centre is in no minimum-distance pair, and M is C_12 plus the isolated centre (Lemma 2).

For R_13^+: the six chord values are joined by ρ. Now ρ equals a chord value only if
sin(πd/13) = 1/2, that is πd/13 = π/6 (since πd/13 ∈ (0, π/2)), which forces d = 13/6, not an
integer. So there are 7 distances. ∎

**Lemma 5 (lattice sets; exact).**
* (a) L12 has exactly 5 distinct distances, with squared values {1, 3, 4, 7, 9}.
* (b) For every p ∈ L12, L12 − p has 11 points and exactly 5 distinct distances. Also,
  min distance = 1 and M(L12 − p) has a vertex of degree ≥ 3.
* (c) S16 has exactly 7 distinct distances, with squared values {1, 3, 4, 7, 9, 12, 13}.
  S16 − (−2,0) has 15 points and exactly 7 distinct distances. Its min distance is 1, and the
  vertex (0,0) has degree 6 in M(S16 − (−2,0)).

*Proof.*
* (a) and the distance counts in (b), (c): exact integer computation over all pairs (66, 55, 120
  and 105 pairs) in `code/verify.py`. Output in `out/verify.txt`.
* The degree claims can also be checked by hand. The six lattice neighbours of (a,b) at distance 1
  are (a±1,b), (a,b±1), (a+1,b−1), (a−1,b+1).
  - For (0,−1) they are (±1,−1), (0,0), (0,−2), (1,−2), (−1,0), all in L12.
  - For (0,−2) they are (±1,−2), (0,−1), (0,−3), (1,−3), (−1,−1), all in L12.
  - Removing one point p leaves one of these two vertices, still with its 6 neighbours
    (if p = (0,−1), use (0,−2), otherwise use (0,−1)). Removing p can delete at most one of those
    neighbours, so that vertex has degree ≥ 5 ≥ 3 in M(L12 − p). The minimum distance is 1, since
    unit pairs remain and lattice distances are ≥ 1.
  - In S16 − (−2,0), the six neighbours (±1,0), (0,±1), (1,−1), (−1,1) of (0,0) all have squared
    norm 1. They are present: the removed points have squared norm 4. So (0,0) has degree 6.
* For (b) "exactly 5": the computation gives 5. Independently, ≤ 5 holds as a subset of L12.

The computed degree sequences are listed in `out/verify.txt`. ∎

**Lemma 6 (similarity invariant).** Suppose `DilationEquivSimilar A B` holds, with A finite and
|A| ≥ 2. Then:
* |A| = |B|;
* the number of distinct distances of A equals that of B;
* M(A) and M(B) are isomorphic graphs, and in particular have the same sorted degree sequence.

*Proof.* A dilation equivalence f : ℝ² ≃ᵈ ℝ² satisfies dist(f x, f y) = r·dist(x, y) for a fixed
real r > 0, and it is a bijection. So f restricted to A is a bijection onto f''A = B, and it
multiplies every distance by r.

It follows that:
* t ↦ r t maps the distance set of A bijectively onto that of B, so the counts agree;
* min-dist(B) = r·min-dist(A);
* {x, y} is an edge of M(A) iff {f x, f y} is an edge of M(B).

So f is a graph isomorphism M(A) → M(B). ∎

**Lemma 7 (the value of f).** Write f(n) = `minimalDistinctDistances ℝ² n`. Then
f(10) = f(11) = f(12) = 5, f(13) = 6, f(14) = f(15) = 7. For these n, an n-point set A is optimal
iff it has exactly f(n) distinct distances.

*Proof.*
* Upper bounds: R_10, R_11, L12, R_13, R_14, R_15 are sets of the right size with exactly 5, 5, 5,
  6, 7, 7 distances (Lemmas 2 and 5a). So f(n) is at most these values, being the infimum of a
  nonempty set of naturals containing them.
* Lower bounds: every n-point set has ≥ 5 distances for n ≥ 10, ≥ 6 for n ≥ 13 and ≥ 7 for n ≥ 14
  (Lemma 1; a superset has at least as many distances as any subset). So every element of the set
  is ≥ these values.

The second sentence is the definition of `IsOptimal`. ∎

## 4. The six cases

**Theorem.** ¬UniqueMinimizer n for n ∈ {10, 11, 13, 14, 15}, and UniqueMinimizer 12.

*Proof.* In each non-unique case I give two n-point sets, both with exactly f(n) distances, so both
are optimal by Lemma 7. In each pair, the minimum-distance graphs are not isomorphic, so the sets
are not similar by Lemma 6.

| n | f(n) | A (M(A)) | B (M(B)) | why M(A) ≇ M(B) |
|---|---|---|---|---|
| 10 | 5 | R_10, 5 dist. (C_10, all degrees 2) | R_11 − 1, 5 dist. (P_10) | B has degree-1 vertices (Lemmas 2, 3) |
| 11 | 5 | R_11, 5 dist. (C_11) | L12 − p, 5 dist. | B has a vertex of degree ≥ 3 (Lemmas 2, 5b) |
| 13 | 6 | R_13, 6 dist. (C_13) | R_12^+, 6 dist. (C_12 + isolated vertex) | B has a degree-0 vertex (Lemmas 2, 4) |
| 14 | 7 | R_14, 7 dist. (C_14) | R_15 − 1, 7 dist. (P_14) | B has degree-1 vertices (Lemmas 2, 3) |
| 15 | 7 | R_15, 7 dist. (C_15) | S16 − (−2,0), 7 dist. | B has a vertex of degree 6 (Lemmas 2, 5c) |

For each row, A and B both satisfy `IsOptimal _ n`. If `UniqueMinimizer n` held, then
`DilationEquivSimilar A B` would hold, contradicting Lemma 6.

**n = 12.** Let A and B be optimal 12-point sets. By Lemma 7, each has exactly 5 distinct distances.
By (T-S), there are dilation equivalences f_A, f_B with f_A '' A = L_S and f_B '' B = L_S, where
L_S is Shinohara's set.

(L12 is one such set by Lemma 5a, so L_S may be taken to be L12, though this is not needed.)

Then g = f_B⁻¹ ∘ f_A is a dilation equivalence, since these are closed under inverse and
composition, with ratio r_A / r_B. And g '' A = f_B⁻¹ '' L_S = B. So
`DilationEquivSimilar A B` holds.

One check on the meaning of "similar". Shinohara's "similar transformation" is the classical
notion: a map multiplying all distances by a constant c > 0. Every such map of ℝ² is a dilation
equivalence (ratio c, and bijective, being c times an isometry of ℝ², and isometries of ℝ² are
affine bijections). So the conclusion holds in the Lean sense. If Shinohara allowed only
orientation-preserving maps, the conclusion would only be stronger. ∎

**Further known minimisers.** These are not needed for the theorem.
* n = 10: by Wei 2012 Thm 11 and Lemma 7, the minimisers are exactly 20 similarity classes:
  R_9^+, R_10, R_11−1, a double R_5, and 16 lattice sets.
* n = 13: by Szöllősi–Östergård Thm 16, the minimisers are exactly R_13, R_12^+, and the hexagram
  with centre.
* n = 14: R_13^+ is a third minimiser (Lemma 4). Its M has an isolated vertex.
* The lattice-restricted search (`code/lattice_search.py`) is consistent with all of this. It
  finds at most 9, 12 and 13 lattice points with ≤ 4, 5 and 6 distances (with the distances
  restricted to a window). There is exactly one similarity class of 12-point 5-distance lattice
  sets, namely L12, and one 13-point 6-distance lattice class, the hexagram with centre.

## 5. Reproduce

```
cd attack/91/t1/prove
python3 -I code/verify.py          > out/verify.txt          # exact integer checks + 50-digit cross-check
python3 -I code/lattice_search.py  > out/lattice_search.txt  # sanity search, ~5 s, needs networkx
```

`verify.py` uses exact integer arithmetic for all lattice sets. Its regular-polygon lines are a
non-load-bearing 50-digit `mpmath` cross-check of Lemmas 2–4. The output shows the distance counts
5, 5, 5, 6, 6, 7, 7, 7, 7 and the degree sequences used above.

## 6. What this does and does not show

**Shows.** The exact truth value of `UniqueMinimizer n` for n = 10, ..., 15, as stated in Section 0,
with full proofs modulo (T-EF), (T-W) and (T-S):
* The non-uniqueness cases (10, 11, 13, 14, 15) depend only on (T-EF) and (T-W). Each also has an
  explicit pair of non-similar minimisers, with an elementary non-similarity certificate (the
  minimum-distance graph).
* For n ≤ 13 only (T-EF) is needed. (T-W) has two independent proofs: a human proof (Wei) and a
  computer classification (Szöllősi–Östergård).
* The uniqueness case n = 12 is exactly as strong as Shinohara's theorem, and nothing more.

**Does not show.**
* Nothing about Problem 91 proper, which asks about all large n.
* Nothing about n ≥ 16. For n = 16, f(16) = 7 by S16 and Lemma 1. Whether S16 is the only
  minimiser is open: it is the Bao–Yu lattice conjecture plus the general k = 7 problem. For
  n ≥ 17, f(n) is not even known.
* No new mathematics. Each case is a short corollary of published work (Section 0).
* I did not read Shinohara 2008 or Erdős–Fishburn 1996 in the original. Their statements are
  taken from verbatim quotations in Wei 2012, Balaji et al. 2019, Nozaki–Shinohara 2020 and the
  Plasma source card.
* The Lean predicates are not formalised. A Lean proof would need (T-EF), (T-W) and (T-S) as
  axioms or sorries, or their full formalisation.

## 7. Sources not read

* erdosproblems.com/91 and forum thread /forum/thread/91. WebFetch returned 403, and the `curl`
  request was refused by this session's permission classifier. **These may already record the
  n ≥ 10 cases.** This must be checked before any claim of novelty or any upstream contribution.
* Shinohara, Discrete Math. 308 (2008) 3048–3055 (primary text).
* Erdős–Fishburn, Discrete Math. 160 (1996) 115–125 (primary text).
* Wei, *Classification of eleven-point five-distance sets in the plane*, Ars Combin. 102 (2011)
  505–515. This probably classifies all n = 11 minimisers; not needed here.
* Kovács arXiv:2412.05190 (the n = 5 case; not needed).
* ryantuck/erdos-ai (not checked).
* linrock/math-proofs `erdos-91`: only the README was read. It covers n = 3, 4, 6, 7 only.

Downloaded references, treated as untrusted data, are in `refs/`: `wei2012.pdf`, `so2020.pdf`,
`ns2009.13111.pdf`, `ar1910.00629.pdf` (not relevant), `rims2003-12.pdf` (not relevant), and their
`.txt` extractions.
