# Problem 23, odd-girth variant (k=3): computed b_3(N) for N <= 14

b_3(N) := max over graphs G on N vertices with no C3 and no C5 (odd girth >= 7) of
D(G) = |E(G)| - maxcut(G). The [Er92b] question for k=3 asks whether b_3(7n) <= n^2.

## Result (exact, computer-verified)
| N | 1-6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|-----|---|---|---|----|----|----|----|----|----|
| b_3(N) | 0 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | **4** | >= 4 (unresolved) |
| best C7 blow-up | - | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 4 | 4 |

- **b_3(14) = 4 = 2^2**: the k=3 statement holds at n=2, and it is tight (balanced C7
  blow-up with parts of size 2: 28 edges, D=4). No counterexample.
- For every N = 7..14 the maximum equals the best C7 blow-up value (min_i s_i*s_{i+1};
  formula checked by brute force for all part sizes in {1,2,3}, N<=15).
- N=15: the "D >= 5?" instance (case: shortest odd cycle = C7) did not finish in ~16 min
  (stopped at the 50-min cap). Only 4 <= b_3(15) <= 6 is known from this run.
- Extremal-graph counts (analogue of A387954) were NOT computed (CP-SAT, not enumeration).

## Method (deviates from PLAN.md: nauty not installed, not installed without OK)
OR-tools CP-SAT 9.15 (single worker per process; multi-worker hangs here), 10 processes.
Feasibility of "D(G) >= t": 0/1 edge vars; clauses forbidding every C3, C5; one exact
integer constraint per bipartition (all 2^(N-1)): #monochromatic edges >= t.
Sound reductions (proofs elementary, written here):
1. Case split on the length L of a shortest odd cycle C (L = 7, 9, ..., N). C is induced;
   relabel it 0..L-1 and fix it. Odd cycles shorter than L forbidden via an odd-closed-walk
   reachability encoding. Vertices outside C ordered by degree (relabelling only).
2. D(G) <= D(G-v) + floor(deg v/2) (add v to the side holding fewer neighbours). So
   t > b(N-1) forces min degree >= 2(t - b(N-1)).
3. For any pair i,j: D(G) <= b(N-2) + floor(d_i/2) + floor(d_j/2); for an edge ij
   (no common neighbours, put i,j on opposite sides, better of two orientations):
   D(G) <= b(N-2) + floor((d_i+d_j-2)/2). Used for N >= 15 and in the tri re-check.
Human-checkable proof that b_3(14) <= 4 given b_3(13) = 2: a vertex outside a shortest
odd cycle C (|C| = L >= 7) has <= 2 neighbours on C (two neighbours must be at C-distance
exactly 2, and three points pairwise at distance 2 need L = 6), so the degrees on C sum to
<= 2L + 2(N-L), some v on C has deg <= 2N/7 = 4, and reduction 2 gives D <= 2 + 2.

## Validation
- Same code with only C3 forbidden (kind 'tri') reproduces OEIS A389646 a(1..12) =
  0,0,0,0,1,1,1,2,2,4,4,5 (two runs: with and without reduction 3); a(13) >= 6 found
  (witness), run stopped before the t=7 proof. a(13), a(14) NOT reproduced.
- Every witness graph re-checked independently (verify.py): odd girth by BFS on
  (vertex, parity), D by numpy enumeration of all 2^(N-1) cuts, exact integers.
  N=14 witness: 28 edges, odd girth 7, D = 4.
- Infeasibility proofs are CP-SAT's word (no DRAT/certificate); solver-trust caveat.

## Prior work (as far as checked)
VERIFIED by reading local copies: erdosproblems.com/23 page and forum (3 comments; StijnC
notes n=1 is true), OEIS A389646 text, Plasma E0023 files in refs/plasma: none gives values
for the odd-girth variant. NOT checked by me: arXiv (planner's API search was
rate-limited), SeqFan thread, ryantuck beyond the planner's note. Novelty of the small
table is therefore unconfirmed; it is a small computation, not a resolution.

## Files
code/bsat.py (plain model), code/bsat2.py (case-split model), code/drive.py (parallel
driver), code/verify.py (independent checker). out/*.jsonl raw runs (og7_run: N<=13,
og7_N14: N=14, og7_N15_16: unfinished, tri_validate2 / tri_pair_11_14: A389646 check).
