# Erdős Problem 585 — exact small values of f(n), 5 ≤ n ≤ 10 (plus n = 11)

**f(n)** := the maximum number of edges of a simple graph on n vertices that does **not**
contain two edge-disjoint cycles with the same vertex set. Call such a pair a *P-pair*,
say G *has P* if it contains one, and *P-free* otherwise.

## Statement established

| n | 5 | 6 | 7 | 8 | 9 | 10 | (11) |
|---|---|---|---|---|---|---|---|
| f(n) | 9 | 12 | 16 | 19 | 23 | 27 | (31) |
| 3n−6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 |
| # extremal graphs (iso classes) | 1 | 3 | 1 | 12 | 8 | 7 | (8) |
| explicit extremal graph | K2∨P3 = K5−e | K2∨P4 | K2∨C5 | K2∨C6 | K2∨θ(3,3,2) | K2∨K4* | |

(Trivially f(1..4) = 0, 1, 3, 6, since K4 is P-free — see Lemma 2.)
Here K2∨H is the join of an edge ab with H (a, b adjacent to each other and to every vertex
of H); θ(3,3,2) is two vertices joined by three internally disjoint paths with 3, 3, 2 edges
(7 vertices, 8 edges); K4* is K4 with the four edges of one 4-cycle subdivided once each
(8 vertices, 10 edges, girth 5).

**Theorem.** f(5)=9, f(6)=12, f(7)=16, f(8)=19, f(9)=23, f(10)=27. The graphs in the last row
attain these values, and the numbers of extremal isomorphism classes are as listed (all
extremal graphs are listed in graph6 in `out/extremal_graphs_n5_10.txt`).

Status of the parts:
* Lower bounds (all n = 5..10): **proved by hand** (Lemma 5 + Lemma 6) and additionally checked
  by two independent programs.
* Upper bounds n = 5..8: computer proof by **exhaustive enumeration of all labelled graphs**
  (`brute.c`), confirmed by a second, independent program (`gen.c`).
* Upper bounds n = 9, 10: computer proof by `gen.c` (Lemma 3 recursion + exhaustive
  neighbourhood extension), confirmed by an independent pure-Python pipeline (`indep.py`)
  that shares no P-test or isomorphism code with `gen.c` and uses only Lemmas 1, 3 and the
  brute-force labelled counts at n = 8.
* n = 11 (f(11) = 31, 8 classes): **single computation** (`gen.c` only; extremal graphs
  re-checked P-free in Python). Bonus, not part of the target; treat as one-source.
* Counts of extremal classes: gen.c lists, verified pairwise non-isomorphic (networkx); for
  n ≤ 8 the orbit sums Σ n!/|Aut| equal the brute-force labelled counts
  (10, 380, 252, 175560); for n = 9 the independent pipeline finds exactly 8 classes, the same 8
  up to isomorphism (`out/n9_lists_agree.txt`); the n = 10 count (7) is from gen.c only.

The sequence 0,1,3,6,9,12,16,19,23,27 (n=1..10) is **not** in the OEIS (search 2026-11-23,
`refs/oeis_search2.html`).

---

## Lemmas

**Lemma 1 (monotonicity).** If H ⊆ G and H has P, then G has P. Hence subgraphs (edge- or
vertex-deleted) of P-free graphs are P-free, and if a P-free n-vertex graph with ≥ m edges
exists, then a P-free n-vertex graph with exactly m edges exists. Consequently
"every n-vertex graph with exactly m edges has P" implies f(n) ≤ m−1.

*Proof.* A P-pair of H consists of cycles of H, which are cycles of G, with the same vertex
set and no common edge. For the second claim delete edges one at a time from a P-free graph
with > m edges; each intermediate graph is P-free by the first claim. ∎

**Lemma 2 (shape of a P-pair).** Let C1, C2 be edge-disjoint cycles with V(C1)=V(C2)=S. Then
R = C1 ∪ C2 is a 4-regular graph with vertex set S, so |S| ≥ 5, and C1, C2 are Hamiltonian
cycles of G[S]. Conversely, if for some S with |S| ≥ 5 (indeed |S| ≥ 3) the graph G[S] contains
two edge-disjoint Hamiltonian cycles, G has P. In particular any graph without a subgraph of
minimum degree ≥ 4 is P-free; K1..K4 are P-free; K5 has P.

*Proof.* Each s ∈ S has exactly 2 incident edges in C1 and 2 in C2, and these four edges are
distinct (edge-disjointness), so deg_R(s) = 4. A simple 4-regular graph has ≥ 5 vertices.
C_i visits every vertex of S exactly once, so it is a Hamiltonian cycle of G[S]. The converse
is the definition. If G has no subgraph of minimum degree ≥ 4, it has no 4-regular subgraph R.
K4 has only 4 vertices. K5 = the 5-cycle 0-1-2-3-4 plus the 5-cycle 0-2-4-1-3, which are
edge-disjoint. ∎

**Lemma 3 (minimum-degree deletion).** Let G be P-free with n ≥ 2 vertices and at least t
edges, and let v be a vertex of minimum degree d. Then G − v is P-free with at least
⌈t(n−2)/n⌉ edges, and in G every vertex has degree ≥ d.

*Proof.* P-freeness by Lemma 1. d ≤ 2|E|/n (average degree), so
|E(G−v)| = |E| − d ≥ |E|(1 − 2/n) ≥ t(n−2)/n; the edge count is an integer. ∎

Corollary used for the hand-checkable upper-bound chain: if f(n−1) is known, a P-free n-vertex
graph with m edges has a vertex v with m − f(n−1) ≤ deg v ≤ ⌊2m/n⌋ and G − v P-free with
m − deg v edges.

**Lemma 4 (exhaustive search is sound and complete).** Define A(k,t) = the set of
isomorphism classes of P-free graphs on k vertices with ≥ t edges. Fix t_N = L and
t_{k−1} = ⌈t_k(k−2)/k⌉. Then every class of A(k,t_k) occurs among the graphs obtained from
some graph H of (a list containing a representative of every class of) A(k−1,t_{k−1}) by adding
a vertex v adjacent to a set Nb with deg_H(x) + [x ∈ Nb] ≥ |Nb| for all x, |E(H)| + |Nb| ≥ t_k,
and the resulting graph P-free.

*Proof.* Take G ∈ A(k,t_k) and v a minimum-degree vertex; set H = G − v. By Lemma 3,
H ∈ A(k−1,t_{k−1}), so some list entry H' ≅ H; transport v's neighbourhood along the
isomorphism. The degree condition is "v has minimum degree", the edge condition is
|E(G)| ≥ t_k. ∎

`gen.c` implements this literally: for every list graph H and **every** subset Nb of V(H)
(all 2^{k−1}), it applies the two filters, discards the graph only if `hasP` returns true, and
otherwise keeps it unless its canonical code was already seen.
* `hasP` returns true only after finding explicit cycles, and **every** such witness is
  re-verified by a separate routine (`verify_witness`: consecutive vertices adjacent, no
  repeated vertex, same vertex sets, no common edge; the program aborts otherwise;
  witnesses_verified counts are in the outputs, e.g. 549 997 for the n = 10 run). So nothing
  P-free is ever discarded.
* The canonical code is the upper-triangle adjacency bit-string of G under a relabelling of G,
  so two graphs with equal codes are isomorphic: deduplication never merges non-isomorphic
  graphs. (If the code were not an isomorphism invariant this could only create duplicates,
  which cannot lower the maximum.) Empirically it *is* a complete invariant: with the P-filter
  off it reproduces the numbers of graphs 1, 2, 4, 11, 34, 156, 1044, 12346, 274668 for
  n = 1..9 (OEIS A000088) — `out/validate_nofilter_n9.txt`.
* `hasP` false negatives would only enlarge the lists (cannot lower the maximum); the
  reported extremal graphs are re-checked P-free by an independent checker (pcheck.py).

Hence max{|E(G)| : G in the computed list at level k} ≥ f(k) whenever f(k) ≥ t_k, and equality
holds because the graphs attaining the maximum are verified P-free independently.

**Lemma 5 (joins with an edge).** Let H be a graph such that for every T ⊆ V(H) with
δ(H[T]) ≥ 2 we have e(H[T]) < 2|T| − 4. Then K2∨H contains no 4-regular subgraph; in
particular it is P-free, and it has 1 + 2|V(H)| + e(H) edges.

*Proof.* Let a,b be the apexes and suppose R ⊆ K2∨H is 4-regular with vertex set S. Put
T = S ∖ {a,b}; since |S| ≥ 5, |T| ≥ 3. Each t ∈ T has deg_R(t) = 4 and at most 2 of its
R-edges go to {a,b}, so in R_T := R[T] (whose edges are edges of H) every vertex has degree ≥ 2;
hence δ(H[T]) ≥ 2. Counting R-degrees over T: 4|T| = 2e(R_T) + e_R(T,{a,b}) and
e_R(T,{a,b}) ≤ deg_R(a)+deg_R(b) ≤ 8 (counting only apexes that lie in S). So
e(H[T]) ≥ e(R_T) ≥ 2|T| − 4, contradicting the hypothesis. By Lemma 2, no P-pair. Edge count:
the edge ab, 2|V(H)| apex edges, e(H). ∎

**Lemma 6 (the six H's satisfy Lemma 5).** The hypothesis of Lemma 5 holds for
H = P3, P4, C5, C6, θ(3,3,2), K4*.

*Proof.* We need: every T with δ(H[T]) ≥ 2 has e(H[T]) < 2|T|−4.
* P3, P4 are trees: no T has δ(H[T]) ≥ 2 (a nonempty graph with δ ≥ 2 contains a cycle).
* C_m (m = 5,6): if δ(H[T]) ≥ 2 then H[T] contains a cycle, the only cycle is C_m, so T = V,
  e = m < 2m − 4 because m > 4.
* θ(3,3,2) with branch vertices x,y and paths x-p1-p2-y, x-q1-q2-y, x-r-y. Every interior
  vertex has H-degree 2, so if T contains it and δ(H[T]) ≥ 2, T contains both its neighbours and
  hence the whole path including x and y. T must contain an interior vertex (else |T| ≤ 2). One
  full path alone gives x of degree 1, so T is the union of ≥ 2 full paths: the cycles of
  lengths 5, 5, 6 (e = |T| < 2|T| − 4 since |T| ≥ 5) or all of H (|T| = 7, e = 8 < 10).
* K4* (K4 on {0,1,2,3}, edges 01, 13, 32, 20 subdivided by one new vertex each, 03 and 12 kept):
  the 7 cycles of K4 become cycles of lengths 5,5,5,5 (triangles: each contains exactly two of
  the subdivided edges) and 8, 6, 6 (4-cycles), so girth(K4*) = 5. The cyclomatic number
  μ(F) = e − v + c(F) is monotone under taking subgraphs, μ(K4*) = 10 − 8 + 1 = 3, so
  e(H[T]) ≤ |T| + 3 − c(H[T]) ≤ |T| + 2, which is < 2|T| − 4 when |T| ≥ 7. Suppose |T| ≤ 6 and
  δ(H[T]) ≥ 2. Each component of H[T] has δ ≥ 2, so contains a cycle, so has ≥ 5 vertices;
  hence H[T] is connected and |T| ∈ {5,6}. Violating the bound needs e(H[T]) ≥ 2|T|−4 ≥ |T|+1,
  i.e. μ(H[T]) ≥ 2, so H[T] contains two distinct cycles C, C'. If they share ≤ 1 vertex,
  |T| ≥ 5 + 5 − 1 = 9. Otherwise C' contains a subpath P with both ends on C, internally disjoint
  from C and not an edge of C (P exists: C' ≠ C, and C' meets C in ≥ 2 vertices), and C ∪ P is a
  theta with path lengths p, q, r ≥ 1 whose three cycles have lengths p+q, q+r, r+p ≥ 5, so
  p+q+r ≥ 8 and it has p+q+r−1 ≥ 7 vertices. Either way |T| ≥ 7, contradiction. ∎
  (All six cases are also verified by exhaustive subset enumeration in `code/lemmaK.py`,
  output `out/lemmaK.txt`.)

**Corollary (lower bounds).** f(5) ≥ 9 (K2∨P3 = K5 − e), f(6) ≥ 12 (K2∨P4), f(7) ≥ 16
(K2∨C5), f(8) ≥ 19 (K2∨C6), f(9) ≥ 23 (K2∨θ(3,3,2)), f(10) ≥ 27 (K2∨K4*), by Lemmas 5–6;
edge counts 1+2·3+2, 1+2·4+3, 1+2·5+5, 1+2·6+6, 1+2·7+8, 1+2·8+10. Also K2∨C_m is P-free for
every m ≥ 5, so **f(n) ≥ 3n − 5 for all n ≥ 7** (proved; probably folklore-level, not
claimed new). Adding a vertex of degree 3 to a P-free graph keeps it P-free (Lemma 2: the new
vertex cannot lie in a 4-regular subgraph), so f(n+1) ≥ f(n) + 3.

**Lemma 7 (upper bounds, computational).**
(a) n = 5..8: `brute n m` enumerates all C(C(n,2), m) labelled graphs with m edges and
decides P by listing all Hamiltonian cycles of every G[S] (|S| ≥ 5, δ(G[S]) ≥ 4) as edge
bitmasks and testing all pairs. Output (`out/brute_small.txt`): for (n,m) = (5,10), (6,13),
(7,17), (8,20) the number of P-free graphs is 0 (of 1, 105, 5985, 3108105). By Lemma 1,
f(5) ≤ 9, f(6) ≤ 12, f(7) ≤ 16, f(8) ≤ 19. The same program gives the labelled P-free counts at
m = f(n): 10, 380, 252, 175560 (and 6368152 at (8,18)).
(b) n = 9, 10 via `gen.c` (Lemma 4) with t_10 = 24: max edges 23 at level 9 and 27 at level 10
(`out/run_n10.txt`); since f(9) ≥ 23 ≥ t_9 = 20 and f(10) ≥ 27 ≥ 24, f(9) ≤ 23 and f(10) ≤ 27.
(c) Independent re-derivation of (b) (`indep.py`, `out/indep.txt`):
  1. The 270 (resp. 12) 8-vertex classes with 18 (resp. 19) edges, taken from gen.c's dump,
     are each checked P-free by `pcheck.py` (explicit enumeration of all cycles, grouped by
     vertex set), pairwise non-isomorphic, and Σ 8!/|Aut| = 6368152 (resp. 175560) equals the
     brute-force labelled count. Since the orbits are disjoint subsets of the set of labelled
     P-free graphs and have the right total size, these lists are complete.
  2. f(9) ≤ 23: a P-free 9-vertex graph with 24 edges has min degree d ≤ ⌊48/9⌋ = 5 and
     24 − d ≤ f(8) = 19, so d = 5 and G − v is one of the 12 classes. All 12·C(8,5) = 672
     extensions have P.
  3. P-free 9-vertex graphs with 23 edges: d ≤ ⌊46/9⌋ = 5 and 23 − d ≤ 19, so G − v is a
     19-edge class with d = 4 or an 18-edge class with d = 5; of the 15960 extensions, the
     P-free ones form exactly 8 isomorphism classes.
  4. f(10) ≤ 27: a P-free 10-vertex graph with 28 edges has d ≤ 5 and 28 − d ≤ 23, so d = 5
     and G − v is one of those 8 classes; all 8·C(9,5) = 1008 extensions have P.

**Proof of the Theorem.** Combine the Corollary (lower bounds) with Lemma 7 (upper bounds). ∎

---

## Reproduce

```
cd attack/585/t1/prove/code
cc -O2 -o gen gen.c && cc -O2 -o brute brute.c
./gen 9 0 nofilter   > ../out/validate_nofilter_n9.txt     # canonical-form validation (A000088)
./gen 10 24          > ../out/run_n10.txt                  # f(5..10), extremal graphs (~45 s CPU)
./gen 11 30          > ../out/run_n11.txt                  # f(11) (~60 s CPU)
DUMP=1 ./gen 8 18    > ../out/dump_n8_ge18.txt
./brute 5 10; ./brute 6 13; ./brute 7 17; ./brute 8 20          # upper bounds (0 P-free)
./brute 5 9; ./brute 6 12; ./brute 7 16; ./brute 8 19; ./brute 8 18   # labelled counts
grep extremal ../out/run_n10.txt | awk '{print $4}' | sed 's/g6=//' | python3 -I pcheck.py
python3 -I orbitcheck.py ../out/run_n10.txt
python3 -I indep.py ../out/dump_n8_ge18.txt                 # ~4 min
python3 -I lemmaK.py ../out/run_n10.txt
```
Outputs: `out/run_n10.txt`, `out/run_n11.txt`, `out/brute_small.txt`, `out/extremal_pcheck.txt`,
`out/extremal_n11_pcheck.txt`, `out/orbitcheck_n10.txt`, `out/indep.txt`, `out/lemmaK.txt`,
`out/extremal_graphs_n5_10.txt` (graph6 of all extremal classes for n = 2..11).

## Attempted n = 12

`./gen 12 34` (t_11 = 29, t_10 = 24) was stopped by the 40-minute wall-clock cap during level 11
(`out/run_n12.txt`, exit=142 from the alarm). f(12) is not determined; f(12) ≥ f(11) + 3 = 34 is
known only conditionally on the single-source f(11) = 31 (unconditionally f(12) ≥ 3·12 − 5 = 31).

## Observations (INFERRED, not proved)

* Every n = 5..10 has an extremal graph of the form K2∨H. For those H,
  f(n) = 2n − 3 + h(n−2) where h(m) = max e(H) over m-vertex H satisfying Lemma 5's hypothesis
  (here h = 2, 3, 5, 6, 8, 10 for m = 3..8). Whether K2∨H stays optimal for larger n is unknown.
  This family is at most linear: applying the hypothesis to the 2-core Q of H (if nonempty) and
  noting that peeling degree-≤1 vertices removes ≤ 1 edge each, e(H) ≤ 2|Q| − 5 + (m − |Q|) ≤ 2m − 5,
  so e(K2∨H) ≤ 4n − 12 — far below the superlinear growth of f (PRS95).
* f(n) − (3n−6) = 0,0,1,1,2,3,(4) for n = 5..11.
* Every extremal graph found for n = 7..11 has two adjacent vertices of degree n−1 or n−2
  (seen in the listed degree sequences; not checked systematically).

## What this does and does not show

* It determines f(n) exactly for 5 ≤ n ≤ 10 (and, single-source, n = 11), with explicit
  extremal graphs and the full list of extremal graphs. Lower bounds are hand proofs; upper
  bounds are computer proofs, each confirmed by two independently written programs.
* It says nothing about the asymptotic question (n log log n ≪ f(n) ≤ n (log n)^{O(1)}); the
  small values are all ≤ 3n−3 and are dominated by sparse "apex" constructions irrelevant to
  the asymptotics.
* The computer-proof parts depend on the correctness of compiled C (gen.c, brute.c) and Python
  (pcheck.py, indep.py, networkx's isomorphism routines). No formal (Lean) verification.
* Novelty: no small values were found on erdosproblems.com/585 (0 comments), the Plasma page
  (which says no exact value found), or the OEIS; a full literature search was not done
  (see below). Exact small values of this extremal function may exist somewhere unnoticed.

## Sources read / not read

Read (VERIFIED): erdosproblems.com/585 and its forum thread (curl, 2026-11-23, `refs/`); Plasma
`wiki/problems/extremal_graph_theory/E0585/_index.md` (`refs/plasma_E0585.md`); formal-conjectures
origin/main has no `585.lean`; OEIS searches for 9,12,16,19,23,27,31 (only unrelated A053096) and
0,1,3,6,9,12,16,19,23,27 (no match).

Sources not read: [CJMM24] arXiv:2404.07190 and [PRS95] full texts; Erdős [Er76b]; ryantuck/erdos-ai;
any arXiv/Google Scholar search for small-case computations (an arXiv API query returned
nothing usable); House of Graphs.
