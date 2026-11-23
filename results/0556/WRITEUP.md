# Erdős #556, target A: R_3(C_10) <= 37. Attempted disproof; partial reduction

Outcome: **PARTIAL**. I found no counterexample, and I have no full proof. What is proved below is a
reduction: any counterexample would have to have a very specific structure (Theorem B).

## 0. Status check (done before starting)

- erdosproblems.com/556 (fetched 2026-11-23, `refs/page556.html`) says DECIDABLE, last edited 8 Feb 2026.
  The forum thread (`refs/forum556.html`) has two comments: Tao (1 Sep 2025, "reduced to a decidable
  one ... but remains open") and Kitamura (13 Jul 2026, n = 3 fails). Neither gives a value for n = 10.
- OEIS A389335 (`refs/oeis_A389335.txt`) lists R_3(C_n) only for n = 3..8: 17, 11, 17, 12, 25, 16.
- Plasma E0556 (`../../refs/plasma_E0556.md`): open, with no claim for n in the residue.
- Two web searches found no upper bound for R(C_10, C_10, C_10). The arXiv hits were 2603.10851,
  which covers complete graphs only, and 2611.11187, which covers the (t-1)-chromatic variant and
  gives only lower bounds for l >= 11.
- So as far as I checked, the target is not decided in the literature. The only route the scout
  found is the unpublished Afzaly–McKay table, which gives ex(27, C_10) = 111 < 117.

## 1. Disproof side (searching for a counterexample)

A 3-colouring of K_37 with no monochromatic C_10 needs every colour class to be C_10-free. One class
has at least 666/3 = 222 edges. So a counterexample needs a C_10-free graph on 37 vertices with at
least 222 edges. This is necessary but not sufficient.

- **Structured example (VERIFIED by exact computation).** Four copies of K_9 in a chain, plus a K_5,
  with consecutive blocks sharing a cut vertex (`out/E2_K9chain37.txt`). It has 37 vertices and 154
  edges, and its cycle lengths are 3..9 only (`out/E2_K9chain37_verify.txt`).
- **Random local search (heuristic).** `code/c10search.c` ran 8 seeds × 300 s of CPU time. It keeps
  the graph C_10-free with an exact path-of-length-9 test, adding and removing edges at random. The
  best edge counts per seed were 151, 151, 150, 151, 135, 150, 151 and 123 (`out/best37_seed*.txt`).
  Each best graph was re-checked as C_10-free by the separate exact checker (`out/best37_verify.txt`).
  All are below even the structured example's 154, and far below 222.
- **Afzaly–McKay table (unverified, not used in any proof).** ex(29, C_10) = 118 and
  ex(30..32, C_10) >= 123, 129, 136. Taken at face value, these put ex(37, C_10) far below 222.

Conclusion (INFERRED): a counterexample is extremely unlikely. I did not try to disprove further.

## 2. Proof side: what is proved

Notation: e(Y) is the number of edges inside Y, and e(X, Y) is the number of edges between X and Y.

**Claim T(n).** Every C_10-free graph on n vertices has at most 6(n-1) edges.

### Lemma 1 (pigeonhole)
T(37) implies R_3(C_10) <= 37.

*Proof.* K_37 has C(37,2) = 666 edges. In any 3-colouring, some colour class has at least 222 edges.
Since 222 > 216 = 6·36, T(37) says that class is not C_10-free. ∎

### Lemma 2 (minimal counterexample)
Suppose T(n) fails for some n <= 37. Let n be the least such value. Then there is a C_10-free graph G
on n vertices with the following properties:
- (a) e(G) = 6n - 5;
- (b) e(Y) <= 6(|Y| - 1) for every nonempty proper subset Y of V(G);
- (c) 13 <= n <= 37;
- (d) δ(G) >= 7;
- (e) for every nonempty proper subset X, e(X, V \ X) >= 7 (so G is 7-edge-connected);
- (f) G is 2-connected.

*Proof.*
- (a) Take a C_10-free G on n vertices with more than 6(n-1) edges. Deleting edges keeps it C_10-free,
  so we may delete edges until exactly 6(n-1) + 1 remain.
- (b) G[Y] is C_10-free on |Y| < n vertices, so T(|Y|) holds by minimality of n. (For |Y| = 1 the
  bound reads 0 <= 0.)
- (c) For n <= 12, C(n,2) = n(n-1)/2 <= 6(n-1), so T(n) holds trivially.
- (d) Apply (b) to Y = V - v: e(G) - deg(v) <= 6(n-2), so deg(v) >= 6n - 5 - 6n + 12 = 7.
- (e) e(X, V \ X) = e(G) - e(X) - e(V \ X) >= 6n - 5 - 6(|X| - 1) - 6(n - |X| - 1) = 7, using (b)
  twice.
- (f) G is connected by (e), and n >= 3. Suppose w is a cut vertex. Then V - w splits into nonempty
  sets A and B with no edges between them. So e(G) = e(A ∪ {w}) + e(B ∪ {w}). Both sets are proper,
  so by (b) e(G) <= 6|A| + 6|B| = 6(n-1) < 6n - 5. Contradiction. ∎

### Lemma 3 (a long cycle exists; CITED, not re-proved)
G has a cycle of length at least min(14, n) >= 13.

*Source.* This is Fan's theorem as quoted in arXiv:1609.03672, Theorem 5. Their reference [6] is
G. H. Fan, "New sufficient conditions for cycles in graphs", J. Combin. Theory Ser. B 37 (1984)
221–227. The quoted text reads:

> Let G be a 2-connected graph on n vertices. Furthermore, suppose that for all pairs of nonadjacent
> vertices v1 and v2 which have a common neighbor, at least one of them has degree at least c/2.
> Then c(G) >= min{c, n}.

pdftotext renders c/2 as "2c". The extracted text is in `refs/arxiv_1609.03672.pdf.txt`, lines
138–141.

Take c = 14. The hypothesis holds by Lemma 2(d) and 2(f).

I read only this secondary quotation, not Fan's paper. Two other classical results would also give a
cycle of length >= 11, but I did not check either against a source. One is Dirac's 1952 theorem. The
other is Erdős–Gallai: e > 4.5(n-1) gives a cycle of length >= 10, hence >= 11 here since G has no C_10.

### Lemma 4 (the shortest long cycle is short; full proof, no citations)
Let H be any C_10-free graph with δ(H) >= 7 and at most 37 vertices. Suppose H has a cycle of length
at least 11, and let L be the least length >= 11 of a cycle in H. Then L <= 15.

*Proof.* Suppose L >= 16, and let C = v_0 v_1 ... v_{L-1} be a cycle of length L. Indices are taken
mod L, and dist(i, j) means cyclic distance, which lies in [0, L/2].

By the choice of L and because H has no C_10, every cycle of H has length at most 9 or at least L.
Call this (★).

**(i) Chords.** Let v_i v_j be a chord with d = dist(i, j) >= 2. The chord and the longer arc form a
cycle of length L - d + 1, which lies in [L/2 + 1, L - 1]. By (★) this length is at most 9, so
d >= L - 8. Together with d <= L/2 this forces L <= 16. When L = 16 it forces d = 8, so each v_i has
at most one chord (to v_{i+8}). When L >= 17 there are no chords at all. In both cases each vertex of
C has at most one chord.

**(ii) Vertices off C.** Let x be a vertex not on C, adjacent to v_i and v_j with d = dist(i, j) >= 1.
The path v_i x v_j and the longer arc form a cycle of length L - d + 2.
- If d >= 3, this length is at most L - 1.
- Since d <= L/2 and L >= 16, the length is at least L/2 + 2 >= 10.

So d >= 3 would violate (★); hence d <= 2. All C-neighbours of x are therefore pairwise within cyclic
distance 2.

Fix one C-neighbour v_a of x. Every other C-neighbour has index in {a-2, ..., a+2}. Suppose the
indices a - k and a + k' (with k, k' >= 1) both occur. Their cyclic distance is k + k', because
k + k' <= 4 < L/2. So k + k' <= 2, which means k = k' = 1. Hence the C-neighbourhood of x lies in
{a-1, a, a+1}, {a, a+1, a+2} or {a-2, a-1, a}, and x has at most 3 neighbours on C.

**(iii) Counting.** Let R = V(H) \ V(C). Each v in C has degree >= 7. It has 2 neighbours along C and
at most 1 chord, so it has at least 4 neighbours in R. Hence e(C, R) >= 4L. By (ii), e(C, R) <= 3|R|.
So |R| >= 4L/3 >= 64/3, which gives |R| >= 22. Then |V(H)| >= L + 22 >= 38 > 37. Contradiction. ∎

`code/window_sizes.py` (output `out/window_sizes.txt`) independently recomputes the bound in (ii)
for every L from 11 to 37. For L >= 13 an off-C vertex has at most 3 neighbours on C; for L = 12 the
maximum is 4, and for L = 11 it is 5.

### Lemma 5 (n >= 25; uses CITED theorems)
In Lemma 2, n >= 25.

*Proof.* Suppose 13 <= n <= 24.

**Nonbipartite case.** Since n² - 26n + 29 <= 0 on [2, 24], we get 6n - 5 >= ⌊(n-1)²/4⌋ + 2.

Brandt's theorem (Discrete Appl. Math. 79 (1997) 63–66) says: a nonbipartite graph of order n with at
least ⌊(n-1)²/4⌋ + 2 edges is weakly pancyclic and has girth 3. "Weakly pancyclic" means it contains
a cycle of every length from the girth up to the circumference. I read this statement only as quoted
in arXiv:2601.15822 (Theorem 2, and "[3, Lemma 2]" for girth 3) and in arXiv:1609.03672 (Theorem 6),
not in Brandt's paper.

By Lemma 3 the circumference is at least 13. So G has cycles of every length from 3 to 13,
including 10. Contradiction.

**Bipartite case.** We need ab >= 6n - 5 where a + b = n and a <= b. Since ab <= n²/4, this requires
n² - 24n + 20 >= 0, which forces n = 24 within our range. Then ab >= 139, so (a, b) is (10, 14),
(11, 13) or (12, 12), with at most 1, 4 or 5 missing edges respectively. Remove from each side every
vertex that touches a missing edge. At least a - 5 >= 5 vertices remain on each side, and they span a
complete bipartite graph containing K_{5,5}, which contains C_10. Contradiction. ∎

### Theorem B (the statement established)
Suppose R_3(C_10) > 37. Then there is a C_10-free graph G with 25 <= n <= 37 vertices and the
following properties:
- e(G) = 6n - 5;
- e(Y) <= 6(|Y| - 1) for every nonempty proper subset Y;
- δ(G) >= 7, G is 2-connected and G is 7-edge-connected;
- G has a cycle of length >= 13, and the least length >= 11 of a cycle in G lies in {11, ..., 15};
- consequently, every cycle of G has length <= 9 or >= L, where L is that least length.

*Proof.* By Lemma 1, T(37) fails. Lemma 2 then gives G, Lemma 3 gives the long cycle, and Lemmas 4
and 5 give the rest.

The lower bound 25 <= n depends on the cited Brandt and Fan theorems. Without them, the same
statement holds with 13 <= n <= 37, provided a cycle of length >= 11 exists; that existence still
needs Lemma 3 or Erdős–Gallai. ∎

## 3. What blocks a full proof (INFERRED analysis)

1. **Degree and connectivity alone cannot work (VERIFIED example E1).** `out/E1_bead31.txt` (built by
   `code/make_bead_graph.py`) is built from C_11 with four "beads". Each bead is a K_5 completely
   joined to a window of three consecutive cycle vertices: {0,1,2}, {3,4,5}, {6,7,8} and {9,10,0}.
   Exact check (`out/E1_bead31_verify.txt`): n = 31, 111 edges, δ = 7, 2-connected, cycle lengths
   {3..8} ∪ {11..20}. So it has no C_10 and its shortest long cycle has length L = 11.
   Any proof of T(37) must therefore use edge density, not just δ >= 7 and n <= 37. E1 breaks
   Lemma 2(b): for a bead D, e(D) + e(D, V \ D) = 25 < 31.
2. **The case L in {11, ..., 15} is open.** Counting edges at C (Lemma 2(b) with Y = V \ V(C)) gives
   chords + e(C, R) >= 5L + 1. This is not a contradiction for L <= 15. For example, an L = 11
   configuration with 26 outside vertices meets it. Closing this case seems to need density bounds
   for the local pieces near C that beat the inductive constant 6. The true constant is about 4.5,
   as for K_9-chains. I could not prove such bounds.
3. **SAT/CEGAR by brute force is far too slow.** `code/lazysat_probe.py` encodes "C_10-free,
   δ >= 7, at least 6n - 5 edges" with CaDiCaL and adds 10-cycle clauses lazily. It shows n = 13 UNSAT
   in 0.2 s, but did not finish n = 14 or n = 15 within about 5 minutes. The
   minimal-counterexample induction also cannot be run with a linear threshold c(m - 1) at the
   scout's m = 27. The chain of three K_9's sharing cut vertices is C_10-free with 108 = 4.5·24
   edges on 25 vertices, so any threshold that is valid at m = 25 needs c >= 4.5. But
   c(27 - 1) <= 116 needs c <= 116/26 < 4.5. With m = 37 and c = 6 the induction does go through
   (Lemma 2), which is why the reduction targets T(37).

## 4. What this does and does not show

- **Does show** (rigorous, with the citations noted): R_3(C_10) <= 37 reduces to excluding one kind of
  graph. That graph is C_10-free, on 25–37 vertices, sparse on every proper subset, has exactly
  6n - 5 edges, minimum degree >= 7, and is 2-connected. Its shortest cycle of length >= 11 has
  length 11–15. The part "L <= 15" (Lemma 4) is fully proved here with no citations.
- **Does show:** that minimum degree, connectivity and order alone cannot settle the question
  (example E1, verified exactly).
- **Does not show** R_3(C_10) <= 37, or any finite upper bound on R_3(C_10) independent of the
  literature.
- **Does not** independently certify the Afzaly–McKay values.
- The disproof search is heuristic evidence only. Nothing was found anywhere near 222 edges.

## 5. Reproduce

All commands are run from this folder (`.../attack/556/t1/disprove`).

```
cc -O2 -o code/verify_graph code/verify_graph.c
python3 code/make_bead_graph.py out/E1_bead31.txt && code/verify_graph out/E1_bead31.txt 20
code/verify_graph out/E2_K9chain37.txt 12
python3 code/window_sizes.py
cc -O2 -o code/c10search code/c10search.c && code/c10search 37 300 <seed> out/best37_seed<seed>.txt
python3 code/lazysat_probe.py 13     # needs python-sat; n=13 UNSAT in ~0.2 s
```

`verify_graph` was sanity-checked on K_9 (lengths 3–9), K_10 (3–10), K_{5,5} (4, 6, 8, 10) and
K_{4,9} (4, 6, 8). The test files are `out/test_*.txt`.

## 6. Sources not read

- The primary papers of Brandt (1997), Fan (1984), Dirac (1952) and Erdős–Gallai (1959). Only the
  secondary quotations named above were read.
- Afzaly–McKay's computation itself. Only the scout's saved web table was used, and only as context.
- Radziszowski DS1 rev. 18: relied on the scout's VERIFIED summary; not re-read here.
- Benevides–Skokan, Łuczak, KSS05 and the 2-colour Ramsey literature on even cycles were not needed
  and were not read.
