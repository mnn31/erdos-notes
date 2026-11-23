# Erdős #776, the delta = 4 threshold: exact values of n_0^{(4)}(r) for 2 <= r <= 40

Date: 2026-11-23. Folder: `attack/776/t1-retry/prove/`. Everything below is reproduced by

    cd attack/776/t1-retry/prove && sh code/run_all.sh          # about 3 min on this (heavily loaded) machine

plus `sh code/negative_tests.sh` (checker rejects corrupted inputs) and, optionally,
`sh code/run_extra.sh` (same pipeline for 41 <= r <= 61) and `code/cpsat_cross.py` (KK-free cross-check).

## 0. Statement established

**Definitions** (Q. Tang, note `../../refs/To_Hunter_v1.pdf`, Sec. 1.1–1.2, and his forum post of 12 Feb 2026;
VERIFIED by reading both). For integers n >= 1, r >= 2, an *r-multiplicity antichain* on [n] = {1,...,n} is a
family F of subsets of [n] with A ⊄ B for all distinct A, B in F, such that every size t in
S(F) := {|A| : A in F} satisfies |F_t| >= r, where F_t = {A in F : |A| = t}.
g(n,r) := max |S(F)| over r-multiplicity antichains F on [n], and

    n_0^{(4)}(r) := min { n_0 : g(n,r) >= n-4 for every integer n > n_0 }.

Convention: n ranges over integers n >= 1 and n_0 over integers n_0 >= 0. (Tang does not state the range of
n_0. The convention matters only for r <= 6, where the inequality holds for *every* n >= 1; with n_0 allowed to
be any integer the minimum would not exist there. For r >= 7 the value is the largest n with g(n,r) < n-4 and
no convention is involved.)

> **Theorem.** For every integer r with 2 <= r <= 40:
>
> | r | n_0^{(4)}(r) |
> |---|---|
> | 2, 3, 4, 5, 6 | 0  (g(n,r) >= n-4 holds for every n >= 1) |
> | 7, 8, 9, 10 | r + 3  (= 10, 11, 12, 13) |
> | 11, 12, ..., 40 | r + 4  (= 15, 16, ..., 44) |
>
> Certified as follows. Write N = N(r) for the tabulated value.
> (a) For every n with max(5, N+1) <= n <= 2r+5 an explicit r-multiplicity antichain on [n] with exactly
>     n-4 sizes is stored in `out/witnesses/wit_r<r>.txt` (block `W n r n-4 ...`) and checked set by set and
>     pair by pair by `code/check.c` (882 blocks, all OK: `out/check_witness.txt`).
> (b) For every n >= 2r+6, g(n,r) >= n-3 (Proposition 9; uses a stored, directly checked base core on r+5
>     points — block `K` of the same file, 39 cores all OK — and two elementary lemmas proved below).
>     This does not use Thiim's delta = 3 theorem.
> (c) For r >= 7: at n = N, for each of the C(N-1,3) choices of three missing levels, the prescribed-profile
>     recurrence overflows; the overflow list is stored in `out/certs/cert_r<r>_n<N>.txt` and recomputed
>     independently (all triples enumerated anew, independent Kruskal–Katona code, 128-bit integers) by
>     `code/check.c` (34 certificates, all OK: `out/check_infeas.txt`). With the Kruskal–Katona theorem this
>     gives g(N,r) <= N-5 (Lemmas 4–5).

**Additional facts established by the same method (secondary).**
- For 41 <= r <= 61 the same pipeline (`code/run_extra.sh`, outputs in `out/extra_41_61/`) gives
  n_0^{(4)}(r) = r + 4: 1092 witness blocks and 21 cores OK, 21 certificates OK. (r = 61 is the largest r
  with 2r+5 <= 127, the checker's bitmask limit.) Same rigor as the Theorem, but this extension was not part
  of the target and was run once.
- For 2 <= r <= 40 the set of n in [5, 2r+5] with g(n,r) < n-4 is exactly: empty (r <= 6), {6,...,r+3}
  (7 <= r <= 10), {5,...,r+4} (11 <= r <= 40). For n > N this is the Theorem. For 7 <= r <= 10 and n = 5,
  any r of the 10 two-subsets of [5] give g(5,r) >= 1 = n-4. For 6 <= n < N (and n = 5 when r >= 11) the
  infeasibility rests on the C scan `code/check.c s` alone (one implementation, via Lemmas 4–5);
  `out/scan_c.txt`. (For r >= 11, n = 5 is also elementary: every level of [5] has <= 10 < r sets.)

The only non-computational input is the Kruskal–Katona theorem (classical, not re-proved), used only for the
lower bound (c). Parts (a), (b) rest on direct checks of explicit set systems plus Lemmas 6–8.

## 1. Is this already decided? (checked 2026-11-23)

- erdosproblems.com/776 and forum thread, fetched today (`refs/page776.html(.txt)`, `refs/forum776.html(.txt)`):
  the page asks only for n_0(r) (the delta = 3 threshold). The only delta = 4 content in the thread is Tang's
  post (12 Feb 2026): n_0^{(4)}(r) >= ceil((r+3)/3) for r >= 12, "C_4 in [1/2, 3]", and "I don't have a good
  guess for the specific value of C_4". No exact delta = 4 values. VERIFIED (read).
- Plasma `wiki/problems/set_systems/E0776/` (`_index.md` and all three claim pages, fetched today into `refs/`):
  grep for delta / n-4 / C_4 / Hunter: no hits. VERIFIED.
- ryantuck/erdos-ai: `conjectures/776.lean`, `deepmind/reviews/776.md`, `deepmind/ai-review/776.md` (fetched
  into `refs/`): grep for n-4 / delta / C_4: no hits. VERIFIED.
- arXiv API (today): three http queries ("multiplicity antichain", antichain+"distinct sizes",
  Erdos+Trotter+antichain) returned empty responses; two https retries returned, respectively, three
  irrelevant titles (antichain+sizes+multiplicity) and no entries ("Erdos Problem 776"). So this search is
  weak; it is backed by the earlier same-day agent's arXiv check in `../../t1/prove/refs/arxiv*.xml` (not
  re-read in detail) and by the forum/Plasma checks above. INFERRED: no published delta = 4 values.
- formal-conjectures: no 776 file (scout note; not re-checked).
- Inside this workspace: an earlier agent run in `../../t1/prove/` (unfinished write-up with placeholders) and
  the scout's `../../compute/delta4.py` report the same numbers. I did not reuse their code; all code here was
  written from scratch, and the numbers agree (`diff` of the N(r) columns: identical).

So, as far as these sources show, the exact delta = 4 values are new.

## 2. Lemmas

Notation: F_t = members of size t; "level t" = all t-subsets of [n]; C(a,b) = binomial coefficient (0 if b > a
or b < 0).

**Lemma 1 (levels 0 and n are never used).** If r >= 2 and F is an r-multiplicity antichain on [n], then
0 ∉ S(F) and n ∉ S(F).

*Proof.* There is exactly one subset of [n] of size 0 and exactly one of size n, so |F_0| <= 1 and |F_n| <= 1.
If t ∈ S(F) then |F_t| >= r >= 2. Hence t ∉ {0, n}. ∎

**Lemma 2 (reduction to exact profiles).** Let r >= 2 and n >= 5. Then g(n,r) >= n-4 iff there are a 3-subset
M of {1,...,n-1} and an antichain on [n] having exactly r members of each size in L := {1,...,n-1} \ M and no
other members.

*Proof.* (<=) Such a family is an r-multiplicity antichain with S = L, |L| = (n-1) - 3 = n-4.
(=>) Let F be an r-multiplicity antichain with |S(F)| >= n-4. By Lemma 1, S(F) ⊆ {1,...,n-1}, a set of n-1
elements. Choose L ⊆ S(F) with |L| = n-4 (possible since |S(F)| >= n-4 >= 1), and put M = {1,...,n-1} \ L, so
|M| = 3. For each t ∈ L choose r members of F_t (possible since |F_t| >= r). The chosen sets form a subfamily of
an antichain, hence an antichain, with exactly r members on each level of L and none elsewhere. ∎

**Kruskal–Katona theorem (classical; used as a black box).** Let k >= 1 and m >= 1, and write
m = C(a_k,k) + C(a_{k-1},k-1) + ... + C(a_s,s) with a_k > a_{k-1} > ... > a_s >= s >= 1 (the k-cascade of m).
Then every family of m distinct k-element sets has (k-1)-shadow ∂D := {X : |X| = k-1, X ⊂ Z for some Z ∈ D} of
size at least KK_k(m) := C(a_k,k-1) + C(a_{k-1},k-2) + ... + C(a_s,s-1). Set KK_k(0) := 0.
(Kruskal 1963; Katona 1968. Not re-read here; see "Sources not read".)

**Lemma 3 (the greedy cascade is a k-cascade).** Let k >= 1, m >= 1. Define a_k := max{a >= k : C(a,k) <= m},
m' := m - C(a_k,k), and, while the current remainder is positive, repeat with k-1 in place of k. This
terminates and produces a representation of m as in the theorem.

*Proof.* For fixed j >= 1 the map a ↦ C(a,j) is strictly increasing on a >= j-1, since
C(a+1,j) - C(a,j) = C(a,j-1) >= 1 there; and C(j,j) = 1. So for a remainder R >= 1 the maximum
a_j = max{a >= j : C(a,j) <= R} exists and is >= j. The new remainder satisfies
0 <= R - C(a_j,j) < C(a_j+1,j) - C(a_j,j) = C(a_j,j-1). If it is positive, the next index is computed with
j-1 >= 1 (see below) and C(a_{j-1},j-1) <= R - C(a_j,j) < C(a_j,j-1) gives a_{j-1} < a_j by monotonicity. If
j = 1, then C(a,1) = a, so a_1 = R and the remainder becomes 0; thus the process never needs j = 0, and it stops
after at most k steps with a_k > ... > a_s >= s >= 1. ∎

Both implementations compute exactly this greedy cascade: `kk()` in `code/search.py` (increasing search from
a = j) and `kk()` in `code/check.c` (decreasing search from the previous a_{j+1} - 1, which is valid by
Lemma 3; inputs with m >= C(128,k), for which the search could not start high enough, are refused — they never
occur because the recurrence only calls kk on m <= C(n,k) with n <= 127). Sanity tests (`out/sanity.txt`):
(1) KK_k(m) equals the brute-force minimum shadow over all m-families for (p,k) ∈ {(5,2),(5,3),(6,2),(6,3),
(6,4)} and all m, and (7,3) for m <= 5; (2) equals the shadow of the first m colex k-sets for k <= 9, m < 600;
(3) Python and C agree on 3160 points (k <= 40, m <= C(85,k)).

**Lemma 4 (prescribed profiles force the recurrence).** Let F be an antichain on [n] with T := max{|A| : A ∈ F}
and f_i := |F_i|. Define m_T := f_T and m_i := f_i + KK_{i+1}(m_{i+1}) for i = T-1, ..., 0, stopping if some
m_j > C(n,j). Then no stop occurs: m_i <= C(n,i) for every 0 <= i <= T.

*Proof.* For 0 <= i <= T let U_i be the set of i-subsets of [n] properly contained in some member of F of size
> i, and D_i := F_i ∪ U_i.
1. F_i ∩ U_i = ∅: a member of F properly contained in another member would contradict the antichain property.
   So |D_i| = f_i + |U_i|.
2. For i < T, ∂D_{i+1} ⊆ U_i: let X be an i-subset of some Z ∈ D_{i+1}. If Z ∈ F_{i+1}, then X ⊊ Z and
   |Z| = i+1 > i. If Z ∈ U_{i+1}, then Z ⊊ Y for some Y ∈ F with |Y| > i+1, so X ⊊ Y. Either way X ∈ U_i.
3. |D_T| >= f_T = m_T.
We show |D_i| >= m_i by downward induction on i; then m_i <= |D_i| <= C(n,i) (D_i is a set of i-subsets of
[n]), which also shows the stopping rule never fires. The base is 3. Step: suppose |D_{i+1}| >= m_{i+1}. If
m_{i+1} = 0, then KK_{i+1}(0) = 0 and |D_i| >= f_i = m_i. Otherwise pick D' ⊆ D_{i+1} with |D'| = m_{i+1};
then ∂D' ⊆ ∂D_{i+1} ⊆ U_i by 2, and Kruskal–Katona (k = i+1 >= 1) gives
|D_i| = f_i + |U_i| >= f_i + |∂D'| >= f_i + KK_{i+1}(m_{i+1}) = m_i. ∎

(Choosing a subfamily of size exactly m_{i+1} avoids needing monotonicity of KK_k.)

**Lemma 5 (overflow certificate => infeasibility).** Let r >= 2, N >= 5. Suppose that for every 3-subset M of
{1,...,N-1}, with L = {1,...,N-1} \ M, f_i = r (i ∈ L), f_i = 0 (i ∉ L), T = max L, the recurrence of Lemma 4
started from m_T = r reaches some i ∈ [0, T] with m_i > C(N,i). Then g(N,r) <= N-5.

*Proof.* If g(N,r) >= N-4, Lemma 2 gives such an M and an antichain with |F_i| = f_i for all i; its maximum
size is T = max L, so Lemma 4 gives m_i <= C(N,i) for all i <= T, contradicting the hypothesis for this M. ∎

`code/check.c i r N` checks exactly the hypothesis of Lemma 5: it loops over all a < b < c in {1,...,N-1},
runs the recurrence from the top level T with exact unsigned 128-bit arithmetic, and requires an overflow for
every triple; it also requires the stored certificate to list the same (M, i, m_i, C(N,i)) in the same order
and the same number of lines. Overflow of 128-bit integers cannot occur: the loop stops at the first
overflow, so every m_{i+1} passed to KK satisfies m_{i+1} <= C(n,i+1); then C(a_{i+1}, i+1) <= C(n, i+1)
forces a_{i+1} <= n (strict monotonicity, Lemma 3), so all cascade entries are <= n and KK_{i+1}(m_{i+1}) is a
sum of at most n binomials C(a, j) with a <= n. In mode i, n = N <= 65 and C(65,32) < 2^62, so every quantity
is < 2^69 (the extension r <= 61 has N <= 65 too); mode s is run only with n <= 85, where every quantity is
< 85 * C(85,42) < 2^89. The
binomial table itself (Pascal's rule up to a = 128) has entries <= C(128,64) < 2^125.

**Lemma 6 (checked witness => g(n,r) >= n-4).** If a block `W n r k cnt` passes `code/check.c w`, then
g(n,r) >= k >= n-4.

*Proof.* The checker verifies, for the cnt bitmasks read (bit e represents the element e+1 of [n]): every mask
has no bit >= n (so it is a subset of [n]); after sorting by (size, value), no two adjacent masks are equal
(so all sets are distinct); for every pair at positions a < b with different sizes (then size(a) < size(b)),
mask_a ⊄ mask_b (sets of equal size that are distinct are automatically incomparable, and a larger set is
never inside a smaller one, so this covers all pairs); every occurring size occurs >= r times; the number of
occurring sizes equals k, and k >= n-4. This is the definition of an r-multiplicity antichain with k sizes. ∎

(How witnesses were produced is irrelevant to Lemma 6. For the record: colex "squashed" profiles — on each
level i ∈ L, the i-sets of colex ranks KK_{i+1}(m_{i+1}), ..., m_i - 1; `code/search.py`.)

**Lemma 7 (two-point padding).** Let C be an antichain on a q-set Q with at least r members of every size
2,...,s, and let G_1,...,G_r be distinct (s-1)-subsets of Q none of which contains a member of C. Take 2t new
points x_1, y_1, ..., x_t, y_t, put X_j := {x_1,...,x_j} (X_0 := ∅) and
H_{i,j} := G_i ∪ X_{j-1} ∪ {x_j, y_j} (1 <= i <= r, 1 <= j <= t). Then C' := C ∪ {H_{i,j}} is an antichain on
q + 2t points with at least r members of every size 2,...,s+t.

*Proof.* |H_{i,j}| = (s-1) + (j-1) + 2 = s+j. For fixed j, H_{i,j} ∩ Q = G_i, so the r sets H_{1,j},...,H_{r,j}
are distinct; thus every size s+1,...,s+t has >= r members, and sizes 2..s keep theirs. Incomparability:
- E ∈ C and H = H_{i,j}: if E ⊆ H then E ⊆ H ∩ Q = G_i (as E ⊆ Q), contradicting the choice of G_i; H ⊆ E is
  impossible since x_j ∈ H \ Q.
- H_{i,j} ≠ H_{i',j'}: if j = j', they are distinct sets of equal size. If j < j', then y_j ∈ H_{i,j}, while the
  only y-point of H_{i',j'} is y_{j'} ≠ y_j, so H_{i,j} ⊄ H_{i',j'}; and H_{i',j'} ⊄ H_{i,j} because
  |H_{i',j'}| > |H_{i,j}|. (j > j' is the same with the roles exchanged.)
- E, E' ∈ C: C is an antichain. ∎

**Lemma 8 (core to full family).** Let n >= 6, r >= 2, h := floor(n/2), and let C be an antichain on a q-set Q
with at least r members of every size 2,...,h-1, where q <= n-1-r. Then g(n,r) >= n-3.

*Proof.* Inside [n] choose pairwise disjoint Q, {a}, P = {p_1,...,p_r} (possible as q + 1 + r <= n). Let Λ
consist of the r pairs {a,p_j} and, for each ℓ ∈ {2,...,h-1}, the sets E ∪ {a} for r chosen members E ∈ C of
size ℓ. Let Υ := {[n] \ L : L ∈ Λ} and F := Λ ∪ Υ.
- Λ consists of distinct sets: pairs are distinct; E ∪ {a} determines E (a ∉ Q); pairs have size 2 and the
  other sets size >= 3.
- Λ is an antichain: {a,p_j} ⊆ E ∪ {a} would force p_j ∈ E ⊆ Q, false; E ∪ {a} ⊆ {a,p_j} is impossible by
  size; E ∪ {a} ⊆ E' ∪ {a} with E ≠ E' gives E ⊆ E' (since a ∉ E'), contradicting that C is an antichain.
- Υ is an antichain of distinct sets: complementation is injective and reverses inclusion.
- Λ ∩ Υ = ∅, and no L ∈ Λ is comparable with [n] \ L' (L' ∈ Λ, possibly L' = L): a ∈ L ∩ L', so
  L ⊄ [n] \ L'; and [n] \ L' ⊆ L would give L ∪ L' = [n], but |L ∪ L'| <= |L| + |L'| - 1 <= 2h - 1 <= n-1
  because every member of Λ has size <= h and a ∈ L ∩ L'. (Also a ∈ L, a ∉ [n] \ L', so L ≠ [n] \ L'.)
- Sizes: Λ has exactly r sets of each size 2,...,h (size ℓ+1 for ℓ = 2..h-1, and size 2 from the pairs);
  Υ has exactly r sets of each size n-h,...,n-2. Since n - h <= h + 1, S(F) = {2,...,n-2}, every size has >= r
  members, and |S(F)| = n-3. ∎

**Proposition 9 (tail).** Fix r. Suppose block `K r+5 r r+2 cnt r` of `out/witnesses/wit_r<r>.txt` passes
`code/check.c w`, i.e. its cnt sets form an antichain on [r+5] with at least r members of every size 2,...,r+2
(and no others), and its r further sets are distinct (r+1)-subsets of [r+5] none containing a core member.
Then g(n,r) >= n-3 for every n >= 2r+6.

*Proof.* Write n = 2r+6+2t or n = 2r+7+2t with t >= 0. Lemma 7 with q = r+5, s = r+2 gives an antichain on
q' = r+5+2t points with >= r members of every size 2,...,r+2+t. Here h = floor(n/2) = r+3+t, so h-1 = r+2+t,
and n-1-r ∈ {r+5+2t, r+6+2t} is >= q'. Also n >= 2r+6 >= 10 >= 6. Lemma 8 applies. ∎

The 39 cores (r = 2..40) all pass (`out/check_witness.txt`, lines `OK K`). The free sets are the r+2 punctures
T \ {x} of one top-level core member T (r of them stored); the checker verifies the "contains no core member"
condition directly. As a test of Lemmas 7–8 (not needed for the proof), `code/tail_demo.py` builds the
Lemma 7+8 families explicitly for n = 2r+6, ..., 2r+17 and every r <= 40; all 468 pass `code/check.c w` with
n-3 sizes (`out/check_tail_demo.txt`).

## 3. Proof of the Theorem

Fix 2 <= r <= 40 and let N = N(r) be the tabulated value.

*Upper bound, n_0^{(4)}(r) <= N:* we need g(n,r) >= n-4 for every n > N.
- n <= 4: the empty family is an r-multiplicity antichain, so g(n,r) >= 0 >= n-4.
- 5 <= n <= 2r+5, n > N: block `W n r n-4` of `out/witnesses/wit_r<r>.txt` exists for exactly these n
  (n = 5..2r+5 when r <= 6; n = N+1..2r+5 when r >= 7) and passes the checker; Lemma 6.
- n >= 2r+6: Proposition 9.

*Lower bound, n_0^{(4)}(r) >= N (only for r >= 7; for r <= 6, N = 0 is the least admissible value):*
`code/check.c i r N cert` passes for each r in 7..40 (`out/check_infeas.txt`), i.e. the hypothesis of Lemma 5
holds at N, so g(N,r) <= N-5 < N-4. Therefore no n_0 < N has the defining property (n = N > n_0 violates it).
Hence n_0^{(4)}(r) = N. ∎

## 4. Verification record (all files under `out/`)

| check | result |
|---|---|
| `search_stdout.txt`, `summary_2_40.txt` | Python exact search; N(r) as tabulated |
| `check_witness.txt` | 882 `OK W` + 39 `OK K`, 0 failures (run under `-fsanitize=undefined`, no runtime errors) |
| `check_infeas.txt` | 34 `OK INFEAS` (r = 7..40), 0 feasible triples, 0 certificate mismatches |
| `scan_c.txt` | independent C scan; largest failing n = 0 (r<=6), r+3 (7..10), r+4 (11..40); failing sets are intervals |
| `check_tail_demo.txt` | 468 Lemma 7+8 families, all OK with n-3 sizes |
| `sanity.txt` | KK brute force / colex / Python-vs-C / n = 6 brute force (r = 2..20): ALL SANITY OK |
| `negative_tests.txt` | duplicated set, comparable pair, short level, element outside [n], bad core free set: all rejected; false infeasibility claims (r=7,N=11), (r=11,N=16), corrupted and truncated certificates: all rejected; unmodified copies accepted |
| `cpsat_cross.txt` | KK-free CP-SAT cross-check on small (r,n), see below |
| `extra_41_61/` | r = 41..61: N = r+4, 1092 W + 21 K OK, 21 certificates OK (witnesses gzipped; `gunzip` before re-checking) |

For every r (2..40) and every n, the stored witness uses missing levels {1, 2, n-1}, i.e. sizes {3,...,n-2}.

Tightness (`cert_tightness.txt`, read off the certificates): at n = N the smallest overflow is by exactly 1 for
every r in 8..40 (e.g. r = 40, N = 44, missing {1,2,43}: m_3 = 13245 > 13244 = C(44,3)); for r = 7 it is 2.
So the lower bound is razor-thin and depends on the exact Kruskal–Katona values; this is why KK was implemented
twice and tested against brute force.

KK-free cross-check (`code/cpsat_cross.py`, OR-tools CP-SAT, model described in the file; it encodes the
antichain condition with "below a member" indicator variables and does not use Kruskal–Katona or the recurrence):
| (r, n) | CP-SAT status | recurrence/table says |
|---|---|---|
| (6, 7) | feasible (family re-verified: antichain, levels 2,3,4 with >= 6 sets) | feasible (N(6) = 0) |
| (7, 7) | INFEASIBLE (2.9 s) | infeasible (7 ∈ failing set {6..10} of r = 7) |
| (6, 8) | feasible (family re-verified, levels 3..6) | feasible |
| (7, 8) | UNKNOWN after 300 s | infeasible |

Larger instances ((7,9), (7,10), ...) did not finish within several minutes on this loaded machine (the
multi-worker runs also hung and were killed), so the KK-free cross-check reaches only n <= 7. Together with
sanity test (4) (exhaustive brute force at n = 6: infeasible exactly for r >= 7, matching the recurrence), this
gives two KK-free confirmations of the lower-bound machinery on small n, but none at the thresholds N(r) >= 10
themselves. Command: `python3 -I code/cpsat_cross.py r n 300 1`; output `out/cpsat_cross.txt`.

## 5. Observations (INFERRED, not proved)

- n_0^{(4)}(r) = r + 4 for 11 <= r <= 61 (proved here for each such r individually). Conjecture: n_0^{(4)}(r) = r+4
  for all r >= 11. In Hunter's parametrization this would give C_4 = 1 (g(n, (1-o(1))n) >= n-4 and
  g(n, (1+o(1))n) < n-4), inside Tang's interval [1/2, 3]. No general proof is attempted; the overflow-by-one
  phenomenon suggests a proof needs exact control of the colex recurrence near levels 2–3.
- Above the threshold the profile "levels 3..n-2" always worked (it is the first one tried).

## 6. What this does and does not show

Does show (rigorously, given the Kruskal–Katona theorem and the correctness of the short checker `code/check.c`,
whose relevant logic is described in Lemmas 5–6 and exercised by negative tests):
- the exact value of n_0^{(4)}(r) for every 2 <= r <= 40 (and, by the same method, 41 <= r <= 61);
- explicit, directly checked witnesses for all n ∈ (n_0^{(4)}(r), 2r+5], n >= 5, and a self-contained proof of
  g(n,r) >= n-3 for n >= 2r+6 (Thiim's padding/core method, re-proved; so the upper half n_0^{(3)}(r) <= 2r+5 of
  Thiim's delta = 3 theorem is re-derived for r <= 61);
- a checkable infeasibility certificate at n = n_0^{(4)}(r) for r >= 7.

Does not show:
- anything for r > 61, the limit of n_0^{(4)}(r)/r, or the value of C_4;
- an infeasibility proof independent of Kruskal–Katona (the CP-SAT runs are only a cross-check for small
  cases, and CP-SAT emits no checkable proof);
- the C scan's failing intervals below N are single-implementation (not needed for the Theorem).
- The convention for r <= 6 (value 0) is a convention: Tang's definition does not specify the range of n_0.

## 7. Reproduction

From `attack/776/t1-retry/prove/`:

    sh code/run_all.sh            # compiles code/check.c (also a UBSan build), runs search, all checks, sanity
    sh code/negative_tests.sh     # corrupted inputs must be rejected
    sh code/run_extra.sh          # optional, r = 41..61 (~11 min)
    python3 -I code/cpsat_cross.py r n [timelimit] [workers]   # optional KK-free cross-check

Files: `code/search.py` (exact search, certificates, colex witnesses, cores), `code/check.c` (independent
checker: modes w / i / s / k), `code/tail_demo.py`, `code/sanity.py`, `code/make_negative.py`,
`code/cpsat_cross.py`. Python is always run with `-I`.

## 8. Sources not read

- Kruskal (1963), Katona (1968): KK used as stated in standard references, from memory of its statement; the
  statement was spot-checked by brute force (sanity test 1) but the theorem itself is not re-proved here.
- Clements (1973), Daykin–Godfrey–Hilton (1974): the sufficiency direction of the profile criterion is not used
  (witnesses are checked directly); necessity is re-proved as Lemma 4.
- Thiim's repository (TECHNICAL_NOTE, UNIFORM_THEOREM, Lean files) and the OV3RK177 replication package: only
  the forum descriptions were read; Lemmas 7–8 were re-proved from scratch.
- He–Tang arXiv:2602.09803 beyond what the scout extracted.
- formal-conjectures (no 776 file per the scout; not re-checked).
