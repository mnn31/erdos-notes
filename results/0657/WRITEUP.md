# Erdős #657, small cases: phi(6) = 6 and phi(7) = 8

## Statement established

Let phi(n) be the minimum number of distinct distances spanned by n distinct points in R^2 such that no
three of them form an isosceles triangle. Degenerate triangles count: a collinear triple x, y, z with
|xy| = |xz| is isosceles. This phi(n) is phi(n,3,3) = n f(n) in the notation of the forum.

**Theorem.** phi(6) = 6 and phi(7) = 8. As a side result, phi(5) = 5.

So Tang's matching bound (n-1 for even n, n for odd n) is tight for n = 3, 4, 5 and fails for n = 6 and n = 7.

| n | Tang lower bound | phi(n) | lower-bound proof here | upper-bound witness here |
|---|---|---|---|---|
| 5 | 5 | **5** | Tang | Lemma 10 (Krawczyk certificate, interval arithmetic) |
| 6 | 5 | **6** | Lemmas 1–5 (exact polynomial identity) | Lemma 6 (6 points with coordinates in Z[√7], exact integer check) |
| 7 | 7 | **8** | Lemmas 1, 2, 7–9 (hand proof for one orbit, exact identities for six) | Lemma 9 (7 integer points, exact integer check) |

Status labels used below: VERIFIED-PROOF means a complete argument written out here. VERIFIED-COMP means a
finite computation in exact arithmetic (integers or rationals), or a rigorous interval-arithmetic
certificate, with the script and output saved. INFERRED means not proved.

---

## Notation

A point set A is *isosceles-free* if it has no isosceles triangle, degenerate ones included. Colour each
edge of K_A by its squared length. A *distance class* is the set of pairs at one common distance. For
pairs {i,j} we write D(i,j) = |p_i - p_j|^2.

---

## Lemma 1 (Tang). A is isosceles-free iff every distance class is a matching. VERIFIED-PROOF

An isosceles triangle, degenerate or not, is three distinct points x, y, z with |xy| = |xz|. That is the
same as two edges xy and xz that share the vertex x and lie in one distance class. So no isosceles triangle
exists iff no class contains two edges at a common vertex, which means every class is a matching. ∎

**Corollary (Tang's bound).** A class has at most floor(n/2) edges, so phi(n) >= C(n,2)/floor(n/2). This
gives phi(6) >= 5 and phi(7) >= 7.

## Lemma 2 (structure at the bound). VERIFIED-PROOF

(a) If 6 isosceles-free points span exactly 5 distances, the 5 classes form a 1-factorization of K6
(5 perfect matchings that partition the 15 edges).
(b) If 7 isosceles-free points span exactly 7 distances, the 7 classes form a near-1-factorization of K7
(7 matchings of size 3 that partition the 21 edges).

*Proof.* (a) The 15 edges fall into 5 classes of size at most 3 (Lemma 1), so every class has exactly 3
edges, and a matching of 3 edges on 6 vertices is perfect. (b) The 21 edges fall into 7 classes of size at
most 3, so every class has exactly 3 edges. ∎

## Lemma 3 (Gram rank). VERIFIED-PROOF

Let p_0, …, p_{m} be points of R^2 and let M be the m×m matrix with
M_ij = D(0,i) + D(0,j) - D(i,j) for 1 <= i, j <= m. Then every 3×3 minor of M is 0.

*Proof.* Put x_i = p_i - p_0. Then D(i,j) = |x_i|^2 + |x_j|^2 - 2 x_i·x_j, so M_ij = 2 x_i·x_j and
M = 2 X Xᵀ, where X is the m×2 matrix with rows x_i. Hence rank M <= 2, and every 3×3 minor is 0. ∎

(In six_lower.py the Gram matrix G = M/2 is used. In the K7 certificates M itself is used. Scaling does not
change which minors vanish.)

---

## Part I: phi(6) = 6

### Lemma 4. Every 1-factorization of K6 is isomorphic to GK6. VERIFIED-COMP

Label the vertices ∞ = 5 and 0, …, 4 (read mod 5), and set
M_k = { {∞,k}, {k+1,k-1}, {k+2,k-2} } for k = 0, …, 4. These are disjoint perfect matchings. The edge
{i,j} ⊂ Z5 lies in M_k exactly when i + j ≡ 2k (mod 5), that is, k = 3(i+j) mod 5.

`six_lower.py` lists every labelled 1-factorization of K6 by exhaustive backtracking: it takes the smallest
uncovered edge and tries every perfect matching through it. There are exactly 6. The script then checks that
the S6-orbit of GK6 is exactly this set of 6. Output: `out/six_lower.txt`.

### Lemma 5. No 1-factorization of K6 can be realized in R^2 with 5 distinct positive class lengths. VERIFIED-COMP

By Lemma 4 we may assume the classes are M_0, …, M_4 above. Let d_k > 0 be the squared length of M_k. With
base point ∞, x_i = p_i - p_∞, and i = 0..4, we get |x_i|^2 = d_i because {∞,i} ∈ M_i, and

  G_ij = x_i·x_j = (d_i + d_j - d_{3(i+j) mod 5}) / 2   (i ≠ j),   G_ii = d_i.

Write [R | C] for the minor det G[R, C], with rows R and columns C taken from {0,…,4}. Then the following
polynomial identity holds in Q[d_0, …, d_4]:

  d_1 d_4 (d_1 - d_4) =
   1/3[012|012] - 1/3[012|014] + 2/3[012|024] + 1/3[012|123] + 1/3[012|124]
 - 1/3[013|014] - 2/3[013|034] - 1/3[013|124] - 2/3[013|134] + 1/3[013|234]
 + 1/3[014|024] + 1/3[014|034] - 1/3[024|123] + 2/3[024|124] + 1/3[024|134]
 - 1/3[034|034] - 1/3[034|134] - 1/3[034|234] - 2/3[123|124] + 2/3[134|234].

*Verification.* `six_lower.py` checks this in two independent ways. First, sympy expands the difference and
gets 0. Second, without sympy, it evaluates both sides with exact Fractions at all 4^5 points of
{0,1,2,3}^5. The difference has degree at most 3 in each variable, so it vanishes identically once it
vanishes on S^5 with |S| = 4: induct on the number of variables, using the fact that a univariate
polynomial of degree at most 3 with 4 roots is zero. Output: 0 failures.

*Proof of Lemma 5.* By Lemma 3, every minor on the right is 0 for a planar realization, so
d_1 d_4 (d_1 - d_4) = 0. But d_1, d_4 > 0 and d_1 ≠ d_4 because the classes are distinct. Contradiction. ∎

**Corollary.** phi(6) >= 6. Combine Lemmas 2(a), 4 and 5. Since phi(6) >= 5 (Tang), a set with 5 distances
would give a planar realization of some 1-factorization of K6, and none exists.

### Lemma 6. phi(6) <= 6. VERIFIED-COMP

Write s = √7 and take the six points

  (34, 0), (-11, -25s), (40, -8s), (-34, 0), (11, -25s), (-40, -8s).

Squared distances are integers: (Δx)^2 + 7(Δc)^2, where y = c·s. `six_upper.py` computes all 15 of them
exactly in integers.

| squared distance | pairs |
|---|---|
| 484 | 02, 14, 35 |
| 2864 | 15, 24 |
| 4624 | 03, 12, 45 |
| 4904 | 04, 13 |
| 5924 | 05, 23 |
| 6400 | 01, 25, 34 |

That is 6 distinct values, and no triple has two equal sides. Equal squared distances are the same as equal
distances, so this is an exact check of isosceles-freeness, degenerate case included. Output:
`out/six_upper.txt`; object: `out/six_points.json`.

*How it was found.* Take the set symmetric about the y-axis, p_i = (x_i, y_i) and p_i' = (-x_i, y_i). The
classes {p_i p_j, p_i' p_j'} and {p_i p_j', p_i' p_j} of size 2 come for free. Then impose
|p_k p_k'| = |p_i p_j| for {i,j,k} = {1,2,3}. This gives a quartic curve in (x_1 : x_2 : x_3), and a small
search found the rational point (34, -11, 40).

**Theorem A. phi(6) = 6.** ∎

(The scout's centrally symmetric family {±p_1, ±p_2, ±p_3} with |2p_k| = |p_i - p_j| does **not** work. The
Gram determinant forces 49 e_3 = 20 e_1 e_2 - 5 e_1^3 in a_k = |p_k|^2, and a numerical scan, `cs6scan.py`,
found no point with a positive semidefinite rank-2 Gram matrix. INFERRED only; the reflection family
replaces it, so this is not needed.)

---

## Part II: phi(7) = 8

### Lemma 7. The near-1-factorizations of K7 form exactly 7 isomorphism classes. VERIFIED-COMP

`nf7.py` lists every partition of E(K7) into 7 matchings of size 3 by exhaustive backtracking. There are
6240, which matches the known number of labelled 1-factorizations of K8, as it must, by adding an eighth
vertex. The script splits them into S7-orbits by generating each orbit in full. It finds 7 orbits with
sizes 30, 630, 2520, 420, 1680, 840, 120, summing to 6240. The representatives R0…R6 are in `out/nf7.txt`
and `out/nf7_reps.pkl`.

### Lemma 8 (rectangle lemma). VERIFIED-PROOF

Let a, b, c, d be distinct points of R^2 with |ab| = |cd|, |ac| = |bd| and |ad| = |bc|. Then one of the
three pairings, namely the one of strictly largest length, consists of two segments with a common midpoint
m, and |a-m| = |b-m| = |c-m| = |d-m|.

*Proof.* Expanding squares gives the identity

|a-c|^2 - |b-d|^2 + |a-d|^2 - |b-c|^2 = 2(a-b)·(a+b-c-d),

so (a-b)·u = 0 with u := a+b-c-d. The same identity with the roles of (a,b) and (c,d) exchanged gives
(c-d)·u = 0.

- If u = 0, then a+b = c+d, and ab and cd have a common midpoint.
- If u ≠ 0, then a-b and c-d are both orthogonal to the nonzero vector u in R^2, so they are parallel. As
  |a-b| = |c-d|, we get c-d = ±(a-b).
  - If c-d = a-b, then a+d = b+c, so ad and bc share a midpoint.
  - If c-d = b-a, then a+c = b+d, so ac and bd share a midpoint.

In every case some pairing, say {xy, zw}, satisfies x+y = z+w = 2m. Its two segments also have equal length
by hypothesis, so |x-m| = |y-m| = |z-m| = |w-m| =: r. Then (z-x)·(y-z) = 0, because z and the endpoints of
the diameter xy lie on a circle (|z-m| = |x-m| = |y-m| with y = 2m-x). So |xy|^2 = |xz|^2 + |zy|^2, and
this pairing is strictly longer than the other two (all points distinct). ∎

### Lemma 9. No near-1-factorization of K7 can be realized in R^2 with 7 distinct positive class lengths.

**Orbit R0 (|Aut| = 168). Hand proof. VERIFIED-PROOF + VERIFIED-COMP for two finite facts.** The classes of R0
are

{03,12,56}, {05,14,36}, {04,15,26}, {06,24,35}, {01,23,45}, {16,25,34}, {02,13,46}.

`rep0_comb.py` checks two finite facts:
- (i) for every class and every pair of its edges {ab}, {cd}, all three opposite pairings of {a,b,c,d} lie
  in common classes;
- (ii) every vertex lies in such a quadruple. There are 7 such quadruples, the complements of the lines of a
  Fano plane.

Suppose R0 is realized. Let X = {e_1, e_2, e_3} be the class of largest distance. By (i), the endpoints of e_1
and e_2 form a quadruple that satisfies Lemma 8. Its three pairings are three distinct classes, and X is the
longest of them, so by Lemma 8, e_1 and e_2 share a midpoint O. Likewise e_1 and e_3 share a midpoint. So the
three edges of X are diameters of one circle Γ with centre O and radius r. Their six endpoints lie on Γ, and
the X-partner of each such point t is its antipode 2O - t.

Let w be the seventh vertex. By (ii), some quadruple Q = {w, x, y, z} satisfies Lemma 8, and x, y, z are
among the six points on Γ. By Lemma 8, the four points of Q lie on a circle with centre m'. Three distinct
points determine at most one circle: a line meets a circle in at most 2 points, so they are not collinear,
and the centre is the intersection of two perpendicular bisectors. Since x, y, z lie on both circles, that
circle is Γ and m' = O. Q's diagonal through w has midpoint O, so w = 2O - t for some t ∈ {x, y, z}. Then w
is the X-partner of t, which is one of the six points other than w. This contradicts distinctness. ∎

**Orbits R1–R6. Exact identities. VERIFIED-COMP.** For each k = 1..6 there is a polynomial identity

  T_k(d) = Σ c · det M[R, C] · μ   (c ∈ Q, μ a monomial, here μ = 1),

where M is the matrix of Lemma 3 with base point 0 and d_c is the squared length of the c-th class of R_k.
The targets are

| orbit | T_k | terms |
|---|---|---|
| R1 | d_3 (d_0 - d_6)(d_1 - d_2) | 27 |
| R2 | d_0^2 (d_3 - d_4) | 41 |
| R3 | d_0 d_4 d_6 | 51 |
| R4 | d_0^3 | 83 |
| R5 | d_0^3 | 84 |
| R6 | d_0^3 | 84 |

The full certificates, with rows, columns and rational coefficients, are in `out/cert_nf7_rep{k}.json`. Each
was found mod p and then solved exactly over Q (`lift.py`, with a sympy expansion check). Each was then
re-verified independently by `verify_cert.py`, which uses no sympy: it evaluates both sides with exact
Fractions on the grid {0,1,2,3}^7. Both sides have total degree 3, so agreement on this grid proves the
identity (same argument as in Lemma 5). Output `out/verify_certs.txt`: 0 failures for all six.
`check_reps.py` confirms that the certificates use exactly the representatives R1–R6 from Lemma 7.

For a realization, every minor vanishes (Lemma 3), so T_k(d) = 0. But each T_k is a product of factors d_i
(positive) and d_i - d_j (nonzero, since classes are distinct). Contradiction. ∎

**Corollary.** phi(7) >= 8. This follows from Lemmas 2(b), 7 and 9 together with Tang's phi(7) >= 7.

### Lemma 10. phi(7) <= 8. VERIFIED-COMP

Take the seven integer points

p0 = (97241, 0), p1 = (-97241, 0), p2 = (-53240, 43759), p3 = (53240, -43759), p4 = (-441, 97240),
p5 = (44000, -53041), p6 = (-44000, 53041).

`seven_upper8.py` computes all 21 squared distances exactly in integers.

| squared distance | pairs |
|---|---|
| 171533124 | 26, 35 |
| 3850938082 | 03, 12, 46 |
| 5647951762 | 05, 16, 24 |
| 18825857600 | 14, 25, 36 |
| 18997390724 | 04, 23, 56 |
| 22762367762 | 06, 15, 34 |
| 24559381442 | 02, 13, 45 |
| 37823248324 | 01 |

That is 8 distinct values, and no triple has two equal sides. Output: `out/seven_upper8.txt`; object:
`out/seven_points_8.json`.

*How it was found.* Least squares over all 444 S7-orbits of partitions of E(K7) into 8 matchings
(`orb8.py`, `num8.py`; 2,106,720 labelled partitions) found realizations for three orbits (79, 80, 293).
Orbit 79 is a 6-point set centrally symmetric about O = 0 (p1 = -p0, p3 = -p2, p6 = -p5) plus a seventh point
q = p4. A Groebner basis of the remaining equations (`p79.py`) gives |q| = |p0|, b = conj(c)·q in complex
notation, and a quadratic for c that is rational when t^2 - 1 is a square, where q = ((1-t^2)/(1+t^2),
2t/(1+t^2)). Taking t = 221/220 (`p79c.py`) and scaling by 97241 gives the points above. Only the final exact
integer check is load-bearing.

**Theorem B. phi(7) = 8.** ∎

### Side result: phi(5) = 5 (Lemma 11). VERIFIED-COMP (interval certificate)

The lower bound is Tang's. For the upper bound, take p0 = (0,0), p1 = (10,0), p2 = (3,a), p3 = (b,c),
p4 = (e,g) and the near-1-factorization of K5 with classes {k+1,k-1}, {k+2,k-2} mod 5. That gives 5
equations with integer coefficients in 5 unknowns. `five_upper.py` runs Newton to 60 digits and applies the
Krawczyk test with mpmath interval arithmetic (outward rounding, 200 bits) on a box of radius 1e-40. It also
asserts that all coefficients are integers, so no inexact constants enter. K(X) ⊂ int X holds, so a unique
exact real solution lies in the box. Interval enclosures of the 10 squared distances show the 5 classes are
pairwise disjoint and all distances are positive. So the 5 points span exactly 5 distances, every class is a
matching, and the set is isosceles-free by Lemma 1. Root to 25 digits:
a = 8.776851404549013519153252, b = 5.258037545497882303789532, c = 9.918979874345375273572802,
e = 10.72345893345894327869163, g = 2.424829513593879036865229. Output: `out/five_upper.txt`; object:
`out/five_points.json`.

(`seven_upper.py` also certifies a 7-point set with 9 distances by the same Krawczyk method. Lemma 10
supersedes it.)

---

## Reproduce

```
cd attack/657/t1/prove/code && bash run_all.sh
```

This runs six_lower, six_upper, nf7, rep0_comb, check_reps, verify_cert (×6), seven_upper8 and five_upper,
writing to `../out/`. The six certificate verifications take a few minutes in total. Regenerating the
certificates (optional) uses `lift.py`; the commands are in the comments of run_all.sh. Python 3.11, sympy
1.14, numpy 1.26, scipy 1.17, mpmath; all scripts run with `python3 -I`.

## What this does and does not show

- It **does** determine phi(6) = 6 and phi(7) = 8 exactly, with phi(5) = 5 as a side result. Tang's parity
  bound is tight for n <= 5 and not tight at n = 6 or 7. Both upper-bound witnesses for n = 6 and 7 are
  exact (integer or Z[√7] coordinates, integer squared distances). Both lower bounds rest on finite exact
  computations:
  - the enumeration of 1-factorizations of K6 and near-1-factorizations of K7;
  - polynomial identities checked in exact rational arithmetic in two independent ways;
  - one hand proof (orbit R0).
- The n = 5 upper bound rests on an interval-arithmetic (Krawczyk) certificate, not on closed-form coordinates.
  It is rigorous given a correct mpmath interval implementation, and it is the only result here that depends
  on floating-point interval code.
- It says **nothing** about the asymptotic question (f(n) → ∞ in the plane). Small values cannot settle
  that. The results are consistent with phi(n)/n growing, but they are equally consistent with
  phi(n) = n + O(1).
- It does not determine phi(8) or beyond. The method (classes are matchings, plus the Gram rank ≤ 2
  condition) extends in principle, but the number of class patterns grows quickly.
- The lower bounds for n = 6, 7 for orbits other than R0 are computer certificates without a conceptual
  explanation. A human proof for GK6 (no rectangle quadruples exist there, since any two classes form a
  Hamiltonian 6-cycle) was not found.
- Novelty: the erdosproblems.com page and forum thread (read 2026-11-23), the Plasma E0657 page and the Lean
  file contain only the n-1 / parity bounds. An arXiv abstract search ("isosceles" AND "distances") found
  nothing on exact small values. Older literature could still contain these values (see below).

## Sources not read

- Fox–Pach–Suk, "More distinct distances under local conditions"; Fish–Lund–Sheffer; Pohoata–Sheffer;
  Sheffer's distinct-distances survey. These are known only through Tang's forum summary and the Plasma page,
  which say they record only phi(n,3,3) >= n-1.
- Dumitrescu [Du08], Erdős [Er73, Er75f, Er97e], Erdős–Pach [ErPa90]: not read directly.
- No full-text search of older literature on isosceles-free or "λ-free" sets for small exact values was done
  (MathSciNet and zbMATH were not checked).
