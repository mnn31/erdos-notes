# Erdős #902, Target A: Cayley tournaments with property S_4 of order 49..65

## Outcome: DISPROVED (computer-assisted, exhaustive)

**Statement established (Theorem).** No Cayley tournament on a group of order n with
31 <= n <= 65 has Schütte's property S_4. (A Cayley tournament must have odd order, and
an S_4 tournament with all in-degrees (n-1)/2 has n >= 31, both by elementary lemmas below.)
The Paley tournament QRT_67 = Cay(Z_67, quadratic residues) has S_4. **So the smallest
order of a Cayley tournament with S_4 is exactly 67.**

In particular the target ("is there a Cayley tournament with S_4 on a group of odd order n,
49 <= n <= 65?") has answer **no**. The 48 <= f(4) <= 67 gap cannot be closed from above by any
Cayley (group-based, vertex-transitive-by-a-regular-group) construction.

This re-verifies, and extends from cyclic groups to all groups, Fisher's unpublished
computation reported in RMHH04 p.166 ("the smallest rotational tournament with domination
number 5 is QRT_67").

The proof is a finite exhaustive computation. Its correctness rests on the lemmas below plus
the correctness of the code. Two independently written checkers (different formulation,
different enumeration, one with and one without the symmetry reduction) agree. Both also
match a third brute-force checker (Python, no reductions at all) on every small case where
that one can finish. See "What this does and does not show".

---

## Status check before working (VERIFIED, 2026-11-23)

- erdosproblems.com/902 (fetched, refs/page.html): OPEN; the page states f(1)=3, f(2)=7, f(3)=19
  and the bounds 2^{n+1}-1 <= f(n) << n^2 2^n, plus n 2^n << f(n). Nothing on Cayley or vertex-transitive tournaments.
- Forum thread (refs/forum.html): 4 comments (Lean formalisation of the classical bounds; GrSp71 is
  "weaker"). Nothing on f(4) or Cayley tournaments.
- Plasma E0902 (refs/plasma__index.md, updated 2026-10-08): "48 <= f(4) <= 67", status open, no
  Cayley/vertex-transitive claim.
- RMHH04 (../../refs/rmhh04.txt, p.166): Fisher's computation covers *rotational* (circulant)
  tournaments only.
- Two web searches ("smallest 4-paradoxical tournament Cayley vertex-transitive", "Schütte property
  S_4 tournament 67 smallest known circulant"): nothing on non-cyclic Cayley tournaments with S_4.
  The second search turned up Jeffries arXiv:2604.08790 and Javier–Llano–Zuazua (QR_p is S_4 iff
  every in/out-neighbourhood is S_3; QR_67 is S_4) per the search summary. I did not read either paper.

So as far as I could check, the non-cyclic Cayley case is not recorded anywhere.

---

## Definitions and conventions

- A tournament T has property **S_k** if every k-set A of vertices has a vertex z ∉ A with
  z -> a for all a ∈ A (RMHH04 p.161: S_k iff domination number γ(T) > k).
- G a finite group, identity e. A **tournament connection set** is S ⊆ G with
  S ∩ S^{-1} = ∅ and S ∪ S^{-1} = G \ {e}. The **Cayley tournament** Cay(G,S) has vertex set G and
  arc x -> y iff x^{-1} y ∈ S.

## Lemma 1 (basic facts)

(a) Cay(G,S) is a tournament.
(b) If G has a tournament connection set then |G| is odd.
(c) For g ∈ G, L_g : x ↦ gx is an automorphism of Cay(G,S).
(d) For a group isomorphism φ: G -> G' (in particular φ ∈ Aut(G)), φ is a tournament isomorphism
    Cay(G,S) -> Cay(G',φ(S)), and φ(S) is a tournament connection set of G'.
(e) (Convention independence.) Let Cay'(G,S) have arcs x -> y iff y x^{-1} ∈ S. Then
    ψ(x) = x^{-1} is an isomorphism Cay'(G,S^{-1}) -> Cay(G,S). Hence the class of Cayley
    tournaments on G is the same under either convention.

*Proof.* (a) For x ≠ y, g = x^{-1}y ≠ e, and exactly one of g ∈ S, g^{-1} ∈ S holds (because
S ∪ S^{-1} = G\{e} and S ∩ S^{-1} = ∅). Here g ∈ S means x -> y. And g^{-1} = y^{-1}x ∈ S means
y -> x. So exactly one arc joins x and y. There are no loops because e ∉ S (e ∉ G \ {e}).
(b) Suppose |G| is even. By Cauchy's theorem G has an element g of order 2, so g = g^{-1}. If g ∈ S
then g ∈ S ∩ S^{-1}, which is impossible. If g ∉ S then g^{-1} = g ∉ S, so g ∉ S ∪ S^{-1}, which is
also impossible.
(c) (gx)^{-1}(gy) = x^{-1}y.
(d) φ(x)^{-1}φ(y) = φ(x^{-1}y), which lies in φ(S) iff x^{-1}y ∈ S. φ is a bijection that preserves
inverses and fixes e, so φ(S) ∩ φ(S)^{-1} = φ(S ∩ S^{-1}) = ∅ and φ(S) ∪ φ(S)^{-1} = φ(G \ {e}) = G' \ {e'}.
(e) In Cay(G,S), ψ(x) -> ψ(y) iff x y^{-1} ∈ S iff (x y^{-1})^{-1} = y x^{-1} ∈ S^{-1}. That is the
arc x -> y of Cay'(G,S^{-1}). Since S ↦ S^{-1} is a bijection on tournament connection sets, the
two conventions give the same isomorphism classes. ∎

## Lemma 2 (reduction of S_k to (k-1)-subsets of G\{e})

For k >= 1 with k <= |G|-1, Cay(G,S) has S_k iff for every (k-1)-subset B ⊆ G\{e} there is
t ∈ S with tB ⊆ S. Equivalently, with R(a) := { t ∈ S : ta ∈ S }:
for all distinct a_1,…,a_{k-1} ∈ G\{e}: R(a_1) ∩ … ∩ R(a_{k-1}) ≠ ∅.

*Proof.* z dominates a set A iff z^{-1}x ∈ S for all x ∈ A. Write t = z^{-1}. Then this says tA ⊆ S.
Also z ∉ A holds automatically, since z -> z is impossible (no loops).
(=>) Let B be a (k-1)-subset of G\{e}. Then A = {e} ∪ B is a k-set, so by S_k some z dominates it.
Put t = z^{-1}. From e ∈ A we get t = te ∈ S, and tB ⊆ S.
(<=) Let A be any k-set and pick b_0 ∈ A. Then A' = b_0^{-1}A is a k-set containing e, so
B = A' \ {e} is a (k-1)-subset of G\{e}. By hypothesis there is t ∈ S with tB ⊆ S, and also
te = t ∈ S, so tA' ⊆ S. Then z' = t^{-1} dominates A'. By Lemma 1(c), L_{b_0} maps A' onto A and
z' to a vertex b_0 z' that dominates A. The two forms agree: t ∈ R(a) for all a ∈ B iff
t ∈ S and tB ⊆ S. ∎

## Lemma 3 (halving the search)

Let G = Z_m ⋊_r Z_k × Z_d (the encoding used below: elements (x,y,w), product
(x1,y1,w1)(x2,y2,w2) = (x1 + r^{y1}x2, y1+y2, w1+w2) with r^k ≡ 1 mod m), let m >= 3 and
g_0 = (1,0,0). Then φ(x,y,w) = (-x,y,w) is an automorphism of G with φ(g_0) = g_0^{-1}. Therefore
every Cayley tournament on G is isomorphic to some Cay(G,S) with g_0 ∈ S.

*Proof.* φ is a bijection (it is an involution). φ(a)φ(b) = (-x1 + r^{y1}(-x2), y1+y2, w1+w2)
= φ(ab). Also g_0^{-1} = (-1,0,0) = φ(g_0). If g_0 ∉ S then g_0^{-1} ∈ S, so g_0 = φ(g_0^{-1})
∈ φ(S), and Cay(G,S) ≅ Cay(G,φ(S)) by Lemma 1(d). ∎
(The code also checks at run time, from the multiplication table, that φ is a bijective
homomorphism with φ(g_0) = g_0^{-1}.)

## Lemma 4 (lower bound n >= 31 for Cayley S_4; elementary)

(a) If T has S_k (k >= 2) and v is any vertex, then T[N^-(v)] has S_{k-1}, where N^-(v) is the
set of in-neighbours of v.
(b) No tournament on <= 2 vertices has S_1.
(c) A Cayley tournament of order n with S_k has (n-1)/2 >= g(k-1), where g(j) is the least order
of an S_j tournament. Hence g(1) >= 3, g(2) >= 7, g(3) >= 15, and a Cayley S_4 tournament has
n >= 31.

*Proof.* (a) Let A ⊆ N^-(v) with |A| = k-1. The k-set A ∪ {v} has a dominator z ∉ A ∪ {v}. Then
z -> v, so z ∈ N^-(v), and z ∉ A with z -> a for all a ∈ A.
(b) A 1-vertex tournament: its vertex has no in-neighbour. A 2-vertex tournament: the winner has no
in-neighbour. S_1 requires every vertex to have an in-neighbour.
(c) In Cay(G,S) the in-neighbourhood of every vertex has size |S^{-1}| = (n-1)/2. By (a) it carries
an S_{k-1} tournament, so (n-1)/2 >= g(k-1). For a general tournament, pick v of minimum in-degree,
which is <= (n-1)/2 (the average). This gives g(k) >= 2g(k-1)+1. From (b), g(1) >= 3, so g(2) >= 7,
g(3) >= 15, and a Cayley S_4 tournament has (n-1)/2 >= 15. ∎

(The sharper published f(3) = 19 and f(4) >= 48 are not needed. The computation covers every odd
order from 31 to 65 directly.)

## Lemma 5 (all groups of odd order 31 <= n <= 65)

Up to isomorphism these are:
- n prime (31,37,41,43,47,53,59,61): Z_n.
- n = 33, 35, 51, 65: cyclic only.
- n = 39: Z_39, Z_13 ⋊ Z_3.  n = 45: Z_45, Z_3 × Z_15.
- n = 49: Z_49, Z_7 × Z_7.  n = 55: Z_55, Z_11 ⋊ Z_5.  n = 57: Z_57, Z_19 ⋊ Z_3.
- n = 63: Z_63, Z_3 × Z_21, Z_7 ⋊ Z_9, Z_3 × (Z_7 ⋊ Z_3).

That is 9 + 2 = 11 groups of order 31..47 and 15 groups of order 49..65.

*Proof* (standard Sylow arguments).
**pq case (p < q primes).** The Sylow q-subgroup Q is normal: n_q ≡ 1 (mod q) and n_q | p < q force
n_q = 1. So G = Q ⋊ P with P ≅ Z_p acting through θ: Z_p -> Aut(Z_q) ≅ Z_{q-1}.
If p ∤ q-1, θ is trivial and G ≅ Z_{pq}. This covers 33 = 3·11, 35 = 5·7, 51 = 3·17 and 65 = 5·13,
since 3∤10, 5∤6, 3∤16 and 5∤12.
If p | q-1, Aut(Z_q) is cyclic and has a unique subgroup of order p. Any two nontrivial θ, θ' then
satisfy θ' = θ ∘ (y ↦ y^j) for some unit j mod p. The map (x,y) ↦ (x, y^{j'}), with j' the inverse
of j, is then an isomorphism between the two semidirect products. So there is exactly one nonabelian
group. This covers 39 = 3·13, 55 = 5·11 and 57 = 3·19.
**p^2 (49).** Groups of order p^2 are abelian: Z_49 or Z_7^2.
**45 = 3^2·5.** n_5 | 9 and n_5 ≡ 1 mod 5 give n_5 = 1. n_3 | 5 and n_3 ≡ 1 mod 3 give n_3 = 1.
So G = P_3 × P_5 is abelian: Z_45 or Z_3 × Z_15.
**63 = 3^2·7.** n_7 | 9 and n_7 ≡ 1 mod 7 give n_7 = 1, so G = Z_7 ⋊ P with |P| = 9, acting via
θ: P -> Aut(Z_7) ≅ Z_6. The image has order 1 or 3.
- In both cases a nontrivial θ has image {1, 2, 4} = ⟨2⟩ ⊂ Z_7^*. If y ∈ P has θ(y) = 4 then
  θ(y^2) = 16 ≡ 2, and y^2 has the same order as y (3 and 9 are odd), so one can choose y with θ(y) = 2.
- P = Z_9: trivial θ gives Z_63. Nontrivial θ: take a generator y with θ(y) = ×2. The group is then
  Z_7 ⋊_2 Z_9 (the multiplication rule is determined), so there is one group, Z_7 ⋊ Z_9.
- P = Z_3^2: trivial θ gives Z_3 × Z_21. Nontrivial θ: the kernel K has order 3. Choose y ∉ K with
  θ(y) = ×2, so P = K × ⟨y⟩. K acts trivially on Z_7 and P is abelian, so K is central. H = Z_7⟨y⟩ ≅
  Z_7 ⋊_2 Z_3 is normalised by Z_7, y and K, so it is normal. K ∩ H = 1 by orders, so
  G = K × H ≅ Z_3 × (Z_7 ⋊ Z_3). One group.
(The same "choose a generator with θ(y) = r" argument proves uniqueness in the pq case.)
The constructions in code/groups.h use the parameters (m,k,r,d):
Z_13⋊Z_3 (13,3,3,1), Z_11⋊Z_5 (11,5,3,1), Z_19⋊Z_3 (19,3,7,1), Z_7⋊Z_9 (7,9,2,1),
Z_3×(Z_7⋊Z_3) (7,3,2,3), and the direct products Z_7×Z_7 (7,1,1,7), Z_3×Z_15 (15,1,1,3),
Z_3×Z_21 (21,1,1,3). In each case r has the required multiplicative order: 3^3≡1 (13),
3^5≡1 (11), 7^3≡1 (19), 2^3≡1 (7).
VERIFIED by computation (out/groupinfo.txt, code/groupinfo.py): each table is closed and
associative (a full check in groups.h; a random check in Python), with identity and inverses. Groups
of equal order are pairwise non-isomorphic, which shows in the abelian flag and the element-order
histograms. For example, at order 63: Z_63 has elements of order 63; Z_3×Z_21 is abelian with
max order 21; Z_7⋊Z_9 is nonabelian with 42 elements of order 9; Z_3×(Z_7⋊Z_3) is nonabelian with
no element of order 9. So every isomorphism class in the list is realised. ∎

(The group list for order 63 relies on standard Sylow/semidirect-product facts that I did not check
with GAP. The 4 groups of order 63 and the 2 of orders 39, 45, 49, 55, 57 match the well-known
counts of groups of these orders. That is INFERRED from memory, but the proof above does not use it.)

## Proposition 6 (the computation). VERIFIED by exhaustive computation

For each of the 26 groups G of Lemma 5, no tournament connection set S with g_0 ∈ S makes
Cay(G,S) satisfy the criterion of Lemma 2 with k = 4. Together with Lemma 3, no Cayley tournament
on any of these groups has S_4.

Table (code/search, halved enumeration; out/main/run_all.log, out/main/run_49_51.log,
out/small/run_small.log):

| group | n | sets tested (= 2^((n-1)/2 - 1)) | S_4 sets found |
|---|---|---|---|
| Z49 | 49 | 8388608 = 2^23 | 0 |
| Z7xZ7 | 49 | 8388608 = 2^23 | 0 |
| Z51 | 51 | 16777216 = 2^24 | 0 |
| Z31 | 31 | 16384 = 2^14 | 0 |
| Z33 | 33 | 32768 = 2^15 | 0 |
| Z35 | 35 | 65536 = 2^16 | 0 |
| Z37 | 37 | 131072 = 2^17 | 0 |
| Z39 | 39 | 262144 = 2^18 | 0 |
| Z13:Z3 | 39 | 262144 = 2^18 | 0 |
| Z41 | 41 | 524288 = 2^19 | 0 |
| Z43 | 43 | 1048576 = 2^20 | 0 |
| Z45 | 45 | 2097152 = 2^21 | 0 |
| Z3xZ15 | 45 | 2097152 = 2^21 | 0 |
| Z47 | 47 | 4194304 = 2^22 | 0 |
| Z53 | 53 | 33554432 = 2^25 | 0 |
| Z55 | 55 | 67108864 = 2^26 | 0 |
| Z11:Z5 | 55 | 67108864 = 2^26 | 0 |
| Z57 | 57 | 134217728 = 2^27 | 0 |
| Z19:Z3 | 57 | 134217728 = 2^27 | 0 |
| Z59 | 59 | 268435456 = 2^28 | 0 |
| Z61 | 61 | 536870912 = 2^29 | 0 |
| Z63 | 63 | 1073741824 = 2^30 | 0 |
| Z3xZ21 | 63 | 1073741824 = 2^30 | 0 |
| Z7:Z9 | 63 | 1073741824 = 2^30 | 0 |
| Z3x(Z7:Z3) | 63 | 1073741824 = 2^30 | 0 |
| Z65 | 65 | 2147483648 = 2^31 | 0 |
| Z67 | 67 | 4294967296 = 2^32 | 1 |

Every `tested=` count equals 2^{(n-1)/2-1} exactly (asserted when the table was built). Z_67 is the positive control.

**Positive control.** The same program on Z_67 finds the S_4 connection sets listed in
out/main/found_Z67_k4.txt (exactly **one** set with g_0 = 1 ∈ S, namely QR_67. By Lemma 3 the only other S_4 connection set on Z_67 is φ(QR_67) = -QR_67 = the non-residues. So QRT_67 is, up to isomorphism, the unique S_4 circulant on 67 vertices.) Each found set was re-checked by code/verify_sets.py, which checks all C(67,4) = 766480
4-subsets directly with no use of Lemma 2: "S_4 HOLDS" (out/main/verify_Z67.txt).
QR_67 holding S_4 is also stated in RMHH04 p.162 (quoting Graham–Spencer).

### How the search program implements Lemma 2 (code/search.c, function test_S)
The non-identity elements are put in a fixed pseudo-random order perm[0..n-2]. For ci = 0,1,…
the program computes R(perm[ci]) = { t ∈ S : t·perm[ci] ∈ S } as a 128-bit mask by looping over
the (n-1)/2 elements t of S. It then checks R(c)∩R(b) ≠ ∅ and R(c)∩R(b)∩R(a) ≠ ∅ for every
earlier pair of positions bi < ci and ai < bi. It returns "S_4" only if every triple of distinct
non-identity elements has been checked (all ci up to n-2), which is exactly Lemma 2's criterion.
It returns "not S_4" early in three cases:
(i) some R(c) = ∅;
(ii) some R(c) ∩ R(b) = ∅;
(iii) some triple intersection is empty.
In cases (i) and (ii) every triple containing c (resp. c and b) has an empty intersection, and such
a triple exists because n-1 >= 3. So each early rejection is justified by an actual violating triple.
The enumeration covers, for each of the (n-1)/2 - 1 inverse pairs other than {g_0, g_0^{-1}}, both
choices. That is 2^{(n-1)/2-1} sets, and the `tested=` counts in the logs equal exactly that number.

## Independent cross-checks (VERIFIED)

1. **Second implementation, code/check2.c** (written separately; different formulation).
   It uses in-neighbourhoods In(x) = { x s^{-1} : s ∈ S } instead of R(·) and the natural element
   order instead of a random one, and it enumerates **all** 2^{(n-1)/2} connection sets with no
   halving (so it does not depend on Lemma 3). It checks In(e)∩In(a)∩In(b)∩In(c) ≠ ∅ for all
   a<b<c. Results (out/check2/run_check2.log, run_check2_small.log): for **all 26 groups** of
   orders 31..65, `tested=` equals 2^{(n-1)/2} (the full space) and `found=0`. That agrees with
   code/search on every group. Positive control (out/check2/run_check2_Z67_parts.log): the Z_67 index
   space was split into 16 equal ranges, and the two ranges containing NQR_67 and QR_67 (parts 7 and 8)
   were run in full (2^29 sets each). check2 found exactly NQR_67 in part 7 and exactly QR_67 in part 8,
   and no other set. NQR_67 was re-verified S_4 by verify_sets.py (out/check2/verify_NQR67.txt).
   (The order 49..65 check2 runs were made with check2.c before the optional `part nparts` arguments
   were added. That edit only adds the optional range; without those arguments the behaviour is
   identical. The order 31..47 and Z_67 runs used the current source.)
2. **Brute force, code/brute.py** (Python, a third separate group construction, no Lemma 2, no
   halving). It builds the whole tournament for every S and checks every k-subset of all n vertices.
   It agrees with code/search (run without halving) on the full list of S_k connection sets in all
   these cases (out/validate/validate_k23.log): Z_7 (k=2: 2 sets), Z_19 (k=2: 494; k=3: 2),
   Z_23 (k=3: 2), Z_7⋊Z_3 (k=2: 1024 = all; k=3: 0), Z_3×Z_3 (k=2: 16; k=3: 0), Z_11 (k=2: 22),
   Z_13 (k=2: 52), Z_9 (k=2: 10), Z_3×Z_5 (k=2: 120; this is Z_15 in a different encoding), Z_5×Z_5 (k=2: 4096), Z_15 (k=2: 120),
   Z_21 (k=3: 0).
   (One earlier comparison showed C=1000 vs py=1024. That was an output cap of 1000 lines in the
   search binary. The uncapped search_val build gives 1024 = 1024, MATCH.)
3. **Toy sanity, k = 3.** Over all groups of odd order 3..23 (out/toy/toy_k3.log, run without halving), the smallest Cayley S_3
   tournament has order 19 (Z_19: exactly QR_19 and its converse). This matches f(3) = 19 from the
   problem page and RMHH04 Thm 5. Z_7⋊Z_3 (order 21) has no S_3 Cayley tournament; Z_23 has QR_23.
4. **Negative controls for verify_sets.py:** QR_59 fails S_4 (3422 undominated 4-sets), which agrees
   with Fisher. QR_67 with the pair {1,66} flipped fails (4020 undominated 4-sets).

## Theorem (main)

The least order of a Cayley tournament with property S_4 is 67. In particular there is no Cayley
tournament with S_4 on any group of order 49 <= n <= 65, so the target statement is **false**.

*Proof.* Let Cay(G,S) be a Cayley tournament with S_4 and n = |G| <= 65. By Lemma 1(b) n is odd, and
by Lemma 4(c) n >= 31. By Lemma 5, G is isomorphic to one of the 26 listed groups, and by
Lemma 1(d) we may take G to be the listed model. By Lemma 3 we may assume g_0 ∈ S. By Lemma 2 the
S_4 property is equivalent to the tested criterion, and Proposition 6 says no such S exists. This
is a contradiction. Finally, Cay(Z_67, QR_67) has S_4 (verified directly by checking all 4-sets),
so 67 is attained. ∎

---

## What this does and does not show

**Does show:**
- No Cayley tournament (on any group, cyclic or not) of order <= 65 has S_4. The smallest one is
  QRT_67's order, 67. This independently re-verifies Fisher's circulant computation (RMHH04 p.166)
  for n <= 65 and extends it to all groups. That includes the non-abelian groups of orders 39, 55,
  57 and 63 and the non-cyclic abelian groups Z_3×Z_15, Z_7^2 and Z_3×Z_21.
- So any tournament witnessing f(4) < 67 must be **non-Cayley**. It could still be
  vertex-transitive non-Cayley, or not vertex-transitive at all.

**Does not show:**
- Nothing about f(4) itself: 48 <= f(4) <= 67 is unchanged.
- Nothing about vertex-transitive non-Cayley tournaments of order 49..65. Every vertex-transitive
  digraph of prime order is a circulant, so the uncovered orders are composite. I did not
  investigate which composite odd orders in 49..65 admit non-Cayley vertex-transitive tournaments.
  INFERRED: such tournaments are rare in small orders, but I have not checked this.
- It is a computer-assisted proof. Rigor depends on the correctness of code/search.c and
  code/check2.c (cross-validated as above) and on the Sylow-based group list (Lemma 5; not checked
  with GAP).
- Statistics such as best_depth in the logs are diagnostics only and carry no mathematical claim.

## Reproduce

From `attack/902/t1/prove/`:

    bash code/run_all.sh

This compiles code/search.c, code/check2.c and the uncapped validator, prints the group
invariants, runs the main search on all 15 groups of orders 49..65 plus Z_67, runs the 11 groups of
orders 31..47, runs the independent check2 on all 26 groups (full space, no halving), runs the
two Z_67 control parts for check2, re-verifies the Z_67 sets exactly, and repeats the brute-force
comparison. Total wall time on the shared machine: about 3 hours. Individual runs:

    cd out/main && ../../code/search Z63 4 10          # group name, k, threads
    cd out/small && ../../code/search C:39,1,1,1 4 10  # custom (m,k,r,d) group
    cd out/check2 && ../../code/check2 Z63 10
    python3 -I code/verify_sets.py 67 1 1 1 4 out/main/found_Z67_k4.txt
    bash -c '...' (see out/validate/validate_k23.log for the brute-force comparison specs;
                   python3 -I code/brute.py m k r d K)

Running times on the heavily loaded machine (load average about 100): code/search took 4 to 8 minutes wall per
order-63/65 group and 17 minutes for Z_67. check2 took 13 to 26 minutes per order-63/65 group.

## Sources not read

- Fisher, private communication 1996 (reported second-hand in RMHH04 p.166). Unpublished.
- Szekeres & Szekeres 1965; Graham & Spencer 1971; Reid & Brown 1972 (only as quoted in RMHH04).
- Jeffries arXiv:2604.08790 and Javier–Llano–Zuazua: seen only in web-search summaries, not read.
- I did not run GAP or SmallGroups. Lemma 5 is proved by hand only.
- ryantuck/erdos-ai was not checked.
