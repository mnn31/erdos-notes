# Erdős 675(a): n-shifts of the sums of two squares exceed exp(n^c) for every c < 2/3

Angle 1 of "beyond 1/2": count points of the conic x^2 + y^2 = r (mod p) in a box with Kloosterman-sum bounds.
Date: 2026-11-23. Builds on ../../PROOF.md (exponent 1/2) and Liu's note (refs in ../../refs/erdos675a.txt).

## 0. Prior-work check done before starting (VERIFIED, 2026-11-23)

- erdosproblems.com/675 and /forum/thread/675 re-fetched today (refs/fetch_20261123/, untrusted data). Still 7
  comments and 1 proof claim. The only part-(a) post is Liu's (2026-05-09, c < 1/10). Nobody has posted 1/2 or anything
  beyond it. The other posts are about part (c) (Ho Boon Suan 25/72, a 3/8 suggestion that was questioned) and one
  typo note.
- Liu's note (../../refs/erdos675a.txt, read in full): Lemma 6 (mod-p^2 lifting), Lemma 7 (two witnesses that differ
  mod p^2 force p | t), Remark 8 / Remark 12 (any witnesses in E will do; "sharp bounds here would likely improve
  the constant"). Liu does not count points on the conic and does not use exponential sums.
- ../../PROOF.md (read in full): exponent 1/2 using explicit witnesses x^2+y^2 and x^2+(p-y)^2. Its last section
  names this angle (p > sqrt n, Weil/Salié plus divisor bound, target n^{2/3}) as not done ("I did not check this").
  This file does it.

## 1. Statements established

Notation. E = {m >= 1 : m = x^2 + y^2, x, y in Z_{>=0}}. t >= 1 is an *n-shift* if a in E iff a + t in E for every
1 <= a <= n. p always denotes a prime with p = 3 (mod 4), and e(z) = exp(2 pi i z).
For m >= 1, rho(m) = #{(x, y) in Z_{>=1}^2 : x^2 + y^2 = m} and D(n) = max_{1 <= m <= n} rho(m).
K(a, b; p) = sum_{u in F_p^*} e((a u + b u^{-1})/p) (Kloosterman sum), and kappa_p = max_{c in F_p^*} |K(1, c; p)|.

**Theorem A (explicit criterion; no hypotheses).** Let n >= 8, Y = floor(sqrt(n/8)), and let p = 3 (mod 4) be
prime with 2 p^2 >= n. Let kappa > 0 be any number with kappa >= kappa_p. If

    (p + 1) Y^2 / p^2  >=  kappa + 2 D(n),                                  (*)

then p divides every n-shift t of E. Admissible choices:
- kappa = 3^{1/4} p^{3/4} (Lemma 6 below, elementary, proved here);
- kappa = 2 sqrt(p) (Weil's bound for Kloosterman sums; CITED, not re-proved; see Section 4).

Since (p+1)/p^2 > 1/p, a sufficient form of (*) is Y^2 >= kappa p + 2 p D(n).

**Theorem B (asymptotic).**
1. (Uses Weil's bound.) For every eps in (0, 1) there is N(eps) such that for n >= N(eps) every n-shift t is
   divisible by every prime p = 3 (mod 4) with p <= (1 - eps)(n/16)^{2/3}. Consequently, for every c < 2/3 there
   is N_c with t > exp(n^c) for every n-shift t and every n >= N_c.
2. (Fully elementary: no Weil, no L-function input beyond L(1, chi_4) > 0 inside PROOF.md Lemma 6.) The same holds
   with every p = 3 (mod 4), p <= (1 - eps)(n / (8 * 3^{1/4}))^{4/7}, so t > exp(n^c) for every c < 4/7.
3. (Adds the cited prime number theorem for progressions mod 4, as in PROOF.md part 3.)
   log t >= (1/2 - o(1)) (n/16)^{2/3} for every n-shift t.

This improves the exponent 1/2 of ../../PROOF.md (and Liu's 1/10). Like those results, it is a lower bound on any
n-shift and says nothing about whether n-shifts exist, which is the actual question (a).

## 2. Lemmas and proofs

Lemmas 1-3 restate PROOF.md Lemmas 1-3 (proofs copied there and re-checked here); Lemmas 4-10 are new.

**Lemma 1 (-1 is a non-residue).** No u in F_p has u^2 = -1. Hence p | x^2 + y^2 implies p | x and p | y; and for
(h1, h2) in F_p^2 \ {0}, h1^2 + h2^2 != 0 in F_p.

Proof. If u^2 = -1 then u^{p-1} = (-1)^{(p-1)/2} = -1, since (p-1)/2 is odd, contradicting Fermat. If p | x^2 + y^2
and p does not divide y, then u = x y^{-1} gives u^2 = -1. The last claim is the same statement over F_p. ∎

**Lemma 2 (Liu, Lemma 6).** If t is an n-shift, a in E, 1 <= a <= n and a = -t (mod p), then a = -t (mod p^2).

Proof. a + t in E, say a + t = u^2 + v^2. p | a + t, so p | u and p | v by Lemma 1, so p^2 | a + t. ∎

**Lemma 3 (conic count).** For r in F_p^*, #{(x, y) in F_p^2 : x^2 + y^2 = r} = p + 1; for r = 0 it is 1.

Proof. r = 0: Lemma 1. r != 0: K = F_p[i] (i^2 = -1) is a field by Lemma 1; Frobenius sends i to -i, so the norm
N(x + iy) = (x+iy)^{p+1} = x^2 + y^2 is a homomorphism K^* -> F_p^* with kernel of size <= p + 1 (roots of
Z^{p+1} = 1), hence image of size >= p - 1, hence onto, and every fibre over r != 0 has exactly (p^2-1)/(p-1) = p+1
elements. (Full write-out: PROOF.md Lemma 3.) ∎

**Lemma 4 (Fourier transform of the conic is a Kloosterman sum).** Fix r in F_p^*, let C_r = {w in F_p^2 :
w1^2 + w2^2 = r}, and for h in F_p^2 put Ĉ_r(h) = sum_{w in C_r} e(-(h1 w1 + h2 w2)/p). Then Ĉ_r(0) = p + 1, and for
h != 0,

    Ĉ_r(h) = - K(1, r (h1^2 + h2^2) / 4; p),   in particular |Ĉ_r(h)| <= kappa_p.

Proof. Ĉ_r(0) = |C_r| = p + 1 by Lemma 3. Write g(u, k) = sum_{x in F_p} e((u x^2 + k x)/p).
(i) g(u, 0)^2 = -p for u != 0: g(u,0)^2 = sum_{x,y} e(u(x^2+y^2)/p) = sum_s #{x^2+y^2 = s} e(us/p)
= 1 + (p+1) sum_{s != 0} e(us/p) = 1 - (p + 1) = -p, by Lemma 3.
(ii) For u != 0, completing the square (2 is invertible), u x^2 + k x = u (x + k/(2u))^2 - k^2/(4u), so
g(u, k) = e(-k^2/(4u p)) g(u, 0), where k^2/(4u) is computed in F_p. (Shift x by k/(2u).)
(iii) Using 1[s = 0] = (1/p) sum_{u in F_p} e(us/p),
Ĉ_r(h) = (1/p) sum_u e(-ur/p) g(u, -h1) g(u, -h2). The u = 0 term is (1/p) g(0,-h1) g(0,-h2), and g(0, k) = p 1[k = 0],
so it vanishes for h != 0. For u != 0, by (ii) and (i), g(u,-h1) g(u,-h2) = -p e(-Q/(4u) / p) with Q = h1^2 + h2^2.
Hence Ĉ_r(h) = - sum_{u != 0} e(-(u r + Q/(4u))/p). Replace u by -u: = - sum_{u != 0} e((u r + (Q/4) u^{-1})/p)
= -K(r, Q/4; p). Finally r != 0, and Q != 0 by Lemma 1, so substituting v = r u gives K(r, Q/4) = K(1, r Q/4). ∎

(Checked numerically for all r and all h when p < 60 and on samples for p < 200; out/check_lemmas.txt.)

**Lemma 5 (elementary Kloosterman bound; Kloosterman's fourth-moment argument).** For c in F_p^*,
|K(1, c; p)|^4 <= p^2 (3p - 5) < 3 p^3, i.e. kappa_p < 3^{1/4} p^{3/4}. (Valid for every odd prime p.)

Proof. For a, b in F_p^*, the substitution v = a u gives K(a, b) = K(1, ab). So for each c != 0 the value K(1, c)
occurs as K(a, b) for exactly the p - 1 pairs with ab = c, and
(p - 1) |K(1, c)|^4 <= sum_{a, b in F_p} |K(a, b)|^4.
Expanding |K|^4 = K K conj(K) conj(K) and summing over a, b in F_p (orthogonality) gives
sum_{a,b} |K(a,b)|^4 = p^2 T, where T = #{(u1,u2,u3,u4) in (F_p^*)^4 : u1+u2 = u3+u4, 1/u1+1/u2 = 1/u3+1/u4}.
Count T. If s = u1 + u2 != 0 then 1/u1 + 1/u2 = s/(u1 u2), and u3 + u4 = s, so the second equation says
u3 u4 = u1 u2; then u3, u4 are the roots of Z^2 - sZ + u1 u2 = (Z - u1)(Z - u2), so (u3, u4) in {(u1,u2),(u2,u1)}:
at most 2 choices for each of the (p-1)(p-2) pairs (u1,u2) with u1 + u2 != 0. If s = 0, then u2 = -u1, the second
equation reads 0 = 1/u3 + 1/u4, and with u3 + u4 = 0 this forces exactly u4 = -u3: (p-1)^2 quadruples. So
T <= 2(p-1)(p-2) + (p-1)^2 = (p-1)(3p-5), and (p-1)|K(1,c)|^4 <= p^2 (p-1)(3p-5). ∎

(Numerically: T bound checked by brute force for p < 50; max |K| / (3^{1/4}p^{3/4}) <= 0.794 for p = 3 mod 4 < 3000.)

**Lemma 6 (Weil's bound; CITED).** For p prime and a, b in F_p^*, |K(a, b; p)| <= 2 sqrt(p). So kappa_p <= 2 sqrt p.
Source: A. Weil, "On some exponential sums", Proc. Nat. Acad. Sci. USA 34 (1948), 204-207. NOT read or re-proved
here (Section 6). Numerical sanity check only: max_c |K(1,c)| / (2 sqrt p) <= 0.99992 for all p = 3 mod 4 < 3000
(out/check_lemmas.txt). Only Theorem B.1, B.3 and the "Weil" column of out/window.txt use Lemma 6.

**Lemma 7 (Parseval for an interval).** For 1 <= Y <= p and A_Y(h) = sum_{a=1}^{Y} e(h a / p),
sum_{h in F_p} |A_Y(h)|^2 = p Y, and A_Y(0) = Y.

Proof. sum_h |A_Y(h)|^2 = sum_{a, b = 1}^{Y} sum_h e(h(a - b)/p) = p #{(a, b) in [1, Y]^2 : a = b mod p} = p Y,
since |a - b| < Y <= p forces a = b. ∎

**Lemma 8 (representation multiplicity; elementary).** For m >= 1, rho(m) <= #{g >= 1 : g^2 | m} * 2^{omega(m)}
<= d(m)^2, where omega = number of distinct prime factors and d = number of divisors. For every delta > 0,
d(m) <= C_delta m^delta with C_delta = prod_{q prime, q < 2^{1/delta}} max_{e >= 0} (e + 1) q^{-e delta} < infinity.
Hence D(n) <= C_delta^2 n^{2 delta}.

Proof. (a) Primitive representations. Let rho*(m) count (x, y) in Z_{>=1}^2 with x^2 + y^2 = m and gcd(x, y) = 1.
For such (x, y), gcd(y, m) = 1 (a prime dividing y and m divides x^2, hence x). Map (x, y) to s = x y^{-1} mod m;
then s^2 = x^2 y^{-2} = -1 (mod m). The map is injective: if (x, y), (x', y') give the same s then m | x y' - x' y; by
the two-squares identity m^2 = (x x' + y y')^2 + (x y' - x' y)^2 and x x' + y y' > 0, |x y' - x' y| < m, so
x y' = x' y, and coprimality with x, y, x', y' >= 1 gives (x, y) = (x', y').
(b) Roots of s^2 = -1 mod m. By CRT the number is the product over q^e || m of the number mod q^e. For odd q, if
s, s' are roots then q^e | (s - s')(s + s'), and q cannot divide both factors (else q | 2s, q | s, but s^2 = -1 mod q),
so s' = +-s: at most 2 roots. For q = 2: e = 1 gives 1 root; e >= 2 gives none (s^2 = 3 mod 4 is impossible).
So rho*(m) <= 2^{omega(m)}.
(c) Every representation (x, y) has g = gcd(x, y) with g^2 | m and (x/g, y/g) a primitive representation of m/g^2.
So rho(m) = sum_{g^2 | m} rho*(m/g^2) <= #{g : g^2 | m} 2^{omega(m)}. Both factors are <= d(m)
(g -> g^2 is injective into divisors; 2^{omega(m)} <= prod (e_q + 1)).
(d) d(m)/m^delta = prod_{q^e || m} (e + 1) q^{-e delta}. If q >= 2^{1/delta} then q^{e delta} >= 2^e >= e + 1, so the
factor is <= 1. If q < 2^{1/delta} the factor is <= max_{e >= 0} (e+1) q^{-e delta}, finite since it tends to 0 as
e -> infinity. ∎

(Numerically: rho(m) <= 2^{omega} #{g} <= d^2 and even rho(m) <= d(m) for all m <= 10^6; D(10^8) = 72.)

**Lemma 9 (every nonzero class has three witnesses).** Let n >= 8, Y = floor(sqrt(n/8)), p = 3 (mod 4) with
2 p^2 >= n, kappa >= kappa_p, kappa > 0, and assume (*). Then for every r in F_p^* there are at least three distinct
m in E with 8 <= m <= n and m = r (mod p).

Proof. Note 1 <= Y <= sqrt(n/8) < sqrt(n/2) <= p. Let w(x) = #{(a, b) in [1, Y]^2 : a + b = x} for x in Z. Then w is
supported on [2, 2Y], 0 <= w(x) <= Y, and sum_x w(x) e(h x / p) = A_Y(h)^2. Put
N_w(r) = sum_{x, y in Z} w(x) w(y) 1[x^2 + y^2 = r mod p].
Fourier inversion on F_p^2, 1_{C_r}(v) = p^{-2} sum_{h} Ĉ_r(h) e((h1 v1 + h2 v2)/p), gives
N_w(r) = p^{-2} sum_{h in F_p^2} Ĉ_r(h) A_Y(h1)^2 A_Y(h2)^2.
The h = 0 term is (p+1) Y^4 / p^2 (Lemma 4, Lemma 7). By Lemma 4 and Lemma 7 the rest is at most, in absolute value,
p^{-2} kappa sum_{h != 0} |A_Y(h1)|^2 |A_Y(h2)|^2 = p^{-2} kappa ((pY)^2 - Y^4) = kappa (Y^2 - Y^4/p^2).
So N_w(r) >= Y^2 ((p+1)Y^2/p^2 - kappa) + kappa Y^4/p^2 > Y^2 ((p+1)Y^2/p^2 - kappa) >= 2 Y^2 D(n), using (*).
On the other hand, let V be the set of values m = x^2 + y^2 with x, y in [2, 2Y] and m = r (mod p). Each m in V lies
in E and satisfies 8 <= m <= 8 Y^2 <= n, and its total weight is sum w(x)w(y) over its representations, which is
<= Y^2 rho(m) <= Y^2 D(n). So N_w(r) <= |V| Y^2 D(n). Since D(n) >= rho(2) = 1 > 0, |V| > 2. ∎

**Lemma 10 (when distinct witnesses automatically differ mod p^2).** Let t be an n-shift, p = 3 (mod 4), p not
dividing t, and S = {a in E cap [1, n] : a = -t mod p}. Then all elements of S are congruent mod p^2 (Lemma 2).
Consequently: if n <= p^2, |S| <= 1; if n <= 2 p^2, |S| <= 2. (In general |S| <= ceil(n/p^2).)

Proof. For a < b in S, p^2 | b - a and 1 <= b - a <= n - 1. If n <= p^2 this is impossible. If n <= 2p^2 then
b - a = p^2 for every pair a < b, which three elements a < b < c cannot all satisfy (c - a = 2p^2 > n - 1). ∎

So "two elements of E in one class mod p differ mod p^2" is automatic exactly in the range p^2 >= n (any two distinct
elements of [1, n] differ by less than p^2); for sqrt(n/2) <= p < sqrt n we ask for three elements instead.

**Proof of Theorem A.** Suppose p does not divide t and let r = -t mod p, so r != 0. Lemma 9 gives three distinct
elements of E cap [1, n] in the class r, contradicting Lemma 10 (2 p^2 >= n). ∎

**Proof of Theorem B.**
Write Y^2 >= (sqrt(n/8) - 1)^2 >= n/8 - sqrt(n) (n >= 1). Fix delta = 1/48, so D(n) <= C n^{1/24} (Lemma 8).

1. (Weil.) Take kappa = 2 sqrt p and p in [sqrt(n/2), (1 - eps)(n/16)^{2/3}]. Then kappa p = 2 p^{3/2}
   <= (1 - eps)^{3/2} n/8 and 2 p D(n) <= 2 C n^{2/3 + 1/24} = o(n). Hence Y^2 >= kappa p + 2 p D(n), the sufficient
   form of (*), once n/8 (1 - (1-eps)^{3/2}) >= sqrt n + 2 C n^{17/24}, i.e. for n >= N(eps). So every such p divides
   t (Theorem A). Primes p = 3 (mod 4) with p < sqrt(n/2) satisfy p <= 1 + 2 sqrt(n/5) (as sqrt(1/2) < 2/sqrt5), so
   they divide t by PROOF.md Theorem part 1 (= Lemmas 2, 4, 5 there). Hence all p = 3 mod 4 up to
   y_n := (1 - eps)(n/16)^{2/3} divide t, and log t >= theta(y_n; 4, 3). By PROOF.md Lemma 7 (elementary:
   theta(y; 4, 3) >= y^{1 - delta'} for y >= y_0(delta')), log t >= y_n^{1 - delta'} > n^c for any c < 2/3 after
   choosing delta' small and n large.
2. (Elementary.) Same with kappa = 3^{1/4} p^{3/4} (Lemma 5): kappa p = 3^{1/4} p^{7/4} <= (1 - eps)^{7/4} n/8 for
   p <= (1 - eps)(n / (8 * 3^{1/4}))^{4/7}, and 2 p D(n) <= 2 C n^{4/7 + 1/24} = o(n). The rest is identical; the
   only inputs are Lemmas 1-5, 7-10 and PROOF.md Lemmas 2-7, all elementary.
3. As in 1 with eps -> 0, plus theta(y; 4, 3) ~ y/2 (PNT for progressions; cited exactly as in PROOF.md part 3). ∎

Remark (exponent alone). For the exponent statements, PROOF.md part 1 is not needed: the primes in
(y_n^{1 - delta'}, y_n] already contribute >= y_n^{1 - delta'} to log t (proof of PROOF.md Lemma 7), and for n large
y_n^{1-delta'} > sqrt(n/2), so all of them lie in the range covered by Theorem A.

## 3. Computations (VERIFIED numerically; code in code/, outputs in out/)

Reproduce (from this folder; each run with python3 -I, numpy 1.26.4):

    python3 -I code/check_lemmas.py > out/check_lemmas.txt   # ~1 min
    python3 -I code/window.py       > out/window.txt         # ~10 s, ~200 MB RAM
    python3 -I code/truth.py        > out/truth.txt          # ~3-4 min

- check_lemmas.py: Lemma 3 and g(u,0)^2 = -p for p < 1000; Lemma 4 identity (all r, h for p < 60, samples to 200);
  Lemma 5 count T (p < 50) and bound (p < 3000); Weil bound sanity (p < 3000, max ratio 0.99992); Lemma 7 (p < 400);
  Lemma 8 inequalities for m <= 10^6. Output: ALL OK.
- window.py: exact D(n) for n <= 10^8 (D(10^4) = 12, D(10^6) = 32, D(10^8) = 72) and the largest prime P(n) for which
  (*) holds (it is monotone in p). Selected rows:

      n        sqrt(n/2)  1+2sqrt(n/5)  P_W(n) (Weil)        P_K(n) (elementary)
      10^6       707.1       895.4        983  (n^0.499)     none
      10^7      2236.1      2829.4       5179  (n^0.531)     2311
      10^8      7071.1      8945.3      26539  (n^0.553)     9103

  First n (step 10^4) where the Weil window passes PROOF.md's range 1+2sqrt(n/5): n = 510000. First n (step 10^5)
  where the elementary window passes it: n = 8.34 * 10^7. So Theorem A is already non-vacuous and stronger than
  PROOF.md part 1 at these sizes; the exponent 2/3 (resp. 4/7) is only approached slowly because of the 2 p D(n)
  term and the constant 16.
- truth.py: (1) exact weighted counts N_w(r) for (n, p) = (10^6, 983), (10^6, 1499), (4*10^6, 2003), (10^7, 5179)
  are all above the proved lower bound (e.g. n = 10^7, p = 5179: min_r N_w = 2.71e8 >= bound 1.23e8).
  (2) Brute-force true range of "every nonzero class mod p has >= 3 elements of E cap [1, n]" (all p = 3 mod 4
  from sqrt(n/2) up): n = 10^4: up to 383; 10^5: up to 2731; 10^6: up to 19727; 10^7: up to 126739
  (first failure at p = n^{0.656}, n^{0.688}, n^{0.716}, n^{0.729}). So the witness property is true well beyond
  what Theorem A certifies; the method, not the property, is the bottleneck.

## 4. VERIFIED vs INFERRED vs CITED

- VERIFIED (proved here, complete): Lemmas 1-5, 7-10; Theorem A with kappa = 3^{1/4} p^{3/4}; Theorem B.2
  (c < 4/7), given PROOF.md Lemmas 6-7 and part 1, which I re-read today and which are elementary.
- CITED, not re-proved, not re-read: Weil's bound (Lemma 6), used for Theorem A with kappa = 2 sqrt p and for
  Theorem B.1 (c < 2/3). It is a standard theorem (also follows from Stepanov's elementary method), and
  numerically consistent for p < 3000, but I did not read the source in this session.
- CITED (as in PROOF.md): PNT for progressions mod 4, only for the constant in Theorem B.3.
- VERIFIED numerically only: the tables in Section 3.
- INFERRED (not checked): that level-of-distribution results for r_2(m) in progressions to modulus up to x^{2/3}
  exist in the literature (the argument above is the standard one behind such results). If so, Theorem B.1 is a
  routine application of known technology rather than new mathematics; the new part would only be the use in 675(a).

## 5. What this does and does not show

- It shows: every n-shift t of E (if one exists) is divisible by all primes p = 3 mod 4 up to about (n/16)^{2/3}
  (Weil) or (n/(8*3^{1/4}))^{4/7} (elementary), hence t > exp(n^c) for every c < 2/3 (resp. 4/7) and all large n.
  This beats the 1/2 of PROOF.md and Liu's 1/10 (and Liu's GRH 1/4 and Linnik-conjecture 1/2).
- It does NOT show that n-shifts exist; question (a) stays open. The bound is vacuous for any n without n-shifts.
- It does NOT reach exponent 1. The exponent 2/3 is the natural limit of this method: the main term is ~ n/p and the
  error is bounded by one Kloosterman sum (~ sqrt p) per frequency with no cancellation between frequencies, giving
  n/p >> p^{1/2}. Going further needs cancellation in sums of the shape
  sum_{h1, h2} |A_Y(h1)|^2 |A_Y(h2)|^2 K(1, r (h1^2 + h2^2)/4; p), i.e. sums of Kloosterman sums over a quadratic form
  in a box of side about p/Y < sqrt p, equivalently type-I sums sum_{d e <= M} chi_4(d) Kl(c d e) of length
  M ~ p^2/n. That is beyond the Pólya-Vinogradov range; results of Kowalski-Michel-Sawin type might give a small
  power saving but I did not read them or attempt it (so no claim). The brute force above suggests the witness
  property itself holds for p up to n^{1 - o(1)}, so any further gain must come from better exponential-sum input or
  a different family of witnesses.
- The overall strategy (p | t for all p = 3 mod 4 up to y) can never give more than log t >~ y/2, so with y <= n it is
  capped at exponent 1.
- Not formalized in Lean. Nothing was committed, pushed, posted or sent.

## 6. Sources not read

- A. Weil, "On some exponential sums", PNAS 34 (1948): not read; used as a black box for the 2/3 statements only.
- Kloosterman 1926 (fourth-moment method): not read; Lemma 5 is proved in full here.
- Davenport, Multiplicative Number Theory (PNT for APs): not read; only for Theorem B.3's constant.
- Literature on sums of two squares / r_2 in arithmetic progressions (level of distribution), Kowalski-Michel-Sawin
  on sums of Kloosterman sums: not searched or read. Novelty of the 2/3 exponent for 675(a) is "not found on the
  erdosproblems page, its forum thread, or Liu's note", not "proved new".
- arXiv, Plasma wiki, formal-conjectures: not re-checked in this session (PROOF.md's checks from earlier today apply).

## Files

- refs/fetch_20261123/ : page675.html(.txt), forum675.html(.txt) (fetched 2026-11-23, untrusted data)
- code/check_lemmas.py, code/window.py, code/truth.py
- out/check_lemmas.txt, out/window.txt, out/truth.txt
