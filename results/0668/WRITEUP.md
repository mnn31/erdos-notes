# Erdős 668, small cases n = 13, 15, 16: the maximiser is unique up to congruence

## Statement established

**Theorem.** For n ∈ {13, 15, 16} let u(n) = 30, 37, 41. Up to congruence (all isometries of
the plane, reflections included) there is **exactly one** n-point set in R^2 with u(n) unit
distances. So the number of incongruent maximisers of the unit-distance count is exactly 1 for
n = 13, 15 and 16.

This is conditional on one cited computer-assisted result, **AMP25** (Alexeev–Mixon–Parshall,
arXiv:2412.11914v2, Theorem 1 with Tables 2 and 3). It says u(13) = 30, u(15) = 37 and
u(16) = 41. It also says that for each of these n there is a single densest unit-distance graph up
to isomorphism, with graph6 codes `L@rLaDBIOidEDJ`, `NGECKA@WW{igRHKpDSW` and
`O@iib@`cC_iOAsAi_ioHZ`. Call these graphs G13, G15 and G16. Everything else is proved here, with
exact computer algebra over Q(√−3) and Q(√33) for the finite checks.

The unique sets have these properties (exact):
* minimum separation² = (7 − √33)/6 for all three n;
* diameter² = 13/2 + √33/6 for n = 13 and n = 15, and 11 for n = 16;
* symmetry group of order |Aut G|/4: 1 for n = 13, 2 for n = 15 and 4 for n = 16.

**Extension, by the same method (toy run, same rigour, also conditional on AMP25):** for n = 20
(u = 54, unique graph) there are **exactly 2** incongruent maximisers. For n = 9, 10 and 12 the
unique graph has a one-parameter family of realisations. Section 6 has the details.

## 0. Checks that the target is open (done 2026-11-23)

* erdosproblems.com/668 (fetched with curl): status open, last edited 27 Dec 2025. It says the
  [EHSVZ25] and [AMP25] computations were "checking only up to graph isomorphism, rather than
  congruency". The forum thread has 3 comments. Alexeev (31 Aug 2025) says AMP25 counts only up to
  graph isomorphism, and that he does not remember whether n = 20 is unique up to congruence.
* Plasma `wiki/problems/distance_problems/E0668/_index.md`: status open, updated 2026-10-15. It
  lists n = 5, 7, 9, 10, 12, 13, 15, 16, 20 as "undetermined".
* arXiv API search, newest first. Queries were abs "unit distance" combined with congruent,
  incongruent, rigid, maximizers or "small point sets", plus "unit distance graphs" AND densest.
  No paper counts the maximisers up to congruence. I read the abstracts of 2610.06246,
  2607.06576 and 2601.18831; they address other questions.

## 1. Setup and reduction to labelled realisations

Identify R^2 with C. Let ω = e^{iπ/3}, so ω² = ω − 1 and ω̄ = 1 − ω. Fix n ∈ {13, 15, 16},
let G = G_n = (V, E) with V = {0, …, n−1}, using the vertex labels from decoding the graph6 code
(`code/graphs.py`). A **realisation** is an injective map p : V → C with |p_u − p_v| = 1 for
every uv ∈ E.

**Lemma 0 (reduction).** Let P ⊂ C have |P| = n and exactly u(n) unit distances. Then there is a
realisation p of G with p(V) = P. Conversely, if p is a realisation of G, then p(V) has exactly
u(n) unit distances. In particular, every non-edge has distance ≠ 1.

*Proof.* The unit-distance graph of P has n vertices and u(n) edges, and u(n) is the maximum
(AMP25). So it is a densest unit-distance graph, and by AMP25 Thm 1(c) / Table 2 it is isomorphic
to G. Composing with an isomorphism gives the realisation p. Conversely, p(V) has n points and at
least |E| = u(n) unit distances, so by maximality it has exactly u(n). (This last part is also
checked directly by exact arithmetic for every realisation below; see Lemma 7.) ∎

**Lemma 1 (congruence criterion).** Let p and q be realisations of G. The sets p(V) and q(V) are
congruent if and only if some automorphism φ ∈ Aut(G) satisfies
|q_{φu} − q_{φv}| = |p_u − p_v| for all u, v ∈ V.

*Proof.* (⇒) Let ι be an isometry with ι(p(V)) = q(V). Put φ = q^{-1} ∘ ι ∘ p. This is a
bijection V → V. Since ι preserves distances, uv is a unit pair for p iff φu φv is a unit pair
for q. By Lemma 0 the unit pairs are exactly the edges for both realisations, so φ ∈ Aut(G). Also
|q_{φu} − q_{φv}| = |ι p_u − ι p_v| = |p_u − p_v|.

(⇐) Translate so that p_0 = 0 and q_{φ0} = 0. By polarisation,
⟨x, y⟩ = (|x|² + |y|² − |x−y|²)/2. Hence ⟨p_u, p_v⟩ = ⟨q_{φu}, q_{φv}⟩ for all u, v. G contains a
triangle {a, b, c}, and p_a, p_b, p_c are the vertices of an equilateral triangle, so they are not
collinear. Then x_1 = p_b − p_a and x_2 = p_c − p_a form a basis of R^2, and so do
y_1 = q_{φb} − q_{φa} and y_2 = q_{φc} − q_{φa}. The pairs have equal Gram matrices (all inner
products are expressible through pairwise distances). So the linear map L with L x_i = y_i
preserves inner products, i.e. it is orthogonal. For any u, the vector p_u − p_a is determined by
its inner products with x_1 and x_2, and q_{φu} − q_{φa} has the same inner products with y_1 and
y_2. So q_{φu} − q_{φa} = L(p_u − p_a). Therefore x ↦ q_{φa} + L(x − p_a) is an isometry of R^2
that maps p(V) onto q(V). ∎

So the number of congruence classes of maximisers equals the number of orbits of Aut(G) on the set
of realisations taken modulo isometries of the plane.

## 2. Linear relations forced by injectivity

**Lemma 2 (4-cycles are rhombi).** Let p be a realisation and a–b–c–d–a a 4-cycle of G (a ≠ c,
b ≠ d). Then p_a + p_c = p_b + p_d.

*Proof.* p_b ≠ p_d by injectivity. Put m = (p_b + p_d)/2 and h = (p_d − p_b)/2 ≠ 0. Take
x ∈ {p_a, p_c}. Then |x − p_b| = |x − p_d| = 1, i.e. |(x − m) + h| = |(x − m) − h| = 1. Subtracting
the squares gives ⟨x − m, h⟩ = 0. Adding them gives |x − m|² = 1 − |h|². So x − m lies on the line
through 0 perpendicular to h, at distance r = (1 − |h|²)^{1/2} ≥ 0 from 0. That leaves at most the
two points m ± r·ih/|h|. They coincide if r = 0. But p_a ≠ p_c, so r > 0 and
{p_a − m, p_c − m} = {r·ih/|h|, −r·ih/|h|}. Hence (p_a − m) + (p_c − m) = 0, i.e.
p_a + p_c = 2m = p_b + p_d. ∎

**Lemma 3 (triangles have one of two orientations).** Let p be a realisation and {a < b < c} a
triangle of G. Then exactly one of the following holds:
p_c − p_a = ω (p_b − p_a)  (σ = +1), or p_c − p_a = ω̄ (p_b − p_a)  (σ = −1).

*Proof.* Put z = p_b − p_a and y = p_c − p_a. Then |z| = |y| = |y − z| = 1, and t = y/z satisfies
|t| = 1 and |t − 1| = |y − z|/|z| = 1. From |t|² = 1 and |t − 1|² = 1 we get 2 Re t = 1. So
t = 1/2 ± i√3/2, i.e. t ∈ {ω, ω̄}. These two values differ, so exactly one holds. ∎

Let T be the list of triangles of G, in the order printed in `out/branch_enum.txt`; there are 11, 14
and 16 of them. For σ ∈ {±1}^T let **L_σ** be the homogeneous complex-linear system in
(p_0, …, p_{n−1}). It contains one equation p_a + p_c − p_b − p_d = 0 for each 4-cycle (19, 27
and 33 of them), and the equation of Lemma 3 with sign σ_t for each triangle t. All coefficients
lie in Q(ω).

**Lemma 4 (branching is exhaustive; mirror symmetry).** (i) Every realisation p satisfies
L_{σ(p)}, where σ(p) records the orientations from Lemma 3. (ii) The complex conjugate p̄ is a
realisation with σ(p̄) = −σ(p).

*Proof.* (i) follows from Lemmas 2 and 3. (ii) Conjugation is an isometry (a reflection), so p̄ is
a realisation. Conjugating p_c − p_a = ω^{±1}(p_b − p_a) gives the same relation with ω̄^{±1}, so
each orientation flips. ∎

So, up to reflection, it suffices to find all realisations with σ_1 = +1 (σ_1 refers to the
first triangle in T).

**Lemma 5 (pruning rule).** Let S be any subset of the equations of L_σ, and suppose that the
vector e_u − e_v (u ≠ v) is a Q(ω)-linear combination of the coefficient rows of S. Then no
realisation has orientation vector σ.

*Proof.* Such a realisation would satisfy every equation in S, hence p_u − p_v = 0. This
contradicts injectivity. ∎

## 3. The exact branch enumeration

**Computation A** (`code/branch_enum.py`; exact arithmetic in Q(ω), stored as pairs of Python
`Fraction`s with ω² = ω − 1). Depth-first search over σ ∈ {±1}^T with σ_1 = +1. The search starts
from the rhombus equations, adds one triangle equation per level, and keeps an exact reduced row
echelon form. At each node it tests every pair u < v for whether e_u − e_v lies in the current row
space, and prunes the subtree if so (Lemma 5). Every σ with σ_1 = +1 either reaches a leaf or has
a pruned prefix, so the search is exhaustive. The output, in `out/branch_enum.txt`, lists every
pruned prefix with the pair it forces to coincide:

| n | rhombus-only kernel dim | DFS nodes | pruned | surviving leaves σ (σ_1 = +) | dim_C ker L_σ |
|---|---|---|---|---|---|
| 13 | 5 | 38 | 17 | `+-+---++---`, `+---++--+--` | 3, 3 |
| 15 | 5 | 52 | 24 | `+++--+---++-++`, `+-+++------+++` | 3, 3 |
| 16 | 5 | 60 | 28 | `++---++-++---++-`, `+--+--++--+--+++` | 3, 3 |

(Example: for n = 13 the prefix `++` is pruned. Triangles (0,4,5) and (1,4,5) with equal
orientation force p_0 = p_1, which is the obvious "two apexes on the same side" contradiction.)

The rank of a matrix over Q(ω) equals its rank over C. So for each leaf, ker_C L_σ is the complex
span of the exact Q(ω) basis that the program computes. It has complex dimension 3 and contains
the constant vector (translations).

**Lemma 6 (each leaf reduces to one unknown on the unit circle).** Fix a surviving leaf σ, and
let e1 = (i1, j1) and e2 = (i2, j2) be the two edges named in the table below. Then there are
explicit a_v, b_v ∈ Q(ω), listed in `out/configs.json` and `out/n*_real*.txt`, with the following
property. Every p ∈ ker L_σ satisfies p_v − p_0 = a_v λ + b_v μ for all v, where
λ = p_{j1} − p_{i1} and μ = p_{j2} − p_{i2}. Consequently every edge vector is α_e λ + β_e μ,
with α_e = a_y − a_x and β_e = b_y − b_x for e = xy. If p is a realisation, then |λ| = |μ| = 1,
and Z := λ μ̄ satisfies, for every edge e,

  |α_e|² + |β_e|² + 2 Re(Z α_e β̄_e) = 1,   |Z| = 1.            (★)

Conversely, take any Z with |Z| = 1 satisfying (★). Then p_v := a_v + b_v Z̄ (that is, λ = 1 and
μ = Z̄) lies in ker L_σ and has every edge of unit length. Two realisations in the same leaf with
the same Z differ by a rotation and a translation.

*Proof.* The linear functionals f ↦ f_y − f_x on ker L_σ vanish on the constant vector, so they
live in a space of dimension 3 − 1 = 2. The program checks that the functionals of e1 and e2 are
independent: a 2×2 minor is nonzero in Q(ω). It then solves for (a_v, b_v) and (α_e, β_e) and
checks the remaining coordinate exactly (the `assert` statements in `code/solve_leaves.py`). The
identities are verified on a Q(ω) basis of ker L_σ, so they hold on all of ker_C L_σ by linearity.
For the expansion, |αλ + βμ|² = |α|²|λ|² + |β|²|μ|² + 2 Re(α β̄ λ μ̄), and |λ| = |μ| = 1 because
e1 and e2 are edges. For the converse, p := a + bZ̄ is the kernel element with λ = 1 and μ = Z̄,
and (★) gives unit edges. Finally, if p and p' share σ and Z, write λ' = e^{iφ}λ. Then
μ' = Z̄λ' = e^{iφ}μ, because μ = Z̄λ when |λ| = 1. So p' − p'_0 = e^{iφ}(p − p_0). ∎

Write Z = U + iV and V' = √3·V. Each equation (★) is a rational linear equation in (U, V'),
because Re(Z(x + yω)) = U(x + y/2) − V'·y/2. **Computation B** (`code/solve_leaves.py`) builds
all |E| equations for each leaf. After removing the identically trivial ones, exactly one distinct
equation remains in each leaf:

| n | leaf | e1, e2 | the nontrivial equation | with U² + V'²/3 = 1, the solutions (U, V') |
|---|---|---|---|---|
| 13 | both | (2,3), (0,6) | V' = 1/2 | U = ±√33/6 |
| 15 | `+++--+---++-++` | (1,2), (3,4) | U = 5/6 | V' = ±√33/6 |
| 15 | `+-+++------+++` | (1,2), (3,4) | U = −5/6 | V' = ±√33/6 |
| 16 | both | (2,3), (0,4) | U = −(V' + 1)/3 | 2V'² + V' − 4 = 0, V' = (−1 ± √33)/4 |

These solutions can be checked by hand. For n = 13: U² = 1 − 1/12 = 11/12. For n = 15:
V'² = 3(1 − 25/36) = 11/12. For n = 16: (V' + 1)²/9 + V'²/3 = 1 ⇔ 4V'² + 2V' − 8 = 0. In each
case a line meets the circle U² + V'²/3 = 1 in exactly two points.

So each leaf contributes exactly two candidate Z, and each n has exactly 4 candidate realisations
with σ_1 = +1, up to rotation and translation.

**Lemma 7 (all four candidates are genuine maximisers).** For each n and each of the 4
candidates, the following hold:
* every edge has squared length exactly 1;
* every pair u ≠ v has squared distance > 0 (injectivity);
* every non-edge has squared distance ≠ 1.

*Proof (Computation C, `code/verify.py`).* The squared distances are
|a λ + b μ|² = |a|² + |b|² + 2(U·Re(a b̄) − V'·y/2), where a b̄ = x + yω. They lie in Q(√33) and are
computed as pairs of rational numbers. There is no floating point and no symbolic simplification.
Positivity of r + s√33 is decided exactly, by comparing r² with 33 s² when the signs differ.
|Z|² = U² + V'²/3 = 1 is also rechecked exactly. All checks pass; see `out/verify.txt`. ∎

By Lemma 4(ii), the realisations with σ_1 = −1 are exactly the mirror images of these 4. So, up
to isometries of the plane, G has exactly 4 labelled realisations.

## 4. Quotient by automorphisms

**Computation D** (`code/verify.py`, continued). The program enumerates Aut(G) with networkx
(VF2): |Aut G| = 4, 8 and 16. For every ordered pair (k, l) of the 4 candidates, and every
φ ∈ Aut(G), it tests exact equality d_k(φu, φv) = d_l(u, v) of all squared distances in Q(√33).

Result: for each n, every pair (k, l) is related by some φ. The stabilisers have orders 1, 2 and 4
for n = 13, 15 and 16. The orbit–stabiliser theorem gives 4·1 = 4, 4·2 = 8 and 4·4 = 16, matching
|Aut G| as it must. By Lemma 1 the four point sets are pairwise congruent.

**Conclusion (proof of the Theorem).** By Lemma 0, the maximisers are exactly the point sets
p(V) of realisations of G. By Lemmas 2–6 and Computations A and B, the realisations up to isometry
are among the 4 candidates. By Lemma 7 all 4 are genuine. By Lemma 1 and Computation D they form a
single congruence class. So the count is exactly 1 for n = 13, 15 and 16. ∎

The coordinates of each realisation, to 40 digits, are in `out/n{13,15,16}_real{0..3}.txt`
(columns: vertex, x, y). Each file also gives the exact form p_v = a_v + b_v μ with
μ = U − iV'/√3.

## 5. Independent numerical cross-check (not part of the proof)

`code/numcheck.py` runs random-start least squares on the edge equations, with 3000 starts per n.
The overdetermined system rarely converges.
* n = 13 and n = 15: 2 converged runs each, both injective, both with the signature found above
  (minimum separation 0.457427…, diameter 2.730829…). See `out/numcheck.txt`.
* n = 16: 0 of 3000 converged, so this check gives no information for n = 16
  (`out/numcheck16.txt`).

This is a weak sanity check only. The proof does not use it. The floating-point branch exploration
`code/explore.py` is a stronger independent check of Computation A.

## 6. Toy and extension runs (same pipeline; `out/toy.txt`, `out/solve_leaves_toy.txt`, `out/verify_toy_n20.txt`)

* n = 5 and n = 7: one leaf each, with kernel dimension 2. A dimension-2 kernel fixes the
  configuration up to similarity, which gives one realisation up to isometry. This agrees with the
  known uniqueness. (The single-class claim for n = 5, 7 was not separately written up here.)
* n = 9, 10, 12: two leaves each, kernel dimension 3, and **every** equation (★) is trivial. So for
  every Z on the unit circle the edges have unit length, giving a one-parameter family. This
  matches the scout's flexibility finding. Injectivity for generic Z was not re-proved here.
* n = 20 (u = 54, unique graph per AMP25): two leaves, kernel dimension 3, one equation each
  (6U + 5 = 0 and 3U − 3V' + 5 = 0). That gives 4 candidates, all passing the exact Lemma 7
  checks. |Aut G20| = 2, and the automorphism test relates only the pairs {0, 3} and {1, 2}. So
  **there are exactly 2 incongruent 20-point sets with 54 unit distances**. Their exact minimum
  separations² are (7 − √33)/6 and 2 − √33/3. The proof is the same as for n = 13, 15, 16; all
  steps are covered by the same code, run with argument `toy`. This settles the scout's T2
  (≥ 2 shown there) and answers Alexeev's forum question for n = 20: not unique.

## 7. What this does and does not show

**Shows (rigorous, given AMP25):**
* the number of incongruent maximisers is exactly 1 for n = 13, 15, 16;
* the same count is exactly 2 for n = 20.

The finite computations use only exact rational arithmetic in Q(ω) and Q(√33). They are:
* row reduction;
* membership in the row space;
* kernel bases;
* the linear equations in (U, V');
* squared distances, with exact sign tests;
* automorphism tests.

The two-point solutions of "line ∩ circle" are solved by sympy, and are also checked by hand
above and re-verified by exact substitution in `verify.py`.

**Does not show:**
* anything about u(n) or the uniqueness of the graph. Those are taken from AMP25, which is
  itself a large computer search; I did not re-verify it. If AMP25 Table 2 missed a densest graph
  for some n, the count for that n could be larger.
* anything about Problem 668's main question (whether the count → ∞) or about n ≥ 22.
* anything about n = 9, 10, 12 beyond what is stated in Section 6 (flexibility is consistent with
  the scout, but injectivity along the family was not re-proved here).
* a formal (Lean) verification.

**Trust in the code:** the soundness of Lemmas 2–5 does not depend on finding *all* 4-cycles. Using
fewer valid relations only enlarges the kernels, so any missed relation could only add spurious
candidates, never lose real ones. Spurious candidates would then be filtered by the exact checks of
Lemma 7. The only properties relied on are:
(a) the DFS covers all 2^{|T|−1} sign vectors, either by reaching them or by a pruned prefix;
(b) the exact Q(ω) arithmetic and row reduction are correct;
(c) the networkx automorphism enumeration is complete. Only the existence of the relating φ is
used, and that is verified exactly. If the enumeration were incomplete, it could only make the
count look larger, never smaller.

Item (b) is cross-checked: the floating-point SVD exploration (`code/explore.py`, all 2^{|T|−1}
branches without pruning) gives the same surviving branches with the same kernel dimensions.

## 8. Reproduce

```
cd attack/668/t1/prove/code
python3 -I analyze.py                                  # graph data, |Aut|
python3 -I branch_enum.py ../out/leaves.json > ../out/branch_enum.txt   # Computation A
python3 -I solve_leaves.py      > ../out/solve_leaves.txt               # Computation B (writes ../out/configs.json)
python3 -I verify.py            > ../out/verify.txt                     # Computations C, D
python3 -I explore.py           > ../out/explore.txt                    # float cross-check of all 2^(T-1) branches
python3 -I numcheck.py 3000 13 15 > ../out/numcheck.txt; python3 -I numcheck.py 3000 16 > ../out/numcheck16.txt   # numerical sanity check (slow, ~10 min each)
python3 -I toy.py               > ../out/toy.txt                        # n = 5,7,9,10,12,20 branch tree
python3 -I solve_leaves.py toy  > ../out/solve_leaves_toy.txt           # (writes ../out/configs_toy.json)
python3 -I verify.py toy        > ../out/verify_toy_n20.txt             # n = 20: exactly 2 classes
```
Tested with Python 3.11, sympy 1.14, networkx 3.6.1, mpmath and numpy/scipy. Runtimes are under
a minute each, except numcheck.

## Sources not read

* The OEIS entry A385657 itself (only cited via the page).
* Schade's original determination of u(n) for n ≤ 14, and any source for u(15) other than
  AMP25 Table 2.
* EHSVZ25 beyond what the scout recorded (no congruence discussion).
* The full text of 2610.06246, 2607.06576 and 2601.18831 (abstracts only).
* ryantuck/erdos-ai: only its 668 files were looked at (`deepmind/ai-review/668.md` and
  `deepmind/reviews/668.md`, which review the Lean formalisation). There are no congruence counts
  there. `conjectures/668.lean` was not read.
