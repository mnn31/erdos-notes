# Erdős #1082, first question, for sets that are convex except for two points

Date: 2026-11-23. Folder: `erdos-work/attack/1082/t1/prove/`.
(The brief pointed to `t1/SCOUT.md`; that file does not exist. The scout notes I read are at
`erdos-work/attack/1082/SCOUT.md`.)

## 1. Statement established

**Theorem.** Let A be a set of n points in R^2 with no three collinear. Suppose some n-2 points of A are in
convex position, meaning they are the vertices of a convex polygon. Then A determines at least ⌊n/2⌋
distinct distances. This covers the case where n-1 points of A are in convex position, since any n-2 of them
are then also in convex position.

The proof relies on these published results, and on nothing else:
* Altman (1963) and Fishburn (1995). Their statements are quoted from the abstract of Fishburn's paper,
  which I read in this session (§3). They are used for every n.
* For n = 6 and n = 8 only, there is also an exact computer check (Lemma 6). It is complete because
  Fishburn's abstract gives the number of extremal quadrilaterals and hexagons. A second route for these
  two values is the published values g(2) = 5 and g(3) = 7 (§8). I read these only in secondary sources.

The bound is sharp, because the regular n-gon has exactly ⌊n/2⌋ distances.

## 2. Is the target already decided? (checked 2026-11-23)

* **erdosproblems.com/1082** (fetched with curl, last edited 11 Apr 2026): the first question is open. The
  page mentions Altman only for convex polyhedra in R^3. It says nothing about planar sets that are almost
  convex.
* **Forum thread** (22 comments, posting suspended): it was read in full. The only comments on the first
  question are sallerk's (31 Aug 2026). They cover n <= 15 through the values g(k), the convex case through
  Altman, and concyclic and lattice searches. Nothing treats sets with n-1 or n-2 points in convex position.
* **Plasma `wiki/problems/distance_problems/E1082`**: I read `_index.md`, the Altman claim and the sallerk
  claim. The status is open. The only partial claims are convex position (Altman) and n <= 15 (sallerk).
* **arXiv**: an abstract search for "distinct distances" and convex returned arXiv:2611.25148
  (Ágoston–Bhowmick, 18 Nov 2026, "A refinement of Szemerédi's distinct-distance bound for points in
  general position"). I read the full text. It proves d(P) >= ⌊n/3⌋+1 using Altman's theorem and the
  diameter graph. It does not treat our class. Its remark 3 cites a stronger result, Bhowmick,
  HAL hal-05864246, (1/3 + 1/4400)n. I read only that paper's HAL abstract, because the PDF download was
  blocked. The abstract does not mention almost-convex sets.

Conclusion: I found no prior treatment of this statement. The new content is the case n >= 16, because
sallerk's note already covers n <= 15.

## 3. Cited results (VERIFIED by reading the source text)

The abstract of P. Fishburn, "Convex polygons with few intervertex distances", Comput. Geom. 5 (1995),
doi 10.1016/0925-7721(94)00020-V, was retrieved through the Semantic Scholar API in this session. It says:

> "Thirty years ago E. Altman proved that every convex n-gon (n≥3) has at least ⌊n/2⌋ different distances
> between vertices and that a convex n-gon for odd n has exactly (n−1)/2 intervertex distances if and only if
> it is regular. We prove that a convex n-gon for even n≥8 has exactly n/2 intervertex distances if and only
> if it is a regular n-gon or a regular (n+1)-gon with a vertex removed. Three hexagons have exactly three
> intervertex distances, and four quadrilaterals have exactly two intervertex distances. [...]"

Labels used below:
* **(Alt)**: every convex m-gon (m >= 3) has at least ⌊m/2⌋ distances.
* **(Alt=)**: for odd m, exactly (m-1)/2 distances holds iff the polygon is regular.
* **(Fi=)**: for even m >= 8, exactly m/2 distances holds iff the polygon is a regular m-gon or a regular
  (m+1)-gon with one vertex removed.
* **(Fi4,6)**: exactly four quadrilaterals have 2 distances, and exactly three hexagons have 3 distances.
  I take these counts to be up to similarity, which is the only meaningful reading.

## 4. Notation

D(X) is the set of distances between distinct points of X. All statements are invariant under similarity.
For N >= 3, let w_j = e^{2πij/N} for j in Z_N, viewed as points of C = R^2, and let P_N = {w_j}. Then
|w_j - w_l| = 2|sin(π(j-l)/N)|. Hence

  D_N := D(P_N) = { 2 sin(πk/N) : 1 <= k <= ⌊N/2⌋ },  |D_N| = ⌊N/2⌋.

The count is exact because πk/N ranges over (0, π/2] there, where sin is strictly increasing. Write
e_k := 4 sin^2(πk/N) = 2 - 2cos(2πk/N). This is strictly increasing in k for 1 <= k <= ⌊N/2⌋.

For a point p and a finite set Q, call p an **extension of Q** if p ∉ Q and |p - v| ∈ D(Q) for every v ∈ Q.

For p in C, |p - w_j|^2 = |p|^2 + 1 - 2 Re(p · conj(w_j)). So for p = r e^{iθ},

  (★) |p - w_j|^2 = 1 + r^2 - 2r cos(2πj/N - θ).

## 5. Lemmas

**Lemma 0.** No 4 points of the plane are pairwise at the same distance.
*Proof.* Suppose four points are pairwise at distance d. Three of them form an equilateral triangle T of
side d. The fourth point is equidistant from the three non-collinear vertices of T, so it is the
circumcentre of T: the perpendicular bisectors of two sides meet in exactly one point. The circumcentre is
at distance d/√3 ≠ d from the vertices. Contradiction. ∎

**Lemma 1 (reduction).** Let n >= 5, let A be n points with no three collinear, and let Q ⊆ A with
|Q| = m = n-2 be in convex position. Suppose |D(A)| < ⌊n/2⌋. Then:
(a) |D(Q)| = ⌊m/2⌋ and D(Q) = D(A);
(b) every point of A \ Q is an extension of Q;
(c) up to similarity, Q is one of the following: a regular m-gon if m is odd; P_m or P_{m+1} \ {w_0} if m is
even and m >= 8; one of the four quadrilaterals of (Fi4,6) if m = 4; one of the three hexagons of (Fi4,6) if
m = 6.
*Proof.* Since no three points of A are collinear, Q is the vertex set of a convex m-gon with m >= 3. By
(Alt), ⌊m/2⌋ <= |D(Q)|. Also D(Q) ⊆ D(A), so |D(Q)| <= |D(A)| <= ⌊n/2⌋ - 1 = ⌊m/2⌋. Hence equality holds
throughout. A subset of a finite set with the same cardinality is the whole set, so D(Q) = D(A). This
proves (a). For (b), take p ∈ A \ Q and v ∈ Q. Then |p - v| ∈ D(A) = D(Q). Part (c) is (Alt=), (Fi=) and
(Fi4,6) applied to Q, which has exactly ⌊m/2⌋ distances by (a). ∎

**Lemma 2 (how many distances a point sees to a regular polygon).** Let N >= 3 and p = r e^{iθ} with r > 0.
* If 2θ ∉ (2π/N)Z (mod 2π), the N numbers |p - w_j| are pairwise distinct.
* Otherwise, fix s ∈ Z_N with 2θ ≡ 2πs/N (mod 2π). Then |p - w_j| = |p - w_l| iff j + l ≡ s (mod N). The
  number of distinct values is (N + f)/2, where f = #{j ∈ Z_N : 2j ≡ s}. Here f = 1 if N is odd, f = 2 if
  N is even and s is even, and f = 0 if N is even and s is odd.

*Proof.* By (★) and r > 0, |p - w_j| = |p - w_l| iff cos(x_j) = cos(x_l), where x_j = 2πj/N - θ. This
holds iff x_j ≡ x_l or x_j ≡ -x_l (mod 2π). For j ≠ l in Z_N, the first is impossible. The second says
2π(j+l)/N ≡ 2θ (mod 2π).

If 2θ is not a multiple of 2π/N, no pair j ≠ l satisfies it. Otherwise it holds iff j + l ≡ s (mod N).
Equal values then correspond exactly to orbits of the involution ι(j) = s - j on Z_N. The orbits have size
1 (fixed points) or 2, so there are (N + f)/2 of them.

Fixed points solve 2j ≡ s (mod N). If N is odd, 2 is invertible, so f = 1. If N is even, there is a
solution only when s is even. In that case j ≡ s/2 (mod N/2), which gives 2 residues mod N. ∎

**Lemma 3 (a line meets a circle at most twice).** Let β ∈ R with sin β ≠ 0, and let λ, μ ∈ R. The
equation cos(t + β) = λ cos t + μ has at most two solutions t ∈ [0, 2π).
*Proof.* Expand cos(t+β) = cos t cos β - sin t sin β. The equation becomes
(cos β - λ) cos t - (sin β) sin t = μ, that is, a · u(t) = μ with a = (cos β - λ, -sin β) ≠ 0 (since
sin β ≠ 0) and u(t) = (cos t, sin t). The solutions u(t) lie on the intersection of the line {a·u = μ} with
the unit circle, which has at most 2 points. The map t ↦ u(t) is injective on [0, 2π). ∎

**Lemma 4 (extensions of a regular polygon).** Let N >= 3 and let p be an extension of P_N.
(i) If N is odd, this is impossible: P_N has no extension.
(ii) If N is even and N >= 6, then p = 0, the centre.

*Proof.* (i) Suppose first p = 0. Then every distance equals 1. But 2 sin(πk/N) = 1 with 1 <= k <= ⌊N/2⌋
forces πk/N = π/6, so N = 6k, which is impossible for odd N. So p ≠ 0. By Lemma 2, p sees at least
(N+1)/2 distinct distances to P_N. Since |D_N| = (N-1)/2 < (N+1)/2, they cannot all lie in D_N.
Contradiction.

(ii) Suppose p ≠ 0. Here |D_N| = N/2. Lemma 2 gives N, N/2+1 or N/2 distinct distances. Only N/2 is
<= |D_N|, so s exists and is odd, and p sees exactly N/2 distinct distances. These form a subset of D_N of
the same size, so the set of distances equals D_N.

Since 2θ ≡ 2πs/N, we have θ ≡ πs/N (mod π). So p = x e^{iπs/N} with x real and x ≠ 0. By (★),
|p - w_j|^2 = 1 + x^2 - 2x cos(π(2j - s)/N). As j runs over Z_N, the integer 2j - s runs over N distinct
odd residues mod 2N, which are all of them. So the set of squared distances is {g_i : 0 <= i <= N/2 - 1}
with g_i = 1 + x^2 - 2x c_i and c_i = cos((2i+1)α), where α = π/N. The residues 2i+1 and 2N-2i-1 give the
same cosine. The angles (2i+1)α lie in (0, π) and increase with i, so c_i is strictly decreasing in i.
Recall that e_k = 2 - 2cos(2kα) for k = 1..N/2 is strictly increasing. The sets {g_i} and {e_k} are
equal, with N/2 elements each.

* If x > 0, g_i is strictly increasing, so the unique order-preserving bijection gives g_i = e_{i+1}.
  That is, 1 + x^2 - 2x cos t_i = 2 - 2cos(t_i + α), with t_i = (2i+1)α. Rearranged:
  cos(t_i + α) = x cos t_i + (1 - x^2)/2 for i = 0, ..., N/2 - 1.
* If x < 0, g_i is strictly decreasing, so g_i = e_{N/2 - i} = 2 - 2cos(π - 2iα) = 2 + 2cos(t_i - α).
  Rearranged: cos(t_i - α) = -x cos t_i + (x^2 - 1)/2 for i = 0, ..., N/2 - 1.

In both cases N/2 >= 3 distinct t_i ∈ (0, π) solve an equation of the form in Lemma 3 with β = ±α, and
sin(±α) ≠ 0 because 0 < α < π. Lemma 3 allows at most two solutions. Contradiction. So p = 0. ∎

**Lemma 5 (extensions of a regular polygon with one vertex removed).** Let M >= 7 be odd and
Q = P_M \ {w_0}. Then D(Q) = D_M, and the only extension of Q is w_0.
*Proof.* For 1 <= k <= (M-1)/2, the vertices w_1 and w_{1+k} lie in Q, because 1+k <= (M+1)/2 < M. So
D(Q) contains every element of D_M. Also D(Q) ⊆ D_M, so D(Q) = D_M, which has (M-1)/2 elements. The point
w_0 is an extension: its distances to Q are chords of P_M.

Let p be an extension.
* p ≠ 0, because 1 ∉ D_M for odd M (see Lemma 4(i)).
* Write p = r e^{iθ} with r > 0. If 2θ ∉ (2π/M)Z, the M-1 distances |p - w_j|, j ≠ 0, are pairwise
  distinct by Lemma 2, and M - 1 > (M-1)/2. This is impossible.
* Otherwise s exists, and ι has a unique fixed point φ, since M is odd. Distances from p to Q are equal
  exactly within the sets O \ {0}, where O runs over the (M+1)/2 orbits of ι. Such a set is empty only for
  O = {0}, which is an orbit iff φ = 0 iff s ≡ 0. If s ≢ 0, p sees (M+1)/2 > |D_M| distinct distances,
  which is impossible. Hence s ≡ 0, so 2θ ≡ 0 and p = x is real, with x ≠ 0.
* By (★), |p - w_j|^2 = h_j := 1 + x^2 - 2x c_j with c_j = cos(2πj/M). Here j and M - j give the same
  value, and j runs over 1..(M-1)/2, where c_j is strictly decreasing because 2πj/M ∈ (0, π). There are
  (M-1)/2 = |D_M| distinct values, so {h_j} = {e_k : 1 <= k <= (M-1)/2}.
* If x > 0, h_j is increasing, so h_j = e_j = 2 - 2c_j. This gives (x - 1)(x + 1) = 2(x - 1)c_j for j = 1, 2.
  If x ≠ 1, then c_1 = c_2 = (x+1)/2, which contradicts c_1 > c_2. Hence x = 1 and p = w_0.
* If x < 0, h_j is decreasing, so h_j = e_{(M+1)/2 - j}. Since 2π((M+1)/2 - j)/M = π + β - t_j with
  t_j = 2πj/M and β = π/M, we get e_{(M+1)/2-j} = 2 + 2cos(t_j - β). So
  cos(t_j - β) = -x cos t_j + (x^2 - 1)/2 for the (M-1)/2 >= 3 distinct values t_j ∈ (0, π). This
  contradicts Lemma 3, since sin β ≠ 0. ∎

**Lemma 6 (small cases m = 4, 6; computer-assisted, exact).**
(a) The following four convex quadrilaterals have exactly 2 distances and are pairwise non-similar:
* the square P_4;
* P_5 \ {w_0};
* the rhombus with a 60° angle, (0,0), (1,0), (3/2, √3/2), (1/2, √3/2);
* the kite (0,0), (√3/2, -1/2), (1,0), (√3/2, 1/2), which has distances {1, √(2-√3)}.

By (Fi4,6) they are all the convex quadrilaterals with 2 distances.

(b) The following three convex hexagons have exactly 3 distances and are pairwise non-similar:
* the regular hexagon P_6;
* P_7 \ {w_0};
* the hexagon H3, which has unit sides and interior angles 90°, 150°, 90°, 150°, 90°, 150°. Its distances
  are {1, √2, √(2+√3)} with multiplicities 6, 3, 6.

By (Fi4,6) they are all the convex hexagons with 3 distances.

(c) For each of these 7 polygons Q, the extensions of Q are as follows:
* none, for the square, the rhombus, the kite and H3;
* only the missing vertex w_0, for P_5 \ {w_0} and for P_7 \ {w_0};
* only the centre, for P_6. The centre is collinear with opposite vertices.

In particular, for no Q in the list is there a pair p ≠ q of extensions with Q ∪ {p, q} free of collinear
triples.

*Proof.* (a) and (b): The script verifies exactly, with sympy minimal polynomials, that each polygon has
exactly the stated number of distances and is strictly convex. Non-similarity holds because the ratios of
largest to smallest distance differ: √2, (1+√5)/2, √3 and 1/√(2-√3) for the quadrilaterals; 2,
sin(3π/7)/sin(π/7) and √(2+√3) for the hexagons. By (Fi4,6) there are exactly 4 and exactly 3 similarity
classes, so these lists are complete.

(c): Any extension p satisfies |p - v_0| = r_1 and |p - v_1| = r_2 for some r_1, r_2 ∈ D(Q). So p is one of
the at most 2|D(Q)|^2 intersection points of two circles, and the script enumerates all of them. Each
candidate is rejected only when an interval-arithmetic enclosure (mpmath.iv, 60 digits) of |p - v|^2, for
some vertex v, is disjoint from the enclosures of every element of D(Q)^2. Every candidate that is not
rejected is checked exactly, with sympy minimal polynomials, both as an extension and for collinearity.

For P_6, (c) also follows from Lemma 4(ii). For P_7 \ {w_0}, (c) is Lemma 5: the exact run did not finish
(§7). For P_5 \ {w_0} and P_4 it does not,
since there M = 5 < 7 and N = 4 < 6. ∎

## 6. Proof of the Theorem

* **n <= 3.** ⌊n/2⌋ <= 1, and any two points give a distance.
* **n = 4.** By Lemma 0, the four points determine at least 2 = ⌊4/2⌋ distances.
* **n >= 5.** Suppose, for contradiction, that |D(A)| < ⌊n/2⌋. Let Q be the convex (n-2)-subset and
  m = n - 2 >= 3. The set A \ Q = {p, q} has two distinct points. By Lemma 1, both are extensions of Q, and Q
  is, up to similarity, one of the polygons in Lemma 1(c).
  * **m odd.** Q is P_m, which has no extension by Lemma 4(i). Contradiction.
  * **m even, Q = P_m with m >= 8.** By Lemma 4(ii), p = q = centre. This contradicts p ≠ q. Moreover, the
    centre is the midpoint of w_0 w_{m/2}, which would put three collinear points in A.
  * **m even, Q = P_{m+1} \ {w_0} with m >= 8.** By Lemma 5, applied with M = m + 1 >= 9, p = q = w_0.
    This contradicts p ≠ q.
  * **m = 4 or m = 6.** By Lemma 6(c), no admissible pair {p, q} exists. Contradiction.

Hence |D(A)| >= ⌊n/2⌋. ∎

(Corollary of the proof: for n >= 5, the conclusion holds even under the weaker hypothesis that A ⊇ Q with
Q in convex position, |Q| = n - 2, and only the triples (centre, w_0, w_{m/2}) excluded from being
collinear. I did not pursue this further.)

## 7. Computations (code in `code/`, outputs in `out/`)

All runs use `python3 -I` from the folder `erdos-work/attack/1082/t1/prove`. The libraries are sympy 1.14,
mpmath 1.3, numpy 1.26 and scipy 1.17.

| Script | Command | Output | Role |
|---|---|---|---|
| `code/small_cases.py` | `python3 -I -u code/small_cases.py quads`; `... hexes`; `... h3` | `out/small_cases_quads.txt`, `out/small_cases_hexes.txt`, `out/small_cases_h3.txt` | **Proof** of Lemma 6 (exact plus interval arithmetic) |
| `code/crosscheck_small.py` | `python3 -I code/crosscheck_small.py` | `out/crosscheck_small.txt` | double-precision cross-check of Lemma 6(c), using two different base pairs |
| `code/check_lemmas.py` | `python3 -I code/check_lemmas.py` | `out/check_lemmas.txt` | double-precision sanity check: the Lemma 2 orbit count on random points for N = 3..40; extensions of P_N for N = 3..60 (only the centre, exactly when 6 \| N); extensions of P_M \ {w_0} for odd M = 5..61 (only w_0) |
| `code/search_fewdist.py` | `python3 -I code/search_fewdist.py 4 2 1 3000`; `... 6 3 <seed> 3000` | `out/search_4_2.txt`, `out/search_6_3_seed*.txt` | heuristic numerical search for convex k-gons with d distances; used only to *find* the kite and H3; not part of the proof |

Results:
* **Quadrilaterals** (exact run, `out/small_cases_quads.txt`): the square, the rhombus and the kite have 0
  extensions. P_5 \ {w_0} has exactly 1 extension, the missing vertex. No valid pairs.
* **Hexagons:** P_6 has exactly 1 extension, the centre, which is collinear with 3 vertex pairs
  (`out/small_cases_hexes.txt`). H3 has 0 extensions (`out/small_cases_h3.txt`). The exact run for
  P_7 \ {w_0} did **not finish**: sympy minimal polynomials of nested heptagon radicals stalled, and I
  killed the run after about 40 minutes, as noted at the end of the output file. This case does not need
  the computer, because Lemma 5 with M = 7 proves it by hand. The double-precision cross-check also finds
  only w_0. So Lemma 6(c) for P_7 \ {w_0} rests on Lemma 5, not on the script.
* **Heuristic searches:** the quadrilateral search found exactly the 4 classes, matching Fishburn's count.
  Of the four hexagon search runs, two found nothing; together the other two found only the regular hexagon
  and H3. The heptagon-minus-vertex class was never hit. The search is heuristic, so this means nothing for
  completeness. Completeness does not depend on these searches.

A bug was caught and fixed during the work. The first version of `to_iv` converted values to mpmath at
15-digit precision, which made exact equalities look unequal: it wrongly reported 0 extensions for P_6.
This was detected because the centre of P_6 must be an extension. The fixed version builds the intervals
from 85-digit decimal strings with a 1e-50 widening. All outputs in `out/small_cases_*.txt` come from the
fixed version.

## 8. What this does and does not show

**Shows (rigorous, given §3):** the first question of #1082 holds for every point set with no three
collinear that has at least n - 2 points in convex position, for all n. For n >= 9 and for every odd n, the
proof uses only (Alt), (Alt=), (Fi=) and Lemmas 0–5, all proved here by hand. For n ∈ {6, 8} it also uses
Lemma 6, which rests on (Fi4,6) and an exact computation.

Alternative route for n ∈ {6, 8}, not used above: a 2-distance planar set has at most 5 points and a
3-distance planar set has at most 7 points. These are the values g(2) = 5 and g(3) = 7 attributed to
Kelly and to Erdős–Fishburn (Discrete Math. 160 (1996)). I read them only in the sallerk forum comment and
the Plasma sallerk claim page, not in the primary papers. The 1996 abstract, which I did read, says only
that maximum sets "are identified for k ⩽ 5". Either route settles n = 6 and n = 8.

**Does not show:**
* anything about sets with 3 or more points outside every convex subset of size n - 2;
* anything about the second question (single point), which is already disproved;
* anything about the general first question.

Any counterexample to the first question must have at least 3 points outside every convex subset. More
precisely, the largest convex-position subset must have size at most n - 3. Combined with sallerk's
n <= 15, a counterexample needs n >= 16 and a largest convex subset of size at most n - 3.

**Points of trust:**
1. The statements of Altman's and Fishburn's theorems come from Fishburn's 1995 abstract. I did not read
   the papers' proofs. The PDF download from CORE was blocked.
2. Reading "three hexagons" and "four quadrilaterals" as similarity classes is my interpretation.
3. Lemma 6 is computer-assisted. Rejections are certified by mpmath interval arithmetic, starting from
   sympy evaluations at 80 digits. I relied on sympy's evalf accuracy rather than on a formally verified
   evaluator.

## 9. Sources not read

* Altman, "On a problem of P. Erdős", Amer. Math. Monthly 70 (1963): the paper itself. The statements were
  taken from Fishburn's abstract.
* Fishburn 1995: the full text. The CORE PDF returned an HTML bot page, so I read the abstract only. In
  particular I did not see its explicit lists of the 4 quadrilaterals and 3 hexagons. I identified them
  myself (Lemma 6) and matched the counts.
* Erdős–Fishburn, "Maximum planar sets that determine k distances", Discrete Math. 160 (1996): abstract
  only. Kelly (1947) and Shinohara on 3-distance sets: not read.
* Bhowmick, HAL hal-05864246: abstract only, because the PDF was blocked. "Erdős Problem a Day #1082 wave 8d"
  (online note cited in arXiv:2611.25148): not found or read.
* Altman, "Some theorems on convex polygons", Canad. Math. Bull. 15 (1972): not read.
* sallerk's NOTE.md, RESULTS.md and REPRODUCE.md on GitHub: not re-read in this session; only the forum
  summary and the Plasma claim page were read. The formal-conjectures Lean file for 1082: not read in this
  session. ryantuck/erdos-ai: not checked.
* arXiv: one abstract keyword query only, not a full literature search. Google Scholar and MathSciNet: not
  searched.
