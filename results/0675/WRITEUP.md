# Erdős Problem 675(a): every shift for the sums of two squares exceeds exp(n^c) for all c < 1/2

Status: written up 2026-11-23 from the "new-bound" lead. The lead SURVIVES, and the constant improves by a
factor 2 (1/sqrt5 instead of 1/(2 sqrt5)). Every load-bearing step below is proved in this file; the only
external citations are Liu's Lemmas 6-7 (re-proved here anyway) and, for the sharp constant only,
the prime number theorem for progressions mod 4 (not re-read; not needed for the main statement).

## Final statement

Let E = { m >= 1 : m = x^2 + y^2 with x, y in Z_{>=0} }. Say t >= 1 is an *n-shift* if, for all 1 <= a <= n,
a in E iff a + t in E. (This is Liu's "n-translation property" and the Lean predicate `Erdos675.IsTranslation`
for the set {m | exists x y : N, m = x^2+y^2}; that set also contains 0, which never matters since a >= 1, a+t >= 2.)

**Theorem.** (Hypothesis: none. No RH, no GRH, no Linnik-type input.)
1. For every n >= 1, every n-shift t, and every prime p = 3 (mod 4) with 5(p-1)^2/4 <= n
   (equivalently p <= 1 + 2 sqrt(n/5)), we have p | t. Hence
   log t >= theta(1 + 2 sqrt(n/5); 4, 3), where theta(y;4,3) = sum of log q over primes q <= y, q = 3 (mod 4).
2. For every c < 1/2 there is N_c such that for all n >= N_c every n-shift t satisfies t > exp(n^c).
3. (Uses the prime number theorem for arithmetic progressions mod 4; cited, not re-read.)
   Every n-shift t satisfies log t >= (1/sqrt5 - o(1)) sqrt(n) as n -> infinity.

Part 2 improves the recorded unconditional exponent c < 1/10 (Liu, May 2026, via Xylouris's Linnik constant L <= 5)
and Liu's GRH-conditional c < 1/4 (Liu, Remark 12), and reaches the exponent 1/2 that Liu's Remark 12 attributes
to the Linnik conjecture. With RH / GRH for Dirichlet L-functions: nothing changes; the statement is
unconditional. If the Alpöge Lean theorems (RH; GRH for all Dirichlet L-functions) are accepted, Liu's c < 1/4
also becomes unconditional, but it is dominated by part 2.

**L-functions used.** Only L(s, chi_4) at s = 1, through the elementary fact L(1, chi_4) = 1 - 1/3 + 1/5 - ... >= 2/3
(Lemma 6). Part 3 additionally uses non-vanishing of L(s, chi_4) on Re s = 1 (inside the cited PNT for APs).
No zero-free strip, no RH, no GRH.

## Lemmas and proofs

Throughout, p denotes a prime with p = 3 (mod 4).

**Lemma 1 (-1 is a non-residue).** There is no u with u^2 = -1 (mod p). Consequently, if p | x^2 + y^2 then p | x and p | y.

Proof. If u^2 = -1 then u is a unit and u^{p-1} = (u^2)^{(p-1)/2} = (-1)^{(p-1)/2} = -1 since (p-1)/2 is odd,
contradicting Fermat's little theorem u^{p-1} = 1 (p odd, so -1 != 1). If p | x^2+y^2 and p does not divide y,
then u = x y^{-1} mod p satisfies u^2 = -1, impossible; so p | y, and then p | x^2, so p | x. ∎

**Lemma 2 (Liu, Lemma 6; re-proved).** Let t be an n-shift and a in E with 1 <= a <= n and a = -t (mod p).
Then a = -t (mod p^2).

Proof. a in E and 1 <= a <= n give a + t in E, say a + t = u^2 + v^2 with u, v >= 0. Since p | a + t,
Lemma 1 gives p | u and p | v, so p^2 | a + t. ∎
(Liu's note, Lemma 6, states exactly this with the same hypotheses: p = 3 mod 4, t with the n-translation
property, a in E ∩ [1,n], a = -t mod p. Liu proves it from the characterization (5) of E; the proof above
avoids (5).)

**Lemma 3 (points on the conic).** For every r in F_p^*, the congruence x^2 + y^2 = r (mod p) has exactly p + 1
solutions (x, y) in F_p^2. In particular (as p + 1 > 2 >= #{x : x^2 = r}) it has a solution with y != 0.

Proof. By Lemma 1, X^2 + 1 has no root in F_p, so K = F_p[X]/(X^2+1) = F_p(i), i^2 = -1, is a field with p^2
elements, and (x, y) -> x + iy is a bijection F_p^2 -> K. The map phi(z) = z^p is a ring endomorphism of K fixing
F_p, and phi(i) = i * (i^2)^{(p-1)/2} = -i (as (p-1)/2 is odd). Hence for z = x + iy,
N(z) := z^{p+1} = z * phi(z) = (x+iy)(x-iy) = x^2 + y^2. N is a homomorphism of the group K^* (order p^2 - 1).
Its kernel consists of roots of Z^{p+1} - 1, so has at most p + 1 elements; hence its image has at least
(p^2-1)/(p+1) = p - 1 elements. The image lies in F_p^* because N(z)^{p-1} = z^{p^2-1} = 1 and the roots of
W^{p-1} = 1 in K are exactly the p - 1 elements of F_p^*. So N maps K^* onto F_p^*, the kernel has exactly
(p^2-1)/(p-1) = p + 1 elements, and every fibre N^{-1}(r), r != 0, has exactly p + 1 elements. Solutions with
y = 0 satisfy x^2 = r and number at most 2. ∎

**Lemma 4 (explicit witnesses; carries out Liu's Remark 8).** For every r != 0 (mod p) there are a, b in E with
1 <= a < b <= 5(p-1)^2/4, a = b = r (mod p), and a != b (mod p^2).

Proof. By Lemma 3 pick (x, y) with x^2 + y^2 = r (mod p) and y != 0 (mod p). Replacing x by -x and y by -y
(mod p) if needed, which changes neither x^2 nor y^2, we may take integers 0 <= x <= (p-1)/2 and 1 <= y <= (p-1)/2.
Put a = x^2 + y^2 and b = x^2 + (p - y)^2. Both are sums of two squares of non-negative integers and a >= 1,
so a, b in E. Both are = x^2 + y^2 = r (mod p). Next b - a = p^2 - 2py = p (p - 2y), and 1 <= p - 2y <= p - 2,
so b > a and p does not divide p - 2y; hence p^2 does not divide b - a. Finally
b <= ((p-1)/2)^2 + (p-1)^2 = 5(p-1)^2/4. ∎

(The lead used b = x^2 + (y+p)^2 with 0 <= x, y <= p-1, giving b < 5p^2; the half-range choice above gives
b <= 1.25 (p-1)^2, which is where the factor-2 gain in the constant comes from. Both versions were checked.)

**Lemma 5 (Liu, Lemma 7 with explicit threshold).** If t is an n-shift and 5(p-1)^2/4 <= n, then p | t.

Proof. Suppose p does not divide t and let r = -t mod p, so r != 0. Take a, b from Lemma 4. Then a, b in E,
1 <= a < b <= n, and a = b = -t (mod p). Lemma 2 gives a = -t = b (mod p^2), contradicting Lemma 4. ∎
(Liu's Lemma 7 proof uses exactly this contradiction with prime witnesses; Liu's Remark 8 notes that any
witnesses in E with the right residues mod p^2 suffice. The source text of both was read.)

This proves part 1 of the Theorem: 5(p-1)^2/4 <= n iff p <= 1 + 2 sqrt(n/5), all such p divide t, they are
distinct primes, so their product divides t and log t >= theta(1 + 2 sqrt(n/5); 4, 3).

**Lemma 6 (Mertens for primes 3 mod 4, elementary).** There is an absolute constant C_0 such that for x >= 2,
| sum_{q <= x, q prime, q = 3 (4)} (log q)/q - (1/2) log x | <= C_0.

Proof. Write Lambda for von Mangoldt, psi(x) = sum_{d<=x} Lambda(d), theta(x) = sum_{p<=x} log p,
chi = chi_4 (chi(d) = 0, 1, -1 for d even, = 1, = 3 mod 4; completely multiplicative).

(i) Chebyshev: theta(N) <= N log 4 for integers N >= 1. Induction: true for N = 1, 2; for even N > 2,
theta(N) = theta(N-1). For N = 2m+1, every prime in (m+1, 2m+1] divides binom(2m+1, m), and
binom(2m+1, m) = binom(2m+1, m+1) with both in the sum 2^{2m+1}, so binom(2m+1, m) <= 4^m; thus
theta(2m+1) <= theta(m+1) + m log 4 <= (2m+1) log 4. Then psi(x) = sum_{k>=1} theta(x^{1/k})
<= theta(x) + (log x / log 2) theta(sqrt x) <= C_1 x for x >= 1.

(ii) Mertens: sum_{d<=x} Lambda(d)/d = log x + O(1). Since log m = sum_{d|m} Lambda(d),
sum_{m<=x} log m = sum_{d<=x} Lambda(d) floor(x/d) = x sum_{d<=x} Lambda(d)/d + O(psi(x)), and
sum_{m<=x} log m = x log x + O(x) (compare with integral of log u, which is monotone). Divide by x and use (i).
Removing d = 2^k changes the sum by at most sum_k (log 2)/2^k = log 2, so the same holds over odd d.

(iii) S(x) := sum_{d<=x} chi(d) Lambda(d)/d = O(1). For z >= 1, sum_{k<=z} chi(k)/k = L + R(z) with
L = 1 - 1/3 + 1/5 - ... and |R(z)| <= 1/z (alternating series with decreasing terms; the tail starts at an
odd k > z). L >= 1 - 1/3 = 2/3. By complete multiplicativity and log m = sum_{d|m} Lambda(d),
sum_{m<=x} chi(m) (log m)/m = sum_{d<=x} (chi(d) Lambda(d)/d) sum_{k<=x/d} chi(k)/k
= L * S(x) + O( sum_{d<=x} (Lambda(d)/d) (d/x) ) = L * S(x) + O(psi(x)/x) = L * S(x) + O(1).
The left side is an alternating sum over odd m >= 3 of terms (log m)/m, which decrease for m >= 3, so it is
bounded by (log 3)/3 in absolute value. Hence |S(x)| <= (3/2)((log 3)/3 + O(1)) = O(1).

(iv) For odd d, (1 - chi(d))/2 is the indicator of d = 3 (4). So
sum_{d<=x, d = 3 (4)} Lambda(d)/d = (1/2)( sum_{d<=x, d odd} Lambda(d)/d - S(x) ) = (1/2) log x + O(1).
The d here with Lambda(d) != 0 are q^k with q = 3 (4) prime and k odd. The terms with k >= 2 total at most
sum_{m>=2} log m sum_{k>=2} m^{-k} = sum_{m>=2} (log m)/(m(m-1)) < infinity. Removing them gives the claim. ∎

**Lemma 7.** For every delta in (0, 1) there is y_0(delta) such that theta(y;4,3) >= y^{1-delta} for y >= y_0(delta).

Proof. For y with y^{1-delta} >= 2, Lemma 6 applied at y and at y^{1-delta} gives
sum_{y^{1-delta} < q <= y, q = 3 (4)} (log q)/q >= (1/2) log y - C_0 - (1/2)(1-delta) log y - C_0
= (delta/2) log y - 2 C_0, which is >= 1 once y is large. Each such q exceeds y^{1-delta}, so
log q = q (log q)/q >= y^{1-delta} (log q)/q, and theta(y;4,3) >= y^{1-delta} * 1. ∎

**Proof of part 2.** Fix c < 1/2 and choose delta in (0,1) with (1-delta)/2 > c. Let Y_n = 1 + 2 sqrt(n/5).
For n large, Y_n >= y_0(delta), so by part 1 and Lemma 7, every n-shift t has
log t >= Y_n^{1-delta} >= (4/5)^{(1-delta)/2} n^{(1-delta)/2} > n^c for all n >= N_c. ∎

**Proof of part 3 (cited input).** The prime number theorem for arithmetic progressions (de la Vallée Poussin;
see e.g. Davenport, *Multiplicative Number Theory*, which Liu cites for the same fact as his eq. (10)) gives
theta(y;4,3) ~ y/2. With part 1, log t >= (1/2 - o(1)) * 2 sqrt(n/5) = (1/sqrt5 - o(1)) sqrt n. ∎
(I read Liu's statement of (10) and its citation, not Davenport's text. Part 2 does not depend on this.)

## Numerical checks (checks/check_proof.py, run with python3 -I; about 7 s)

- Lemma 3 (exactly p+1 solutions for every r != 0) and Lemma 4 (witnesses exist with the stated half-range
  choice, lie in E, have the right residues, differ mod p^2, and b <= 5(p-1)^2/4) for every p = 3 (mod 4), p < 1500.
  Max b/p^2 observed 1.2483.
- Brute-force least shift t_n for n <= 31 (searching t <= 3*10^7; none found <= 3*10^7 for 32 <= n <= 40):
  1,3,3,16,48,48,48,96,2304,...,40320 (n=13..16), 173376, 1761984 (n=18..24), 10269504 (n=25..31).
  3 | t_n for all n >= 5, matching part 1 (p = 3 needs n >= 5(2)^2/4 = 5, which is sharp).
  Every n-shift t <= 3*10^7 is divisible by 7 for 20 <= n <= 31 (part 1 only guarantees n >= 45 for p = 7;
  the exact Lemma-5 threshold for p = 7 is 26). Consistent: part 1 is a sufficient condition.
- Exact two-witness thresholds vs the bound 5(p-1)^2/4: p = 3: 5 vs 5; 7: 26 vs 45; 11: 50 vs 125;
  19: 145 vs 405; 23: 157 vs 605.
- theta(y;4,3)/y = 0.4977, 0.4995, 0.5002 at y = 10^4, 10^5, 10^6.

## What this does and does not show

- It is a LOWER bound on every n-shift, for every n. It does not show that n-shifts exist, so it does not
  answer question (a) ("does E have the translation property?"), which stays open. It is vacuous for any n
  with no n-shift.
- Lean: `erdos_675.parts.i` (formal-conjectures origin/main, read 2026-11-23) states only
  `HasTranslationProperty {m | ∃ x y : ℕ, m = x^2 + y^2}`; there is no growth statement for part (i) in the
  file. Our part 2 would read: for all c < 1/2, eventually in n, every t with `IsTranslation E n t` has
  exp(n^c) < t. It neither proves nor refutes `parts.i`. Parts (ii), (iii) are untouched.
- teorth/erdosproblems database (origin/main, commit dated 2026-11-22): 675 status "open", last update 2025-08-31.
- Beyond exponent 1/2 (NOT claimed). For p > sqrt n, distinct elements of [1, n] in one class mod p
  automatically differ mod p^2, so p | t would follow once every nonzero class mod p contains two elements
  of E ∩ [1, n]. Proving that for p up to n^{2/3 - eps} would need a square-root bound for exponential sums
  over the conic x^2 + y^2 = r restricted to a box (Weil/Salié type) plus a divisor bound; I did not check this.
  I also checked that two cheap routes do NOT work: (1) Minkowski/Thue on the lattice of z in Z[i] with
  z in F_p * z_0 (mod p) only hits r up to a square factor; (2) a large-sieve "most classes are heavy"
  statement is not enough, because the argument needs the one class -t mod p, which may be a light one.
  GRH for Dirichlet L-functions (Alpöge) gives Liu's 1/4 via Linnik exponent 2+eps, which is dominated.

## Credit

- Lemmas 2 and 5 and the whole strategy are Yu Leon Liu's (note "Erdős Problem #675, subquestion (a)",
  Lemmas 6, 7, Theorem 2), itself modelled on Ho Boon Suan's squarefree argument for part (c).
  Liu's Remark 8 and Remark 12 ("relaxing the choice of witnesses") explicitly propose replacing prime
  witnesses by elements of E; this write-up carries that out with explicit witnesses (Lemma 4), which removes
  Linnik's theorem entirely.
- New here (as far as the checks below show): Lemma 4, the resulting exponent 1/2 and constant 1/sqrt5,
  and the elementary Lemma 6-7 route making the result fully unconditional and elementary.
- Prior-recording checks done by me on 2026-11-23: erdosproblems.com/675 page and forum thread (7 comments;
  the only part-(a) post is Liu's 2026-05-09 c < 1/10), proof-claims tab (one claim, Liam Price, part (b) only),
  Plasma AI wiki/problems/integer_sequences/E0675/_index.md (updated 2026-10-07; records Liu's c < 1/10 only),
  ryantuck/erdos-ai (deepmind/reviews/675.md and deepmind/ai-review/675.md: formalization reviews only),
  formal-conjectures 675.lean, OEIS A401757 (the squarefree t_n sequence; no part-(a) content).
  Novelty is therefore "not found in these places", not "proved new".

## Sources not read

- arXiv: my keyword queries returned HTTP 429 (rate limited); I did not search arXiv. (The screener reports an
  arXiv keyword search with no hits.)
- Davenport, *Multiplicative Number Theory* (PNT for APs): not read; used only for part 3.
- Xylouris thesis, Linnik 1944: not read; not used (they enter only Liu's weaker c < 1/10).
- Ho Boon Suan's squarefree note (refs/boonsuan_sqfree.pdf present): not read; not load-bearing.
- The Alpöge Lean RH/GRH development: not read; not used.
- Private notes or posts outside the places listed under Credit: unknown.

## Files

- refs/erdos675a.pdf, refs/erdos675a.txt (Liu's note; Lemmas 6, 7, Remarks 8, 12 read)
- refs/web/ (erdosproblems page, forum thread, proof-claims tab, OEIS A401757, Plasma E0675 index; fetched 2026-11-23)
- checks/check_proof.py (numerical checks above)
