# Erdős Problem 959: exact values of `extremalGap n` for n = 5, 6, 7

## Statement established

With the definitions of `Erdos959` in formal-conjectures (`origin/main:FormalConjectures/ErdosProblems/959.lean`):

> **Theorem.** `extremalGap 5 = 5`, `extremalGap 6 = 8`, `extremalGap 7 = 9`.

The scout's guess for n = 6 (lower bound 7, with the question reduced to rigid 9-edge configurations) was not sharp. The value 8 comes from a
**flexible** 9-edge configuration: a unit equilateral triangle together with its translate by a generic unit vector (the "translation prism").

Along the way the proof re-derives (VERIFIED here, not quoted) the unit-distance maxima u(4)=5, u(5)=7, u(6)=9, u(7)=12. It also gives a complete
description of the 5-point sets with 7 unit distances, the 6-point sets with 9, and the 7-point sets with 12. Every 7-point set with 11 unit distances
repeats some non-unit distance.

Outcome: **PROVED**. The proof uses three kinds of computer checks: (i) rational/exact arithmetic in Q(ω) and Q(√3), done by our own code, (ii) an
exhaustive graph enumeration that agrees with the networkx graph atlas, (iii) two resultant eliminations done in sympy over Q(√−3). (iii) relies on
sympy being correct. See "What this does and does not show".

## Status check (done before the work)

* erdosproblems.com/959 (curl, 2026-11-23): OPEN. The page asks for the asymptotic order. It cites only CDL25 (≫ n log n). It records 0 comments and 2 proof
  claims, and no small values. Forum thread: 0 comments. (`refs/page.html`, `refs/forum.html`)
* Plasma `wiki/problems/distance_problems/E0959` (index plus 3 claim pages, `refs/plasma_*.md`): only asymptotic lower bounds (CDL25 n log n,
  Snyder n^{1+c/loglog n}, Xeff n^{1+c}). No small values.
* CDL25 (arXiv 2505.04283, `refs/cdl25.pdf`): grep of the text for small-n tables found only results on a different statistic (a(X) multiplicity
  vectors, Conjecture 1.1 about n=5,6). There is no table of max f(d1)−f(d2).
* Lean file: `erdos_959` (asymptotic, open) and `erdos_959.lower_bound` (solved). No small values.
* OEIS (`refs/oeis_*.txt`): `seq:1,4,5,8,9` gives 48 hits. None of them concerns distances in the plane. `1,4,5,8,9 distance` gives one unrelated hit.
  So the sequence (values for n = 3..7 are 1, 4, 5, 8, 9) is not in OEIS.
* VERIFIED in `FormalConjecturesForMathlib/Geometry/2d.lean:31`: `ℝ²` is `EuclideanSpace ℝ (Fin 2)`, so `dist` is the Euclidean distance.

## Conventions

* A *configuration* is a finite set P ⊂ ℝ² (an injective `Fin n → ℝ²`). Identify ℝ² with ℂ. Set ω = e^{iπ/3}, so ω² = ω − 1, ω̄ = 1 − ω, and
  ω^k (k = 0..5) are the six unit vectors at 60° spacing.
* For a configuration P, f(d) is the number of unordered pairs at distance d. *Unit graph* G(P): vertices P, edges = pairs at distance 1.
  deg(v) means degree in G(P). L(n,m) is the set of n-point configurations with exactly m unit distances.
* f₂(P) := the largest f(d) over d ≠ 1 (0 if there is none).
* Λ = Z[ω] is the triangular lattice. Points x + yω (x, y ∈ Q) have |x + yω|² = x² + xy + y².
* Similarity (scaling) and isometries (including reflections) preserve every multiplicity. So "WLOG" placements below are harmless.

## Lemmas

**Lemma 0 (reduction to unit distances).** Let n ≥ 3 and let P be admissible (injective, ≥ 2 distinct distances). Let m be the largest multiplicity. Then
`multiplicityGap P` equals m − f(d') if exactly one distance d* has multiplicity m, where f(d') is the largest multiplicity among the other distances.
It equals 0 if two distances tie at m. After scaling so that d* = 1, the gap is m − f₂(P) with m = number of unit distances, and f₂(P) ≥ 1.
Also `extremalGap n` = max{ multiplicityGap P : P admissible }.

*Proof.* `multiplicityGap P = sup_d (f(d) − runnerUp(d))` with truncated subtraction, and runnerUp(d) = max of f over the other represented
distances. Suppose d* is the unique maximiser. The term at d* is f(d*) − max_{d≠d*} f(d). Every other term is f(d) − runnerUp(d) with runnerUp(d) ≥ f(d*) ≥ f(d), so it truncates to 0.
If two distances tie at the maximum, each term is ≤ 0 → 0. Admissible means at least two distances, so the runner-up of d* is ≥ 1. Scaling by 1/d*
preserves all multiplicities and admissibility. The gap of any P is ≤ m ≤ C(n,2). So `Nat.findGreatest (AttainableGap n) (C(n,2))` is the largest
attainable gap, which is the maximum, and attainable gaps exist for n ≥ 3. ∎

**Lemma 1 (two circles).** Two distinct points s, t have at most two common unit neighbours. There are two if 0 < |s−t| < 2, one if |s−t| = 2, and none
if |s−t| > 2. The two points are v = (s+t)/2 ± i (t−s) √(1/D − 1/4) with D = |s−t|². Consequently G(P) contains no K_{2,3}. G(P) contains no K₄
either: three mutually unit points form an equilateral triangle abc, and a 4th point unit from a and b is c or the reflection c* of c in ab, with
|c* − c| = √3 ≠ 1. Every triangle in G(P) is a unit equilateral triangle. If two unit triangles share an edge and have distinct apexes, the apexes are
mirror images, at distance √3.

*Proof.* The unit circles about s ≠ t are distinct, so they meet in ≤ 2 points. These are symmetric about the line st, at height √(1 − D/4) above the
midpoint. The rest is immediate. ∎

**Lemma 2 (deletion).** If P ∈ L(n,m) and v ∈ P has deg(v) = k, then P∖{v} ∈ L(n−1, m−k), since the unit graph of a subset is the induced subgraph.
The minimum degree δ satisfies δ ≤ 2m/n. If u(n−1) is the maximum number of unit distances on n−1 points, then δ ≥ m − u(n−1).

**Lemma 3.** u(4) = 5, and L(4,5) consists of the *rhombus* R (two unit triangles sharing an edge; long diagonal √3), unique up to congruence.

*Proof.* Four points with 6 unit distances would be a K₄, contradicting Lemma 1. Five unit distances on 4 points give K₄ minus an edge: two triangles
sharing an edge with distinct apexes. By Lemma 1 the apexes are mirror images. ∎

**Lemma 4 (computation C1, `code/exact_checks.py`).** u(5) = 7, and L(5,7) = {T}, the *trapezoid* T = {0, 1, 2, ω, 1+ω}. T has squared distance
multiplicities {1: 7, 3: 2, 4: 1}.

*Proof.* Take R = {0, 1, ω, 1+ω} (WLOG by Lemma 3). If P has 5 points and m ≥ 8, Lemma 2 gives 3 ≤ m − 5 ≤ δ ≤ 2m/5, so m = 8 and δ = 3. Then
P∖{v} = R and v ∉ R has 3 unit neighbours in R. If m = 7, then 2 ≤ δ ≤ 14/5, so δ = 2, P∖{v} = R, and v has exactly 2 unit neighbours in R. In
both cases v is a common unit neighbour of a pair of R. All pairwise squared distances in R are 1 or 3. For D ∈ {1, 3}, √(1/D − 1/4)·i(t−s) equals
(2ω−1)(t−s)·h with h = 1/2 or 1/6 respectively (because 2ω − 1 = i√3). So every candidate v lies in Q(ω) and is computed exactly by the program
(D = 4 gives h = 0; D > 4 gives nothing). The program finds 4 candidates, and each has exactly 2 unit neighbours in R. So the case m = 8 is impossible.
Each of the 4 resulting sets is carried onto T by a lattice symmetry, so all are congruent to T. ∎

**Lemma 5 (3-regular graphs).** A 3-regular graph on 6 vertices with no K_{2,3} is the triangular prism (two disjoint triangles abc, a′b′c′ plus the
matching aa′, bb′, cc′).

*Proof.* Its complement is 2-regular on 6 vertices, so it is C₆ or 2C₃. The complement of 2C₃ is K_{3,3}, which contains K_{2,3}. The complement of C₆
(vertices 1..6 in cyclic order) is the prism with triangles {1,3,5}, {2,4,6} and matching 1–4, 3–6, 5–2. (Cross-checked: `code/graph_facts.py`.) ∎

**Lemma 6 (unit realisations of the prism).** Let P = {a, b, c, a′, b′, c′} be injective with all 9 prism edges of unit length. Then, up to
congruence, a = 0, b = 1, c = ω and (a′, b′, c′) = (a+u, b+u, c+u) for some unit vector u. Conversely every such set with injective points realises the 9
edges. The non-unit pairs are the 6 *cross pairs* {x, y+u} (x ≠ y in {a, b, c}), at distances |h + u| where h runs over the six vectors ω^k.

*Proof.* Use a congruence, and a reflection if needed, to place a = 0, b = 1, c = ω. Write a′ = u, b′ = 1 + v, c′ = ω + w with |u| = |v| = |w| = 1.
Since |b′ − a′| = 1, s := 1 + v − u is a unit vector and 1 + v = u + s.
*Claim:* if α + β = γ + δ ≠ 0 with all four unit vectors, then γ ∈ {α, β}. Indeed γ and the sum σ satisfy |σ − γ| = |δ| = 1. So γ is a common unit
neighbour of 0 and σ, and by Lemma 1 the only such points are α and β (both qualify).
If 1 + v = 0 then b′ = 0 = a, a collision. Otherwise the claim (with α = 1, β = v, γ = u) gives u ∈ {1, v}:
 – u = 1 gives a′ = 1 = b, a collision;
 – so u = v (and s = 1), i.e. b′ − a′ = 1. The point c′ is the apex of a unit triangle on a′b′, so c′ = u + ρ with ρ ∈ {ω, ω̄}.
   If ρ = ω, then w = u (translation). If ρ = ω̄, then w = u + ω̄ − ω = u − i√3, and |w| = |u| = 1 forces u ∈ {ω, ω²}. Then a′ = ω = c, or b′ = 1 + ω² = ω = c.
   Both are collisions.
For the converse and the cross pairs: |x′ − x| = |u| = 1 and the triangle a′b′c′ is a translate. Also |(y+u) − x| = |(y − x) + u|, and y − x runs over
{±1, ±ω, ±ω²} = {ω^k}. ∎

**Lemma 7 (computation C2).** u(6) = 9, and L(6,9) = Λ-type ∪ Prism-type:
* Λ-type: exactly three sets up to congruence, all inside Λ (listed in `out/exact_checks.txt`). Each is T plus one point.
* Prism-type: the sets T_u = {0, 1, ω, u, 1+u, ω+u} of Lemma 6 with |h + u| ≠ 1 for all six h = ω^k.

*Proof.* Suppose m ≥ 10 on 6 points. Lemma 2 gives m − 7 ≤ δ ≤ m/3, so m = 10 and δ = 3. Then P∖{v} = T (Lemma 4) and v ∉ T has 3 unit neighbours
in T. The pairwise squared distances in T are in {1, 3, 4}, so as in Lemma 4 all common unit neighbours of pairs of T are computed exactly. The program
finds 5 such points outside T, each with exactly 2 unit neighbours in T. So m = 10 is impossible.
Now m = 9. Lemma 2 gives 2 ≤ δ ≤ 3. If δ = 2, then P = T ∪ {v} with v one of those 5 points, which gives the three Λ-type sets. If δ = 3, then G(P) is
3-regular, has no K_{2,3} (Lemma 1), and so is the prism (Lemma 5). Lemma 6 applies, and "exactly 9" forces |h + u| ≠ 1 for every cross pair. ∎

**Lemma 8.** u(7) = 12, and L(7,12) = {W}, the regular hexagon with its centre. W has squared-distance multiplicities {1: 12, 3: 6, 4: 3}, so its gap
is 6.

*Proof.* If m ≥ 13 on 7 points, then m − 9 ≤ δ ≤ 2m/7, so m ≤ 12.6, a contradiction. For m = 12: 3 ≤ δ ≤ 24/7, so δ = 3. Pick v with deg(v) = 3.
Then H = P∖{v} ∈ L(6,9).
*H cannot be prism-type.* Then G(P) would consist of the prism graph plus v joined to 3 prism vertices. Up to symmetry the triples of prism vertices are:
 (i) {a,b,c}, which gives K₄ with v;
 (ii) {a,b,a′}. Here b and a′ have the common prism neighbours a and b′, and with v they have three, a K_{2,3};
 (iii) {a,b,c′}. Here a and c′ have the common neighbours c and a′, and with v they have three, a K_{2,3}.
The cases with two vertices in a′b′c′ are symmetric. All of these contradict Lemma 1.
*So H is Λ-type.* Then v is a common unit neighbour of a pair of H. All squared distances within H are integers of the form x² + xy + y², and those
≤ 4 are 1, 3, 4. So v is computed exactly (computation C3). The program finds that the only such v with 3 unit neighbours, over all three Λ-type H,
gives the set W (up to congruence), and that W has exactly 12 unit distances. ∎

**Lemma 9 (graph enumeration, `code/enum_graphs.py`, `code/graph_facts.py`).** Up to isomorphism, there are exactly 3 graphs on 7 vertices with 11 edges,
no K₄, no K_{2,3}, and minimum degree ≥ 3:
* A = {03,04,05,06,12,15,16,24,26,34,35}
* B = {04,05,06,12,13,15,16,24,26,34,35}
* C = {02,04,05,06,12,13,16,26,34,35,45} (C is the Moser spindle)

*Proof (computer).* `enum_graphs.py` builds all K₄-free, K_{2,3}-free graphs edge by edge. It takes canonical forms as the minimum edge bitmask over all
7! vertex permutations, which is exact with no hashing. Its counts per edge number, [1,1,2,5,10,21,39,58,73,73,47,18,4,0], agree with a filter of the
networkx atlas of all 1044 graphs on 7 vertices. The atlas filter returns exactly 3 graphs with 11 edges and δ ≥ 3, isomorphic to A, B, C
(`out/graph_facts.txt`). ∎

**Lemma 10 (graphs A and B have no injective unit realisation; computation in `code/graphA.py`, `code/graphB.py`).**
There is no injective P whose unit graph contains A, and likewise for B.

*Proof for A.* The edges 03, 04, 05, 34, 35 form a rhombus with triangles 034 and 035. WLOG (Lemma 3, congruence) p0 = 0, p3 = 1, p4 = ω, p5 = ω̄.
Triangle 126 is a unit triangle, so p6 = x, p1 = x + y, p2 = x + σy with |x| = |y| = 1 and σ ∈ {ω, ω̄}. The remaining edges give
|p1 − p5|² = 1 and |p2 − p4|² = 1. On |x| = |y| = 1 we have x̄ = 1/x and ȳ = 1/y. Clearing the monomial denominators gives polynomials P1, P2 in
Q(√−3)[x, y], and every real solution is a common zero with x, y ≠ 0.
The resultant Res_y(P1, P2) lies in the ideal (P1, P2). So the x of any common zero is one of its roots. For σ = ω its roots are {0, ω, ω̄, −1};
for σ = ω̄ they are {0, ω, ω̄} (exact factorisation over Q(√−3)). For each root with |x| = 1, all y with P1 = P2 = 0 are the roots of gcd(P1(x₀,·), P2(x₀,·)).
The program checks that the root list is complete and that the two polynomials are not both identically zero. Every one of the 10 resulting
configurations has two coinciding points (`out/graphA.txt`).
*Proof for B.* Triangles 126 and 135 share vertex 1. WLOG p1 = 0, p2 = 1, p6 = ω, p3 = y, p5 = σy (σ ∈ {ω, ω̄}), p4 = 1 + z, p0 = 1 + z + t, all of
y, z, t unit. The remaining edges are 34, 05, 06, which give E1(y,z), E2(y,z,t), E3(y,z,t). The resultants R1 = Res_t(E2, E3) and
R2 = Res_z(R1, E1) lie in the ideal. R2(y) factors exactly with roots {0, ω², ω⁴, 1} for both σ.
y = 0 is not unit. y = 1 gives p3 = 1 = p2, a collision. For each remaining y₀ the program takes all z₀ with E1 = 0 and |z₀| = 1, and then all t:
 – either the roots of gcd(E2, E3), each of which gives a collision;
 – or, in one case (σ = ω̄), E2 and E3 vanish identically in t. Then p4 = p5 = p6, a collision.
(`out/graphB.txt`) ∎

**Lemma 11.** Every P ∈ L(7,11) has f₂(P) ≥ 2.

*Proof.* Lemma 2 gives 2 ≤ δ ≤ 22/7, so δ ∈ {2, 3}.

*δ = 3.* The degrees are 3,3,3,3,3,3,4 and G(P) is K₄- and K_{2,3}-free (Lemma 1), so G(P) ≅ A, B, or C (Lemma 9). A and B are impossible
(Lemma 10). In C, triangles 026 and 126 share edge 26 with distinct apexes 0 and 1, so |p0 − p1| = √3 (Lemma 1). Likewise triangles 045 and 345 give
|p0 − p3| = √3. The pairs {0,1} and {0,3} are non-edges of C, so f(√3) ≥ 2.

*δ = 2.* Take deg(v) = 2. Then H = P∖{v} ∈ L(6,9) and v has exactly 2 unit neighbours in H.
 – *H is Λ-type.* v is computed exactly as in Lemma 8 (computation C4). The program finds 3 sets up to congruence, with f₂ = 4, 5, 5.
 – *H = T_u is prism-type.* Let s, t be the two unit neighbours of v.
   • If |s − t| ≠ 1, then {s, t} is a cross pair {x, y+u}. Both y and x+u are unit neighbours of x and of y+u, and they are distinct (else u = y − x and
     x + u = y, a collision). By Lemma 1, v ∈ {y, x+u} ⊂ H, a contradiction.
   • If {s, t} is a triangle edge, say {x, y} ⊂ {a, b, c} with third vertex z, then v = x + y − z (the apex other than z). Then
     |v − (x+u)| = |y − z − u| = |(z+u) − y|. So the pairs {v, x+u} and {y, z+u} (distinct, since v ∉ H) have equal length. That length is a cross
     distance of T_u, hence ≠ 1 (Lemma 7). For an edge of the translated triangle, v = x + y − z + u, and |v − y| = |x − z + u| = |(x+u) − z| works
     the same way.
   • If {s, t} = {x, x+u}, then v = x + ρu with ρ ∈ {ω, ω̄}, and ρ − 1 = ρ². For y ≠ x in {a,b,c}:
     |v − (y+u)| = |(x − y) + ρ²u| = |ρ̄²(x − y) + u| = |h + u| with h := ρ̄²(x−y) ∈ {ω^k}. Choose p ≠ q in {a, b, c} with q − p = h (every ω^k is such a
     difference). Then |(q+u) − p| = |h + u| too. The pairs {v, y+u} and {p, q+u} are distinct and the common length is a cross distance (≠ 1).
   In every case some non-unit distance occurs twice. ∎

**Lemma 12 (constructions, computation C5, exact arithmetic in Q(√3)).** Let A = (0,0), B = (1,0), C = (1/2, √3/2), u = (3/5, 4/5),
r = (5/13, −12/13).
* n = 5: T = {A, B, (2,0), C, C+B} has multiplicities 7, 2, 1, so its gap is 5.
* n = 6: T_u = {A, B, C, A+u, B+u, C+u} has 9 unit distances and 6 other, pairwise distinct, distances (squared: 16/5, 4/5, 13/5 ± 4√3/5,
  7/5 ± 4√3/5). Its gap is 8.
* n = 7: T_u ∪ {A + r} has exactly 10 unit distances and 11 other, pairwise distinct, distances. Its gap is 9.

All points are distinct and all squared distances lie in Q(√3). They are compared exactly as pairs of rationals (`out/exact_checks.txt`, "ALL EXACT
CHECKS PASSED"). ∎

## Proof of the Theorem

By Lemma 0, `extremalGap n` = max over admissible P of m − f₂(P), where m is the top multiplicity scaled to the unit (gap 0 if the top is tied).
Here f₂ ≥ 1, so every gap is ≤ m − 1.

* **n = 5.** m ≤ 7 (Lemma 4). If m = 7, then P = T and f₂ = 2, so the gap is 5. If m ≤ 6, the gap is ≤ 5. So extremalGap(5) ≤ 5, and T attains 5
  (Lemma 12).
* **n = 6.** m ≤ 9 (Lemma 7), so the gap is ≤ 8. T_u attains 8 (Lemma 12).
* **n = 7.** m ≤ 12. If m = 12, then P = W and the gap is 6 (Lemma 8). If m = 11, then f₂ ≥ 2 (Lemma 11) and the gap is ≤ 9. If m ≤ 10, the gap is ≤ 9.
  T_u ∪ {A+r} attains 9 (Lemma 12). ∎

(Also: extremalGap(3) = 1 because u(3) = 3 and an isosceles non-equilateral triangle attains 1; extremalGap(4) = 4 from Lemma 3 and the rhombus
{1:5, 3:1}. These agree with the scout's hand values but were not re-checked by code beyond Lemma 3.)

## Reproduce

From `attack/959/t1/prove`:
```
python3 -I code/exact_checks.py   > out/exact_checks.txt   # C1–C5 (Lemmas 4,7,8,11-lattice,12); <1 s
python3 -I code/graph_facts.py    > out/graph_facts.txt    # Lemma 5 cross-check, Lemma 9; few s (imports enum_graphs.py)
python3 -I code/graphA.py         > out/graphA.txt         # Lemma 10, graph A; ~1 min
python3 -I code/graphB.py         > out/graphB.txt         # Lemma 10, graph B; a few min
python3 -I code/enum_graphs.py    > out/enum_graphs.txt    # graph lists for n<=7
```
Python 3.11, sympy 1.14.0, networkx 3.6.1, numpy 1.26.4. Exploration only (not used in the proof): `code/explore.py 7 10 1 120`
(`out/explore_n7.txt`; random least-squares realisations of all K₄/K_{2,3}-free graphs, best numerical gap 9) and `code/try_prism_plus.py`.

## What this does and does not show

* It shows the three exact values above, for the Lean definitions as written (Euclidean distance; gap 0 on ties; the maximum is over injective
  configurations with ≥ 2 distances).
* It says nothing about the asymptotic order in `erdos_959`. These are small-case (OEIS-type) data.
* Trust base:
  - Lemmas 0–3, 5, 6, the prism parts of Lemmas 7, 8 and 11, and the Moser-spindle case are proved by hand above.
  - Lemmas 4, 7, 8, the lattice case of Lemma 11, and Lemma 12 use our own exact rational arithmetic in Q(ω) / Q(√3) (`fractions.Fraction`). Every
    candidate point is asserted to be at unit distance from its two generators.
  - Lemma 9 rests on two independent enumerations that agree (own canonical-form code and the networkx atlas).
  - Lemma 10 rests on sympy's resultant, factorisation over Q(√−3), `roots` (completeness asserted by multiplicity count) and `simplify` for the
    collision tests. A sympy bug there is the main residual risk.
* Not formalised in Lean. No claim is made about extremalGap(n) for n ≥ 8.
* A numerical search (Exploration) agrees independently. For n = 7 it found the best gap 9 with no 11-unit configuration having f₂ = 1. For n = 6
  the prism gives gap 8.

## Sources not read

* The Snyder and Xeff write-ups and Lean archives (only Plasma's summaries were read). They concern asymptotics.
* Erdős [Er84d] original text.
* The literature on small unit-distance maxima (Schade; Ágoston–Pálvölgyi; Alexeev–Mixon–Parshall), which is not quoted: u(5..7) were re-derived here.
  OEIS A186705 (title only seen in search output) lists 1,3,5,7,9,12 for u(2..7), consistent with Lemmas 3–8.
* OEIS beyond the first 50 hits of `seq:1,4,5,8,9`.
