# Erdős #719 (Erdős–Sauer), the case n = r + 3: proof

Date: 2026-11-23. Folder: `erdos-work/attack/719/t1/prove/`.

## Statement established (PROVED)

**Theorem.** Let r >= 3 and n = r + 3. For every r-uniform hypergraph G on n vertices,

    |E(G)| - r * nu(G)  <=  ex_r(n; K_{r+1}^r),

where nu(G) is the maximum number of pairwise edge-disjoint copies of K_{r+1}^r in G.
In fact the stronger inequality |E(G)| - ceil(n/2) * nu(G) <= ex_r(n; K_{r+1}^r) holds
for every r >= 1 with n = r + 3 (and ceil(n/2) <= r exactly when n >= 6).

Consequently every r-graph on n = r+3 vertices is the union of at most ex_r(n; K_{r+1}^r)
copies of K_r^r and K_{r+1}^r, no two sharing an edge (Lemma 1). Together with the easy
Proposition 6 (n <= r+2), the Erdős–Sauer conjecture holds **for all r >= 3 and all n <= r+3**.

Equivalent dual form (Lemma 2), also proved: for every N >= 6 and every family T of 3-subsets
of [N], if F is the graph of pairs of [N] contained in no member of T, then

    |T| + (N-3) * nu(F)  >=  c(N),

where c(N) is the minimum number of 3-subsets of [N] that together contain every pair, and nu(F)
is the matching number of F. The proof never uses any formula for c(N).

## Status check before working (done 2026-11-23)

- erdosproblems.com/719 (fetched with curl, saved `refs/page719.html`): status open, 1 comment,
  1 proof claim. Forum thread (`refs/forum719.html`): still only Zeraoulia's comment of 8 Feb 2026
  (r=3, n=6 exhaustive; and the remark that (r,n)=(7,8) is immediate). VERIFIED by reading.
- Plasma `wiki/problems/set_systems/E0719/_index.md` (saved `refs/plasma_E0719__index.md`, updated
  2026-10-15): "The case r=3 with n>=10, and every case r>=4 beyond the trivial range n<=r+1, are
  untouched by any claim found." Claims: Erdős–Goodman–Pósa (r=2) and Zeraoulia (r=3, n<=9 only;
  `refs/plasma_claims_2026_09_07_zeraoulia.md`). VERIFIED by reading.
- formal-conjectures `719.lean` (origin/main): `erdos_719` for all r >= 2, all n, marked research open.
- arXiv API keyword searches ("Erdos Sauer hypergraph", "clique decomposition hypergraph Turan",
  "edge-disjoint hypergraph Turan", "Erdos-Goodman-Posa"): nothing relevant. Quick only.
- So the case n = r+3 for r >= 4 is not covered by any source I read. Whether it is folklore or in
  Sauer's own papers is NOT checked (see "Sources not read").

## Notation

V = [N], N = n = r + 3. For X ⊆ V write X^c = V \ X. A "triple" is a 3-subset of V. A triple
*covers* a pair if it contains it. c(N) = min number of triples covering all C(N,2) pairs.
For a graph F, nu(F) is its matching number. m = |E(G)|.

## Lemma 1 (decomposition count)

If G contains j pairwise edge-disjoint copies of K_{r+1}^r, then G is the union of m - r*j copies
of K_r^r and K_{r+1}^r, no two sharing an edge. Hence the conjecture holds for G as soon as
m - r*nu(G) <= ex_r(n; K_{r+1}^r).

*Proof.* Take the j cliques; they use j(r+1) distinct edges (edge-disjoint, each has r+1 edges).
Take each of the remaining m - j(r+1) edges as a single K_r^r. These pieces pairwise share no edge
and their union is G. The count is j + m - j(r+1) = m - r*j. ∎

## Lemma 2 (complement dictionary for n = r+3)

Let G be an r-graph on V. Let T = { e^c : e an r-subset of V, e not in E(G) } (a family of
triples), t = |T|, so m = C(N,3) - t, and let F = { pairs A ⊆ V : no member of T contains A }.
Then:

(a) An (r+1)-set S ⊆ V spans a copy of K_{r+1}^r in G iff S^c ∈ F.
(b) Two distinct (r+1)-sets S, S' share an r-subset iff |S^c ∩ S'^c| = 1.
(c) nu(G) = nu(F).
(d) ex_r(N; K_{r+1}^r) = C(N,3) - c(N).

*Proof.* (a) |S^c| = N - r - 1 = 2. The r-subsets of S are S \ {x}, x ∈ S, and
(S \ {x})^c = S^c ∪ {x}. So S \ {x} is a non-edge iff S^c ∪ {x} ∈ T. The triples containing the
pair S^c are exactly S^c ∪ {x} with x ∉ S^c, i.e. x ∈ S. Hence all r-subsets of S are edges iff no
triple of T contains S^c, i.e. iff S^c ∈ F.

(b) Distinct (r+1)-sets share an r-subset iff |S ∩ S'| >= r, and |S ∩ S'| <= r since they are
distinct, so iff |S ∩ S'| = r. Now |S ∩ S'| = N - |S^c ∪ S'^c| = N - 4 + |S^c ∩ S'^c|
= r - 1 + |S^c ∩ S'^c|, which equals r iff |S^c ∩ S'^c| = 1.

(c) A copy of K_{r+1}^r in G is determined by its vertex set S (its edges are all r-subsets of S),
and by (a) the map S -> S^c is a bijection from copies in G onto F. Two copies are edge-disjoint
iff their vertex sets are distinct and share no r-subset, iff (by (b)) the pairs S^c, S'^c are
distinct and do not meet in exactly one point. Two distinct pairs meet in 0 or 1 points, so this
means the pairs are disjoint. Hence edge-disjoint families of copies correspond exactly to
matchings in F, and nu(G) = nu(F).

(d) G -> T is a bijection between r-graphs on V and families of triples on V (complementation of
sets is a bijection between r-subsets and 3-subsets). By (a), G is K_{r+1}^r-free iff F is empty,
iff T covers every pair. So the maximum of m = C(N,3) - |T| over K_{r+1}^r-free G is
C(N,3) - c(N). ∎

Computational check of Lemma 2: `duality full` enumerates all 2^20 3-graphs on 6 vertices and
computes nu(G) by brute-force clique packing in G and nu(F) by brute-force matching in the dual;
0 mismatches, ex_3(6;K_4^3) = 14 (so c(6) = 6), max(m - 3 nu) = 14, 0 violations. `duality random`
checks nu(G) = nu(F) on 200,000 random dense G for each (r,n) = (3,6), (4,7), (5,8), (6,9) with
nu ranging over 0..4: 0 mismatches. (out/duality_full_r3n6.txt, out/duality_random.txt)

## Lemma 3 (maximum-matching structure)

Let F be a graph on V, M a maximum matching of F, k = |M|, W = V(M) (so |W| = 2k), U = V \ W.
For x ∈ W let N_U(x) be the set of F-neighbours of x in U. Then
(i) no edge of F has both ends in U;
(ii) for every ab ∈ M, either N_U(a) = ∅, or N_U(b) = ∅, or N_U(a) = N_U(b) = {u} for a single
vertex u.

*Proof.* (i) If uv ∈ F with u, v ∈ U, then M ∪ {uv} is a matching of size k+1, contradiction.
(ii) Suppose N_U(a) and N_U(b) are both nonempty. Let u ∈ N_U(a), u' ∈ N_U(b). If u ≠ u', then
(M \ {ab}) ∪ {ua, bu'} is a matching: u, u' ∉ W are not covered by M, a and b are covered in M
only by ab, and u, a, b, u' are four distinct vertices. It has size k+1, contradiction. So every
element of N_U(a) equals every element of N_U(b); as both sets are nonempty, they are the same
singleton {u}. ∎

## Lemma 4 (covering lemma)

Let N >= 3 and let F be a graph on V with nu(F) = k. There is a family C of triples with
|C| <= k * ceil(N/2) such that every edge of F is covered by a member of C.

*Proof.* Pairing fact: for x ∈ V and Y ⊆ V \ {x}, there are ceil(|Y|/2) triples, each containing x,
that cover every pair {x,y}, y ∈ Y. (Split Y into floor(|Y|/2) pairs {y,y'} and, if |Y| is odd, one
leftover y; use {x,y,y'} for each pair and {x,y,z} for the leftover, with any z ∉ {x,y}, which
exists as N >= 3.)

Fix a maximum matching M, and W, U as in Lemma 3.

Step 1 (pairs inside W). List W = {w_1, ..., w_{2k}}. For each j apply the pairing fact to
x = w_j, Y = {w_l : l > j}. This covers every pair inside W with
sum_{j=1}^{2k} ceil((2k-j)/2) = sum_{s=0}^{2k-1} ceil(s/2) triples. Grouping s = 2i-1, 2i
(i = 1..k-1), each contributing i, plus s = 2k-1 contributing k and s = 0 contributing 0, this sum
is 2 * (k-1)k/2 + k = k^2 (and 0 when k = 0).

Step 2 (edges between W and U). For each ab ∈ M, by Lemma 3(ii):
 (α) if one endpoint, call the other one h, has no U-neighbour, apply the pairing fact to x = h,
     Y = U: ceil(|U|/2) triples covering every pair {h,u}, u ∈ U;
 (β) otherwise N_U(a) = N_U(b) = {u}; add the single triple {a,b,u}. Here |U| >= 1, so
     1 <= ceil(|U|/2).

Coverage. Let xy ∈ F. Both ends in U is impossible by Lemma 3(i). Both ends in W: covered in
Step 1. Otherwise x ∈ W is an endpoint of some ab ∈ M and y ∈ U is an F-neighbour of x; in case (α)
x must be h (the other endpoint has no U-neighbour), so xy is covered; in case (β) y = u and
{a,b,u} covers xy.

Count. |C| <= k^2 + k * ceil((N-2k)/2) = k * (k + ceil((N-2k)/2)) = k * ceil(N/2), using that k is
an integer. ∎

Computational check of Lemma 4 (`lemma_cover`): implements exactly this construction (with a
brute-force maximum matching), asserts Lemma 3(i),(ii) on every input, checks that C covers every
edge of F and that |C| <= nu(F)*ceil(N/2).
- Exhaustive over all labelled graphs for N = 3..8 (8 + 64 + 1024 + 32768 + 2097152 + 268435456
  graphs): 0 failures, 0 structural-assertion failures (out/lemma_cover_exh3to7.txt,
  out/lemma_cover_exh8.txt).
- Random (G(N,p) with random p, star-like, clique-on-subset; random relabelling): 200,000 graphs for
  each N in {6,7,9,10,11,12,13,14,16,18} and 20,000 for N = 20: 0 failures
  (out/lemma_cover_random.txt).
(An earlier run of the random test had an array overflow bug for N >= 12, which produced spurious
failures; it was fixed — arrays `pu/pv` enlarged from 64 to 512 — and all reported outputs are from
the fixed code.)

## Theorem 5 (main theorem)

For every N >= 3 and every family T of triples on V = [N], with F the graph of pairs covered by no
member of T:  c(N) <= |T| + ceil(N/2) * nu(F).  For N >= 6 this gives c(N) <= |T| + (N-3) * nu(F).
Hence for r >= 3, n = r+3 and every r-graph G on [n]: m - r*nu(G) <= ex_r(n; K_{r+1}^r).

*Proof.* Let k = nu(F) and take C from Lemma 4. Every pair not in F is covered by T (definition of
F) and every pair in F is covered by C, so T ∪ C covers all pairs and
c(N) <= |T ∪ C| <= |T| + k*ceil(N/2).
For N >= 6: if N is even, ceil(N/2) = N/2 <= N-3 iff N >= 6; if N is odd then N >= 7 and
ceil(N/2) = (N+1)/2 <= N-3 iff N >= 7. So ceil(N/2) <= N-3 and c(N) <= |T| + (N-3)k.

Now let r >= 3, n = N = r+3 >= 6, G an r-graph on [N], and T, F as in Lemma 2, so m = C(N,3) - |T|,
nu(G) = nu(F) = k (Lemma 2(c)) and ex = C(N,3) - c(N) (Lemma 2(d)). Then
m - r*nu(G) = C(N,3) - |T| - (N-3)k <= C(N,3) - c(N) = ex_r(n; K_{r+1}^r).
The stronger form m - ceil(n/2) nu(G) <= ex is the same computation with the first inequality,
valid for all N >= 4 (r >= 1). By Lemma 1, G is the union of at most ex pieces. ∎

## Proposition 6 (n <= r+2, r >= 2)

For r >= 2, n <= r+2 and every r-graph G on [n]: m - r*nu(G) <= ex_r(n; K_{r+1}^r).

*Proof.* n < r: G has no edges, so m = 0 <= ex. n = r: there is no (r+1)-set, so ex = C(r,r) = 1
>= m. n = r+1: the only possible clique is on all of [n]; deleting one edge from the complete
r-graph leaves C(r+1,r) - 1 = r edges and no clique, and any graph with all r+1 edges contains it,
so ex = r. If G is complete, m - r*nu = r+1-r = 1 <= r; otherwise m <= r = ex.
n = r+2 = N: complement each r-set to a pair; an (r+1)-set S has |S^c| = 1, and S contains the
non-edge e iff S^c ⊆ e^c. So G is K_{r+1}^r-free iff the complements of its non-edges (a set of
pairs) meet every vertex, which needs at least ceil(N/2) pairs (each pair meets 2 vertices) and
ceil(N/2) pairs suffice (floor(N/2) disjoint pairs, plus one more pair through the leftover vertex
if N is odd; N >= 4). So ex = C(N,2) - ceil(N/2). If nu(G) = 0, m <= ex by definition. If
nu(G) >= 1, m - r*nu(G) <= C(N,2) - (N-2) <= C(N,2) - ceil(N/2) because ceil(N/2) <= N-2 for
N >= 4. ∎

**Corollary 7.** The Erdős–Sauer inequality (hence the decomposition of #719) holds for all r >= 3
and all n <= r+3 (Proposition 6 and Theorem 5). For r = 2 it holds for n <= 4 by Proposition 6;
r = 2, n = 5 is not covered by Theorem 5 (ceil(5/2) = 3 > 2) but is a case of the
Erdős–Goodman–Pósa theorem (recorded on the Plasma page; the paper itself was not read by me) and
of the scout's exhaustive es.c run (2,5).

## What this does and does not show

Does:
- Settles every case n = r+3 (r >= 3), in particular the infinite family (4,7), (5,8), (6,9), ...
  of r >= 4 cases that the Plasma page calls untouched; with Proposition 6, all n <= r+3, r >= 3.
- Rigorous, self-contained, and independent of the exact covering numbers c(N) (no Fort–Hedlund or
  Schönheim formula is used). Lemmas 2 and 4 are also checked by computation (see above).
- Gives a stronger inequality: in the n = r+3 range a clique only needs to "save" ceil(n/2) rather
  than r = n-3 edges.

Does not:
- Say anything about n >= r+4 (e.g. (r,n) = (4,8), Target T2) or about r = 3, n >= 10. The same
  dual approach for s = n - r >= 4 would need covering (s-1)-sets by s-sets around a maximum packing
  of (s-1)-sets pairwise meeting in <= s-3 points; the crude bound from a maximal packing
  (k * s * ceil((N-s+2)/2)) exceeds the budget k(N-s), so a finer structure lemma (analogue of
  Lemma 3) would be needed. Not attempted.
- Establish novelty. The range n - r <= 3 is "near-trivial" in the sense that the factor r = n-3 is
  large compared with the cost ~n/2 of covering a matching edge's neighbourhood; the argument is
  elementary and may well be folklore or appear in Sauer's work. Only the sources listed above were
  checked.
- The scout's es2.c runs for (4,7) and (5,8) were not re-run here; my own direct exhaustive check
  is for (3,6) only (plus the lemma checks above).

## Code, outputs, reproduction

- `code/lemma_cover.c` — checks Lemmas 3 and 4 (exhaustive N <= 8, random up to N = 20).
- `code/duality.c` — checks Lemma 2 (nu(G) = nu(F)) and the full (3,6) case directly.
- `code/run_all.sh` — reproduces every file in `out/` (about 15 minutes):

      sh attack/719/t1/prove/code/run_all.sh

- Outputs: `out/lemma_cover_exh3to7.txt`, `out/lemma_cover_exh8.txt`, `out/lemma_cover_random.txt`,
  `out/duality_full_r3n6.txt`, `out/duality_random.txt`.
- Downloads (untrusted data): `refs/page719.html`, `refs/forum719.html`, `refs/plasma_*.md`,
  `refs/arxiv*.xml`.

## Sources not read

- Erdős 1981 (Combinatorica 1, 25–42) original statement; Erdős–Goodman–Pósa 1966; any paper of
  N. Sauer on clique decompositions of hypergraphs (possible prior source for this range).
- The full Zeraoulia Zenodo PDF (only the Plasma summary / scout's abstract record).
- MathSciNet, zbMATH, Google Scholar; the proof-claims tab beyond what the Plasma page summarises.
- Fort–Hedlund / Schönheim covering results (not needed by the proof).
