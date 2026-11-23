# Erdős #643, t = 3: exact values of f_3(n) for 6 <= n <= 11 (computer-assisted)

Notation: an *avoiding* family is a family F of 3-subsets of an n-set with no four
distinct members A, B, C, D such that A ∪ B = C ∪ D and A ∩ B = C ∩ D = ∅.
f_3(n) is the largest size of an avoiding family on n points, so the problem's
f(n;3) equals f_3(n) + 1. Füredi's lower bound is
F(n) = C(n-1,2) + floor((n-1)/3): take all triples through one point, plus
floor((n-1)/3) pairwise disjoint triples that avoid that point.

## Statement established

**Theorem.** f_3(6) = 11, f_3(7) = 17, f_3(8) = 23, f_3(9) = 30, f_3(10) = 39 and
f_3(11) = 48. In each case this equals Füredi's lower bound F(n). So
f(n;3) = 12, 18, 24, 31, 40, 49 for n = 6, ..., 11.

Up to isomorphism, the extremal families are as follows:
* n = 6: 18 classes. These are all the families with 11 members.
* n = 7, 8, 10, 11: exactly one class each. It is Füredi's construction (C1).
  For n = 11 the uniqueness comes from the C code only. Python confirmed the
  upper bound 48 at n = 11 but was not run at THR = 48.
* n = 9: exactly two classes. One is (C1). The other (C2) is (C1) with one
  star triple swapped for a triple that meets one of the matching triples.
  These are the r = 3 analogues of the two Huang–Ma–Yang extremal families.

**Status:** this is computer-assisted. The upper bounds come from an exhaustive
isomorph-free classification. It was implemented twice, in C and in Python,
and the two codebases share no code. Both reproduce the same class counts at
every level, and labeled counts give an extra check (see §4). The lower bounds
come from explicit families saved to files and checked against the definition.

Here n = 8, 9, 10 answer the scout's target T1. The value at n = 11 is a bonus.
§6 adds **f_3(12) = 58**, verified by the C implementation only.

## 1. Lemmas

Throughout, [n] = {0, ..., n-1}. A family on [n] is a set of 3-subsets of [n].

**Lemma 1 (local form).** F is avoiding iff every 6-set S has at most one
partition {A, B} into two triples with A, B ∈ F.

*Proof.* Suppose A, B, C, D are distinct members with A ∪ B = C ∪ D = S and
A ∩ B = C ∩ D = ∅. Then |S| = 6, and {A,B} and {C,D} are partitions of S. They
are different partitions, because the four sets are distinct. Conversely, take
two different partitions {A,B} ≠ {C,D} of the same 6-set S with all four parts
in F. Then A ≠ B, since they are disjoint and nonempty, and likewise C ≠ D.
Suppose A = C. Then B = S \ A = S \ C = D, so {A,B} = {C,D}, a contradiction.
Suppose A = D. Then B = C, the same contradiction. The cases B = C and B = D
are symmetric. So A, B, C, D are four distinct members forming the forbidden
configuration. ∎

**Lemma 2 (heredity, invariance).** A subfamily of an avoiding family is
avoiding. If F is avoiding on [n+1] and v ∈ [n+1], then F − v := {T ∈ F : v ∉ T}
is an avoiding family on [n+1] \ {v}. Any image σ(F) of F under a bijection σ
of the ground set is avoiding iff F is.

*Proof.* The forbidden configuration is four members of the family. Any four
members of a subfamily are also four members of F. The condition is defined
only through ∪, ∩ and equality, and a bijection preserves all three. ∎

**Lemma 3 (one-vertex extension).** Let H be a family on [n], let w = n be a new
vertex, and let L be a set of pairs of [n]. Put G = H ∪ {p ∪ {w} : p ∈ L}.
(Every family G on [n+1] has this form, with H = G − w and L the link of w.)
Call two distinct pairs p, q of [n] *H-conflicting* if some 5-set Q ⊆ [n] has
p ∪ q ⊆ Q, Q \ p ∈ H and Q \ q ∈ H. Then G is avoiding iff H is avoiding and no
two pairs of L are H-conflicting.

*Proof.* (⇒) H ⊆ G, so H is avoiding by Lemma 2. Suppose p, q ∈ L conflict
via Q, and put S = Q ∪ {w}, a 6-set. The sets p∪{w} and Q\p are disjoint
members of G whose union is S. The same holds for q∪{w} and Q\q. The two
partitions {p∪{w}, Q\p} and {q∪{w}, Q\q} differ, because their w-parts differ
(p ≠ q). By Lemma 1, G is not avoiding.
(⇐) Suppose G is not avoiding. By Lemma 1 some 6-set S has two different
partitions {A,B} ≠ {C,D} with all four parts in G. If w ∉ S, all four parts
lie in H, so H is not avoiding. If w ∈ S, then w lies in exactly one part of
each partition, say w ∈ A and w ∈ C. Since A, C ∈ G contain w, we have
A = p ∪ {w} and C = q ∪ {w} with p, q ∈ L. Also B, D ∈ G do not contain w, so
B, D ∈ H. Put Q = S \ {w}. Then B = Q \ p and D = Q \ q. If p = q, then A = C
and B = D, so the partitions agree, a contradiction. So p ≠ q, and p, q
conflict via Q. ∎

So the extensions of a fixed H are exactly the independent sets L of the
*conflict graph* K(H) on the C(n,2) pairs of [n]. The forbidden configurations
that involve w are pairwise constraints on L.

**Lemma 4 (minimum degree).** If G is a family on N vertices with e members,
some vertex v has deg(v) ≤ floor(3e/N). Then |G − v| ≥ e − floor(3e/N).

*Proof.* The degrees sum to 3e, so the minimum degree is at most 3e/N, and it
is an integer. G − v loses exactly the deg(v) members that contain v. ∎

**Lemma 5 (monotone threshold).** For N ≥ 3, g(e) = e − floor(3e/N) is
nondecreasing in e.

*Proof.* g(e+1) − g(e) = 1 − (floor(3(e+1)/N) − floor(3e/N)). Since 3/N ≤ 1,
the floor increases by at most 1, so the difference is ≥ 0. ∎

**Theorem 6 (completeness of the classification).** Fix a target size THR on
N points. Put thr_N = THR and thr_n = max(0, thr_{n+1} − floor(3·thr_{n+1}/(n+1)))
for 3 ≤ n < N. Define lists Λ_n as follows.
* Λ_3 contains ∅ and {{0,1,2}}, keeping those with at least thr_3 members.
* Λ_{n+1} is built from each H ∈ Λ_n. Enumerate every independent set L of
  K(H) such that |H| + |L| ≥ thr_{n+1} and w = n has minimum degree in
  G = H ∪ w·L, that is, |L| ≤ deg_G(u) for all u ∈ [n]. Store some family
  isomorphic to each such G.

Then every avoiding family on [n] with at least thr_n members is isomorphic
to a member of Λ_n. Every member of Λ_n is avoiding and has at least thr_n
members. In particular, f_3(N) ≥ THR iff Λ_N ≠ ∅.

*Proof.* Soundness: every stored G is avoiding by Lemma 3 (induction on n),
and it has at least thr_{n+1} members by construction. Stored copies are
isomorphic images, so Lemma 2 applies.

Completeness, by induction on n. The base case n = 3 lists every family on [3]
of the required size. For the step, let G be avoiding on [n+1] with
e ≥ thr_{n+1} members. By Lemma 4, choose v of minimum degree
δ ≤ floor(3e/(n+1)), and let σ swap v and w = n. In G1 = σ(G), the vertex w
has minimum degree δ. By Lemma 2, H1 = G1 − w is avoiding on [n], and by
Lemmas 4 and 5, |H1| = e − δ ≥ g(e) ≥ g(thr_{n+1}) ≥ thr_n. By induction there
is τ ∈ Sym([n]) with τ(H1) = H ∈ Λ_n. Extend τ by τ(w) = w. Then
G2 = τ(G1) = H ∪ w·L, where L = τ(link_{G1}(w)) and |L| = δ. G2 is avoiding, so
L is independent in K(H) by Lemma 3. Also |H| + |L| = e ≥ thr_{n+1}, and w
still has minimum degree, because τ preserves degrees. So the enumeration
visits G2 ≅ G and stores a copy isomorphic to it. ∎

*Remark (the canonical form is not load-bearing).* The code stores canon(G),
the smallest bitmask among the images of G under a set of vertex permutations.
canon(G) is always an isomorphic copy of G, which is all Theorem 6 needs. If
the colour refinement used to restrict those permutations were buggy, the only
effect would be duplicate representatives, which costs speed but never
correctness. For the same reason, a hash collision in the colour refinement
cannot lose a family.

## 2. Algorithm and code

* `code/classify.c` (128-bit masks, n ≤ 10) and `code/classify_big.c`
  (256-bit masks, n ≤ 12). These implement Theorem 6 directly.
  * K(H) is built from the 5-set rule of Lemma 3.
  * L is enumerated by include/exclude backtracking over the pairs. The only
    pruning is |L| + #(still allowed pairs) ≥ need, which is valid because L
    can only grow by allowed pairs.
  * The minimum-degree test is applied at the leaves.
  * Every stored family is re-checked against Lemma 1 by an independent routine
    (`is_avoiding`). The count "non-avoiding found" is 0 in every run.
  * For each level, the program also prints max(|H| + α(K(H))) over Λ_n. This
    is only a sanity statistic.
* `code/verify_py.py` is an independent re-implementation that shares no code
  with the C programs. It tests avoidance straight from the definition, by
  grouping disjoint pairs of members by their union. It finds conflicts by
  brute-force avoidance tests of H + {p∪w, q∪w}, not by the 5-set rule. It uses
  a different canonical form: permutations respecting the invariant
  (degree, sorted codegree multiset). It also asserts that every generated G is
  avoiding.
* `code/dfs_count.c` is a labeled exhaustive search over all triples. It uses
  no symmetry reduction and no lemma beyond the definition. It counts the
  labeled avoiding families of exactly M members on [n] (n ≤ 8).
* `code/labeled_check.py` reads a dump of classes. It re-checks avoidance by
  the definition and computes |Aut| by brute force over all n! permutations.
  It checks that the classes are pairwise non-isomorphic, using the full-S_n
  minimum image, and outputs Σ n!/|Aut| per size, which should equal the
  labeled count.
* `code/cpsat.py` and `code/cpsat2.py` are OR-tools CP-SAT models. **They
  contributed nothing.** The n = 8, k = 24 run hit its time limit with no
  verdict. On this shared machine the n = 7, k = 18 re-run sat at about 0% CPU
  for 30 minutes and was killed. No CP-SAT result is claimed.
* `code/check_avoid.py` is a definition-based avoidance check of the extremal
  dumps. It also prints the degree sequences (`out/check_avoid.txt`).

Reproduce, from `code/`:
```
gcc -O2 -o classify classify.c && gcc -O2 -o classify_big classify_big.c && gcc -O2 -o dfs_count dfs_count.c
for a in "6 0" "7 17" "7 18" "8 23" "8 24" "9 30" "9 31" "10 39" "10 40"; do eval "./classify $a"; done   # -> out/classify_runs.txt
./classify_big 11 49 ; ./classify_big 11 48 ../out/n11_size48.txt                                       # -> out/classify_big_11_*.txt
for a in "7 17" "7 18" "9 30" "9 31" "10 39" "10 40"; do eval "python3 -I verify_py.py $a"; done         # -> out/verify_py.txt
python3 -I verify_py.py 8 24 ; python3 -I verify_py.py 8 23 ; python3 -I verify_py.py 6 0
./dfs_count 7 15; ./dfs_count 7 16; ./dfs_count 7 17; ./dfs_count 7 18
./classify 7 15 ../out/n7_ge15.txt; python3 -I labeled_check.py 7 ../out/n7_ge15.txt
./classify 6 0 ../out/n6_all.txt;  python3 -I labeled_check.py 6 ../out/n6_all.txt
python3 -I labeled_check.py 8 ../out/n8_size23.txt
python3 -I labeled_check.py 9 ../out/n9_size30.txt; python3 -I labeled_check.py 10 ../out/n10_size39.txt
./dfs_count 8 24; ./dfs_count 8 23                       # -> out/dfs_count_n8.txt (about 5 + 8 min)
python3 -I verify_py.py 11 49                            # -> out/verify_py_11_49.txt (about 50 min on a loaded machine)
./classify_big 12 59                                     # -> out/classify_big_12_59.txt (about 8 min)
```
Total run time is seconds for the C classification and minutes for the
Python checks.

## 3. Results (VERIFIED by computation)

The values below come from `out/classify_runs.txt` and
`out/classify_big_11_49.txt`.

| n | thresholds thr_3..thr_n used for "≥ F(n)+1" | Λ_n for THR = F(n)+1 | max over Λ_{n-1} of \|H\|+α(K(H)) | F(n) | classes of size F(n) |
|---|---|---|---|---|---|
| 7 | 1,3,6,11,18 | empty | 17 | 17 | 1 |
| 8 | 1,2,5,9,15,24 | empty | 23 | 23 | 1 |
| 9 | 1,2,4,8,14,21,31 | empty | 30 | 30 | 2 |
| 10 | 1,2,4,7,12,19,28,40 | empty | 39 | 39 | 1 |
| 11 | 1,2,4,7,12,18,26,36,49 | empty | 48 | 48 | 1 |

n = 6 was classified completely (THR = 0). It has 568 classes, and the maximum
size is 11 with 18 classes.

Level sizes for the n = 10 run (THR = 40). These match across runs with
different targets wherever the size ranges overlap.

| level | thr | classes | by size |
|---|---|---|---|
| 7 | 12 | 8600 | 12:6071 13:2116 14:366 15:42 16:4 17:1 |
| 8 | 19 | 3470 | 19:2952 20:448 21:60 22:9 23:1 |
| 9 | 28 | 162 | 28:142 29:18 30:2 |
| 10 | 40 | 0 | |

The n = 11 run (THR = 49) adds these levels:
* level 8 (thr 18): 18:19248 and above as before.
* level 9 (thr 26): 10213 classes.
* level 10 (thr 36): 466 classes (36:415 37:46 38:4 39:1).
* level 11: empty.

Extremal families (saved; each line is "size triples..." with vertices
written as digits, and 10 written as "10" in the n = 11 file):
* `out/n7_size17.txt`
* `out/n8_size23.txt`: the star at 7 plus {2,3,4} and {0,1,5}. Over the 8
  points this is Füredi's (C1).
* `out/n9_size30.txt` holds two families:
  * (C1): the star at 6 (28 triples) plus {2,3,4} and {0,1,5}.
  * (C2): the star at 5 minus {5,7,8}, plus {2,3,4}, {0,1,6} and {6,7,8}.
* `out/n10_size39.txt`: the star at 9 plus {0,1,8}, {2,3,7} and {4,5,6}.
* `out/n11_size48.txt`: the star at 10 plus three disjoint triples.

## 4. Independent cross-checks

1. **Python re-implementation** (`out/verify_py.txt`, `out/verify_py_11_49.txt`,
   plus the n = 6 and n = 8 runs). Its class counts are identical to the C
   code at every level, for n = 6 (THR 0), 7 (17, 18), 8 (23, 24),
   9 (30, 31), 10 (39, 40) and **11 (49)**. The n = 11 run gives these
   levels:
   * level 7 (thr 12): 8600 classes
   * level 8 (thr 18): 22718
   * level 9 (thr 26): 10213
   * level 10 (thr 36): 466
   * level 11: 0, after 49 min. It also finds Λ empty at F(n)+1, and 1, 1, 2, 1 classes at F(n)
   for n = 7, 8, 9, 10.
2. **Labeled counts with no symmetry and no lemmas** (`dfs_count`). These match
   Σ n!/|Aut| over the classified classes exactly:
   * n = 6: 5120 families of size 11 and 24064 of size 10. These agree with the
     closed form (1+2x)^10 + 10x^2(1+2x)^9, which counts n = 6 families via
     Lemma 1 (10 complementary pairs, at most one pair fully present).
   * n = 7: 78484 of size 15, 2450 of size 16, 70 of size 17, and **0 of size
     18**. This proves f_3(7) = 17 without the extension machinery.
   * n = 8: **0 families of size 24**, after 5,028,460,613 search nodes. This
     proves f_3(8) ≤ 23 using nothing but the definition. There are **560
     families of size 23** (7,505,935,562 nodes). This equals 8!/72, so every
     23-family is a relabeling of the single classified class, which confirms
     uniqueness independently. See `out/dfs_count_n8.txt`.
3. **Full-S_n orbit sums** (`labeled_check.py`). The 568 classes at n = 6
   reproduce, size by size, the coefficients of
   (1+2x)^10 + 10x^2(1+2x)^9 (for example x^2: 190 and x^9: 51200). The 47
   classes at n = 7 of size ≥ 15 give 78484, 2450 and 70, equal to
   dfs_count. The n = 8 extremal class has |Aut| = 72 and gives 560 labeled
   copies, which equals dfs_count. At n = 9, the two classes give 17640
   labeled families of size 30 in total. At n = 10, the single class gives
   2800 = 10!/1296 (`out/labeled_check_n9_n10.txt`).
4. The lower bounds are verified directly: every family in the out/*.txt files
   passes the definition-based avoidance test in `labeled_check.py`. The
   families also match Füredi's explicit construction, so F(n) ≤ f_3(n) is in
   any case a theorem (Füredi 1984; the construction's validity is a two-line
   check).

## 5. What this does and does not show

* It shows the exact values f_3(n) = F(n) for 6 ≤ n ≤ 11. It also shows the
  classification of extremal families up to isomorphism for 7 ≤ n ≤ 11.
* For these n, f_3(n) < C(n,2). So Zhang's bound f_3(n) ≤ C(n,2) is not
  attained for 6 ≤ n ≤ 11. This is consistent with Zhang's equality cases,
  which are n ≡ 1, 5 (mod 20).
* It is a finite computation. It says nothing about general n. In particular
  it does not decide the smallest n > 5 with f_3(n) > F(n). Such n exist: for
  n = 21, Füredi's Steiner-system family has 210 > 196 = F(21) members.
* The proof is computer-assisted. Its correctness rests on Lemmas 1–5 and
  Theorem 6, which are proved above, and on the code. Code correctness is
  supported by two independent implementations that agree level by level, by
  labeled exhaustive counts that need no lemmas (n ≤ 7, and n = 8 if finished),
  and by orbit-sum identities. There is no formal (Lean or DRAT) certificate.
* Novelty is INFERRED, not verified. The values may appear in sources not read
  (below). Zhang's arXiv paper (intro read; full text grepped for "small",
  "computer", "table", "exhaust") and the HMY preprint (grepped) contain no
  small-n table. Plasma, the forum and the erdosproblems.com page list no small
  values.

## 6. n = 12 (single implementation only)

`./classify_big 12 59` returns Λ_12 = ∅ (`out/classify_big_12_59.txt`, 8.5 min
wall). Its levels and thresholds are:

| level | thr | classes |
|---|---|---|
| 7 | 10 | 28391 |
| 8 | 16 | 701383 |
| 9 | 24 | 471241 |
| 10 | 33 | 314683 |
| 11 | 45 | 1359 |
| 12 | 59 | 0 |

The maximum of |H| + α(K(H)) over Λ_11 is 58.

Together with Füredi's construction, this gives **f_3(12) = 58 = F(12)**.
The status is weaker than for n ≤ 11. The run used only the C code, because
the Python re-implementation is too slow at this size. Still, the C code is
the same one that agreed with Python at every level for n ≤ 11, and the
level-7/8 size histograms of this run agree with the n ≤ 11 runs on their
common size range. I count n = 12 as VERIFIED by one implementation. The
headline theorem keeps it separate.

I did not classify the extremal 58-families at n = 12. The run
`classify_big 12 58` has lower thresholds, and it reached 2,343,774 classes at
level 10. I stopped it at the 40-minute cap (`out/classify_big_12_58.txt`).
Füredi's (C1) on 12 points attains 58. Whether the analogue of (C2) also
attains it (3 | 12) is unchecked.

## Sources not read

* Füredi, Combinatorica 4 (1984), full text. Only Plasma's library summary was
  read; it mentions no small-n values.
* Pikhurko–Verstraëte, JCTA 116 (2009), full text.
* Huang–Ma–Yang arXiv:2609.37744. Downloaded to refs/ and grepped only.
* Zhang arXiv:2610.34038. Introduction read, rest grepped only.
* Mubayi–Verstraëte; Marchant (cited by Zhang), not read.
* OEIS was not searched for the sequence 11, 17, 23, 30, 39, 48.

## Notes

* The brief's path `t1/prove/../SCOUT.md` does not exist. The scout notes I
  read are at `attack/643/SCOUT.md`.
* Pre-check, done before starting:
  * The erdosproblems.com/643 page and forum thread (3 comments) give no
    small values.
  * Plasma's E0643 page and its Zhang claim page say exact f(n;3) for n not
    ≡ 1, 5 (mod 20) is open.
  * Zhang's and HMY's arXiv texts show no small-n table under the greps
    listed.
* Sequence of f_3(n) for n = 3..12, with n ≤ 5 trivial since f_3(n) = C(n,3)
  there: 1, 4, 10, 11, 17, 23, 30, 39, 48, 58.
