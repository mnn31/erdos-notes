# Erdős #1011: the exact value g(6) = 12

Folder: `attack/1011/t1/prove/`
(code in `code/`, outputs in `out/`, downloaded pages in `refs/`).

## Statement established

Let g(r) be the least m such that some triangle-free graph G with chi(G) >= r becomes
bipartite after deleting m vertices. (This is the erdosproblems.com g(r), "the largest m
such that for any triangle-free graph with chromatic number >= r, at least m vertices of G
need to be removed to obtain a bipartite graph"; the two descriptions give the same number.)
Write oct(G) for the least number of vertices whose deletion leaves G bipartite, and
h(k) for the least order of a triangle-free graph with chi >= k.

**Theorem A (all r >= 3, hand proof).** h(r-2) <= g(r) <= h(r-2) + 1.

**Theorem B (computer-assisted).** g(6) = 12.

Theorem B uses one computed fact (Lemma 5): the only triangle-free graph on at most 11
vertices with chi >= 4 is the Grötzsch graph, up to isomorphism. This is also a classical
theorem (Chvátal 1974), but I did not read that paper, so the proof here rests on the
enumeration in Lemma 5. Every other step is proved by hand below and also checked by computer.

**Witness for g(6) <= 12.** The Mycielski graph M_6 = M(M(Grötzsch)) has 47 vertices and
236 edges. It is triangle-free, has chi = 6, and becomes bipartite after deleting 12
explicit vertices (Lemma 2).

Conditional corollary. Simonovits ([Si74], Thm 2.7, as quoted on erdosproblems.com; I did not
read it) gives f_r(n) = n^2/4 - g(r) n/2 + O(1). With Theorem B this gives
f_6(n) = n^2/4 - 6n + O(1). This depends on Simonovits's statement, which has no printed proof.

---

## Definitions and conventions

Graphs are finite and simple. N(v) is the neighbourhood of v. A set is independent if it
contains no edge. "G - S bipartite with parts A, B" means V(G) \ S = A ⊔ B with A and B
independent. A proper k-colouring is a map V -> {0,...,k-1} with different colours at the
ends of every edge.

**Mycielskian.** For a graph F, M(F) has vertex set V(F) ∪ {x' : x in V(F)} ∪ {w}. Its edges
are: every edge of F; x' ~ y whenever xy is an edge of F; and w ~ x' for every x. There are no
other edges. In particular, the copies x' form an independent set, and w is adjacent to
nothing in V(F).

**Grötzsch graph Gr = M(C5)**, labelled as in `code/gstar.py`: outer cycle 0-1-2-3-4-0;
copy 5+i adjacent to i-1 and i+1 (mod 5); hub 10 adjacent to 5,...,9. (Computer check:
11 vertices, 20 edges, triangle-free, chi = 4, isomorphic to networkx `mycielski_graph(4)`;
`out/verify_main.out`.)

---

## Lemma 1 (Mycielski). If F is triangle-free with chi(F) = k, then M(F) is triangle-free and chi(M(F)) = k + 1.

*Proof.* Triangle-free. Suppose T is a triangle in M(F). Since the copies form an
independent set, T contains at most one copy. If T contains w, then its other two vertices
are neighbours of w, so both are copies. That is impossible, so w is not in T. If T contains
no copy, it is a triangle of F, which is impossible. So T = {x', y, z} with y, z in V(F) and
yz an edge. Then x' ~ y and x' ~ z mean xy and xz are edges of F, so {x, y, z} is a triangle
in F (x differs from y and z because F has no loops). Contradiction.

chi <= k+1. Take a proper k-colouring c of F. Give each x' the colour c(x), and give w the
new colour k. An edge x'y comes from an edge xy of F, so c(x) != c(y). The edges at w join
colour k to colours below k. Edges inside F are proper by assumption.

chi >= k+1. Suppose c is a proper k-colouring of M(F), and rename the colours so that
c(w) = k-1. Every copy is adjacent to w, so c(x') <= k-2 for all x. Define c' on V(F) by
c'(x) = c(x) if c(x) != k-1, and c'(x) = c(x') otherwise. Then c' uses only the colours
0..k-2. It is proper: let xy be an edge of F. The case c(x) = c(y) = k-1 cannot happen. If
neither is k-1, then c'(x) = c(x) != c(y) = c'(y). If c(x) = k-1 != c(y), then
c'(x) = c(x'), and x' ~ y gives c(x') != c(y) = c'(y). So chi(F) <= k-1, a contradiction. ∎

## Lemma 2 (deleting |H|+1 vertices makes the double Mycielskian bipartite). Let H be any graph, M1 = M(H) with hub w1, and M2 = M(M1) with hub w2. Write x* for the copy in M2 of a vertex x of M1. Let S = V(H) ∪ {w2}. Then M2 - S is bipartite with parts X = {w1, w1*} ∪ {h* : h in V(H)} and Y = {h' : h in V(H)} ∪ {(h')* : h in V(H)}.

*Proof.* The vertices of M2 are V(M1) ∪ {x* : x in V(M1)} ∪ {w2}, and
V(M1) = V(H) ∪ {h'} ∪ {w1}. Removing S leaves exactly X ∪ Y, and X and Y are disjoint.
We list every edge of M2 that has both ends outside S, and check that each one joins X to Y.

(i) Edges inside M1 avoiding V(H). In M1 the copies h' are adjacent only to vertices of
V(H) and to w1. The hub w1 is adjacent only to copies. So the only such edges are h'w1
(Y to X).

(ii) Edges inside M2 between two starred vertices: none, since the copies of M2 are independent.

(iii) Edges x* ~ y with y in V(M1) \ V(H). By definition x* ~ y iff xy is an edge of M1.
For x = h in V(H): the M1-neighbours of h outside V(H) are the copies u' with u ~ h in H.
These give edges h* u' (X to Y). For x = h': the M1-neighbours of h' outside V(H) are just
w1. This gives (h')* w1 (Y to X). For x = w1: the M1-neighbours of w1 are all the copies u',
giving w1* u' (X to Y).

(iv) Edges at w2: w2 is in S.

So every edge of M2 - S joins X to Y, and X, Y are independent in M2 - S. ∎

(Computer check for H = Gr, K2, C5: `out/verify_main.out`. For H = Gr the explicit X, Y
form a proper bipartition of the 35 remaining vertices.)

## Lemma 3 (a colouring criterion). Let G be triangle-free and S ⊆ V(G) with G - S bipartite, with parts A, B. Suppose G[S] has a proper k-colouring κ in which no independent set of G[S] meets all k colour classes. Then chi(G) <= k + 1.

*Proof.* For b in B, the set N(b) ∩ S is independent in G[S]: an edge st inside it would
make b, s, t a triangle. By hypothesis this set misses some colour γ(b) in {0..k-1}. Colour
G by: s -> κ(s) for s in S; b -> γ(b) for b in B; a -> k for a in A. Check every edge type:
S–S edges are proper because κ is proper. A–A and B–B edges do not exist (A and B are
independent). A–S and A–B edges join colour k to a colour <= k-1. For a B–S edge bs, we have
s in N(b) ∩ S, so κ(s) != γ(b) by the choice of γ(b). So the colouring is proper and uses
k+1 colours. ∎

## Lemma 4 (the Grötzsch graph has a 4-colouring with no rainbow independent set). Let κ(0..4) = 0,1,0,1,2, κ(5+i) = κ(i) for i = 0..4, and κ(10) = 3. Then κ is a proper 4-colouring of Gr, and no independent set of Gr meets all 4 colour classes.

*Proof.* Proper. On the cycle the edges 01, 12, 23, 34, 40 get the colour pairs (0,1),
(1,0), (0,1), (1,2), (2,0). The copy 5+i is adjacent to i-1 and i+1, which are cycle
neighbours of i, so their colours differ from κ(i) = κ(5+i). The hub has colour 3 and its
neighbours 5..9 have colours <= 2. Gr has no other edges.

No rainbow independent set. The hub 10 is the only vertex of colour 3, so an independent set
I that meets every class contains 10. The non-neighbours of 10 are exactly 0,1,2,3,4, so
I ⊆ {10} ∪ {0,...,4}. The set I ∩ {0,...,4} is independent in the 5-cycle, so it has at most
2 vertices. Hence |I| <= 3 and I meets at most 3 colours. Contradiction. ∎

(Computer check: all 103 independent sets of Gr listed; none is rainbow; `out/verify_main.out`.)

## Lemma 5 (computed). Up to isomorphism, every triangle-free graph on at most 11 vertices is 3-colourable, except the Grötzsch graph on 11 vertices.

*Method (`code/tfenum.py`).* Generation step: if F is triangle-free on n vertices and v is a
vertex of F, then F - v is triangle-free and N(v) is independent in F - v. So F is isomorphic
to R + v, where R is any graph isomorphic to F - v, and v is joined to the image of N(v),
which is an independent set of R. So, starting from the list of all triangle-free graphs on
n-1 vertices up to isomorphism, the graphs R + (vertex joined to I), over all
representatives R and all independent sets I of R, include every triangle-free graph on n
vertices. Levels n = 2..10 are deduplicated exactly. Graphs are bucketed by an isomorphism
invariant (degree sequence and a WL hash) and compared with networkx VF2 `is_isomorphic`
inside each bucket. The hash only splits graphs into buckets; it never decides that two
graphs are equal. Every candidate at every level n <= 11 goes through an exact backtracking
3-colouring search. Each "3-colourable" verdict is certified: the colouring found is
re-checked edge by edge (assert). The non-3-colourable candidates are collected and
deduplicated.

*Output (`out/tfenum.out`).* Distinct triangle-free graphs on n = 1..10 vertices:
1, 2, 3, 7, 14, 38, 107, 410, 1897, 12172. These agree with OEIS A006785 (`refs/oeis_A006785_b.txt`),
which is an independent check that the enumeration is complete. There are no
non-3-colourable graphs for n <= 10. At n = 11, all 1,506,339 candidates were tested.
Exactly one isomorphism class is non-3-colourable: 20 edges, isomorphic to Gr (saved in
`out/noncol3.json`). The proof does not need deduplication at n = 11, because every
candidate there is tested. An optional full deduplication at n = 11 (`--full`) was meant
to recheck the count 105071, but in pure Python it hit the 40-minute cap and was stopped
(`out/tfenum_full.out`). That count check was NOT done.

*What this relies on.* The generation step (proved above), the correctness of networkx
VF2 at levels <= 10 (cross-checked by the OEIS counts), and the correctness of the 3-colouring
search when it answers "no". A wrong "no" could only add graphs to the kept list, and the
kept list contains only Gr, which really has chi = 4 by Lemma 1 (Gr = M(C5)). A wrong "yes"
is ruled out by the certificate check. So the only uncertified part is the deduplication
at levels <= 10, which the OEIS counts corroborate.

## Theorem A. For every r >= 3, h(r-2) <= g(r) <= h(r-2) + 1.

*Proof.* Lower bound (this is the forum observation attributed to Z. Hunter, reproved here).
Let G be triangle-free with chi(G) >= r, and let S be a set with G - S bipartite. Colouring
G[S] with chi(G[S]) colours and G - S with 2 new colours gives chi(G) <= chi(G[S]) + 2. So
chi(G[S]) >= r-2, and G[S] is triangle-free, so |S| >= h(r-2). Hence g(r) >= h(r-2).

Upper bound. Let H0 be triangle-free with chi(H0) = k >= r-2 on h(r-2) vertices. Applying
Lemma 1 twice, M2 = M(M(H0)) is triangle-free with chi(M2) = k+2 >= r. By Lemma 2, deleting
h(r-2) + 1 vertices of M2 leaves a bipartite graph. So g(r) <= h(r-2) + 1. ∎

## Theorem B. g(6) = 12.

*Proof.* Upper bound. Apply Lemmas 1 and 2 to H0 = Gr (chi(Gr) = 4 by Lemma 1, since
Gr = M(C5) and chi(C5) = 3). M(M(Gr)) is triangle-free, has chi = 6, and becomes bipartite
after deleting the 12 vertices V(Gr) ∪ {w2}. So g(6) <= 12.

Lower bound. Let G be triangle-free with chi(G) >= 6, and suppose G - S is bipartite with
|S| <= 11, with parts A, B. As in Theorem A, chi(G[S]) >= 4. G[S] is triangle-free on at most
11 vertices, so by Lemma 5 G[S] is isomorphic to Gr (in particular |S| = 11). Pull the
colouring κ of Lemma 4 back to G[S] through such an isomorphism. Independent sets
correspond under the isomorphism, so no independent set of G[S] meets all 4 colour classes.
Lemma 3 with k = 4 then gives chi(G) <= 5, a contradiction. So every triangle-free G with
chi >= 6 has oct(G) >= 12, which means g(6) >= 12. ∎

**Computer corroboration of the upper bound.** M(M(Gr)) as built in `code/verify_main.py`
has 47 vertices and 236 edges. It is triangle-free and isomorphic to networkx
`mycielski_graph(6)`. CaDiCaL reports it not 5-colourable, and it finds a 6-colouring,
which was re-checked. Deleting the 12 vertices gives the explicit bipartition (all in
`out/verify_main.out`). The non-5-colourability is proved by Lemma 1; the SAT run is only a
cross-check.

---

## Consistency checks

- The same two-sided argument gives g(4) = 3 and g(5) = 6, matching the known values
  (RWWY24 for f_4, which gives g(4) = 3; Kitamura's Lean-checked f_5 claim, which gives
  g(5) = 6). Lower bounds: for r = 4, the only triangle-free graph on <= 2 vertices with
  chi >= 2 is K2. For r = 5, the only one on <= 5 vertices with chi >= 3 is C5: it must
  contain an odd cycle, which has length 5 because there are no triangles, and any chord of
  a 5-cycle makes a triangle. K2 coloured 0,1 and C5
  coloured 0,1,0,1,2 have no rainbow independent set (independent sets have size <= 1,
  respectively <= 2, which is less than the number of colours). Upper bounds:
  M(M(K2)) = Gr becomes bipartite after deleting 3 vertices, and M(M(C5)) (23 vertices) after
  deleting 6. Computer checks are in `out/verify_main.out`.
- The scout's reduction (G*(H), `code/gstar.py`) agrees. The rule-based 5-colouring of
  G*(Gr) from Lemmas 3 and 4 (a_I -> 4, b_J -> least colour missing from J, H -> κ) is
  proper by computer check. Also, M(M(Gr)) with S = V(Gr) ∪ {w2} has G[S] = Gr + K1 (w2 has
  no neighbour in V(Gr)), so the scout's homomorphism gives chi(G*(Gr + K1)) >= 6 by hand.
  This explains the scout's CaDiCaL UNSAT result without needing a DRAT certificate.
- Exploration only, not used in any proof (`out/plus_k1_test.out`): for 12 small triangle-free H,
  chi(G*(H + K1)) >= chi(H) + 2, which is consistent with Lemma 2. A 60-vertex induced
  subgraph of G*(Gr + K1) that is not 5-colourable was found by core-guided shrinking
  (`out/shrink.out`, `out/critical_W.json`). It is superseded by M_6.

## Reproduce

```
cd attack/1011/t1/prove/code
python3 -I tfenum.py ../out/noncol3.json            # Lemma 5, about 5 min -> out/tfenum.out
python3 -I tfenum.py ../out/noncol3_full.json --full # optional n = 11 count check; did not finish in 40 min
python3 verify_main.py                               # Lemmas 1-4, Thm B checks -> out/verify_main.out
python3 plus_k1_test.py                              # exploration only
python3 shrink.py ../out/critical_W.json             # exploration only
python3 colour_groetzsch.py ../out/gstar_groetzsch_5col.json  # SAT 5-colouring of G*(Gr), exploration only
```
(`verify_main.py`, `plus_k1_test.py` and `shrink.py` import pysat from the user
site-packages, so they are run without `-I`. They read no external data.)

## What this does and does not show

Shows (VERIFIED):
- Theorem A, h(r-2) <= g(r) <= h(r-2)+1 for every r >= 3, by a complete hand proof
  (Lemmas 1, 2). So g(r) is determined by h(r-2) up to an additive 1.
- g(6) = 12. The upper bound is pure hand proof (witness M_6, 47 vertices, oct <= 12, chi = 6).
  The lower bound is a hand proof (Lemmas 3, 4) plus the computed Lemma 5 (Grötzsch is the
  unique triangle-free graph on <= 11 vertices with chi >= 4). Lemma 5 is also a classical
  theorem (Chvátal 1974), which I did not read.

Does not show:
- Anything about f_6(n) beyond the conditional corollary. The expansion
  f_r(n) = n^2/4 - g(r)n/2 + O(1) is Simonovits's statement, which I did not read and which
  has no printed proof per the Plasma page. The O(1) term of f_6 and any exact formula for
  f_6(n) remain open.
- g(7). Theorem A gives g(7) in {h(5), h(5)+1}. If h(5) = 22 (Jensen–Royle 1995, NOT verified
  here), then g(7) is 22 or 23. Deciding it would need every triangle-free 5-chromatic graph
  on 22 vertices and Lemma 3's criterion, or the G*(H) test, for each.
- Novelty is not certified. The double-Mycielski bound g(r) <= h(r-2)+1 is short, and
  Simonovits (thesis or [Si74]) may contain it. erdosproblems.com, its forum thread, the
  Plasma E1011 page, ryantuck/erdos-ai (1011 files) and some arXiv API keyword searches
  (`refs/arxiv_search.txt`) do not mention it or the value g(6).
- The one uncertified computational step is the exact deduplication at levels <= 10
  (networkx VF2). It is corroborated by the OEIS A006785 counts and by Chvátal's theorem as
  usually cited.

## Sources not read
- [Si74] M. Simonovits, Extremal graph problems with symmetrical extremal graphs, additional
  chromatic conditions, Discrete Math. 7 (1974) 349–376 (Theorem 2.7, Remark 2.8), and
  Simonovits's PhD thesis.
- V. Chvátal, The minimality of the Mycielski graph (1974): the uniqueness of Grötzsch as
  the smallest triangle-free 4-chromatic graph. Replaced here by Lemma 5.
- T. Jensen, G. Royle, Small graphs with chromatic number 5: a computer search (1995): h(5) = 22.
- RWWY24 (Ren, Wang, Wang, Yang) and Kitamura's erdos-1011-lean repository: used only through
  the erdosproblems.com, forum and Plasma summaries for g(4) = 3 and g(5) = 6.
- Davies–Illingworth [DaIl22] and Hefty–Horn–King–Pfender [HHKP25]: not needed.
