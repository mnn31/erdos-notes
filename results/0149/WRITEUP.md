# Erdős #149, Delta = 4: exhaustive search over 4-regular graphs on <= 15 vertices

Run 2026-11-22, about 30 min wall clock. No counterexample. Nothing was sent anywhere.

## Result (VERIFIED by computation, two independent checks)
sq(G) = strong chromatic index = chi(L(G)^2). Conjecture at Delta=4: sq <= 20.

| n | connected 4-regular graphs (= OEIS A006820) | max sq | graphs attaining max |
|---|---|---|---|
| 10 | 59 | 20 | 1 (C5 blow-up C5[2], the known extremal graph) |
| 11 | 265 | 17 | 1 |
| 12 | 1,544 | 15 | 3 |
| 13 | 10,778 | 16 | 1 |
| 14 | 88,168 | 17 | 3 |
| 15 | 805,491 | 17 | 11 |

So every 4-regular graph on at most 15 vertices (connected or not; a disconnected one has components on <= 10
vertices) has sq <= 20, and for 11 <= n <= 15 the maximum is only 17, three below the conjectured bound.
Consequence (by monotonicity of sq under subgraphs): no counterexample at Delta=4 is a subgraph of a 4-regular
graph on <= 15 vertices. This does NOT cover every Delta<=4 graph on <= 15 vertices (not every such graph extends
to a 4-regular graph on the same vertex set), and says nothing about n >= 16.

Full histograms of sq over connected graphs (out/sq/n*.w*.txt SUMMARY lines; the "hard" cases are resolved below):
- n=11: 10:2 11:131 12:94 13:27 14:4 15:3 16:3 17:1
- n=12: 9:3 10:48 11:472 12:897(+1 hard, SAT gives 12) 13:101 14:19 15:3
- n=13: 9:17 10:1324 11:4083 12:4025 13:1217(+5 hard, SAT gives 13 for all five) 14:92 15:14 16:1
- n=14: 9:51 10:23491 11:36670 12:22335 13:4212 14:625 15:56 16:6 17:3, plus 719 graphs where the exact
  DSATUR search hit its node limit. Each has greedy bound <= 17 except one (greedy 18), which SAT gives sq = 14;
  the 16 with greedy bound 17 SAT-check as sq <= 16. So the max 17 and the count 3 are exact; the lower bins are not.
- n=15 (threshold mode): 803,971 graphs have greedy DSATUR <= 15 colours (so sq <= 15). The rest: 11:30 12:351
  13:293 14:31 15:7 16:22 17:11, plus 775 node-limit cases: 610 with greedy bound 16, 145 with bound 17 (all 145
  SAT-check as sq <= 16), 20 with bound 18-19 (SAT gives sq in 13..15). So max 17 and the count 11 are exact.

## How it was computed (code/)
- nauty is NOT installed (installing it needed the user's OK), so code/g4.c has its own generator and canonical form:
  canonical labelling = lexicographically least adjacency matrix over all leaves of an individualisation-refinement
  tree (no automorphism pruning). Graphs on n vertices come from smaller 4-regular graphs by four expansions:
  (0) delete two disjoint edges ab, cd and add a vertex joined to a,b,c,d; (1) replace a triangle by two adjacent
  twins joined to its three vertices; (2) replace a vertex by K4; (4) delete an edge xy and insert K5 minus an edge pq, with new edges xp, yq
  ; plus disjoint unions. Completeness is not proved; it is CHECKED: the counts equal OEIS A006820 for
  every n = 5..15 (connected) and the disconnected counts equal the OEIS multiset-transform row (1,1,3,8,25,88).
  For n = 10..12 the set was also closed under all double-edge switches (which connect all realisations of a degree
  sequence) and nothing new appeared. Expansion ops 0-2 alone missed graphs (58 instead of 59 at n=10, etc.);
  the K5-minus-edge op fixed that.
- sq: build L(G)^2 as 64-bit masks; max clique (lower bound) + greedy DSATUR (upper bound); if they differ, exact
  DSATUR branch-and-bound with a node limit; leftovers flagged HARD.
- Independent check (code/satcheck.py): networkx builds the conflict graph separately, CaDiCaL (pysat) decides
  k-colourability. It confirmed sq for every extremal graph above (n=10: 20; n=11: 17; n=12: three 15s; n=13: 16;
  n=14: three 17s; n=15: two of the eleven 17s), every HARD case that could matter, and agreed with the C code on
  40 of 40 random n=12 graphs (out/xcheck/).
- Edge lists of the extremal graphs for n = 10..14: out/extremal_graphs.txt. All n=15 graphs with sq >= 16 are the
  "G" lines in out/sq/n15.w*.txt (index into out/levels/all15.bin, rows = adjacency bitmasks).
- Level files: out/levels/all<n>.bin = all 4-regular graphs (connected or not) on n vertices, n uint32 rows each.

## Not done / limits
- n=16 (8.04M graphs) and n=17 (86M) are NOT done: generation at n=15 took about 9 minutes, so n=16 would take
  roughly 90 min with this generator (nauty geng would be much faster, if the user OKs installing it).
- The side question (can a Delta<=4 graph have a strong clique of 21 edges?) was not attempted.
- Non-regular Delta<=4 graphs on 11..15 vertices are covered only if they extend to 4-regular graphs on the same
  vertex set.

## Prior public work (what I checked)
- VERIFIED by reading: refs/page.txt, refs/forum.txt, refs/plasma_index.md (Plasma E0149 page): theorems only; no
  search of 4-regular graphs recorded. Plasma's own search scope lists no computation.
- VERIFIED by reading: ryantuck/erdos-ai sonnet-5-5-review/149.md "Computation" addendum: an exact search over all
  labelled graphs on <= 7 vertices (no graph above 5/4 Delta^2; Delta = 4 cannot occur there) plus C5 blow-ups.
  Nothing on 4-regular graphs on 11+ vertices.
- NOT checked: House of Graphs, MathSciNet/zbMATH, papers on the strong chromatic index of small 4-regular graphs.
  So "not recorded publicly" means only "not on these pages". These numbers are new only as far as these pages show.
