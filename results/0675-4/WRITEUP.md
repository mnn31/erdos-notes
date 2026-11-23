# Erdős 675(a), existence angle 1: what it takes for E to have the translation property

Date: 2026-11-23. Outcome: **PARTIAL**. Existence of n-shifts for all n is NOT proved. Proved instead:

1. **(Unconditional reformulation, Theorem 1.)** E has the translation property if and only if every finite
   subset of E has a positive translate inside E. The hard half of the problem is therefore exactly the
   "membership" half; the "non-membership" half (a not in E implies a+t not in E) comes for free from the
   membership half applied to a longer range (quantitatively: a one-sided shift for E∩[1, 5n²/4] is an n-shift).
2. **(Conditional existence, Theorem 2.)** Dickson's prime k-tuples conjecture for linear forms implies that E has
   the translation property, with n-shifts of the explicit shape t = 4·M_n·x.
3. **(Computation, Proposition 3.)** n-shifts exist for every n <= 39 (explicit t, checked by factorization);
   the least n-shifts are tabulated for n <= 39; no 40-shift is <= 10^11.

GRH (now a Lean theorem by Alpöge, per the task statement; I did not read that development) does not enter
anywhere, and I explain in Section 6 why I could not make it help with existence.

## 0. Setup and notation (VERIFIED against sources)

E = { m >= 1 : m = x² + y², x, y in Z_{>=0} }. For n >= 1, t >= 1 is an **n-shift** if for all 1 <= a <= n:
a in E iff a + t in E. E has the **translation property (TP)** if an n-shift exists for every n.
This is the definition on erdosproblems.com/675 (fetched 2026-11-23, refs/page675.html) and Definition 1 of
Liu's note (../../refs/erdos675a.txt). v_p(m) is the exponent of the prime p in m; q always denotes a prime
q ≡ 3 (mod 4).

**Prior work checked before starting (VERIFIED, read 2026-11-23).** Forum thread /forum/thread/675 (7 comments,
refs/forum675.html): the only part-(a) comment is Liu's lower bound (c < 1/10); Liu's note says explicitly
"We do not address the existence of such t". ../../PROOF.md (this project) proves every n-shift is divisible by
every q with 5(q-1)²/4 <= n; it also does not address existence. Nothing in these sources discusses
existence, conditional existence, or the reformulation below.

## 1. Basic lemmas

**Lemma 1.** If q ≡ 3 (mod 4) is prime, there is no u with u² ≡ -1 (mod q). Hence q | x² + y² implies q | x and q | y.

Proof. If u² ≡ -1 then u^(q-1) = (u²)^((q-1)/2) ≡ (-1)^((q-1)/2) = -1, since (q-1)/2 is odd; this contradicts
Fermat (q odd, so -1 ≢ 1). If q | x²+y² and q ∤ y, then u = x·y^(-1) mod q has u² ≡ -1; impossible. So q | y,
hence q | x², so q | x. ∎

**Lemma 2 (Fermat-Euler characterization; closure).** (a) E is closed under multiplication and contains 1, 2, every
square, and every prime p ≡ 1 (mod 4). (b) For m >= 1: m in E iff v_q(m) is even for every prime q ≡ 3 (mod 4).

Proof. (a) (x²+y²)(u²+v²) = |xu - yv|² + (xv + yu)², 1 = 1²+0², 2 = 1²+1², s² = s²+0². For p ≡ 1 (mod 4):
by Wilson, -1 ≡ (p-1)! = prod_{j=1}^{(p-1)/2} j(p-j) ≡ (-1)^((p-1)/2) (((p-1)/2)!)² = (((p-1)/2)!)², since
(p-1)/2 is even; let s = ((p-1)/2)!. Let k = floor(sqrt p) (so k < sqrt p < k+1, p not a square). The (k+1)²
> p numbers u - s·v (0 <= u, v <= k) are not all distinct mod p, so there are (x, y) ≠ (0,0) with |x|, |y| <= k
and x ≡ s·y (mod p). Then x² + y² ≡ (s²+1) y² ≡ 0 (mod p) and 0 < x² + y² <= 2k² < 2p, so x² + y² = p.
(b) (=>) Let m = x² + y² in E and k = v_q(m). Induct on k. If k >= 1, Lemma 1 gives q | x, q | y, so q² | m,
k >= 2 and m/q² = (x/q)² + (y/q)² is in E with v_q = k - 2, which is even by induction; so k is even.
(<=) m = 2^e · prod p_i^{f_i} · prod q_j^{2 g_j} with p_i ≡ 1 (mod 4) is a product of elements of E (part (a)). ∎

**Lemma 3 (valuation of a sum).** If v_p(a) = k and p^(k+1) | t then v_p(a + t) = k. If v_p(t) = j < v_p(a) then
v_p(a + t) = j.

Proof. a = p^k a', p ∤ a', t = p^(k+1) t'': a + t = p^k (a' + p t''), and a' + p t'' ≢ 0 (mod p). The second
statement is the same with the roles of a and t exchanged. ∎

**Lemma 4 (witness pairs; = PROOF.md Lemmas 3-4, re-proved here).** Let q ≡ 3 (mod 4) and r ≢ 0 (mod q).
There are w_1 < w_2 in E with w_1 ≡ w_2 ≡ r (mod q), w_1 ≢ w_2 (mod q²), and w_2 <= 5(q-1)²/4.

Proof. By Lemma 1, K = F_q[i] (i² = -1) is a field with q² elements. Frobenius z -> z^q fixes F_q and sends
i to i·(i²)^((q-1)/2) = -i, so N(z) := z^(q+1) = z·z^q = x² + y² for z = x + iy. N is a homomorphism K* -> K*;
N(z)^(q-1) = z^(q²-1) = 1, so N(K*) ⊆ F_q* (the roots of W^(q-1) = 1 in K are exactly F_q*). The kernel has
<= q+1 elements (roots of Z^(q+1) = 1), so |N(K*)| >= (q²-1)/(q+1) = q-1: N is onto F_q*, and every fibre
has exactly q+1 elements. So x² + y² ≡ r has q+1 solutions mod q, at most 2 of them with y ≡ 0 (x² ≡ r);
take one with y ≢ 0. Replacing x by -x and y by -y if needed, take integers 0 <= x <= (q-1)/2,
1 <= y <= (q-1)/2. Put w_1 = x² + y², w_2 = x² + (q-y)². Both are in E, both ≡ r (mod q),
w_2 - w_1 = q(q - 2y) with 1 <= q - 2y <= q - 2, so w_2 > w_1 and q² ∤ w_2 - w_1;
and w_2 <= ((q-1)/2)² + (q-1)² = 5(q-1)²/4. ∎

## 2. Theorem 1: the translation property is the "membership half" alone

Call t >= 1 a **one-sided N-shift** if a + t in E for every a in E ∩ [1, N].

**Lemma 5 (one-step forcing).** Let q ≡ 3 (mod 4), j >= 0, and let t be a one-sided N-shift with q^j | t.
Then q^(j+1) | t, provided
- j odd and q^(j+1) <= N, or
- j even and q^j · 5(q-1)²/4 <= N.

Proof. Suppose q^(j+1) ∤ t, so v_q(t) = j.
*j odd.* a := q^(j+1) is a square (j+1 even), so a in E, and a <= N; hence a + t in E. But
v_q(a) = j+1 > j = v_q(t), so v_q(a + t) = j (Lemma 3), which is odd: a + t ∉ E (Lemma 2b). Contradiction.
*j even.* Write t = q^j u with q ∤ u and let r ≡ -u (mod q), r ≢ 0. Take w_1, w_2 from Lemma 4 and set
a_i = q^j w_i. Since j is even, a_i in E (Lemma 2a), and 1 <= a_i <= q^j·5(q-1)²/4 <= N; so a_i + t = q^j (w_i + u)
is in E. Since j is even, w_i + u has the same valuation parities as a_i + t at every prime, so w_i + u in E
(Lemma 2b). Now q | w_i + u (as w_i ≡ r ≡ -u), so by Lemma 2b v_q(w_i + u) >= 2: w_i ≡ -u (mod q²) for i = 1, 2,
so w_1 ≡ w_2 (mod q²), contradicting Lemma 4. ∎

**Lemma 6 (one-sided implies two-sided).** Let n >= 1, N >= 5n²/4, and t a one-sided N-shift. Then t is an n-shift.

Proof. N >= 5n²/4 >= n, so a in E ∩ [1, n] gives a + t in E. Let b <= n, b ∉ E. By Lemma 2b there is
q ≡ 3 (mod 4) with k := v_q(b) odd; q <= q^k <= b <= n, so q^(k+1) <= n² and (5/4) q^(k+1) <= N.
Apply Lemma 5 for j = 0, 1, ..., k (starting from q^0 | t). Each hypothesis holds: for odd j <= k,
q^(j+1) <= q^(k+1) <= N; for even j <= k (so j <= k-1, as k is odd), q^j·5(q-1)²/4 < (5/4) q^(j+2) <= (5/4) q^(k+1) <= N.
So q^(k+1) | t, and Lemma 3 gives v_q(b + t) = k, odd; hence b + t ∉ E. ∎

**Lemma 7 (shifts compose).** If t_1 is an n-shift and t_2 is an (n + t_1)-shift, then t_1 + t_2 is an n-shift.
More generally, put n_0 = n and choose t_i an n_{i-1}-shift, n_i = n_{i-1} + t_i (i = 1, 2, ...). Then for all
0 <= i < j, s_{i,j} := t_{i+1} + ... + t_j is an n_i-shift, hence an n-shift.

Proof. Induction on j. j = i+1: by choice. j > i+1: for 1 <= a <= n_i, a in E iff a + s_{i,j-1} in E (induction),
and 1 <= a + s_{i,j-1} <= n_i + t_{i+1} + ... + t_{j-1} = n_{j-1}, so, t_j being an n_{j-1}-shift,
a + s_{i,j-1} in E iff a + s_{i,j} in E. Finally an n_i-shift is an n-shift because n_i >= n. ∎

**Theorem 1 (unconditional).** The following are equivalent.
- (i) E has the translation property.
- (ii) For every finite A ⊆ E there is t >= 1 with A + t ⊆ E.
- (iii) For every finite A ⊆ E and every M >= 1 there is t >= 1 with M | t and A + t ⊆ E.

Quantitatively: any t with (E ∩ [1, ceil(5n²/4)]) + t ⊆ E is an n-shift.

Proof. (iii) => (ii): take M = 1. (ii) => (i): given n, apply (ii) to A = E ∩ [1, N], N = ceil(5n²/4), and use Lemma 6.
(i) => (iii): let A ⊆ E be finite, n = max(A ∪ {1}), M >= 1. Using (i) choose t_1, t_2, ..., t_M as in Lemma 7.
Among the M+1 partial sums S_0 = 0, S_1 = t_1, ..., S_M = t_1 + ... + t_M two are congruent mod M, say S_i ≡ S_j
with i < j. Then s = S_j - S_i = s_{i,j} >= 1, M | s, and s is an n-shift (Lemma 7); so a + s in E for all a in A. ∎

Consequences worth recording (each immediate from Theorem 1):
- The "non-membership" half is never the obstruction: for every n the CRT gives t (any multiple of
  prod_{q<=n} q^(e_q) with q^(e_q) > n) with a ∉ E => a + t ∉ E for all a <= n (Lemma 3), and Lemma 6 shows the
  membership half on [1, 5n²/4] forces this anyway.
- TP is a pure **recurrence statement**: "every finite configuration that occurs in E occurs again (shifted) in E",
  equivalently a qualitative k-tuple statement for E restricted to tuples A that already lie in E (which
  automatically have no local obstruction; see Lemma 8).
- TP would give n-shifts in every residue class 0 (mod M), for every M.

**Lemma 8 (no local obstruction).** For every n and y there is t >= 1 such that for all 1 <= a <= n and all primes
q ≡ 3 (mod 4) with q <= y: v_q(a + t) ≡ v_q(a) (mod 2). (Take t = prod_{q<=n} q^(e_q) · prod_{n<q<=y} q with
q^(e_q) > n: for q <= n use Lemma 3; for q > n, q ∤ a + t since a + t ≡ a ≢ 0 (mod q).) So whether t is an
n-shift is decided entirely by the primes q > y dividing the numbers a + t, for any y one likes; existence is a
question about large prime factors, i.e. a sieve / k-tuples question.

## 3. Theorem 2: Dickson's conjecture implies the translation property

**Hypothesis D (Dickson's conjecture, stated in full here; not proved, not cited for any content).**
Let f_i(x) = b_i x + c_i (1 <= i <= k) with integers b_i >= 1, c_i. If for every prime p there is an integer x with
p ∤ f_1(x)···f_k(x), then there are infinitely many positive integers x for which f_1(x), ..., f_k(x) are all prime.

**Theorem 2.** Assume Hypothesis D (for all k). Then E has the translation property. Explicitly: for n >= 1 let
e_p be least with p^(e_p) > n, M_n = prod_{p <= n prime} p^(e_p), and A = E ∩ [1, n]. Then there is x >= 1 such
that 1 + 4(M_n/a)x is prime for every a in A, and every such x gives the n-shift t = 4 M_n x.

Proof. Every a <= n divides M_n (each p | a has p <= n and p^(v_p(a)) <= a < p^(e_p)). Put c_a = M_n / a and
g_a(x) = 1 + 4 c_a x (a in A), linear forms with leading coefficient 4c_a >= 1. At x = 0 the product of the g_a
is 1, so no prime divides the product for every x: the family is admissible, and D gives x >= 1 with all g_a(x)
prime. Let t = 4 M_n x and 1 <= a <= n.
- a in E: a + t = a(1 + 4 c_a x) = a·g_a(x). g_a(x) is a prime ≡ 1 (mod 4), so in E (Lemma 2a), hence a + t in E.
- a ∉ E: take q ≡ 3 (mod 4) with k = v_q(a) odd (Lemma 2b). q^k <= a <= n < q^(e_q), so k + 1 <= e_q and
  q^(k+1) | M_n | t. Lemma 3: v_q(a + t) = k is odd, so a + t ∉ E. ∎

Remarks. (1) Only "g_a(x) in E for all a in A" is used, so the weaker hypothesis
"for every finite family c_1, ..., c_k >= 1 there is x >= 1 with 1 + 4c_i x in E for all i" already implies TP.
(2) The number of forms is k = |E ∩ [1,n]|, which tends to infinity, so D is needed for every k; no fixed-k case
(and no known theorem) suffices. (3) D is a special case of Schinzel's Hypothesis H (both are standard open
conjectures; I state D in full above so nothing depends on recalling a reference). (4) The shifts produced have
log t ≍ log M_n, i.e. of order n; the proved lower bound (PROOF.md) is log t >= (1/sqrt5 - o(1)) sqrt n.
The data in Section 4 (log t_n / n ≈ 0.52-0.65 for n = 24..39) fit neither end conclusively.

Sanity run (code/verify.py part [3]): for every n <= 12 the least x with all g_a(x) prime was found
(e.g. n = 10: 7 forms, x = 2465883, t = 5219781134400) and t = 4 M_n x was checked to be an n-shift by writing
down explicit two-square representations of a + t for a in E and an odd q-valuation for a ∉ E.

## 4. Proposition 3: computation (VERIFIED by two independent programs for existence; minimality by one + partial cross-check)

**Proposition 3.** E has an n-shift for every n <= 39. The least n-shift t_n is:

| n | least n-shift t_n | factorization |
|---|---|---|
| 1 | 1 | 1 |
| 2-3 | 3 | 3 |
| 4 | 16 | 2^4 |
| 5-7 | 48 | 2^4·3 |
| 8 | 96 | 2^5·3 |
| 9-12 | 2304 | 2^8·3^2 |
| 13-16 | 40320 | 2^7·3^2·5·7 |
| 17 | 173376 | 2^6·3^2·7·43 |
| 18-24 | 1761984 | 2^6·3^2·7·19·23 |
| 25-31 | 10269504 | 2^6·3^4·7·283 |
| 32-36 | 755048448 | 2^13·3^2·7^2·11·19 |
| 37-39 | 87196919040 | 2^8·3^3·5·7^2·11·31·151 |
| 40 | none <= 10^11 | |

- Existence (all n <= 39): each listed t is checked to be an n-shift in pure Python by trial-division factorization
  of a + t, a <= n (verify.py [1]); E-membership by factorization was itself checked against brute-force
  x² + y² search for m <= 20000 ([0]).
- Minimality: the C program scans every t in [1, 10^11] (segmented sieve over primes ≡ 3 mod 4; see code comments).
  For n <= 31 it agrees with an independent numpy brute force over t <= 3·10^7 ([1b]); for 32 <= n <= 40 minimality
  rests on the C program alone.
- Consistency with the lower-bound theory: 3 | t_n for n >= 5 and 9 | t_n for n >= 9 (Lemma 5 with j = 1 applied to
  an n-shift needs only 9 <= n), as forced. The previously known values (n <= 31, PROOF.md) are reproduced.
- Forcing lemma sanity check ([2]): for N in {5, 8, 12, 16, 20, 24, 28}, all one-sided N-shifts t <= 2·10^7 are
  divisible by the prime powers Lemma 5 predicts. Observation (empirical only, not proved): in these ranges every
  one-sided N-shift was already a genuine N-shift, far better than the n <= sqrt(4N/5) that Lemma 6 guarantees.

## 5. A small negative result on algebraic families

**Remark 9.** One might hope for a polynomial family t(m) with a + t(m) identically a sum of two squares of
polynomials for every a in E ∩ [1, n]. The simplest shape, t = D m² with integer-coefficient linear polynomials,
already fails as soon as n >= 2. Proof: if a + D m² = (αm + β)² + (γm + δ)² identically (α, β, γ, δ in Z), comparing
coefficients gives α² + γ² = D, αβ + γδ = 0, β² + δ² = a. As a >= 1, (β, δ) ≠ 0, so the vector (α, γ), being orthogonal
to (β, δ) in Q², equals λ(-δ, β) for some rational λ, and D = λ²(β² + δ²) = λ² a. Doing this for a = 1 and a = 2
(both in E) gives D = λ_1² = 2 λ_2², so 2 would be a rational square: impossible. (Only this one-variable quadratic
shape is excluded; I found no other identity either, but did not search systematically.)

## 6. Where each route to unconditional existence breaks (the gap)

All of the following is INFERRED (my analysis), not a theorem, unless marked.

- **CRT on small primes (VERIFIED as far as it goes: Lemma 8, Theorem 1).** CRT handles every prime <= y for any y,
  and handles the whole non-membership half. What remains, after fixing t ≡ 0 (mod M_n), is exactly
  "1 + 4 c_a x in E for all a in E ∩ [1, n]": k ≍ n / sqrt(log n) one-variable linear forms simultaneously in E.
  By Theorem 1 nothing weaker can suffice: TP is equivalent to the recurrence of every finite E-configuration.
- **Sieve.** Detecting "m in E" for m <= X requires excluding primes q ≡ 3 (mod 4) to odd powers up to X (Lemma 8 shows
  no finite set of small primes decides it). A sieve of dimension κ = k/2 (k forms, each with a half-dimensional
  condition) has a sifting limit growing with κ, so with any fixed level of distribution it can only sieve up to
  X^θ with θ -> 0 as k -> ∞, leaving each value with many possible large prime factors ≡ 3 (mod 4). It cannot
  certify all k values at once.
- **GRH / Alpöge.** GRH for Dirichlet L-functions gives (pointwise) level of distribution 1/2 for primes, and for E,
  in progressions, which is what Bombieri-Vinogradov already gives on average. That does not touch the sifting-limit
  problem above, so I see no way for GRH to give existence. On the lower-bound side GRH only gives Liu's c < 1/4,
  already dominated by PROOF.md's unconditional c < 1/2.
- **Maynard-Tao type sieves.** (Not read; recalled only, so not used.) They produce many, not all, of an admissible
  family of linear forms prime simultaneously; we need all k.
- **Green-Tao / Matthiesen-type linear-equations theory.** (Not read; recalled only.) That theory handles systems of
  finite complexity (pairwise non-proportional forms in >= 2 variables); the system a + t (one variable t) consists
  of pairwise proportional forms, i.e. infinite complexity. Rewriting t with more variables does not change this,
  since all forms still share the same linear part.
- **Algebraic identities.** Remark 9 rules out the simplest polynomial family; I found no other.

Conclusion: within the tools I could check, existence for E is equivalent (Theorem 1) to an open qualitative
k-tuples statement for E with k -> ∞, implied by Dickson's conjecture (Theorem 2). I did not find an unconditional
route, and I do not claim one is impossible.

## 7. What this does and does not show

Does show (rigorous):
- Theorem 1: TP(E) <=> every finite subset of E has a positive translate in E <=> the same with t in any prescribed
  ideal MZ; and any t that preserves membership of E ∩ [1, 5n²/4] is a full n-shift. Unconditional and elementary.
- Theorem 2: Dickson's conjecture => TP(E), with explicit shifts t = 4 M_n x.
- Proposition 3: n-shifts exist for all n <= 39 (explicit, independently checked); least shifts listed; no 40-shift <= 10^11.

Does not show:
- Unconditional existence of n-shifts for all n (part (a) remains open). No disproof either.
- Anything from GRH; GRH is not used.
- Minimality of t_n for 32 <= n <= 39 by two independent programs (only the C scan covers t > 3·10^7).
- The empirical "one-sided N-shift is already an N-shift" observation in Section 4 is not proved.
- Novelty: Theorems 1-2 were not found in the forum thread, the problem page, Liu's note, or PROOF.md; I did not
  search arXiv or the literature on k-tuples of sums of two squares, so they may be known or folklore.

## 8. Sources not read

- Dickson (1904), Schinzel-Sierpiński (Hypothesis H): not read; Hypothesis D is stated in full above and used only as a hypothesis.
- Maynard / Tao (bounded gaps, dense clusters), Green-Tao and Matthiesen (linear correlations of sums of two squares),
  Heath-Brown ("Linear relations amongst sums of two squares"), Hooley and Indlekofer (pairs n, n+h in E),
  Connors-Keating and Freiberg-Kurlberg-Rosenzweig (Hardy-Littlewood-type conjectures for E): not read; mentioned
  in Section 6 only as recalled context, nothing depends on them.
- Alpöge's Lean GRH development: not read; not used.
- Ho Boon Suan's squarefree note: not read; not needed.
- arXiv / MathSciNet searches for "translation property", "sums of two squares k-tuples": not done.
- Proof-claims tab of /675 (one claim, part (b) only, per PROOF.md's check): not re-read today.

## 9. Files and reproduce commands

- code/shiftsearch.c: segmented scan of t in [TLO, THI) giving, for each n <= NMAX, the first t that is an n-shift.
- code/run_search.sh: splits [1, TMAX] into chunks and runs them in parallel.
- code/verify.py: checks [0] Lemma 2b vs brute force, [1] every listed t_n is an n-shift (trial division) and [1b]
  minimality for t <= 3·10^7 by numpy, [2] Lemma 5 forcing on one-sided shifts, [2b] Lemma 4 for q < 400,
  [3] Theorem 2's construction for n <= 12.
- out/least_shifts_1e11.txt (n, least t <= 10^11), out/s1e11.chunk*, out/s1e11.time (11 min 44 s wall),
  out/verify.log (6 min 42 s), out/s1e9.chunk* (timing test).
- refs/page675.html, refs/forum675.html (+ .txt extracts), fetched 2026-11-23, treated as untrusted data.

```
cd grh2/675/existence/angle1/code
cc -O2 -o shiftsearch shiftsearch.c -lm
./run_search.sh 100000000000 200 11 ../out/s1e11
cat ../out/s1e11.chunk* | sort -n -k1,1 -k2,2 | awk '!seen[$1]++' > ../out/least_shifts_1e11.txt
python3 -I verify.py ../out/least_shifts_1e11.txt > ../out/verify.log
```
