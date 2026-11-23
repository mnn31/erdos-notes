# Erdős 668, n = 20: exactly two incongruent 20-point sets with 54 unit distances

Folder: `attack/668/t2-retry/prove/`.
The brief pointed to `../SCOUT.md`, but no `t2-retry/SCOUT.md` exists. I used
`attack/668/SCOUT.md`.

## Statement established

**Theorem (conditional on AMP25, Lemma 1).** Up to congruence (every isometry of R²,
reflections included, as in `erdos_668` of formal-conjectures, which uses `ℝ² ≃ᵢ ℝ²`), there are
**exactly two** 20-point sets in R² that determine u(20) = 54 unit distances.

Write ω = e^{iπ/3}, R4 = {0, 1, ω, ω̄} (two unit triangles on the common edge 01) and
T5 = {−1, 0, 1, ω, ω²} (a strip of three unit triangles). The two sets are

  P₋ = R4 + ρ₋·T5  and  P₊ = R4 + ρ₊·T5,  where ρ_ε = ω̄·(−5 + ε i√11)/6 and |ρ_ε| = 1.

| class | closed form | diameter² | min separation² | coordinates (40 digits) |
|---|---|---|---|---|
| 0 | P₋ | 11 | (7 − √33)/6 ≈ 0.20924 | `out/n20_class0.txt` |
| 1 | P₊ | 12 + √33/3 ≈ 13.91485 | 2 − √33/3 ≈ 0.08515 | `out/n20_class1.txt` |

The diameters and minimum separations are exact values in Q(√33). Exact comparisons
(`code/prove20.py`) show they are the true maximum and minimum of the 190 squared distances.

**The hypothesis.** The theorem uses only one outside input: AMP25 (Alexeev–Mixon–Parshall,
arXiv:2412.11914v2). That paper gives u(20) = 54 and says the 54-edge unit-distance graph on 20
vertices is unique up to isomorphism (Lemma 1). The target statement makes the same assumption
(it calls 54 "u(20)"). Everything after Lemma 1 is proved here. The finite case analysis uses
exact rational arithmetic, and each of its steps carries a certificate that is checked by
direct multiplication.

## 0. Status check (done 2026-11-23, before the main work)

* erdosproblems.com/668 (curl, `refs/page668.html`): status open, last edited 27 Dec 2025. The
  page says the EHSVZ25 and AMP25 counts were "checking only up to graph isomorphism, rather
  than congruency".
* Forum thread (`refs/forum668.html`): 3 comments, none later than 31 Aug 2025, and posting is
  suspended. Alexeev writes that n = 20 has a unique graph, "but I do not remember offhand whether
  it is also unique in the point set congruence sense". Nobody has answered.
* Plasma `wiki/problems/distance_problems/E0668/_index.md` (`refs/plasma_E0668_index.md`; latest
  commit on the path is 2026-10-19). Lines 59–64 say that for n = 5, 7, 9, 10, 12, 13, 15, 16, 20
  "the count of incongruent maximizers is undetermined". The only claim page concerns n = 4.
* arXiv API: abs:"unit distance" AND (congruent / congruence / incongruent / maximizers), newest
  first (`refs/arxiv1.xml`, `refs/arxiv2.xml`). There were 4 hits, and none of them counts
  maximisers up to congruence (2608.13592, 2606.27352, 2512.15516, 2112.10245; titles only).
* Earlier runs in this workspace reached the same count with other code: `../../t2/prove`,
  `../../t2/disprove`, and §6 of `../../t1/prove`. None of that is published. My code is written
  from scratch and imports nothing from those runs. I used their coordinate files only for the
  cross-check in §5.

So, as far as these sources show, the public record does not settle the n = 20 count. INFERRED,
not VERIFIED: no paper outside the arXiv/forum/Plasma coverage settles it.

## 1. Notation

Points of R² are complex numbers. ω = e^{iπ/3} = (1 + √−3)/2, so ω² = ω − 1, ω̄ = 1 − ω = ω^{−1}
and N(a + bω) = a² + ab + b². G = (V, E) is the graph with graph6 code
`S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T[`, decoded by my own decoder (`decode_g6` in
`code/prove20.py`). That code appears in AMP25 Table 3 and in the ancillary file `graph6.txt`,
line 51. G has V = {0, …, 19}, |E| = 54, 22 triangles and 48 four-cycles, and degree sequence
4³ 5⁸ 6⁷ 7².

A **realisation** of G is an injective p : V → C with |p_x − p_y| = 1 for every edge xy.

## 2. Lemmas

**Lemma 1 (cited input; VERIFIED by reading AMP25 v2 via pdftotext).**
(a) AMP25 defines a unit-distance graph as a simple graph with an *injection* f : V → R² such that
{u, v} ∈ E implies ‖f(u) − f(v)‖ = 1. They write U(n) for the set of these graphs and
u(n) = max |E(G)| over U(n) (Introduction, first paragraph).
(b) Theorem 1(a) gives u(20) = 54.
(c) Theorem 1(c) says that for n ≤ 21 the densest graphs in U(n) are enumerated in Table 2. In
Table 1, the n = 20 row is "20 54 4.8·10^29 7 1 1", and its last column ("embeddable (thus
counting all unit-distance graphs)") is 1. Table 3 gives that one graph's graph6 code, shown in §1.

This lemma is not re-proved here. It rests on AMP25's computer search, which in turn uses the
Globus–Parshall list of 74 minimal forbidden subgraphs and AMP25's own embeddability solver.

**Lemma 2 (reduction).** A set S ⊂ C with |S| = 20 determines exactly 54 unit distances if and
only if S = p(V) for some realisation p of G. In that case the unit pairs of S are exactly the
images of the 54 edges.

*Proof.* First, G is the graph of Lemma 1(c). By Computation D below, G has a realisation and it
has 54 edges, so G ∈ U(20) with u(20) edges. Lemma 1(c) says there is only one such graph up to
isomorphism, so G is that graph. This step does not depend on my having copied the graph6 code
correctly: any decoded graph with a realisation and 54 edges on 20 vertices is the extremal graph.

(⇒) Let H be the unit-distance graph of S: vertex set S, with an edge for each pair at distance 1.
The inclusion S → C is an injection under which every edge has unit length, so H ∈ U(20) with
|E(H)| = 54 = u(20). By Lemma 1(c), H ≅ G. Composing an isomorphism G → H with the inclusion gives
a realisation p with p(V) = S.

(⇐) p is injective, so |p(V)| = 20. The 54 edges give 54 distinct pairs at distance 1, and by
Lemma 1(b) there are no more.

(Computation D also checks directly, for every realisation, that no non-edge has length 1, so the
"no more" part does not even need u(20) = 54.) ∎

**Lemma 3 (triangles).** Let {a < b < c} be a triangle of G and p a realisation. Then
p_c − p_a = ω^{s}(p_b − p_a) for exactly one s ∈ {+1, −1}.

*Proof.* Put z = p_b − p_a, which is not 0, and t = (p_c − p_a)/z. Then |t| = |p_c − p_a| = 1 and
|t − 1| = |p_c − p_b|/|z| = 1. Hence 1 = |t − 1|² = |t|² − 2 Re t + 1 = 2 − 2 Re t, so Re t = 1/2.
With |t| = 1 this gives Im t = ±√3/2, that is, t ∈ {ω, ω̄} = {ω^{+1}, ω^{−1}}. These two values
differ, so s is unique. ∎

**Lemma 4 (4-cycles are rhombi).** Let x, b, y, d be four distinct vertices with xb, by, yd and dx
all in E, and let p be a realisation. Then p_x + p_y = p_b + p_d.

*Proof.* Let m = (p_b + p_d)/2 and h = (p_d − p_b)/2. Injectivity gives h ≠ 0. For
q ∈ {p_x, p_y}, put r = q − m. Then |r + h|² = |q − p_d|² = 1 and |r − h|² = |q − p_b|² = 1.
Subtracting gives 4 Re(r h̄) = 0. Adding gives 2|r|² + 2|h|² = 2, so |r|² = 1 − |h|². So r lies on
the line iℝh, at distance (1 − |h|²)^{1/2} from 0. There are at most two such points, and they
are negatives of each other. p_x ≠ p_y (injectivity), so p_x − m and p_y − m are those two points,
and their sum is 0. Hence p_x + p_y = 2m = p_b + p_d. ∎

In the code, each pair {x, y} with two common neighbours b, d gives one row
p_x + p_y − p_b − p_d = 0. Each 4-cycle is found once from each diagonal, giving 96 rows. The
common neighbours of x and y are never x or y, so the four vertices are distinct, as Lemma 4
requires.

**Definition.** Order the triangles T₁ < … < T₂₂ lexicographically. For a sign word
σ = (σ₁, …, σ_k), with k ≤ 22, let M_σ be the matrix whose rows are the 96 rhombus rows and the
rows p_c − p_a − ω^{σ_j}(p_b − p_a) for T_j = {a < b < c}, j ≤ k. All of its entries lie in Q(ω).

**Lemma 5 (pruning).** Suppose that for some u ≠ v there is a vector c over Q(ω) with
Σ_i c_i·row_i(M_σ) = e_u − e_v. Then no realisation has an orientation vector (Lemma 3) beginning
with σ.

*Proof.* Suppose p is such a realisation. By Lemmas 3 and 4, M_σ p = 0. Then
p_u − p_v = Σ c_i (row_i · p) = 0, which contradicts injectivity. ∎

**Lemma 6 (coverage).** Let 𝒲 be a finite set of sign words of length ≤ 22. Suppose 𝒲 is
prefix-free and Σ_{w∈𝒲} 2^{−|w|} = 1. Then every σ ∈ {±1}^{22} has exactly one prefix in 𝒲.

*Proof.* For w ∈ 𝒲, let C_w be the set of length-22 words that extend w, so |C_w| = 2^{22−|w|}.
Suppose two sets C_w and C_{w'} share an element. Then w and w' are both prefixes of it, so one
of them is a prefix of the other. That contradicts prefix-freeness unless w = w'. So the sets C_w
are pairwise disjoint. Their total size is 2^{22}·Σ 2^{−|w|} = 2^{22} = |{±1}^{22}|, so they
cover every word, each one exactly once. ∎

**Lemma 7 (a leaf has kernel of dimension 3).** Let σ be a full-length sign word (a leaf) with no
pruning certificate. Let F = {f₀, f₁, f₂} be the three non-pivot columns of the reduced row-echelon
form of M_σ, and let K ∈ Q(ω)^{20×3} be the matrix the program reads off from that form (K is the
identity on the rows F). Suppose two things are checked:
(i) M_σ·K = 0, by direct multiplication;
(ii) each of the 17 reduced rows equals an explicit combination Σ c_i row_i(M_σ), again by direct
multiplication, and each reduced row has a 1 in its pivot column and 0 in the other pivot columns.
Then ker_C M_σ is exactly the set {K t : t ∈ C³}, and t = (p_{f₀}, p_{f₁}, p_{f₂}).

*Proof.* By (ii), the 17 reduced rows lie in the row space. They are linearly independent: in the
17 pivot columns they form an identity block. So rank M_σ ≥ 17. Rank does not change when the
field is extended from Q(ω) to C, so dim_C ker ≤ 3. By (i), the three columns of K lie in the
kernel. They are independent, because restricted to the rows F they form an identity block. So
they span the kernel.

For p in the kernel, the vector p − K(p_{f₀}, p_{f₁}, p_{f₂}) is in the kernel and is 0 on F. The
map from the kernel to C³ that reads off the F-coordinates is a linear bijection, because it sends
the basis to the standard basis. So that vector is 0. ∎

**Lemma 8 (reduction to one unit complex number z).** Keep the setting of Lemma 7. Assume also
that the constant vector lies in the kernel, which the program checks as K·(1,1,1)ᵀ = 1. For an
edge e = (a, b), let ℓ_e ∈ Q(ω)³ be the functional t ↦ (Kt)_b − (Kt)_a. Fix two edges e₁, e₂
whose functionals are linearly independent. Suppose the program has found α_e, β_e, γ_x, δ_x in
Q(ω), checked by direct substitution, such that
ℓ_e = α_e ℓ_{e₁} + β_e ℓ_{e₂} for every edge e, and
(row x of K) − (row f₀ of K) = γ_x ℓ_{e₁} + δ_x ℓ_{e₂} for every vertex x.
Let p be a realisation with M_σ p = 0. Then there are an isometry g (a rotation followed by a
translation) and a z ∈ C with |z| = 1 such that

 (g∘p)_x = γ_x + δ_x z for all x, and |α_e + β_e z| = 1 for every edge e. (★)

Write z = X + iY and W = √3·Y. Then (★) is equivalent to the conditions

 X² + W²/3 = 1, and (2c₁ + c₂) X − c₂ W = 1 − N(α_e) − N(β_e) for every edge e, (★★)

where c₁ + c₂ω = ᾱ_e β_e.

*Proof.* By Lemma 7, p = Kt. Put x₁ = ℓ_{e₁}(t) = p_{b₁} − p_{a₁} and y₁ = ℓ_{e₂}(t). Both have
modulus 1, since e₁ and e₂ are edges. Set g(q) = x̄₁ (q − p_{f₀}), which is a rotation (|x₁| = 1)
composed with a translation, and put z = x̄₁ y₁, so |z| = 1. Then
(g∘p)_x = x̄₁ (γ_x x₁ + δ_x y₁) = γ_x + δ_x z.
The edge e has vector α_e x₁ + β_e y₁ = x₁(α_e + β_e z), and its length is 1. This proves (★).

For (★★), use |z| = 1:
|α + βz|² = |α|² + |β|²|z|² + 2 Re(ᾱβz) = N(α) + N(β) + 2 Re(ᾱβz).
Write ᾱβ = c₁ + c₂ω = (c₁ + c₂/2) + i(√3/2)c₂. Then
2 Re(ᾱβz) = (2c₁ + c₂)X − √3 c₂ Y = (2c₁ + c₂)X − c₂W.
Also |z|² = X² + W²/3. Every step is reversible. ∎

**Lemma 9 (line meets ellipse).** Fix rationals A, B, C with (A, B) ≠ (0, 0). The set
{(X, W) ∈ R² : AX + BW = C, X² + W²/3 = 1} has at most 2 points.

*Proof.* If B ≠ 0, substitute W = (C − AX)/B. This gives (3B² + A²)X² − 2ACX + (C² − 3B²) = 0,
whose leading coefficient is positive, so it has at most 2 roots X. Each root X determines W.
If B = 0, then X = C/A is fixed and W² = 3(1 − X²), so there are at most 2 values of W. ∎

**Lemma 10 (distance-preserving bijections extend).** Let P, Q ⊂ C be finite and f : P → Q a
bijection with |f(x) − f(y)| = |x − y| for all x, y ∈ P. Suppose P contains three non-collinear
points. Then f is the restriction of an isometry of R², so Q = g(P) for that isometry g.

*Proof.* Pick non-collinear a, b, c ∈ P. Put u₁ = b − a, u₂ = c − a, v₁ = f(b) − f(a) and
v₂ = f(c) − f(a). By polarisation, ⟨s, t⟩ = (|s|² + |t|² − |s − t|²)/2. So for all q, q' ∈ P,
⟨q − a, q' − a⟩ = ⟨f(q) − f(a), f(q') − f(a)⟩.
In particular u₁, u₂ and v₁, v₂ have the same Gram matrix. It is nonsingular because u₁ and u₂
are independent, so v₁ and v₂ are independent too. Let L be the linear map with L uᵢ = vᵢ. L
preserves the Gram matrix of a basis, so L is orthogonal.

Take q ∈ P. The vectors f(q) − f(a) and L(q − a) have the same inner products with v₁ and v₂
(namely ⟨q − a, uᵢ⟩), and v₁, v₂ form a basis. So the two vectors are equal, and f is the
restriction of x ↦ f(a) + L(x − a). ∎

**Lemma 11 (an invariant).** If Q = g(P) for an isometry g, then P and Q have the same multiset
of squared pairwise distances. *Proof.* g is a bijection P → Q that preserves distances. ∎

## 3. Computations (exact; `code/prove20.py`, `code/fields.py`; output `out/n20.txt`, `out/n20.json`)

The arithmetic types are Q(ω) as pairs of `Fraction`s, Q(√−3), and F = Q(√−3, √D) with D
squarefree, written as P + Q√D with P, Q ∈ Q(√−3). Real numbers x₀ + x₁√D are compared exactly:
when x₀ and x₁ have opposite signs, the program compares x₀² with D x₁². No sympy or floating
point is used anywhere in the proof path.

**A (structure).** 20 vertices, 54 edges, 22 triangles, 96 rhombus rows (48 four-cycles). The
rhombus rows alone have rank 15.

**B (branching, Lemmas 3–6).** A depth-first search adds the triangle rows in order, trying both
signs at every triangle with no mirror reduction. After each step it tests every pair u < v for
e_u − e_v ∈ row space. Results:
* 167 nodes, **80 pruned words and 4 leaves**;
* the 84 words are prefix-free and have Kraft sum exactly 1 (Lemma 6);
* for each of the 80 pruned words, `solve_combination` (a separate Gauss–Jordan routine on the
  transposed system) finds c, and `check_combination` confirms Σ c_i row_i = e_u − e_v by direct
  multiplication: 80/80 (Lemma 5).

By Lemmas 3–6, every realisation p satisfies M_σ p = 0 for one of the four leaves:
* σ¹ = `+++----+--++-++--+---+`
* σ² = `+----+-+++-++++-----+-`
* σ³ = `-++++-+---+----+++++-+` = −σ²
* σ⁴ = `---++++-++--+--++-+++-` = −σ¹

**C (leaves, Lemmas 7–9).** In every leaf, rank M_σ = 17. Checks (i) and (ii) of Lemma 7 pass,
the constants lie in the kernel, and the identities of Lemma 8 pass, with e₁ = (3, 4) and
e₂ = (0, 7). After deleting zero rows and proportional duplicates, the 54 equations (★★) reduce
to a single line in each leaf. Zero rows occur only for edges whose functional is a sixth root
of unity times ℓ_{e₁} or ℓ_{e₂}, and every one of them satisfies 0 = 0. The lines are:

| leaf | line (★★) | z = X + iW/√3 |
|---|---|---|
| σ¹ | X = −5/6 | (−5 ± i√11)/6 |
| σ² | X + W = −5/3 | X = (−5 ± √33)/12, W = −5/3 − X |
| σ³ | X − W = −5/3 | X = (−5 ± √33)/12, W = X + 5/3 |
| σ⁴ | X = −5/6 | (−5 ± i√11)/6 |

By Lemma 9 each leaf has at most 2 solutions z, and the program writes down both. So every
realisation is isometric to one of 8 candidates q = γ + δz. These candidates are not assumed to
be realisations. That is checked next.

**D (candidates).** For each of the 8 candidates the program computes all 190 squared distances
exactly in Q(√33). For all 8:
* every edge has squared length exactly 1 (for e₂ this is |z| = 1);
* every pair has squared distance > 0, so the candidate is injective;
* no non-edge has squared distance 1, so the number of unit pairs is exactly 54.

So all 8 are realisations, and Lemma 9's bound is attained in every leaf. Their exact diameter²
and min-separation² values are listed in `out/n20.txt`.

**E (congruence, Lemmas 10–11).** For each candidate, the program backtracks over *all*
bijections V → V that preserve the exact squared-distance matrix, using no automorphism group.
Results:
* candidates {0, 3, 4, 7} map to candidate 0, and {1, 2, 5, 6} map to candidate 1 (bijections
  printed in `out/n20.txt`);
* the exact squared-distance multisets of candidates 0 and 1 differ. For instance, the diameter²
  is 11 versus 12 + √33/3, and these differ because √33 is irrational.

## 4. Proof of the Theorem

Let S be a 20-point set with 54 unit distances. By Lemma 2, S = p(V) for a realisation p. By
Lemmas 3–6 and Computation B, M_σ p = 0 for some leaf σ. By Lemmas 7–9 and Computation C, an
isometry carries p to one of the 8 candidates. By Computation E and Lemma 10, each candidate's
point set is congruent to that of candidate 0 or candidate 1. (Every candidate contains an
equilateral triangle, hence three non-collinear points.) So S is congruent to P⁽⁰⁾ or P⁽¹⁾, the
point sets of candidates 0 and 1. Both have 54 unit distances (Computation D), so both are
maximisers. They are not congruent (Lemma 11 and Computation E). Hence there are exactly two
congruence classes. ∎

**Closed form (exact, `code/explicit.py`, `out/explicit.txt`).** The sets R4 + ρ_ε T5 consist of
20 distinct points with exactly 54 unit pairs. R4 + ρ₋T5 has a distance-preserving bijection to
candidate 0, and R4 + ρ₊T5 has one to candidate 1. In each case the other pairing has no such
bijection.

Geometrically, this is the Minkowski sum of R4 (5 edges, 4 points) and T5 (7 edges, 5 points),
which gives 4·7 + 5·5 = 53 unit pairs. On top of that there is one extra edge joining
ω̄ + ρ·1 and ω + ρ·ω². Its length is 1 exactly when the angle between the two √3-diagonals,
ω − ω̄ and ρ(1 − ω²), is the Moser angle arccos(5/6). The two classes correspond to the two
signs of that angle. INFERRED from these checks; I only verified the closed form, not this
description of it.

**Remark (orientation-preserving congruence; exact, `code/chirality.py`, `out/chirality.txt`).**
Candidates 0 and 1 each have exactly one distance-preserving self-bijection, the identity.

Suppose P̄ = g(P) for an orientation-preserving isometry g. Then conj∘g maps P onto P and
reverses orientation. Its restriction to P is a distance-preserving self-bijection, so it is the
identity on P. An isometry that fixes three non-collinear points is the identity, so conj∘g would
be the identity, which preserves orientation. That is a contradiction.

So each class is chiral. If congruence is restricted to orientation-preserving isometries
(rotations and translations), the count is 4: P₋, its mirror image, P₊ and its mirror image. The
target statement, the problem page and the Lean statement all use full congruence, and under
full congruence the count is 2.

## 5. Toy cases and cross-checks (same program; validation, not part of the proof)

| n | graph6 | DFS nodes / pruned / leaves | leaf kernel | result |
|---|---|---|---|---|
| 4 | `C^` | 7 / 2 / 2 | dim 2 | 1 class (rhombus, diam² 3) |
| 5 | `DR{` | 11 / 4 / 2 | dim 2 | 1 class (diam² 4) |
| 7 | `FoSvw` | 23 / 10 / 2 | dim 2 | 1 class (hexagon + centre) |
| 9, 10, 12 | | 39/16/4, 47/20/4, 71/32/4 | dim 3, no equation on z | flexible (continuum of solutions; injectivity not checked) |
| 13, 15, 16 | | 75/34/4, 103/48/4, 119/56/4 | dim 3 | 8 realisations, 1 class each |
| 20 | as above | 167 / 80 / 4 | dim 3 | 8 realisations, **2 classes** |

* n = 4 matches the known uniqueness (two triangles on a common edge). For n = 13, 15 and 16 the
  node counts, the class counts and the invariants (min sep² (7 − √33)/6, and diam² 11 for
  n = 16) agree with the independent referee recomputation in `../../t1/prove/REFEREE-logic.md`.
  For n = 9 and 12, the flexibility agrees with the scout's Cartesian-product description.
* `code/crosscheck.py` (mpmath, 40 digits; `out/crosscheck.txt`):
  * the maximum edge error is 6e−40, there are 54 unit pairs at tolerance 1e−30, and the closest
    non-edge has |d − 1| = 0.19099921;
  * sorted distance lists agree to within 1e−29 with the scout's two sets
    (`scout_code/n20_class{0,1}.txt`, which are my classes 0 and 1) and to within 1e−39 with
    `t2/prove/out/n20_class{1,0}.txt`.

## 6. Reproduce

```
cd attack/668/t2-retry/prove/code
python3 -I prove20.py 'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T[' ../out/n20        # main proof, ~30 s
python3 -I explicit.py 'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T[' | tee ../out/explicit.txt
python3 -I chirality.py 'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T[' | tee ../out/chirality.txt
A=attack/668
python3 -I crosscheck.py ../out/n20.json ../out $A/scout_code/n20_class0.txt $A/scout_code/n20_class1.txt \
    $A/t2/prove/out/n20_class0.txt $A/t2/prove/out/n20_class1.txt | tee ../out/crosscheck.txt
for c in 'C^' 'DR{' 'FoSvw' 'H{dQXgj' 'IISpZATaw' 'KwC[KLQIibDJ' 'L@rLaDBIOidEDJ' \
         'NGECKA@WW{igRHKpDSW' 'O@iib@`cC_iOAsAi_ioHZ'; do
  n=$(python3 -I -c "import sys;print(ord(sys.argv[1][0])-63)" "$c"); python3 -I prove20.py "$c" ../out/toy_$n; done
```
I used Python 3.11.7. The proof path uses only the standard library (`fractions`). mpmath 1.3.0
is used only for printing 40-digit coordinates and for the cross-check.

`out/n20.json` contains: the edge list, the triangles, the 80 pruned words with their coincident
pairs, the leaves, and all 8 candidates. Each candidate is stored with exact coordinates, as
(a, b, c, d) meaning a + b√−3 + (c + d√−3)√33, and with 40-digit numerics.

## What this does and does not show

**Does show (rigorous, given Lemma 1 = AMP25):** at n = 20, the number of incongruent planar
point sets that maximise the number of unit distances is exactly 2, given explicitly as
R4 + ρ_± T5. Each class is rigid: an isolated realisation, not a continuum. This answers, for
n = 20, the question Alexeev left open on the forum. "Congruent" here means related by any
isometry, reflections included, which is the notion used by the Lean statement and the problem
page. If only orientation-preserving isometries are allowed, the count is 4, because both classes
are chiral (Remark in §4).

**Does not show:**
* Anything about the actual Problem 668 (does the count tend to infinity?). This is one data point.
* Lemma 1 is cited, not re-proved. If AMP25's computer enumeration had missed a second 54-edge
  unit-distance graph on 20 vertices, there could be more classes. The lower bound "≥ 2 classes,
  each with 54 unit distances" needs only u(20) ≤ 54. Even that is not needed for "these two sets
  have 54 unit distances and are incongruent".
* The programs are trusted: about 600 lines of Python using `Fraction`. Mitigations:
  * every pruning step and every rank bound carries a certificate, re-checked by plain
    multiplication;
  * coverage is checked by the Kraft sum;
  * all 8 candidates are verified directly;
  * the results agree with three earlier independent implementations and with the toy cases.
  There is no Lean formalisation.
* The n = 9, 10, 12 rows say only that the edge-length equations leave z free. Injectivity and the
  absence of extra unit distances along those families were not checked here.

## Sources not read

* The proofs of AMP25 Theorem 1(a) and (c), and AMP25's code. I read only the definitions,
  Theorem 1, Table 1, the Table 3 entry and Appendix A text, via pdftotext of
  `../../refs/amp25_2412.11914v2.pdf`.
* Globus–Parshall (minimal forbidden subgraphs), on which AMP25 rests.
* EHSVZ25 (arXiv:2406.15317), Schade's thesis, Ágoston–Pálvölgyi, and OEIS A385657.
* The full texts of the four arXiv hits in §0 (titles only); MathSciNet / zbMATH (not searched).
* ryantuck/erdos-ai (not re-checked in this run; the t1 run reports it has only a Lean review
  for 668).
