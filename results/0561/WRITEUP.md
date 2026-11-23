# Erdős #561, target T1: six small open star-forest instances (computer-assisted)

Date: 2026-11-23. Folder: `attack/561/t1/prove`.

## 0. Statement established

Write `(n_1,...,n_s)` for the star forest `K_{1,n_1} ⊔ ... ⊔ K_{1,n_s}`, and `r̂(F1,F2)` for the least
number of edges of a graph H with `H → (F1,F2)`, meaning every red/blue colouring of E(H) has a red F1 or a
blue F2.

**Theorem (computer-assisted).** The Burr–Erdős–Faudree–Rousseau–Schelp value `Σ_{k=2}^{s+t} l_k`,
`l_k = max{n_i + m_j − 1 : i + j = k}`, is the true size Ramsey number for these six pairs:

| F1 | F2 | l_k | r̂(F1,F2) |
|---|---|---|---|
| (2,2,1) = 2K_{1,2} ⊔ K_2 | (2,1,1) = K_{1,2} ⊔ 2K_2 | 3,3,2,2,1 | **11** |
| (2,2,1) | (2,2,1) | 3,3,3,2,1 | **12** |
| (2,1,1) | (2,2,1,1) | 3,3,2,2,1,1 | **12** |
| (3,2,1) | (2,1,1) | 4,3,3,2,1 | **13** |
| (2,2,2) | (2,1,1) | 3,3,3,2,2 | **13** |
| (2,2,1) | (2,1,1,1) | 3,3,2,2,2,1 | **13** |

So none of these six instances is a counterexample to Problem 561.

**Additional result: sweep.** The same holds for **every** pair of star forests with conjectured value
`Σ l_k ≤ 13` (787 pairs up to swapping the colours, 786 of them non-trivial). It also holds for the 11 value-14
pairs in which both forests have ≥ 3 stars and neither is a matching. These include the smallest
instance of the scout's target T2: r̂(K_{1,3} ⊔ 3K_2, K_{1,2} ⊔ 2K_2) = 14. See §5.

The proof is computer-assisted. The upper bound is a short proof (Lemma 3). The lower bound is a finite
check: for each graph with `value − 1` edges, a colouring with no red F1 and no blue F2 was found, and a
second, independent program re-checked every such colouring. That the graph lists are complete is shown
by matching the OEIS counts (Lemma 5).

## 1. Status check (done before investing)

- erdosproblems.com/561 (fetched 2026-11-23, `refs/page561.html`): open; page last edited 01 Feb 2026;
  it lists BEFRS78, GySc02 and DJKR25 only. VERIFIED by reading.
- Forum thread (`refs/forum561.html`): 5 comments. One is the Cipollini partial lower bound (the
  `Σ l_k − Σ η_k` argument). The others are an FLN26 report and a reply saying ChatGPT found serious
  gaps in it, plus two site-maintenance notes. None computes any instance. VERIFIED by reading.
- Plasma page `wiki/problems/ramsey_theory/E0561/_index.md` (`refs/plasma_index.md`): `status: open`,
  `updated: 2026-10-29`. The newest repository commit touching the folder (2026-11-16) only rewords the
  statement (two-graph size Ramsey number). It has no small-case computations. VERIFIED by reading the
  diff.
- arXiv: my API query returned HTTP 429 (rate limited), so I did not repeat the scout's arXiv search.
  See "Sources not read".

## 2. Lemmas

Throughout, star forests have every star with at least one edge, and a "copy" means a subgraph, not
necessarily induced.

**Lemma 1 (monotonicity).** If `H → (F1,F2)` and H is a subgraph of H', then `H' → (F1,F2)`.

*Proof.* Take a colouring c' of H'. Its restriction c to E(H) is a colouring of H, so it has a red F1 or a
blue F2 made of edges of H. Those edges have the same colours under c', so the same copy is in H'. ∎

**Lemma 2 (reduction to exactly N edges, no isolated vertices).** Let N ≥ 1. If some graph with at
most N edges arrows (F1,F2), then some graph with exactly N edges and no isolated vertices arrows
(F1,F2).

*Proof.* Let H arrow the pair with e(H) ≤ N edges. Since F1 and F2 have edges, e(H) ≥ 1 (with no edges
the empty colouring has neither copy). Deleting isolated vertices changes neither the set of
colourings nor any copy (a copy of a forest without isolated vertices uses no isolated vertex of H), so
the result H₀ still arrows. Add `N − e(H₀)` new pairwise vertex-disjoint edges on new vertices. This
gives H₁ ⊇ H₀ with exactly N edges and no isolated vertices, and H₁ arrows by Lemma 1. ∎

So `r̂(F1,F2) ≥ v` follows once every graph with exactly v − 1 edges and no isolated vertices,
taken up to isomorphism, has a colouring with no red F1 and no blue F2. Arrowing is invariant under
isomorphism.

**Lemma 3 (upper bound; the standard construction, re-proved here).** Let `n_1 ≥ ... ≥ n_s`,
`m_1 ≥ ... ≥ m_t` and `U = ⊔_{k=2}^{s+t} K_{1,l_k}`. Then `U → (F1,F2)`, so `r̂(F1,F2) ≤ Σ l_k`.

*Proof.* Fix a colouring of U, and let c_k be the centre of the k-th star, with r_k red and b_k blue
edges, `r_k + b_k = l_k`. Process k = 2, 3, ..., s+t in order, keeping two counters i and j that start at
(i,j) = (1,1). The invariant is i + j = k when star k is processed. We also keep a red copy of
`K_{1,n_1} ⊔ ... ⊔ K_{1,n_{i−1}}` and a blue copy of `K_{1,m_1} ⊔ ... ⊔ K_{1,m_{j−1}}`, using only stars
2..k−1, at most one copy-star per star of U.

- If i = s+1, the red copy is a red F1 and we stop. If j = t+1, we likewise have a blue F2.
- Otherwise 1 ≤ i ≤ s, 1 ≤ j ≤ t and i + j = k. By the definition of `l_k`,
  `l_k ≥ n_i + m_j − 1`. Then `r_k ≤ n_i − 1` and `b_k ≤ m_j − 1` cannot both hold, because they would
  give `l_k ≤ n_i + m_j − 2`. If r_k ≥ n_i, take n_i red edges at c_k as the red K_{1,n_i} and set
  i ← i+1. Otherwise b_k ≥ m_j: take a blue K_{1,m_j} and set j ← j+1. Either way i + j goes up by 1,
  so the invariant holds for k+1. The new star lies in a component of U not used before, so the copies
  stay vertex-disjoint.

After the last star (k = s+t), i + j = s+t+1. With i ≤ s+1 and j ≤ t+1, this forces i = s+1 or
j = t+1. So a red F1 or a blue F2 has been built. ∎

The code also checks Lemma 3 directly, by exhausting all colourings, for every instance it runs
(`star union arrows: total 1 arrowing 1` in every log).

**Lemma 4 (colour symmetry).** `r̂(F1,F2) = r̂(F2,F1)`.

*Proof.* Swapping the two colours maps the colourings of H bijectively onto themselves and turns a red F1
or blue F2 into a blue F1 or red F2. ∎

The sweep therefore lists each unordered pair once.

**Lemma 5 (the graph lists are complete).** For e = 1, ..., 13, the file `out/graphs/g{e}.txt` has
exactly one graph from each isomorphism class of graphs with e edges and no isolated vertices.

*Proof.* (a) *Every line is such a graph.* `code/check_graph_files.py` checks that each line has e
distinct edges, no loops, and vertex labels exactly {0, ..., n−1}, so there are no isolated vertices
(`out/graph_files_check.txt`: `wellformed=True` for every e).

(b) *Pairwise non-isomorphic.* The generators (`code/gen.py` for e ≤ 12, `code/gen_next.py` for e = 13)
group candidates by a key that is an isomorphism invariant: the networkx Weisfeiler–Lehman hash with 4
iterations, plus the sorted degree sequence. Graphs with different keys are therefore non-isomorphic.
Inside a group, a candidate is kept only if networkx's exact VF2 test `is_isomorphic` finds it
non-isomorphic to every graph already kept. So the kept graphs are pairwise non-isomorphic.

(c) *Count.* The number of lines equals the OEIS A000664 value (number of graphs with e edges and no
isolated vertices) for every e ≤ 13: 1, 2, 5, 11, 26, 68, 177, 497, 1476, 4613, 15216, 52944, 193367
(`refs/b000664.txt`; `out/graph_files_check.txt`: `MATCH` for every e).

By (b) the lines represent distinct classes. By (c) there are as many lines as classes. So every class is
represented.

Independently of OEIS, the generation scheme is complete. If G has e ≥ 2 edges and no isolated vertices,
delete any edge xy and then any vertices left isolated. The result P has e−1 edges and no isolated
vertices, so (by induction) it is isomorphic to a listed graph P'. G is obtained from P by adding an edge
of one of three kinds: between two non-adjacent vertices of P, from a vertex of P to a new vertex, or
between two new vertices. The generator tries all three kinds on P', so a graph isomorphic to G is a
candidate. Exact VF2 deduplication never removes the last representative of a class. ∎

**Lemma 6 (certificates).** Fix (F1,F2) with value v. Suppose that for every line of
`out/graphs/g{v−1}.txt` a colouring is recorded that has no red F1 and no blue F2. Then
`r̂(F1,F2) ≥ v`.

*Proof.* By Lemma 5 every graph with v−1 edges and no isolated vertices is isomorphic to a listed graph,
so it does not arrow. By Lemma 2 no graph with ≤ v−1 edges arrows. ∎

How the certificates are produced and checked:

- `code/arrow.c` tries the colourings of each graph in order (bit i of the mask set means edge i is
  red) and stops at the first one with neither copy. Containment of a star forest is decided by
  exhaustive backtracking: choose a centre, choose a leaf set among its unused neighbours, recurse. The
  only pruning is two exact facts. (i) A forest with Σ sizes edges needs at least that many edges of the
  colour. (ii) Stars of equal size are interchangeable, so their centres can be taken in increasing
  order. The first colouring found is written to a witness file (`*_witnesses.tsv`: mask, tab, edge
  list).
- `code/verify_witness.py` re-checks every witness with a different algorithm. It enumerates the centres
  of the stars with ≥ 2 leaves and decides their leaves by bipartite b-matching (augmenting paths). The
  single-edge components are then found by a maximum matching (Edmonds' blossom algorithm, networkx)
  on the rest of the graph. It reports `bad 0` in every run. I tested its containment routine against
  plain brute force on 3000 random graphs with up to 9 vertices and random forests: 0 mismatches.
- `code/arrow.c` was also cross-checked against the scout's independent Python checker
  (`attack/561/code/arrow.py`). On all graphs with e edges, for 9 pairs, the two programs gave exactly
  the same set of arrowing graphs. This includes 5 cases where the set is non-empty
  (`out/crosscheck_scout.txt`, `AGREE` on every line).

A good colouring is a finite certificate. Lemma 6 therefore depends only on Lemma 5 and on the
correctness of `verify_witness.py` (or, independently, of `arrow.c`). Each was tested as above.

**Lemma 7 (a human-checkable partial argument, for (2,2,1) vs (2,1,1)).** Let G have 10 edges. Suppose
two vertices u, v together meet at least 6 edges. Then G does not arrow ((2,2,1),(2,1,1)).

*Proof.* Colour blue every edge meeting {u,v}, and the others red. Each component of a blue star forest
contains a blue edge, and each blue edge meets {u,v}. Disjoint components therefore need distinct
vertices of {u,v}, so the blue graph contains no star forest with 3 components, and in particular no
blue (2,1,1). The red graph has at most 10 − 6 = 4 edges. But (2,2,1) has 5 edges, so there is no red
F1. ∎

By computation (`code/cover_lemma.py`, `out/cover_lemma.txt`), Lemma 7 handles 3992 of the 4613
ten-edge graphs, and the independent verifier confirms its explicit colouring on all 3992. The other
621 graphs are handled only by the computer certificates. I did **not** find a human proof for them.

## 3. Validation of the pipeline on known values

All of these were run with the final code by `code/reproduce.sh`:

- Refereed values, with no arrowing graph at value − 1 and the star union arrowing at value
  (`out/validation_small.txt`): r̂(K_{1,2},K_{1,2}) = 3; r̂(2K_2,2K_2) = 3 (BEFRS uniform);
  r̂(K_{1,3},K_{1,3}) = 5; r̂(K_{1,2}, 2K_{1,2}) = 6 (DJKR 2.3); r̂((2,2),(2,2)) = 9 (BEFRS);
  r̂((3,1),(3,1)) = 9 (DJKR 2.5, all odd); r̂((2,2),(3,2)) = 11 (DJKR 2.4); r̂((2,2,2),(2)) = 9 (DJKR 2.3).
- Positive controls (`out/positive_controls.txt`). The arrowing 3-edge graphs for (2) vs (2) are exactly
  K_{1,3} and K_3. The arrowing 6-edge graphs for (2) vs (2,2) are exactly 2K_{1,3}, K_{1,3} ⊔ K_3 and
  2K_3, as in the DJKR 2.3 characterisation the scout quotes. So the checker does detect arrowing.

## 4. The six target instances (`out/main_*.txt`)

Each line has the form "graphs checked / arrowing / witnesses / bad witnesses".

| pair | value v | graphs with v−1 edges | arrowing | independently verified witnesses |
|---|---|---|---|---|
| (2,2,1) v (2,1,1) | 11 | 4613 | 0 | 4613, bad 0 |
| (2,2,1) v (2,2,1) | 12 | 15216 | 0 | 15216, bad 0 |
| (2,1,1) v (2,2,1,1) | 12 | 15216 | 0 | 15216, bad 0 |
| (3,2,1) v (2,1,1) | 13 | 52944 | 0 | 52944, bad 0 |
| (2,2,2) v (2,1,1) | 13 | 52944 | 0 | 52944, bad 0 |
| (2,2,1) v (2,1,1,1) | 13 | 52944 | 0 | 52944, bad 0 |

Together with Lemmas 3 and 6 this proves the theorem in §0. The certificates are saved as
`out/runs/<F1>_vs_<F2>_e<v−1>_witnesses.tsv`.

**Extremal graphs (all graphs with exactly v edges that arrow), for the information they give:**

- (2,2,1) v (2,1,1), 11 edges, 6 graphs (`out/extremal_2.2.1_vs_2.1.1_e11.txt`). Each one is
  `X ⊔ 2K_{1,2}` with X one of:
  - D, the 7-edge tree made of two K_{1,3} with an edge joining a leaf of one to a leaf of the other;
  - S ⊔ K_{1,3}, where S is K_{1,3} with one leg extended (the spider S(2,1,1));
  - S ⊔ K_3;
  - two components from {K_{1,3}, K_3} plus K_2 (3 graphs).

  So minimum graphs are **not** always star unions with K_{1,3} → K_3 swaps. The 4-edge spider S plays
  the role of K_{1,3} ⊔ K_2, and the 7-edge tree D plays the role of 2K_{1,3} ⊔ K_2. This is in line with
  Cheng's C_5 ⊔ K_2 remark.
- (2,2,1) v (2,2,1), 12 edges: 9 graphs. (2,1,1) v (2,2,1,1), 12 edges: 7 graphs. Both lists contain D
  and S in the same roles (`out/extremal_*_e12.txt`).

## 5. Sweep over all small pairs (`out/sweep_*.txt`)

`code/all_pairs.py V` lists every pair (F1,F2), up to swapping, with value ≤ V. This is exhaustive:
`value ≥ Σ_i n_i` (the diagonals k = i+1 contain (i,1), giving `l_{i+1} ≥ n_i + m_1 − 1 ≥ n_i`) and
likewise `value ≥ Σ_j m_j`, so both sides are partitions of integers ≤ V. For each pair,
`code/sweep_one.sh` runs the whole pipeline. Witness files are gzip-compressed in `out/sweepw/`.

**Results.** Every pair passed. The star union arrows, no graph with v − 1 edges arrows, and every
witness was independently verified (`bad 0`).

| value v | pairs | graphs checked per pair (v−1 edges) | all pass | log |
|---|---|---|---|---|
| 2–12 | 577 (2, 5, 8, 13, 22, 29, 47, 64, 90, 119, 178) | 1 … 15216 | yes | `out/sweep_le12.txt` |
| 13 | 209 | 52944 | yes | `out/sweep_13.txt` |
| 14 (frontier only) | 11 | 193367 | yes | `out/sweep_14_frontier.txt` |

(Value 1 is the single trivial pair K_2 v K_2, with r̂ = 1.)

The value-14 frontier set (`code/filter14.py`, `out/pairs14_frontier.txt`) contains the pairs where
both forests have ≥ 3 stars and neither is a matching:
(2,1,1,1,1)v(2,1,1,1), (2,2,1,1)v(2,1,1,1), (2,2,1,1)v(2,2,1), (2,2,1,1,1)v(2,1,1), (2,2,2)v(2,2,1),
(2,2,2,1)v(2,1,1), (3,1,1)v(2,2,1), **(3,1,1,1)v(2,1,1)** (the smallest T2 instance), (3,2,1)v(2,2,1),
(3,2,1,1)v(2,1,1) and (3,2,2)v(2,1,1). In all 11, r̂ equals the formula value 14.

The other 298 value-14 pairs were **not** run. The full value-14 sweep was estimated at about 3 hours,
over the 40-minute cap. Each of those pairs has a side with ≤ 2 stars or a side that is a matching. The
frontier run took 8 min of wall clock. The value-13 sweep took about 35 min, and the value ≤ 12 sweep
took about 15 min.

## 6. What this does and does not show

**Shows (rigorously, computer-assisted):** the six values in §0. In particular,
r̂(2K_{1,2} ⊔ K_2, K_{1,2} ⊔ 2K_2) = 11, and the BEFRS formula is correct for every star-forest pair with
value ≤ 13, and for the 11 value-14 frontier pairs of §5. This includes every pair the scout listed as open under all known claims
up to value 13. It also includes every small case of the unrefereed claims (Cheng 2010 Thm 18, You 2026
Thm 1.2, Cipollini, tienxion) and of FLN26, so it independently checks them at value ≤ 13. The checks
cover only the values, not their proofs.

**Trust base:** networkx 3.6.1 (WL hash, VF2, blossom matching), the OEIS A000664 counts, `arrow.c`, and
`verify_witness.py`. The good colourings are certificates that anyone can re-check. The one step that is
not certificate-checkable is that the graph list is complete (Lemma 5). It rests on two independent
arguments: the count matching OEIS, and the generation-scheme proof (which itself relies on VF2 being
exact).

**Does not show:**
- Anything about Problem 561 in general. These are finitely many cases, and nothing here extends to an
  infinite family.
- A human-readable lower-bound proof for any of the six instances. Lemma 7 covers 3992 of 4613 graphs
  for the first one; the rest is machine-checked only.
- Anything about T2 (star plus matching with a > b, p > q ≥ 3) beyond its smallest instance,
  (3,1,1,1) v (2,1,1) = 14, which was checked here. The next T2 instances have value ≥ 16 and were not
  run.
- The 298 value-14 pairs outside the frontier set were not run.

**Operational note:** in the first sweep, 7 + 2 verifier runs crashed with an empty output. They passed
when rerun alone. The likely cause is system load: the machine load average was about 80, and in one case
my own `gzip` of witness files raced a running job. I then added the verifier's stderr to the log. The
final logs come from a clean rerun of `code/reproduce.sh` with the final code. The first-pass logs are
kept in `out/old/`.

## 7. Reproduce

```
cd attack/561/t1/prove
bash code/reproduce.sh        # compiles code/arrow.c; uses out/graphs if present, else regenerates
```

Graph generation took about 3 min for e ≤ 12 and 9 min for e = 13 (10 workers). The sweeps took
about 15 + 35 + 8 min. Single instances run in
seconds to minutes. A single instance can be run with
`python3 -I code/run_instance.py 2,2,1 2,1,1 out/graphs out/runs`. Python 3.11 (anaconda),
networkx 3.6.1, Apple clang `cc -O2`.

## 8. Sources not read

- BEFRS78, GySc02, DJKR25 (`../../refs/djkr.txt`), Cheng 2010 (`../../refs/cheng.txt`), You 2026
  (`../../refs/you.txt`) and FLN26 (`../../refs/fln_2606.04439v3.pdf`): **not read by me**. Their coverage
  claims are taken from SCOUT.md and serve only to motivate the choice of instances. No proof here uses
  them. In particular, the "known value" validations in §3 rely on the scout's reading of DJKR and
  BEFRS.
- The tienxion proof claim and the Plasma claim pages under `E0561/claims/`: not read.
- arXiv: no fresh search (the API returned 429). I relied on the scout's search of 2026-11-22.
- OEIS A000664: only the b-file numbers were used, not the derivation behind them.
