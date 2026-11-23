# Erdős Problem 719, target T2: (r, n) = (4, 8) — PROVED (plus the family n = r+4 whenever an SQS(n) exists)

Agent brief: try to PROVE T2. Outcome: **PROVED**, by a short averaging argument (random relabelling of a
Fano plane). The same argument proves the inequality for every pair (r, n) with n = r+4 for which a
Steiner quadruple system SQS(n) exists; unconditionally this covers n = 2^k (k >= 3) and n = 10.

## 0. Statements established

**Theorem A (target).** Every 4-uniform hypergraph G on 8 vertices satisfies

    |E(G)| - 4·ν(G) <= 56 = ex_4(8; K_5^4),

where ν(G) is the maximum number of pairwise edge-disjoint copies of K_5^4 in G. Moreover equality holds
iff G is K_5^4-free with exactly 56 edges, and if G has at most 13 non-edges then |E(G)| - 4ν(G) <= 55.
Equivalently (Lemma 1): every 4-graph on 8 vertices is the union of at most ex_4(8;K_5^4) = 56 copies of
K_4^4 and K_5^4, no two sharing a K_4^4. So the Erdős–Sauer question has a positive answer at (r,n) = (4,8).

**Theorem B (extension, n = r+4).** Let N >= 6, r = N-4, and suppose there is a Steiner quadruple system
on N points (a family of 4-subsets of [N] containing every 3-subset of [N] exactly once). Then
ex_r(N; K_{r+1}^r) = C(N,4) - C(N,3)/4 and every r-graph G on N vertices satisfies
|E(G)| - r·ν(G) <= ex_r(N; K_{r+1}^r).

**Corollary C (unconditional instances of B).** Theorem B's hypothesis holds, by explicit construction
checked in this file / by computer, for N = 2^k (every k >= 3) and for N = 10. Hence the Erdős–Sauer
inequality holds for (r, n) = (2^k - 4, 2^k) for all k >= 3 and for (r, n) = (6, 10).

**Corollary C' (CONDITIONAL, not verified here).** If the classical theorem "an SQS(N) exists iff N ≡ 2 or
4 (mod 6)" (Hanani 1960; quoted from memory, source NOT read) is correct, then the Erdős–Sauer inequality
holds for every pair (r, n) = (N-4, N) with N ≡ 2, 4 (mod 6), N >= 8.

## 1. Status check before working (2026-11-23)

- erdosproblems.com/719 (refs/page719.html): label open; 1 comment, 1 proof claim.
- Forum thread (refs/forum719.html): one comment (Zeraoulia, 8 Feb 2026): exhaustive check of r=3, n=6
  and the trivial case (r,n) = (7,8). Nothing on r = 4 / n = 8.
- Plasma page wiki/problems/set_systems/E0719/_index.md (refs/plasma_E0719.md; last commits on the folder
  2026-10-14..19): "The case r=3 with n>=10, and every case r>=4 beyond the trivial range n<=r+1, are
  untouched by any claim found." Claims index (refs/plasma_E0719_claims.md): only EGP 1966 (r=2) and
  Zeraoulia 2026 (r=3, n<=9).
- arXiv API searches ("Erdos Sauer hypergraph", "clique decomposition hypergraph"; refs/arxiv_*.xml):
  no relevant hit (only fractional-decomposition papers).
- formal-conjectures 719.lean (origin/main): `erdos_719`, `research open`, all r >= 2, all n.
So the target was not decided in any source checked. (Sibling workspace t1 in this repo claims n = r+3 for
all r; I did not re-verify it and nothing below depends on it.)

## 2. Notation

V = vertex set, |V| = N. For the problem at hand N = 8, r = 4; Theorem B uses N = r+4 in general.
An r-graph G on V is a set E(G) of r-subsets of V; m = |E(G)|; non-edges are the r-subsets not in E(G);
t = number of non-edges, so m = C(N,r) - t. A *copy of K_{r+1}^r in G* is an (r+1)-set S all of whose r
subsets lie in E(G) (a copy is determined by its vertex set S). D := C(N,3).

For an r-set e put ē := V \ e (a 4-set, since N - r = 4) — the *shadow* of e. A 3-set A ⊆ V is **full**
(for G) if A ⊄ ē for every non-edge e. A family of 3-sets is a **packing** if any two of its members share
at most one point.

## 3. Lemmas and proofs

**Lemma 1 (piece count).** For any r-graph G, the minimum number of pieces in a decomposition of E(G) into
pairwise edge-disjoint copies of K_r^r (single edges) and K_{r+1}^r (contained in G) is m - r·ν(G).

*Proof.* In any such decomposition let k be the number of K_{r+1}^r pieces; they are pairwise edge-disjoint
copies in G, so k <= ν(G); they use (r+1)k edges, and the remaining m - (r+1)k edges must be single-edge
pieces (the pieces partition E(G)). Total pieces m - rk >= m - rν(G). Taking a family of ν(G) edge-disjoint
copies plus all other edges as singletons attains m - rν(G). ∎

So Problem 719 at (r,n) asks exactly whether m - rν(G) <= ex_r(n; K_{r+1}^r) for all G.

**Lemma 2 (dual description; any N = r+4, r >= 1).** Let G be an r-graph on V, |V| = N = r+4.
(a) For a 3-set A, the (r+1)-set S_A := V \ A spans a copy of K_{r+1}^r in G iff A is full.
(b) For distinct 3-sets A, B, the (complete) copies on S_A and S_B share an r-set iff |A ∩ B| >= 2.
(c) ν(G) equals the maximum size of a packing consisting of full 3-sets.

*Proof.* (a) For an r-set e: e ⊆ S_A iff e ∩ A = ∅ iff A ⊆ V \ e = ē. S_A spans a copy iff no r-subset of
S_A is a non-edge iff there is no non-edge e with A ⊆ ē, i.e. iff A is full.
(b) |S_A ∩ S_B| = |V \ (A ∪ B)| = N - |A ∪ B| = N - 6 + |A ∩ B| = r - 2 + |A ∩ B|. An r-set lies in both
S_A and S_B iff |S_A ∩ S_B| >= r iff |A ∩ B| >= 2; any such r-set is an edge of both copies.
(c) Copies of K_{r+1}^r in G are in bijection with full 3-sets via S ↦ V \ S (by (a)); by (b) a family of
copies is pairwise edge-disjoint iff the corresponding 3-sets pairwise share <= 1 point. ∎

**Lemma 3 (extremal number via coverings).** With N = r+4, let τ(N) be the minimum size of a family of
4-subsets of V such that every 3-subset of V lies in at least one member. Then
ex_r(N; K_{r+1}^r) = C(N,4) - τ(N), and τ(N) >= C(N,3)/4, with equality iff an SQS(N) exists.

*Proof.* e ↦ ē is a bijection from r-subsets to 4-subsets of V (and C(N,r) = C(N,4)). By Lemma 2(a), G is
K_{r+1}^r-free iff no 3-set is full iff the shadows of the non-edges cover all 3-sets. Hence a K-free G
has at least τ(N) non-edges, and taking the non-edges to be the shadows' preimages of an optimal covering
gives a K-free G with exactly τ(N) non-edges. So ex = C(N,4) - τ(N). Each 4-set contains exactly 4
three-subsets, so a covering has >= D/4 members, with equality iff every 3-set is covered exactly once,
i.e. iff the covering is an SQS(N). ∎

**Lemma 4 (XOR Steiner quadruple systems).** Let V = F_2^k (k >= 2), N = 2^k, and Σ = {4-subsets
{a,b,c,d} of V with a ⊕ b ⊕ c ⊕ d = 0}. Every 3-subset of V lies in exactly one member of Σ. In particular
for N = 8: τ(8) = 14 and ex_4(8; K_5^4) = 70 - 14 = 56.

*Proof.* Let {a,b,c} be distinct and d := a ⊕ b ⊕ c. If d = a then b ⊕ c = 0, i.e. b = c, impossible;
likewise d ≠ b, c. So {a,b,c,d} is a 4-set with XOR 0, and it is the only member of Σ containing {a,b,c}
because the fourth element of any such member must equal a ⊕ b ⊕ c. The rest follows from Lemma 3
(C(8,3)/4 = 14). ∎
Computer check (out/check48_mode1.txt): 14 XOR-zero 4-sets, each triple in exactly one; the 4-graph G* of
4-sets with nonzero XOR has 56 edges and 0 copies of K_5^4 (checked directly on all 56 five-sets).
(out/general.txt also checks k = 3, 4, 5.)

**Lemma 5 (averaging).** Let G be an r-graph on V, |V| = N = r+4, with t non-edges, and let P be a packing
of b 3-subsets of V. Then ν(G) >= b - ⌊4bt / C(N,3)⌋.

*Proof.* Let σ be a uniformly random permutation of V. For fixed p ∈ P and fixed 3-set A, exactly
3!(N-3)! of the N! permutations map p onto A, so σ(p) is uniform over the D = C(N,3) three-subsets. Define
X(σ) := Σ_{non-edges e} Σ_{p ∈ P} [σ(p) ⊆ ē]. Since ē has exactly C(4,3) = 4 three-subsets,
E[X] = t · b · 4/D. A random variable on a finite uniform probability space takes some value <= its mean,
so there is σ0 with X(σ0) <= 4bt/D, and since X(σ0) is an integer, X(σ0) <= ⌊4bt/D⌋. If σ0(p) is not full,
then σ0(p) ⊆ ē for some non-edge e, so p contributes at least 1 to X(σ0); hence at most ⌊4bt/D⌋ of the b
sets σ0(p) are not full. The sets σ0(p), p ∈ P, pairwise share <= 1 point (σ0 is a bijection, so
|σ0(p) ∩ σ0(q)| = |p ∩ q|). So at least b - ⌊4bt/D⌋ full 3-sets form a packing, and Lemma 2(c) gives the
bound. ∎

**Lemma 6 (Fano packing on 8 points).** Identify V = {0,...,7} with F_2^3. The family
L = {{a, b, a⊕b} : a, b ∈ V \ {0}, a ≠ b} has exactly 7 members and is a packing.

*Proof.* For distinct nonzero a, b, the element a⊕b is nonzero and differs from a and b, so each member is
a 3-set of nonzero vectors. Conversely a 3-set {x,y,z} of nonzero vectors is in L iff x⊕y⊕z = 0 (if
z = x⊕y it is generated by (x,y); any generating pair forces the third element to be the XOR of the other
two). Each member arises from its 6 ordered pairs, and there are 7·6 = 42 ordered pairs, so |L| = 7. If two
members share two points x ≠ y, the third point of each is x ⊕ y, so they are equal. ∎
Computer check (out/check48_mode1.txt): the 7 lines are {1,2,3},{1,4,5},{2,4,6},{3,5,6},{3,4,7},{2,5,7},
{1,6,7}; any two meet in exactly one point; over all 8! permutations every 3-set is the image of a line
exactly 5040 = 7·8!/56 times (the uniformity used in Lemma 5).

**Proof of Theorem A.** N = 8, r = 4, D = 56, C(8,4) = 70, ex_4(8;K_5^4) = 56 (Lemma 4). Let G have t
non-edges, m = 70 - t.
- If t >= 14: m - 4ν(G) <= m = 70 - t <= 56, with equality iff t = 14 and ν(G) = 0.
- If t <= 13: Lemma 5 with P = L (b = 7) gives ν(G) >= 7 - ⌊28t/56⌋ = 7 - ⌊t/2⌋ >= 7 - t/2. Hence
  m - 4ν(G) <= 70 - t - 28 + 2t = 42 + t <= 55 < 56.
So m - 4ν(G) <= 56 always, with equality iff t = 14 and ν(G) = 0, i.e. iff G is K_5^4-free with 56 edges
(and such G exist, e.g. G* of Lemma 4). By Lemma 1 this is the decomposition statement. ∎

(For the record: the brief's necessary condition for a violation, t + 4ν <= 13, is exactly what Lemma 5
rules out: t + 4ν >= t + 28 - 2t = 28 - t >= 15 for t <= 13.)

**Lemma 7 (sum-zero packing on Z_N).** For N >= 3 let P_N = {3-subsets {i,j,k} of Z_N : i+j+k ≡ 0 mod N}.
Then P_N is a packing and |P_N| >= N(N-3)/6.

*Proof.* If two members share {i,j}, their third elements are both ≡ -(i+j), so they coincide. Call an
unordered pair {i,j} (i ≠ j) *good* if k := -(i+j) mod N is not in {i,j}; then {i,j,k} ∈ P_N. Every member
of P_N contains exactly 3 pairs, all good, and each good pair lies in exactly one member, so
|P_N| = (#good pairs)/3. If {i,j} is bad then -(i+j) ≡ i, giving j ≡ -2i, or -(i+j) ≡ j, giving i ≡ -2j;
either way {i,j} = {x, -2x} for some x ∈ Z_N. There are at most N such pairs, so
|P_N| >= (C(N,2) - N)/3 = N(N-3)/6. ∎
Computer check (out/general.txt): for N = 6..64, P_N is a packing, |P_N| >= N(N-3)/6, and
4|P_N|(N-4) >= C(N,3).

**Proof of Theorem B.** Let N >= 6, r = N-4 >= 2, assume an SQS(N) exists. By Lemma 3, τ(N) = D/4 and
ex := ex_r(N;K_{r+1}^r) = C(N,4) - D/4. Let G have t non-edges; m = C(N,4) - t.
- If t >= D/4: m - rν <= C(N,4) - t <= ex.
- If t < D/4: put s := D/4 - t > 0. Lemma 5 with P = P_N, b = |P_N|, gives
  ν >= b - ⌊4bt/D⌋ >= b - 4bt/D = (4b/D)·s. Hence r·ν >= (N-4)(4b/D)·s >= s, provided
  4b(N-4) >= D. By Lemma 7, 4b(N-4) >= 4·N(N-3)(N-4)/6, and
  4N(N-3)(N-4)/6 >= N(N-1)(N-2)/6 ⟺ 4(N-3)(N-4) >= (N-1)(N-2) ⟺ 3N² - 25N + 46 >= 0,
  which holds for all N >= 6 (value 4 at N = 6; the quadratic is increasing for N >= 25/6).
  Therefore m - rν <= C(N,4) - t - s = C(N,4) - D/4 = ex. ∎

**Proof of Corollary C.** N = 2^k, k >= 3: Lemma 4 gives an SQS(N) (and N >= 8 >= 6). N = 10: the 30
blocks listed in out/general.txt were found by exact-cover search and verified to contain each of the 120
triples of {0,...,9} exactly once. Apply Theorem B. ∎

## 4. Computation (tests of the lemmas; the proofs above do not depend on it)

All code in code/, outputs in out/. Reproduce (from the prove/ folder):

    cd code && cc -O2 -o check48 check48.c && ./check48 1 > ../out/check48_mode1.txt \
      && ./check48 2 5 2 > ../out/check48_mode2_t5.txt && ./check48 3 2000 1 > ../out/check48_mode3.txt
    python3 -I general.py > ../out/general.txt
    cc -O2 -o check_n10 check_n10.c && ./check_n10 300 7 > ../out/check_n10.txt

- `check48 1`: Lemmas 4 and 6 at N = 8 and the uniformity in Lemma 5 (all 8! permutations).
- `check48 2 5 2`: EXHAUSTIVE over all 4-graphs on 8 vertices with t <= 5 non-edges
  (1 + 70 + 2415 + 54740 + 916895 + 12103014 graphs). For each: exact ν via the dual packing (Lemma 2(c));
  check m - 4ν <= 56; check ν >= 7 - ⌊t/2⌋ (Lemma 5 + 6); and, *directly in the original hypergraph*
  (70-bit edge masks, K_5^4 as 5-edge sets, no use of Lemma 2), find ⌈(m-56)/4⌉ edge-disjoint copies;
  for t <= 2 also confirm the direct search reaches the dual ν.
- `check48 3 2000 1`: for t = 6..20, 2000 random non-edge sets plus 20 local-search runs (minimising ν)
  per t; exact ν computed both directly (edge-mask packing) and via Lemma 2(c) and compared; checks
  m - 4ν <= 56 and ν >= 7 - ⌊t/2⌋.
- `general.py`: Lemma 4 for k = 3,4,5; Lemma 7 and the inequality 4b(N-4) >= C(N,3) for N = 6..64; SQS(10).
- `check_n10`: Theorem B at N = 10 (r = 6): random and local-search non-edge sets for t = 0..34; values are
  capped (search stops at bound+2), checks t + 6ν >= 30 and the Lemma 5 bound with b = 12.

### 4a. Results (copied from out/*.txt)
- check48_mode1: 14 XOR-zero 4-sets, each triple covered exactly once, complement-closed; G* has 56 edges,
  0 copies of K_5^4, m - 4ν = 56; 7 Fano lines pairwise meeting in exactly 1 point; every triple is a line
  image exactly 5040 times over the 40320 permutations.
- check48_mode2_t5 (exhaustive, 13,077,135 graphs, t <= 5): 0 violations of m - 4ν <= 56; 0 failures of
  the direct (non-dual) search to find ⌈(m-56)/4⌉ copies; 0 failures of ν >= 7 - ⌊t/2⌋; min ν = 8,8,8,8,7,7
  for t = 0..5; max(m - 4ν) = 38,37,36,35,38,37.
- check48_mode3 (t = 6..20): 0 violations, 0 direct-vs-dual mismatches of exact ν (≈ 30,000 graphs),
  0 failures of ν >= 7 - ⌊t/2⌋. Local search reached ν = 1 at t = 13 and ν = 0 at t = 14, so the
  thresholds in the proof are attained (the Lemma 5 bound is tight at t = 13).
- general.txt: XOR SQS(8), SQS(16), SQS(32) exact; Lemma 7 + 4b(N-4) >= C(N,3) for N = 6..64; an SQS(10)
  (30 blocks, listed) found and verified.
- check_n10.txt: 0 violations of t + 6ν >= 30, 0 failures of the Lemma 5 bound (t = 0..34).

## 5. What this does and does not show

Does show (rigorous, by hand; computation only as cross-check):
- The Erdős–Sauer inequality / decomposition statement of Problem 719 holds for (r, n) = (4, 8), with
  ex_4(8; K_5^4) = 56, and the extremal value of m - 4ν is attained only by the extremal K_5^4-free graphs.
- More generally it holds for (r, n) = (N-4, N) whenever an SQS(N) exists; unconditionally for
  N = 2^k (k >= 3) and N = 10, i.e. (r,n) = (4,8), (6,10), (12,16), (28,32), ...
- The value of ex_r(N; K_{r+1}^r) for these N: C(N,4) - C(N,3)/4.

Does not show:
- Anything for n = r+4 when no SQS(n) exists (n odd, or n ≡ 0 mod 6). There τ(N) > C(N,3)/4 and the
  averaging bound, which only "pays back" C(N,3)/4 - t, is not enough as written; for odd N the
  Schönheim-type excess is of order N²/24 (INFERRED, not computed), which exceeds what the argument
  provides. This is the natural next case, e.g. (r,n) = (5,9).
- The full N ≡ 2, 4 (mod 6) family is only CONDITIONAL on Hanani's existence theorem (not read).
- Nothing about n >= r+5 for r >= 4, nor about the general conjecture.
- No Lean formalization.

VERIFIED vs INFERRED: every lemma above is proved in full here and tested by the listed computations.
The only statements taken from memory are Hanani's theorem (Corollary C' only) and the remark about the
size of the covering excess for odd N; both are marked and nothing in Theorems A, B or Corollary C uses
them.

## 6. Sources not read

- Hanani, "On quadruple systems" (Canad. J. Math. 1960) — existence of SQS(N) for N ≡ 2,4 mod 6.
- Erdős [Er81] (Combinatorica 1, 1981) original statement — read only via erdosproblems.com and Plasma.
- Zeraoulia's Zenodo preprint (r = 3, n <= 9) — not read (only the Plasma/forum summaries).
- MathSciNet / Sauer's papers; any literature on covering numbers C(v,4,3) (Turán (4,3) covering).
- Sibling workspace t1 (n = r+3) — not re-verified.
