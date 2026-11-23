# Problem 580: edge form (Zhao Conj. 1.3) and Komlos-Sos at small n. Computation result

Run 2026-11-22, about 22:10-22:40 PST. Machine heavily shared (load avg ~140), so wall times are not benchmarks.
Nothing was posted, committed or sent anywhere.

## Statements checked (host graph G on N vertices)
- E(N,J,D,E): every G with >= J vertices of degree >= D contains every tree with E edges.
- Loebl edge form at even n=2k: E(2k,k,k,k). Odd n=2k+1 reduces to 2k by deleting one high-degree vertex
  (argued in PLAN.md and Plasma's finite-reduction note).
- m(n,n/2) here means the least J such that E(n,J,n/2,n/2) holds. That is my working definition.
  I did NOT read Zhao's definition of m(n,k) in the paper; Plasma's index quotes the bounds
  n/2 - sqrt(n) - 2 < m(n,n/2) <= n/2 for n >= n0.

## Method (code/lks.c; reduction from PLAN.md)
L = J vertices of degree >= D, S = rest. Delete S-S edges. Trim each u in L to exactly max(0, D - deg_L(u))
S-neighbours. Every hypothesis graph contains one of these reduced hosts, and containing a tree is monotone,
so checking the reduced hosts is enough. H = G[L] runs over the networkx graph atlas (graphs on <=7 vertices
up to isomorphism). The S side is a non-increasing sequence of N-J column bitmasks with prescribed row sums.
Trees come from networkx.nonisomorphic_trees. Embedding is by bitmask backtracking. No Aut(H) reduction is used.
All counting is exact integer arithmetic.

## Results (all VERIFIED by running the code here; no human review)
| statement | reduced hosts | hosts missing a tree |
|---|---|---|
| Loebl edge, n=2,4,6,8,10 (J=k) | 1, 3, 13, 210, 9482 | 0 |
| Loebl edge, n=12 (J=6) | 2,175,917 | 0 |
| **Loebl edge, n=14 (J=7)**, 4 chunks covering work items [0,122341) | **2,138,992,095** | **0** |
| **E(14,5,7,7)**: only 5 vertices of degree >= 7 | 2,456,658 | **0** |
| E(14,4,7,7) | 35,713 | 31 |
| E(16,5,8,8) | partial run | >= 2 (the run was stopped once counterexamples appeared) |

So the edge form (Zhao Conj. 1.3) holds for every n <= 15: even n directly, odd n by the reduction.
The n=14 case already follows from the stronger E(14,5,7,7). The full J=7 run is a consistency check.
n=16 was NOT done: the J=6 run ran about 2% in 80 s, and a count-only pass did not finish in 2 min.

m(n,n/2) (least J; monotone in J, so the boundary pair settles it):
| n | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 |
|---|---|---|---|---|---|---|---|---|
| m(n,n/2) | 1 | 1 | 2 | 3 | 3 | 5 | 5 | >= 6 |
(n=2: J=1 with D=E=1 holds trivially, by hand.) Files: out/m_n_half.txt, out/m14_J4.txt, out/loebl_n14_part*.txt,
out/n16_J5_partial_cex.txt. The extremal witnesses are spiders. At n=12, J=4 the missing tree is S(2,2,2):
L is a C4, and the two pairs of opposite vertices each have 4 private S-neighbours. At n=14, J=4 it is S(3,2,2).
At n=16, J=5 it is S(2,2,2,2).
(I inferred, without checking, that this resembles Zhao's Construction 1.7.)

Komlos-Sos, all (n,k) with 2 <= n <= 12 and 1 <= k <= n-1, J = ceil(n/2) vertices of degree >= k:
- edge form (trees with k edges): 0 counterexamples in all 66 cases;
- page form (trees with k vertices): 0 counterexamples in all 55 cases (k >= 2).
(out/komlos_sos_n_le_12.txt, 121 RESULT lines.)

## Validation
- Atlas graph counts per order 1..7 = 1,2,4,11,34,156,1044 (OEIS A000088). Tree counts for 2..15 vertices
  = 1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741 (A000055).
- Positive controls: lowering D to k-1 gives counterexamples at n=6,8,10 (2K_k-type). The reduced-host
  counts for D=k and D=k-1 agree (13, 210, 9482), as the H -> complement(H) plus column-complement
  bijection predicts.
- Splitting the work range gives sums that match the unsplit run (n=12: 1,269,082 + 906,835 = 2,175,917).
- Every reported counterexample (14 hosts) was re-checked with networkx GraphMatcher monomorphism
  (code/indep_check.py). In each one the hypothesis holds and the tree is absent.
- code/indep_enum.py independently re-implements the enumeration (itertools multisets) plus networkx embedding.
  It matches the C program exactly: N=8,J=4: 210/0; N=10,J=5: 9482/0; N=10,J=3: 111/0; N=10,J=2: 9/9.
  N=12,J=4: 8455 hosts, 5 missing a tree (C program: 8455, 5).
- Random greedy-edge-minimal hosts, which do not use the reduction (networkx): 300 each at
  (n,J) = (10,5),(10,3),(12,6),(12,5),(12,4),(14,7). No missing tree.
  As expected, random sampling did not hit the rare n=12, J=4 counterexamples.
- n=14, J=5: networkx re-checked a 1-in-997 systematic sample of the C-enumerated hosts (2462 hosts). All contain all 23 trees (out/n14_J5_sample_check.txt). This checks the embedding routine, not completeness of the enumeration.
- NOT independently re-verified exhaustively: the J=7 and J=5 runs at n=14 (C only). The 2.1e9-host run has no second
  implementation. Its correctness rests on the same code that matches the Python re-implementation at n <= 12.

## Literature / rival check (step 0)
- Web search (2 queries) found no paper doing an exhaustive small-n check of Loebl/LKS in the edge form.
  The only computer check found is Zeraoulia's vertex-form SAT claim (preprints.org 202607.1163),
  which is unreviewed. MathSciNet/zbMATH were NOT accessed.
- A search snippet (not read first-hand) says Piguet-Stein proved LKS for all trees of diameter <= 5.
  If that is right, every k <= 5 case here is already implied. The new content would be k = 6, 7,
  where paths and long spiders have diameter > 5.
- Plasma E0580 (local copy refs/plasma_index.md) records the edge form as unchecked for n < n0 and m(n,n/2)
  as unknown. ryantuck/erdos-ai: no 580-specific file found (only session logs whose names match "580").

## Caveats
Unreviewed computation. The reduction is elementary but was argued only here and in PLAN.md.
The m(n,n/2) definition is inferred. The small-n values say nothing about Zhao's asymptotic regime.
