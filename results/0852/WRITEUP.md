# Erdős #852 — a conditional upper bound for h(x) under RH

Written 22 Nov 2026. Status of this file: a complete argument for a PARTIAL result.
It does not answer either question of Erdős Problem 852.

## 0. Setting and exact statements

Notation (the problem page's indexing): p_1 = 2 < p_2 = 3 < ... are the primes,
d_k = p_{k+1} - p_k for k >= 1. For integers n >= 1 and H >= 1 call (n, H) a
*distinct run* if d_n, d_{n+1}, ..., d_{n+H-1} are pairwise distinct. For real x > 1,
h(x) is the largest H such that (n, H) is a distinct run for some integer 1 <= n < x.
(Under RH, Lemma 4(a) below shows that every such H is < x once x >= 50, so h(x) is finite.)
theta(y) = sum of log p over primes p <= y (the usual, right-continuous Chebyshev function).
pi(y) = number of primes <= y. log is the natural logarithm.

"RH" means the Riemann Hypothesis for the Riemann zeta function only: every zero of zeta
in the critical strip has real part 1/2. No hypothesis on Dirichlet L-functions is used.

**Theorem A (the lead, with explicit constants).** Assume RH. Let x >= 50 be real, let
1 <= n < x be an integer and let (n, H) be a distinct run. Then

    H <= (2/sqrt(pi)) * x^{1/4} * (log x)^{5/4} + 2 log x + 25.48 .

Consequently h(x) <= 4 x^{1/4} (log x)^{5/4} for all x >= 50, i.e.
h(x) = O(x^{1/4} (log x)^{5/4}).

**Theorem B (a strengthening found while checking the lead).** Assume RH. With the same
x, n, H,

    H <= 4 sqrt(2) * x^{1/4} * (log x)^{3/4} + 12 log x + 140 .

Consequently h(x) = O(x^{1/4} (log x)^{3/4}).

Theorem B implies the O-form of Theorem A. They are kept separate because they rest on
different citations: A needs only the von Koch / Schoenfeld bound for theta (Lemma 2),
B needs an explicit form of Cramér's theorem (Lemma 7).

The lead as received claimed h(x) << x^{1/4} (log x)^{5/4} under RH for zeta. That claim
SURVIVES in full (Theorem A). The lead's step 4 (psi, with a separate prime-power term
and "H >= S/(3 log P)") is replaced below by a cleaner step with theta; nothing in the
lead's outline turned out to be false. One attribution in the lead was wrong, see "Credit".

## 1. Lemmas for Theorem A

**Lemma 1 (sum of a distinct run).** If (n, H) is a distinct run and
S := p_{n+H} - p_n, then S >= H^2 - H + 1.

Proof. S = d_n + ... + d_{n+H-1} (telescoping). For k >= 2 both p_k and p_{k+1} are odd,
so d_k is a positive even integer; d_1 = 1. If e_1 < e_2 < ... < e_m are distinct positive
even integers then e_i >= 2i, so their sum is >= m(m+1).
If n >= 2, all H terms are distinct positive even integers and S >= H(H+1) >= H^2 - H + 1.
If n = 1, the term d_1 equals 1 and the other H - 1 terms are distinct positive even
integers, so S >= 1 + (H-1)H = H^2 - H + 1. QED

**Lemma 2 (von Koch, in Schoenfeld's explicit form; CITED).** Assume RH. Then for every
real y >= 599,

    |theta(y) - y| <= sqrt(y) (log y)^2 / (8 pi).

Citation whose text I read: J. Büthe, "Estimating pi(x) and related functions under
partial RH assumptions", arXiv:1410.7015v4 (25 May 2022), Theorem 2 (Section 7).
What it states: if RH holds for all zeros with 0 < Im(rho) <= T, and
4.92 sqrt(x / log x) <= T, then |vartheta(x) - x| <= (sqrt(x)/(8 pi)) log(x)^2 for x > 599
(and the analogous bound for psi for x > 59).
Hypothesis check: under full RH the first hypothesis holds for every T > 0, so for each
x > 599 one may take T = 4.92 sqrt(x / log x). Only zeta is involved.
Convention check: Büthe's vartheta is the *normalized* function (Section 7 defines it with
the normalized characteristic function of Section 2, which gives weight 1/2 at the
endpoint), so it equals theta(y) at every non-prime y and equals theta(y) - (1/2) log y
at a prime y. To get the lemma for the usual theta and for y >= 599: fix y >= 599 and take
non-prime reals y_k > y decreasing to y. Then theta(y_k) = vartheta(y_k), theta(y_k) -> theta(y)
because theta is right-continuous, and the right-hand side is continuous, so the inequality
passes to the limit. QED

Remarks on this citation.
- arXiv v4 is a corrected version: its arXiv comment says a missing summand in Theorem 1
  was added, that the explicit tables remain valid, and that a corrigendum to the journal
  version (Math. Comp. 85 (2016), 2483-2498) was in preparation. I cite v4, not the journal
  text, which I did not read.
- Büthe's proof of Theorem 2 relies on computer calculations by its author for
  x < 10^19 (stated in the proof). I did not rerun them.
- Büthe presents the bound as Schoenfeld's (1976). I could NOT obtain Schoenfeld's paper
  (ams.org returned HTTP 403), so the attribution to Schoenfeld's "Theorem 10" is from
  memory and is not used; see "Sources not read".
- Sanity check only, not part of the proof: check852.py confirms the inequality of
  Lemma 2 for all y in [599, 2*10^7] (largest ratio 0.984) and that it fails just below
  599, matching the threshold in the source.
- Robustness: the O-forms of Theorems A and B need only theta(y) = y + O(sqrt(y) log^2 y)
  under RH (von Koch 1901). The constant 1/(8 pi) and the threshold 599 only affect the
  explicit constants.

**Lemma 3 (size of p_m).** Assume RH. For every integer m >= 1,
p_m <= max(599, 4 m log(2m)).

Proof. Let y = p_m and suppose y > 599. The function g(t) = (log t)^2 / sqrt(t) has
g'(t) = (log t)(4 - log t) / (2 t^{3/2}) < 0 for t > e^4 (about 54.6), so for y >= 599,
g(y) <= g(599) < 1.68 and sqrt(y)(log y)^2/(8 pi) = y g(y)/(8 pi) < 0.07 y. By Lemma 2,
theta(y) >= y/2. Also theta(p_m) = log p_1 + ... + log p_m <= m log p_m. Hence
p_m <= 2 m log p_m. Next, log t <= sqrt(t) for all t > 0 (the function sqrt(t) - log t
has its minimum at t = 4, where it equals 2 - log 4 > 0). So p_m <= 2 m sqrt(p_m), i.e.
sqrt(p_m) <= 2m, so log p_m <= 2 log(2m), and p_m <= 4 m log(2m). QED

(The bound p_m << m log m is unconditional, by Chebyshev. It is derived from Lemma 2
here only so that the proof has a single analytic input.)

**Lemma 4 (location of the run).** Assume RH. Let x >= 50 be real, 1 <= n < x an integer
and (n, H) a distinct run. Put P := p_{n+H}. Then
(a) H < x;
(b) P <= 8 x log(4x) <= 16 x log x;
(c) log P <= 2 log x.

Proof. (a) Suppose H >= x. Then H >= 50 and n < x <= H, so n + H < 2H and P <= p_{2H}.
By Lemma 3, p_{2H} <= max(599, 8 H log(4H)) = 8 H log(4H), because
8 H log(4H) >= 400 log 200 > 2119. By Lemma 1, H^2 - H + 1 <= S = P - p_n < P <= 8 H log(4H),
hence H - 1 < 8 log(4H). But phi(H) := H - 1 - 8 log(4H) has phi'(H) = 1 - 8/H > 0 for
H > 8 and phi(50) = 49 - 8 log 200 > 6.6, so phi(H) > 0 for all H >= 50. Contradiction.
(b) By (a), m := n + H is an integer with m < 2x. The function t -> 4 t log(2t) is
increasing for t >= 1/2, so by Lemma 3, P = p_m <= max(599, 8 x log(4x)) = 8 x log(4x)
(again 8 x log(4x) >= 400 log 200 > 599). And log(4x) <= 2 log x because x >= 4.
(c) 8 log(4x) <= x for x >= 50 (true at x = 50, where the left side is < 42.4, and the
left side grows more slowly than x for x > 8). So P <= x^2. QED

**Lemma 5 (the RH step).** Assume RH. Let (n, H) be a distinct run, A := p_n,
P := p_{n+H}, S := P - A, and suppose P >= 599. Then

    S <= H log P + sqrt(P) (log P)^2 / (4 pi) + 599 .

Proof. Put A' := max(A, 599), so 599 <= A' <= P and P - A' >= S - 599. The primes in
(A', P] are among the primes in (A, P], which are exactly p_{n+1}, ..., p_{n+H}, each
<= P. Hence theta(P) - theta(A') <= H log P. By Lemma 2 at y = P and at y = A', and since
t -> sqrt(t)(log t)^2 is increasing for t >= 1,

    theta(P) - theta(A') >= (P - A') - 2 sqrt(P)(log P)^2/(8 pi)
                         >= S - 599 - sqrt(P)(log P)^2/(4 pi).

Combine the two displays. QED

**Lemma 6 (a quadratic inequality).** Let H >= 1, L >= 0, B >= 0 be real with
H^2 - H + 1 <= L H + B. Then H < L + 1 + sqrt(B).

Proof. With a := (L+1)/2 the hypothesis gives (H - a)^2 <= B - 1 + a^2 < B + a^2
<= (sqrt(B) + a)^2, so H - a < sqrt(B) + a. QED

**Proposition A.** Assume RH. For every distinct run (n, H), with P := p_{n+H},

    H < (1/(2 sqrt(pi))) P^{1/4} log P + log P + 25.48 .

Proof. If P < 599 then by Lemma 1, H^2 - H + 1 <= S < 599, so H <= 24 (since
25^2 - 25 + 1 = 601), and the claim holds. If P >= 599, Lemmas 1 and 5 give
H^2 - H + 1 <= H log P + B with B = sqrt(P)(log P)^2/(4 pi) + 599. By Lemma 6 and
sqrt(u + v) <= sqrt(u) + sqrt(v),
H < log P + 1 + (1/(2 sqrt(pi))) P^{1/4} log P + sqrt(599), and sqrt(599) < 24.48. QED

**Proof of Theorem A.** Let x >= 50, 1 <= n < x, (n, H) a distinct run, P = p_{n+H}.
The right side of Proposition A is increasing in P. By Lemma 4(b),(c),
P^{1/4} <= 2 x^{1/4} (log x)^{1/4} and log P <= 2 log x, so

    H < (1/(2 sqrt(pi))) * 2 x^{1/4}(log x)^{1/4} * 2 log x + 2 log x + 25.48
      = (2/sqrt(pi)) x^{1/4} (log x)^{5/4} + 2 log x + 25.48 .

For the simplified form: D(x) := (4 - 2/sqrt(pi)) x^{1/4}(log x)^{5/4} - 2 log x - 25.48
satisfies D(50) > 8 (the first term is > 42.0, and 2 log 50 + 25.48 < 33.31) and
D'(x) >= (3.58 x^{1/4}(log x)^{1/4} - 2)/x > 0 for x >= 50, so D(x) > 0 for x >= 50. QED

## 2. Lemmas for Theorem B

**Lemma 7 (explicit Cramér theorem; CITED).** Assume RH. For every real t >= 1.4 * 10^5
the open interval (t - w(t), t + w(t)), where

    w(t) := (3/2) sqrt(t) log t + 2 sqrt(t),

contains at least sqrt(t) primes.

Citation whose text I read: A. W. Dudek, L. Grenié, G. Molteni, "Primes in explicit short
intervals on RH", arXiv:1503.05403v2 (2 Oct 2015; arXiv lists DOI
10.1142/S1793042116500858, Int. J. Number Theory), Theorem 1.1. What it states: assume RH,
x >= 2, c := 1/2 + 2/log x; then there are at least sqrt(x) primes in
(x - (c+1) sqrt(x) log x, x + (c+1) sqrt(x) log x). Here (c+1) sqrt(x) log x = w(x).
Hypothesis check: "RH" there is RH for zeta (the proof uses the explicit formula over the
nontrivial zeros of zeta). The theorem is stated for x >= 2. I use it only for
x >= 1.4 * 10^5, because that is the range in which the paper's Section 3 derives the
count from its inequality (3.1); the sentence in Section 3 covering 2 <= x <= 1.4 * 10^5 is
brief and I did not want to depend on my reading of it.
I did not check the paper's internal estimates. Corroboration read: A. W. Dudek,
arXiv:1402.6417v2, quotes Cramér's theorem in the same shape (its Theorem 1) and proves
a c = 3 + eps version for large x.

**Lemma 8 (packing).** Assume RH. Let 1.4 * 10^5 <= a < b be real, W := w(b) and
K := floor((b - a)/(2W)). Then pi(b) - pi(a) >= K sqrt(a).

Proof. For k = 1, ..., K put t_k := a + (2k-1) W and I_k := (t_k - W, t_k + W)
= (a + (2k-2)W, a + 2kW). The I_k are pairwise disjoint open intervals inside (a, b),
because a + 2KW <= b. Also a <= t_k < b, and w is increasing on [1, infinity), so
w(t_k) <= W and (t_k - w(t_k), t_k + w(t_k)) is contained in I_k. By Lemma 7 each I_k
contains at least sqrt(t_k) >= sqrt(a) primes. QED

**Proposition B.** Assume RH. Let (n, H) be a distinct run, A := p_n, P := p_{n+H},
and suppose P >= 5.6 * 10^5. Put lambda := 3 log P + 4, so that 2 w(P) = lambda sqrt(P).
Then A >= P/4 and

    H < sqrt(lambda) P^{1/4} + 2 lambda + 1 = sqrt(3 log P + 4) P^{1/4} + 6 log P + 9 .

Proof. Throughout, S := P - A, and by Lemma 1, H^2 - H + 1 <= S <= P - 2, which gives
(H - 1/2)^2 < P, i.e. H < sqrt(P) + 1/2.

Step 1: A >= P/4. Suppose A < P/4. Apply Lemma 8 with a = P/4 >= 1.4 * 10^5, b = P:
pi(P) - pi(P/4) >= floor((3P/4)/(lambda sqrt(P))) * sqrt(P)/2 >= 3P/(8 lambda) - sqrt(P)/2.
Since (P/4, P] is inside (A, P], the left side is <= H < sqrt(P) + 1/2. Hence
3P/(8 lambda) < (3/2) sqrt(P) + 1/2 <= 2 sqrt(P), i.e. sqrt(P) < (16/3) lambda
= 16 log P + 64/3. But f(P) := sqrt(P) - 16 log P - 64/3 has f'(P) > 0 for P > 1024 and
f(40000) = 200 - 16 log 40000 - 64/3 > 9, so f(P) > 0 for P >= 40000. Contradiction.

Step 2. Now A >= P/4 >= 1.4 * 10^5. Apply Lemma 8 with a = A, b = P. The number of primes
in (A, P] is exactly H, so H >= floor(S/(lambda sqrt(P))) * sqrt(A)
>= (S/(lambda sqrt(P)) - 1) * sqrt(P)/2. (If the bracket is negative this is trivial; if
not, use floor(u) >= u - 1 and sqrt(A) >= sqrt(P)/2.) Therefore
S <= 2 lambda H + lambda sqrt(P). With Lemma 1, H^2 - H + 1 <= (2 lambda) H + lambda sqrt(P),
and Lemma 6 gives H < 2 lambda + 1 + sqrt(lambda) P^{1/4}. QED

**Proof of Theorem B.** Let x >= 50, 1 <= n < x, (n, H) a distinct run, P = p_{n+H}.
If P < 5.6 * 10^5, Proposition A (whose right side is increasing in P and is < 140.86 at
P = 5.6 * 10^5) gives H <= 140. If P >= 5.6 * 10^5, Proposition B applies; its right side
is increasing in P, and by Lemma 4, P^{1/4} <= 2 x^{1/4}(log x)^{1/4} and
3 log P + 4 <= 6 log x + 4 <= 8 log x (as log x >= 2). So
H < sqrt(8 log x) * 2 x^{1/4}(log x)^{1/4} + 12 log x + 9
  = 4 sqrt(2) x^{1/4} (log x)^{3/4} + 12 log x + 9.
In both cases the stated bound holds. QED

## 3. Sanity check (not part of the proof)

check852.py (in this folder; pure Python, a few seconds) sieves primes to 2 * 10^7 and
confirms: Lemma 2 on [599, 2 * 10^7]; Lemma 3 for all m <= 1270607; the record values
of the longest distinct run (n, H) = (1,2), (7,3), (23,4), (30,5), (94,6), (219,7),
(279,8), (773,9), (1856,10), (3724,11), (6999,12), (7000,13), (19205,15), (184163,16),
(280103,17), (849876,18); and that Theorems A and B hold at those points. The true h(x)
in this range is about the size of log x, far below both bounds, so this checks the
definitions and arithmetic, not the strength of the theorems.

## 4. What this does and does not show

Shown: IF the Riemann Hypothesis holds, then h(x) << x^{1/4} (log x)^{3/4} (Theorem B),
and in particular h(x) << x^{1/4} (log x)^{5/4} (Theorem A, the lead), with the explicit
constants above for x >= 50.

Not shown, and not touched:
- Question (i) of the problem, h(x) > (log x)^c for some c > 0. This is a LOWER bound.
  An upper bound says nothing about it.
- Question (ii), h(x) = o(log x). The bounds here are of size x^{1/4 + o(1)}, far above
  log x. They are consistent with (ii) being true and with (ii) being false.
- So Erdős Problem 852 remains open exactly as on the page (status "open" on the page and
  in data/problems.yaml, last_update 2025-08-31). This file should not be described as
  progress on the problem as posed. It is at most a remark for the "estimate h(x)" part.

Relation to the Lean statement (formal-conjectures, origin/main,
FormalConjectures/ErdosProblems/852.lean): the file has erdos_852.parts.i (open),
erdos_852.parts.ii (open) and erdos_852.variants.tendsto_atTop (solved, h(x) -> infinity).
None of them is implied or refuted by Theorems A/B. The file contains no upper-bound
variant and no conditional (RH) variant. In its language Theorem A would read: under RH
there is C such that for all large real x, every n < x and every H with
DistinctGapRun n H satisfy H <= C x^{1/4} (log x)^{5/4}. Indexing: Lean's primeGap is
0-based (p_0 = 2), so a Lean run starting at n < x is a run here starting at n + 1 < x + 1;
the Lean-indexed maximum is therefore at most h(x + 1), and the same O-bounds hold.
Nothing here was formalised or compiled.

Is the result unconditional? This file proves "RH implies ...". The page saved in
refs/sutherland.html (as of 22 Nov 2026) reports checks of a Lean proof of RH announced on
20 Nov 2026, with some checks still running. I did not examine that proof. Whether the
hypothesis can be dropped depends entirely on that, and no claim about it is made here.

How it compares with the forum (comparisons INFERRED from sources I read only in part):
- Forum post by user rickyc (4 Aug 2026): h(x) << x^{0.26 + o(1)} unconditionally, by
  the same template with a short-interval theorem of R. Li (arXiv:2308.04458, v8 has no
  journal reference on arXiv). In v8 the relevant statement is Theorem 2 (intervals of length
  x^{theta + eps}, 0.52 <= theta <= 0.525); the post calls it "Thm 3". With
  Baker-Harman-Pintz (exponent 0.525) the same template gives x^{0.2625 + o(1)}.
  Under RH the exponent becomes 1/4. The gain is only 0.26 -> 0.25.
- Forum post by user Aron (15 Apr 2026): h(x) << x^{0.41 + eps} from Stadlmann's bound on
  the sum of squared gaps. Under RH, Selberg's bound (sum of d_n^2 over p_n <= X is
  << X log^3 X, as quoted in the introduction of Stadlmann, arXiv:2212.10867v2) would give
  only H^3 << X log^3 X, i.e. x^{1/3 + o(1)}, weaker than Theorems A and B.
- Lower bounds: the forum also has claims that h(x) >> (log x)^{1/3} unconditionally
  (posts by Przemek Chojecki and DavidTurturean, 24 Apr 2026, AI-assisted, unrefereed).
  If correct, that would answer question (i). I did not check them and nothing here
  depends on them or bears on them.
- Limit of the method: the argument only uses that an interval (A, P] of length
  >> sqrt(P) log P has about the expected number of primes. RH gives no information on
  shorter intervals, and a distinct run of length H needs only length about H^2, so this
  route cannot go below P^{1/4} (log P)^{1/2}. Theorem B is at that limit.

Novelty: I found no published statement of Theorem A or B (the triage note reports the
same). Both are short corollaries of known conditional theorems plus the forum's
template, and should be described that way.

## 5. Credit

- The template (S >= H^2 - H + 1 from parity and distinctness; H < x; P <= p_{2x};
  count primes in (A, P] with a short-interval theorem) is from the forum thread for #852:
  the parity/sum bound and "H < x" are in the post by user Aron (post 5426, 15 Apr 2026),
  and the short-interval packing is in the post by user rickyc (post 8358, 4 Aug 2026).
  CORRECTION to the lead and to TRIAGE.md: they attribute the Li-based post to
  carlos_toledo and the x^{0.41} post to Sothanaphan. In refs/forum.html each author line
  FOLLOWS its post; post 8358 is by rickyc and post 5426 is by Aron. carlos_toledo's post
  (8584) is the interval-arithmetic recomputation of constants; natso26 (Nat Sothanaphan)
  posted only the two short "standard check" replies. Several of these posts say they were
  produced with AI assistance and none is refereed.
- Lemma 2 carries Theorem A: von Koch (1901) for the O-form; Schoenfeld (1976) for the
  constant 1/(8 pi), as presented and re-proved under partial RH by J. Büthe.
- Lemma 7 carries Theorem B: Cramér (1920) for the O-form; Dudek, Grenié and Molteni for
  the explicit form used.
- The assembly (Lemmas 3-6, 8, Propositions A, B) is elementary and was done for this file.
  The triage reader had the 5/4 version; the 3/4 version was added in this pass.

## 6. Sources not read

- L. Schoenfeld, "Sharper bounds for the Chebyshev functions theta(x) and psi(x). II",
  Math. Comp. 30 (1976), 337-360. ams.org returned 403. Its content is taken only through
  Büthe's Theorem 2.
- H. von Koch (1901) and H. Cramér (1920): not obtained. Named for credit only.
- Journal versions of Büthe (Math. Comp. 2016) and of Dudek-Grenié-Molteni (IJNT): not
  read; the arXiv versions named above were read (statements, and the proofs of the two
  cited theorems at reading level, without checking their numerics).
- Baker-Harman-Pintz (2001) and Selberg (1943): not read; seen only as quoted in Li's and
  Stadlmann's introductions. Used only in the comparison paragraph.
- Li (arXiv:2308.04458v8) and Stadlmann (arXiv:2212.10867v2): only the introductions and
  main theorem statements were read. Used only in the comparison paragraph.
- [Er85c] Erdős, "On some of my problems in number theory I would most like to see solved"
  (1985): not obtained. The problem statement is taken from the erdosproblems.com page.
- The linked write-ups in the forum (ulam.ai PDF, Overleaf, ChatGPT sessions): not opened.
- The Lean proof of RH and the announcement it refers to: not examined.
