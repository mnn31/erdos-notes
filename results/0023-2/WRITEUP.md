# Erdős #23, generalisation [Er92b], case k = 3, n = 2 (14 vertices, odd girth ≥ 7)

Status: **PROVED (computer-assisted)**. Every certificate below was checked on 2026-11-23.

## Statement established

**Theorem.** Let G be a simple graph on 14 vertices with no cycle of length 3 and no cycle of length 5.
Then G can be made bipartite by deleting at most 4 edges, i.e. D2(G) ≤ 4.
The bound is sharp: the balanced blow-up C7[2] has 14 vertices, no C3 or C5, and D2(C7[2]) = 4.

This is the case k = 3, n = 2 of Erdős's question as quoted on erdosproblems.com/23:
"a graph on (2k+1)n vertices in which every odd cycle has size ≥ 2k+1 can be made bipartite by deleting at most n^2 edges".
Because cycles of length 1 do not exist in simple graphs, "no C3 and no C5" is the same as "every odd cycle has length ≥ 7" (see Lemma 1).

How the proof is split:
- Shortest odd cycle of length 11 or 13: a hand proof (Lemma 4).
- Shortest odd cycle of length 7 or 9: UNSAT certificates (DRUP), checked by a small independent checker (Lemmas 5–6).
- Cases 11 and 13 were also certified by computer.
- Pipeline B, an independent re-encoding, agrees on cases 7 and 9 (no certificate; see §4).

Status of the open question before this work: the page lists no small-case result for k ≥ 3. The forum (3 comments) only notes that n = 1 is trivial. Plasma's E0023 page mentions the generalisation once ("no proof"). A web search found the conjecture only restated in surveys. (VERIFIED from page23.html, forum23.html, and refs/plasma_E0023_index.md line 38.)

---

## 1. Definitions

- For a graph G = (V, E) and a 2-colouring σ : V → {0,1}, an edge uv is *uncut* if σ(u) = σ(v).
  unc(σ) is the number of uncut edges.
- D2(G) := min over σ of unc(σ).

**Lemma 0.** G can be made bipartite by deleting at most m edges iff D2(G) ≤ m.

*Proof.*
(⇐) Pick σ with unc(σ) = D2(G) ≤ m and delete the uncut edges. Every remaining edge joins the two colour classes, so σ is a proper 2-colouring and the rest is bipartite.
(⇒) Suppose F is a set of edges with |F| ≤ m and G − F bipartite, with proper 2-colouring σ. Every edge of G not in F is cut by σ, so the uncut edges of σ lie in F. Hence unc(σ) ≤ |F| ≤ m. ∎

## 2. Lemmas with full proofs

**Lemma 1 (odd closed walks).** If a graph has a closed walk of odd length L, then it has a cycle of odd length ≤ L.

*Proof.* Strong induction on L. Let W = (w0, w1, …, wL = w0) be a closed walk of odd length L. L = 1 is impossible since there are no loops, so L ≥ 3.
- If w0, …, w_{L−1} are pairwise distinct, then W is a cycle of length L (L ≥ 3).
- Otherwise w_i = w_j for some 0 ≤ i < j ≤ L−1. Split W into W1 = (w_i, …, w_j) of length j − i and W2 = (w_j, …, w_L = w0, …, w_i) of length L − (j − i). Both are closed walks, both are shorter than L, and both have length ≥ 1. Their lengths add to the odd number L, so one of them has odd length L' < L. By induction it contains an odd cycle of length ≤ L' < L. ∎

Consequence: G has no C3 and no C5 iff G has no closed walk of length 3 or 5, iff every odd cycle of G has length ≥ 7.
- A C3 or C5 is itself such a closed walk.
- Conversely, such a walk gives an odd cycle of length ≤ 5 by Lemma 1, and that cycle is a C3 or a C5.
The same argument shows: if the shortest odd cycle has length g, then G has no closed walk of odd length ≤ g − 2.

**Lemma 2 (case split).** Let G on 14 vertices have no C3 and no C5. Then either G is bipartite (so D2(G) = 0), or the length g of a shortest odd cycle satisfies g ∈ {7, 9, 11, 13}.

*Proof.* A non-bipartite graph contains an odd cycle (standard: BFS-layer parity gives a proper 2-colouring when there is no odd cycle). Its length is odd and ≥ 7 by Lemma 1. A cycle has at most 14 vertices and g is odd, so g ≤ 13. ∎

**Lemma 3 (structure around a shortest odd cycle).** Let C = c_0 c_1 … c_{g−1} be a shortest odd cycle of G, with g ≥ 7. Indices are mod g.
- (i) C is an induced cycle.
- (ii) Every vertex x ∉ C has at most 2 neighbours on C. If it has two, they are c_a and c_{a+2} for some a.

*Proof.*
(i) Suppose a chord c_a c_b exists. It splits C into two arcs of lengths p, q ≥ 2 with p + q = g. This gives two cycles of lengths p + 1 and q + 1, and these lengths add to g + 2, which is odd. So exactly one of them is odd. Its length is ≤ max(p, q) + 1 ≤ (g − 2) + 1 < g, which contradicts minimality.

(ii) Let x ∉ C be adjacent to c_a and c_b, with a ≠ b. The two arcs of C between c_a and c_b have lengths p, q ≥ 1, with p + q = g odd. Each arc plus the path c_b x c_a is a cycle (x is not on C), of length p + 2 or q + 2. Say p is odd, so q is even. Then p + 2 is an odd cycle length, so p + 2 ≥ g = p + q, which gives q ≤ 2. Since q is even and ≥ 1, q = 2. So any two C-neighbours of x are at distance exactly 2 along C (the other arc has length g − 2 ≥ 5).

Now suppose x had three C-neighbours. By relabelling they are c_a, c_{a+2}, c_{a−2}, since each pair is at C-distance 2 and they are distinct. Then c_{a+2} and c_{a−2} are joined by arcs of lengths 4 and g − 4 ≥ 3, so neither arc has length 2. Contradiction. ∎

**Lemma 4 (hand proof for g ∈ {11, 13}).** Let G on 14 vertices have no C3 and no C5, with shortest odd cycle of length g ≥ 11. Then D2(G) ≤ 3.

*Proof.* Let C be a shortest odd cycle, X = V ∖ V(C), so |X| = 14 − g ≤ 3.

Colouring of C: for t ∈ {0, …, g−1}, the path P_t = c_{t+1}, c_{t+2}, …, c_{t+g} (note c_{t+g} = c_t) uses every edge of C except c_t c_{t+1}. Colour the vertices of P_t alternately 0, 1, 0, …. Then every edge of C except c_t c_{t+1} is cut. By Lemma 3(i) there are no other edges inside V(C).

Forbidden positions: by Lemma 3(ii), each x ∈ X with two C-neighbours has them as c_{a_x}, c_{a_x+2}. Let F be the set of all a_x and a_x + 1 (mod g) over such x. Then |F| ≤ 2|X| ≤ 6 < 11 ≤ g, so we can choose t ∉ F.

Why t ∉ F works: for each such x, the edges c_{a_x} c_{a_x+1} and c_{a_x+1} c_{a_x+2} both lie on P_t. So c_{a_x}, c_{a_x+1}, c_{a_x+2} are three consecutive vertices of P_t, and c_{a_x} and c_{a_x+2} get the same colour.

Colour each x ∈ X as follows:
- if x has at least one C-neighbour, give it the opposite of that colour (well defined, since all its C-neighbours share a colour);
- otherwise give it colour 0.

Now every edge between X and C is cut. The uncut edges are among c_t c_{t+1} and the edges inside X. G[X] has at most 3 vertices and no triangle, so it has at most 2 edges. Hence D2(G) ≤ 1 + 2 = 3. ∎

(The same argument fails for g = 9: there |X| = 5, |F| can be 10 > 9, and G[X] can have 6 edges. Cases g = 7 and g = 9 are therefore done by computer.)

**Lemma 5 (the CNF Φ_g and its soundness).** Fix g ∈ {7, 9, 11, 13}. Φ_g is the DIMACS file `out/cnf/N14_g{g}_T5.cnf` written by `code/cegar.py`. Its variables and clauses are:

- **Edge variables.** e_{uv} for each pair 0 ≤ u < v ≤ 13. The file's `c e u v id` comment lines give the mapping.
- **Walk variables** W_k(u, v) for 2 ≤ k ≤ g − 2 and all ordered pairs (u, v), including u = v. We write W_1(u, v) := e_{uv} for u ≠ v.
  - Clause ¬W_{k−1}(u, w) ∨ ¬e_{wv} ∨ W_k(u, v) for every k, every u, w with W_{k−1}(u, w) defined, and every v ≠ w.
  - Unit clause ¬W_k(u, u) for every odd k with 3 ≤ k ≤ g − 2.
- **Cycle units.** e_{i,i+1 mod g} for 0 ≤ i < g.
- **Lex symmetry breaking.** For g ≤ i ≤ 12, let a = (e_{i,0}, …, e_{i,g−1}) and b = (e_{i+1,0}, …, e_{i+1,g−1}). The clauses say a ≤_lex b, using auxiliary prefix-equality variables q_{i,j}:
  - (¬q_{i,j−1}) ∨ ¬a_j ∨ b_j, with the first literal omitted for j = 0;
  - (¬q_{i,j−1}) ∨ a_j ∨ b_j ∨ q_{i,j} and (¬q_{i,j−1}) ∨ ¬a_j ∨ ¬b_j ∨ q_{i,j}, for j < g − 1.
- **Cut constraints.** One for each of a list of bipartitions σ (recorded in `N14_g{g}_T5_cuts.json` as row indices r: vertex v ≥ 1 is on side (r >> (v−1)) & 1, and vertex 0 is on side 0). Each is the pysat sequential-counter encoding of "at least 5 of the variables {e_{uv} : σ(u) = σ(v)} are true", with fresh auxiliary variables per constraint.

*Claim.* If some G on 14 vertices with no C3, no C5, shortest odd cycle of length g, and D2(G) ≥ 5 existed, then Φ_g would be satisfiable.

*Proof.*

Relabelling.
- Relabel G so that a shortest odd cycle is 0, 1, …, g−1 in cyclic order.
- Then permute the vertices g, …, 13 among themselves so that their 0/1 adjacency vectors to (0, …, g−1) are in non-decreasing lexicographic order.

This permutation fixes 0, …, g−1, so the cycle is still there. Relabelling changes neither the cycle lengths nor D2.

Assignment.
- e_{uv} := [uv ∈ E(G)].
- W_k(u, v) := [G has a walk of length k from u to v].
- q_{i,j} := [vectors of i and i+1 agree in positions 0..j].
- Card-encoding auxiliaries: as described under "Cut constraints" below.

Clause by clause:
- *Walk clauses.* A walk of length k−1 from u to w followed by the edge wv is a walk of length k from u to v, so these hold.
- *Units ¬W_k(u, u) for odd k ≤ g − 2.* A closed walk of odd length k ≤ g − 2 would give an odd cycle of length ≤ g − 2 by Lemma 1, contradicting minimality of g. So these hold.
- *Cycle units.* They hold by the labelling.
- *Lex clauses.* Take the first group: if the prefixes up to j−1 agree and a_j = 1, then b_j = 1, since otherwise a >_lex b against the sort order. For the other two groups: if the prefixes up to j−1 agree and a_j = b_j, then q_{i,j} = 1 by definition. So all lex clauses hold.
- *Cut constraints.* D2(G) ≥ 5 means every σ leaves ≥ 5 uncut edges, so at least 5 of the listed edge variables are true. The sequential-counter encoding of "at least 5" then has a satisfying extension to its own fresh auxiliary variables.

Caveat on the cut constraints: we use this completeness property of pysat's `CardEnc.atleast(..., EncType.seqcounter)` without re-deriving it. It was tested on 300 random instances (`verify.py`, part (a), 0 mismatches). Pipeline B independently uses the totalizer encoding instead.

The auxiliary variable sets are pairwise disjoint: all named variables are allocated before any cardinality encoding, from one `IDPool`. So the assignments do not conflict, and Φ_g is satisfiable. ∎

**Lemma 6 (Φ_g is unsatisfiable; machine-checked).** For each g ∈ {7, 9, 11, 13}, Φ_g is unsatisfiable.

*Evidence (VERIFIED by computation, `out/rupcheck_N14_T5.txt`).*

How the certificates were made and checked: glucose3 produced a DRUP refutation for every g, and maplechrono produced a second one for g = 7. `code/rupcheck.c` is a ~200-line forward RUP checker with two watched literals, written for this task. For every added lemma it checks that the negated lemma propagates to a conflict against the current database.

Why the checker is sound:
- By induction, each accepted lemma is implied by the original formula.
- Deletions can only weaken the database.
- The checker never deletes unit clauses, or clauses with a literal assigned at top level.
- A proof is accepted only if top-level propagation reaches a conflict.

| g | clauses | vars | proof (solver) | lemmas checked | result |
|---|---|---|---|---|---|
| 7 | 297 231 | 158 126 | glucose3 | 39 626 | VERIFIED UNSAT |
| 7 | 297 231 | 158 126 | maplechrono | 29 160 | VERIFIED UNSAT |
| 9 | 119 744 | 58 514 | glucose3 / glucose4 | 2 014 / 2 187 | VERIFIED UNSAT |
| 11 | 30 732 | 7 374 | glucose3 / glucose4 | 93 / 93 | VERIFIED UNSAT |
| 13 | 35 782 | 7 746 | glucose3 / glucose4 | 2 / 2 | VERIFIED UNSAT |

Checker self-tests (all behaved as required):
- A bogus "0" proof for a satisfiable CNF: rejected.
- A bogus proof with unit lemmas 5 and −5: rejected at lemma 1.
- The g = 9 proof with every third lemma dropped: rejected at lemma 5.
- The g = 9 proof with deletions stripped: still accepted, as it must be.

The glucose4 proof for g = 7 was **rejected**: lemma 17462 is not RUP. A naive independent Python unit-propagation script (no watched literals) confirmed this lemma is not RUP while the previous one is. So the checker agrees with brute force, and that glucose4 proof (as emitted through pysat) is defective. That file is kept as `N14_g7_T5_glucose4_REJECTED.drup` and is **not** used.

Plain re-solves of all four Φ_g from scratch were also UNSAT with glucose4, minisat22, maplechrono and cadical195 (`out/resolve_N14_T5.txt`).

**Proof of the Theorem.** Let G be on 14 vertices with no C3 and no C5.
- If G is bipartite, D2(G) = 0.
- Otherwise its shortest odd cycle has length g ∈ {7, 9, 11, 13} (Lemma 2).
- If g ∈ {11, 13}, D2(G) ≤ 3 by Lemma 4.
- If g ∈ {7, 9} and D2(G) ≥ 5, Lemma 5 makes Φ_g satisfiable, contradicting Lemma 6. So D2(G) ≤ 4.

Lemma 0 converts this into "delete at most 4 edges".

Sharpness: C7[2] (vertex 2i + a, a ∈ {0, 1}; adjacent iff the classes i, i' are consecutive mod 7) has 28 edges, shortest odd cycle 7, and D2 = 4. This was checked by exhaustive enumeration of all 2^13 bipartitions in `verify.py`. The T = 4 search also independently found a graph with D2 = 4. It is 4-regular with 7 twin pairs, i.e. a copy of C7[2]. ∎

## 3. Calibration (VERIFIED by computation)

The same program `cegar.py`, run with odd girth ≥ 5 (triangle-free), reproduces OEIS A389646 exactly. A389646 is the maximum D2 of a triangle-free graph on N vertices, fetched as text from oeis.org: 0,0,0,0,1,1,1,2,2,4,4,5,6,…

| N | OEIS | cegar.py (T SAT / T+1 UNSAT) |
|---|---|---|
| 5 | 1 | 1 |
| 8 | 2 | 2 |
| 10 | 4 | 4 |
| 11 | 4 | 4 |
| 12 | 5 | 5 |

Walk encoding test (`verify.py` (b)): 400 random graphs each for g = 7 and g = 9 contain the fixed cycle and are lex-sorted. For each, "base CNF + edge assumptions SAT" matched "no odd cycle shorter than g", computed by BFS on the bipartite double cover, with 0 mismatches.

Side table (VERIFIED by cegar.py only, no certificates): the maximum D2 over graphs with odd girth ≥ 7 on N vertices is
- 1 for N = 7, 8, 9, 10;
- 2 for N = 11, 12, 13;
- 4 for N = 14.

Each lower bound comes with a witness whose D2 was recomputed exactly. The upper bounds are single-pipeline UNSAT results. (`out/table_fN_oddgirth7.txt`)

## 4. Independent second pipeline, "pipeline B" (cross-check, not a certificate)

`code/cegar2.py` shares no encoding code with `cegar.py`:
- explicit clauses for every cycle of length 3, …, g−2 in K14 (≈1.26 M clauses for g = 9);
- totalizer cardinality encoding;
- plain-Python D2;
- symmetry breaking either none, or (option `sym`) brute-force forbidden pairs of adjacency vectors.

Results:

| g | symmetry breaking | result | cuts | time | file |
|---|---|---|---|---|---|
| 9 | none | UNSAT | 476 | 225 s | `out/run2_N14_g9_T5.txt` |
| 7 | brute-force lex pairs | UNSAT | 811 | 110 s | `out/run2sym_N14_g7_T5.txt` |
| 7 | none | inconclusive | — | stopped at the 40-minute cap | `out/run2_N14_g7_T5.txt` |

Calibration of cegar2, against OEIS A389646:
- Triangle-free N = 10: T = 5 UNSAT for g = 5, 7, 9; T = 4 SAT with exact D2 = 4.
- Triangle-free N = 12 with `sym`: T = 6 UNSAT for g = 5, 7, 9, 11, and T = 5 SAT. Both match the OEIS value 5 (`out/calib2sym_N12.txt`).

## 5. Reproduce

```
cd code
cc -O2 -o rupcheck rupcheck.c
python3 -I cegar.py 14 7 5 cadical153 ../out/cnf      # writes Φ_g and cut lists; prints UNSAT for g=7,9,11,13
python3 -I cegar.py 14 7 4 cadical153 ../out/cnf      # finds a D2=4 witness (C7[2])
for g in 7 9 11 13; do python3 -I mkproof.py ../out/cnf/N14_g${g}_T5.cnf ../out/cnf/N14_g${g}_T5_glucose3.drup glucose3; ./rupcheck ../out/cnf/N14_g${g}_T5.cnf ../out/cnf/N14_g${g}_T5_glucose3.drup; done
python3 -I mkproof.py ../out/cnf/N14_g7_T5.cnf ../out/cnf/N14_g7_T5_maplechrono.drup maplechrono
python3 -I resolve.py ../out/cnf/N14_g7_T5.cnf          # re-solve with 4 solvers
python3 -I verify.py                                     # encoding tests + witness/blow-up checks
python3 -I cegar2.py 14 7 5 9 cadical153                 # independent pipeline, g=9
python3 -I cegar2.py 14 7 5 7 cadical153 sym             # independent pipeline, g=7
```

Notes:
- The scripts add `~/.local/lib/python3.11/site-packages` (python-sat 1.9.dev15) to `sys.path`, because `-I` drops user site-packages.
- Runtimes: cegar.py N = 14, T = 5 took about 100 s. Checking the g = 7 proof took about 1 minute.
- Exact CNF and proof hashes are in `out/sha256.txt`.
- Solver nondeterminism: rerunning `cegar.py` can give a different cut list, and so a different Φ_g. Each such Φ_g is equally sound by Lemma 5. The certified one is the file in `out/cnf`.

## 6. What this does and does not show

Does show:
- The k = 3, n = 2 instance of Erdős's generalisation is true: every 14-vertex graph with odd girth ≥ 7 can be made bipartite by deleting ≤ 4 edges, and 4 is attained.
- The method is a hand argument for shortest odd cycle ≥ 11, plus DRUP-certified SAT refutations for shortest odd cycle 7 and 9.

Does not show:
- Anything for n ≥ 3 (e.g. 21 vertices, ≤ 9 deletions), for k ≥ 4, or for vertex counts that are not multiples of 7. The side table for N ≤ 13 is uncertified.
- Anything about #23 proper (k = 2), which is already settled for small n per OEIS A389646 and the scout notes.
- Uniqueness of the extremal graph. We only observed that the one witness found is C7[2].

Trust base:
1. the correctness of `rupcheck.c` (self-tested; agrees with a naive checker on the one disputed lemma);
2. Lemma 5's reading of `cegar.py` (the CNF is what the code says), and the CNF file being the one that code wrote;
3. completeness of pysat's sequential-counter "at least" encoding (tested, not proved here).

A fully formal proof (e.g. Lean plus a verified DRAT checker such as cake_lpr) was not done.

Novelty (INFERRED): we found no prior statement of this case. The checks were the problem page, the forum, Plasma's E0023 page, and one web search. It is a small finite case, and someone may well have checked it unpublished.

## 7. Sources not read

- Erdős [Er92b] (original source of the generalisation): not read. The statement is taken from erdosproblems.com/23 text.
- arXiv:1306.5167 (Füredi–Simonovits survey, Conjecture 14.12 per search snippet): not opened.
- Fox–Himwich–Mani arXiv:2102.10220, Balogh–Clemen–Lidický [BCL21], Ferudun arXiv:2606.28041: not read.
- Andrásfai–Erdős–Sós-type min-degree results for odd girth: not used, not read.
- Plasma E0023 claim pages: not read (only `_index.md`, grepped).
- OEIS A389646: only the %N/%S lines were fetched.
