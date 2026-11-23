# Erdős 675(a), beyond exponent 1/2: the Gaussian-integer route (angle 2)

Date: 2026-11-23. Status: **the exponent 1/2 is beaten.** Every n-shift of E has log t > n^θ for every θ < 3/5
(this proof is elementary and complete in this file), and for every θ < 2/3 if Weil's bound for Kloosterman
sums is used as a cited theorem. I also show exactly where the method has to stop:

- the "local" information (one prime at a time) forces p | t **exactly when** n ≥ F*(p), where F*(p) is a
  least-two-witnesses quantity defined below;
- no combination of local conditions can ever give more than log t ≫ n (exponent 1);
- primes p ≡ 1 (mod 4) and p = 2 can never be forced to divide t by these methods;
- prime-power refinements only change constants.

## 0. Setting and what was checked first

E = {m ≥ 1 : m = x² + y², x, y ∈ Z}. t ≥ 1 is an **n-shift** if, for all 1 ≤ a ≤ n, a ∈ E ⇔ a + t ∈ E.
Throughout, p is a prime with p ≡ 3 (mod 4), ψ(u) = exp(2πiu/p), and K = F_p(i) = F_p[X]/(X²+1).

Prior work, all read before starting (VERIFIED, 2026-11-23):
- Forum thread erdosproblems.com/forum/thread/675 (fresh fetch: refs/web/forum675.html; identical text to the
  copy in ../../refs/web): the only part-(a) post is Liu's c < 1/10 (2026-05-09). Nothing on exponent ≥ 1/2.
- Liu's note (../../refs/erdos675a.txt): Lemma 6 (the mod-p² lifting), Lemma 7 (two witnesses), Remark 8 and
  Remark 12 ("relaxing the choice of witnesses … a question about E in arithmetic progressions").
- ../../PROOF.md (local, unpublished): exponent 1/2 via the explicit witnesses x² + y², x² + (p−y)² ≤ 5(p−1)²/4.
  Its "Beyond exponent 1/2" paragraph names, without checking it, the route via exponential sums over the conic
  restricted to a box. **This file carries that route out**, with an elementary replacement for Weil's bound.
- arXiv keyword queries (refs/arxiv/*.xml; "sums of two squares" with "progressions" or "level of
  distribution", "translation property", "Erdos 675") found nothing on this question.

## 1. Statement established

Define, for each prime p ≡ 3 (mod 4),

  **F\*(p)** = the least N such that every nonzero residue class r mod p contains two elements of E ∩ [1, N]
  that are distinct mod p².

(F*(p) ≤ 5(p−1)²/4 by PROOF.md Lemma 4. For example F*(3) = 5, F*(7) = 26, F*(11) = 50.)

**Theorem A (unconditional, elementary, self-contained).**
(i) For every ε > 0 there is p₁(ε) such that F*(p) ≤ 2p^{5/3+2ε} for all primes p ≡ 3 (mod 4) with p ≥ p₁(ε).
(ii) For every θ < 3/5 there is N_θ such that for every n ≥ N_θ, every n-shift t of E satisfies log t > n^θ.

**Theorem B (uses Weil's bound |Kl(s)| ≤ 2√p, cited and not re-proved).**
(i) F*(p) ≤ 6p^{3/2} for all sufficiently large primes p ≡ 3 (mod 4).
(ii) For every θ < 2/3, every n-shift t satisfies log t > n^θ once n is large enough. With the prime number
theorem for progressions mod 4 (also cited), log t ≥ (1/2 − o(1))(n/6)^{2/3}.

**Proposition C (exactness of the local method).** For a prime q ≡ 3 (mod 4), let LOC_q(t) be the
statement "v_q(a + t) is even for every a ∈ E ∩ [1, n]". Every n-shift satisfies every LOC_q. Let Q be any finite
set of primes ≡ 3 (mod 4) and let p ∈ Q. Then:
 - if n ≥ F*(p), every t ≥ 1 satisfying LOC_p is divisible by p;
 - if n < F*(p), there is t ≥ 1 with p ∤ t satisfying LOC_q for **every** q ∈ Q.

**Proposition D (ceiling for local arguments).** For any finite set Q of primes ≡ 3 (mod 4), the gcd D_Q of all
t ≥ 1 satisfying LOC_q for every q ∈ Q divides ∏_{q∈Q, q≤n} q^{j_q}, where j_q is the least j with q^j > n. So
log D_Q ≤ Σ_{q≤n} log(qn) ≪ n, and D_Q has no prime factor that is 2, ≡ 1 (mod 4), or > n.

**Lemma 15 (prime powers).** If t is an n-shift and k = v_p(t), then either k is odd and p^{k+1} > n, or
k is even and p^k·F*(p) > n.

Together, C and D show that the exponent available from local information is governed exactly by how fast
F*(p) grows. Theorem A gives F*(p) ≤ p^{5/3+o(1)}, so the exponent is 3/5. Theorem B gives F*(p) ≪ p^{3/2}, so
the exponent is 2/3. A bound F*(p) ≤ p^{1+o(1)} would give every θ < 1, and Proposition D says no local method
can go past exponent 1. Numerically, F*(p) is about p (log p)^{3/2} (ratio ≤ 1.75) for p ≤ 20000 (§5).

## 2. Lemmas and proofs

**Lemma 1 (−1 is a non-residue; PROOF.md Lemma 1).** There is no u ∈ F_p with u² = −1, and if p | x² + y² then
p | x and p | y.
Proof. If u² = −1 then u^{p−1} = (−1)^{(p−1)/2} = −1 ≠ 1, which contradicts Fermat. If p ∤ y, then u = x/y mod p
would satisfy u² = −1. So p | y, and then p | x² gives p | x. ∎

**Lemma 2 (even valuation).** If m ∈ E then v_p(m) is even. Also E·E ⊆ E, and p^{2j}·E ⊆ E.
Proof. Suppose v_p(m) ≥ 1 and m = x² + y². By Lemma 1, p | x and p | y, so m/p² = (x/p)² + (y/p)² is 0 or in E.
It is not 0 because m ≥ 1. Repeat until p ∤ m. If v_p(m) were odd, this would reach some m' ∈ E with
v_p(m') = 1, which Lemma 1 rules out (p | m' would force p² | m'). Closure under products is Brahmagupta's
identity (x²+y²)(u²+v²) = (xu−yv)² + (xv+yu)², and p^{2j} = (p^j)² + 0² lies in E. ∎

**Lemma 3 (witness principle; Liu's Lemmas 6–7).** Let t be an n-shift. If a ∈ E ∩ [1, n] and a ≡ −t (mod p),
then a ≡ −t (mod p²). Consequently, if n ≥ F*(p) then p | t.
Proof. a + t ∈ E and p | a + t, so Lemma 2 gives p² | a + t. If p ∤ t, put r = −t mod p ≠ 0. Since n ≥ F*(p),
there are a, b ∈ E ∩ [1, n] with a ≡ b ≡ r (mod p) and a ≢ b (mod p²). The first part gives
a ≡ −t ≡ b (mod p²), a contradiction. ∎
(Only LOC_p was used here: a ∈ E ∩ [1, n] ⇒ v_p(a+t) even.)

**Lemma 4 (trace–norm count; the conic sum is a Kloosterman sum).** Write Tr z = z + z^p and N z = z^{p+1} on K.
For z = x + iy we have Tr z = 2x and N z = x² + y² (PROOF.md Lemma 3). For s ∈ F_p^* let
G(s) = Σ_{z∈K, N z = s} ψ(Tr z) and Kl(s) = Σ_{x∈F_p^*} ψ(x + s x^{−1}). Then G(s) = −Kl(s).
Proof. Fix a ∈ F_p and s ≠ 0, and let f = X² − aX + s, with discriminant Δ = a² − 4s. Every z ∈ K is a root of
(X − z)(X − z^p) = X² − (Tr z)X + N z. So the z with Tr z = a and N z = s are among the roots of f in K.
Conversely, a root z ∉ F_p has conjugate root z^p, so Tr z = a and N z = s. A root z ∈ F_p has Tr z = 2z and
N z = z², so it qualifies only when 2z = a and z² = s. Counting case by case:
- if Δ is a non-residue, f is irreducible and both roots lie in K∖F_p, giving 2 solutions;
- if Δ is a nonzero residue, both roots lie in F_p but neither has 2z = a, giving 0;
- if Δ = 0, the double root z = a/2 qualifies, giving 1.
So #{z : Tr z = a, N z = s} = 1 − (Δ/p), with (·/p) the Legendre symbol. In the same way,
#{x ∈ F_p^* : x + s/x = a} = #{x : x² − ax + s = 0} = 1 + (Δ/p); here x = 0 is never a root since s ≠ 0. Hence
G(s) + Kl(s) = Σ_a ψ(a)·2 = 0. ∎

**Lemma 5 (Fourier coefficients of the conic).** For r ∈ F_p^* let C_r = {(x, y) ∈ F_p² : x² + y² = r}, which has
p + 1 points (PROOF.md Lemma 3). For (h, k) ∈ F_p², set S_r(h,k) = Σ_{(x,y)∈C_r} ψ(hx + ky). Then S_r(0,0) = p + 1,
and for (h,k) ≠ (0,0),
  S_r(h,k) = −Kl( r(h² + k²)/4 ),   and the argument r(h²+k²)/4 is nonzero.
Proof. Let c = (h − ik)/2 ∈ K. Since i^p = −i, c^p = (h + ik)/2 and z^p = x − iy for z = x + iy. So
Tr(cz) = ½[(h−ik)(x+iy) + (h+ik)(x−iy)] = hx + ky. The map z ↦ cz is a bijection from {N z = r} onto
{N w = N(c)·r}, and N(c) = (h² + k²)/4, which is nonzero by Lemma 1. Hence S_r(h,k) = G(r(h²+k²)/4), and
Lemma 4 finishes the proof. ∎

**Lemma 6 (fourth moment of Kloosterman sums; Kloosterman's elementary method).**
Σ_{s∈F_p^*} |Kl(s)|⁴ ≤ p²(3p − 5) < 3p³. In particular |Kl(s)| < 3^{1/4} p^{3/4}.
Proof. For a, b ∈ F_p let Kl(a,b) = Σ_{x≠0} ψ(ax + bx^{−1}). Expanding the fourth power and summing over a and b,
  Σ_{a,b} |Kl(a,b)|⁴ = p²·#{(x₁,x₂,x₃,x₄) ∈ (F_p^*)⁴ : x₁+x₂ = x₃+x₄, x₁⁻¹+x₂⁻¹ = x₃⁻¹+x₄⁻¹}.
Let σ = x₁ + x₂. If σ ≠ 0, then x₁⁻¹ + x₂⁻¹ = σ/(x₁x₂), so the second equation forces x₁x₂ = x₃x₄. Then {x₃, x₄}
and {x₁, x₂} are the root multisets of the same quadratic, which leaves at most 2 choices of (x₃, x₄) for each of
the (p−1)(p−2) pairs (x₁, x₂). If σ = 0, then x₂ = −x₁ and x₄ = −x₃, which gives (p−1)² solutions. The total is
at most (p−1)(3p−5). For ab ≠ 0, substituting x ↦ x/a gives Kl(a,b) = Kl(ab), so each s ≠ 0 occurs p − 1
times. Dropping the terms with ab = 0, which are ≥ 0, gives (p−1)Σ_s |Kl(s)|⁴ ≤ p²(p−1)(3p−5). ∎

**Lemma 7 (representation numbers).** Let r₂(a) = #{(x,y) ∈ Z² : x² + y² = a}. Then r₂(a) ≤ 4d(a)², where d is
the divisor function. Also, for every δ > 0 there is c_δ with d(m) ≤ c_δ m^δ for all m ≥ 1.
Proof. *Primitive representations* are those with gcd(x,y) = 1. Write r₂*(m) for their number. If x² + y² = m
is primitive then gcd(y, m) = 1, so u ≡ x y^{−1} (mod m) satisfies u² ≡ −1 (mod m). Suppose two primitive
representations (x,y) and (x',y') give the same u. Then δ = xy' − x'y ≡ 0 (mod m), and
γ = xx' + yy' satisfies γ² + δ² = m², so δ ∈ {0, ±m}.
- If δ = 0, coprimality gives (x',y') = ±(x,y).
- If δ = ±m, then γ = 0, and coprimality gives (x',y') = ±(−y,x).
So each u comes from at most 4 representations. The congruence u² ≡ −1 has at most 2^{ω(m)} solutions mod m:
by CRT; modulo an odd prime power, u² ≡ v² for units forces u ≡ ±v; modulo 2^e there is 1 solution for e = 1
and none for e ≥ 2. Hence r₂*(m) ≤ 4·2^{ω(m)} ≤ 4d(m). Then r₂(a) = Σ_{g²|a} r₂*(a/g²) ≤ 4d(a)·#{g : g² | a}
≤ 4d(a)². For the divisor bound, write d(m)/m^δ = ∏_{ℓ^e‖m} (e+1)/ℓ^{eδ}. Each factor with ℓ ≥ 2^{1/δ} is ≤ 1.
The fewer than 2^{1/δ} remaining factors are each ≤ max_e (e+1)2^{−eδ} < ∞. ∎

**Lemma 8 (Fejér weights).** Let B be an integer with 2B − 1 ≤ p. Define w on F_p by w(x) = B − |x| when x has a
representative with |x| < B (this is well defined because 2B − 1 ≤ p), and w(x) = 0 otherwise. Let
ŵ(h) = p^{−1} Σ_x w(x) ψ(−hx). Then:
- w(x) = Σ_h ŵ(h) ψ(hx);
- ŵ(h) = |D(h)|²/p ≥ 0, where D(h) = Σ_{a=0}^{B−1} ψ(ha);
- ŵ(0) = B²/p and Σ_h ŵ(h) = w(0) = B;
- ŵ(h) ≤ min(B²/p, p/(4h²)) for 1 ≤ |h| ≤ (p−1)/2.
Proof. Let I = {0, …, B−1}. Since 2B − 1 ≤ p, w(x) = #{(a,b) ∈ I² : a − b ≡ x}, so
Σ_x w(x)ψ(−hx) = D(h)·D(−h) = |D(h)|². Fourier inversion on F_p gives the first identity, and evaluating it at
x = 0 gives Σ_h ŵ(h) = w(0) = B. For h ≢ 0, |D(h)| = |1 − ψ(hB)|/|1 − ψ(h)| ≤ 1/|sin(πh/p)| ≤ p/(2|h|), using
sin(πu) ≥ 2u on [0, 1/2]. ∎

**Lemma 9 (counting identity).** For r ∈ F_p^* let
  N(r) = Σ_{x,y∈Z, |x|,|y|<B, x²+y² ≡ r (mod p)} (B − |x|)(B − |y|).
Then N(r) = (p+1)B⁴/p² − Σ_{s∈F_p^*} W_r(s) Kl(s), where
  W_r(s) = Σ { ŵ(h)ŵ(k) : (h,k) ≠ (0,0), r(h²+k²)/4 = s } ≥ 0  and  Σ_s W_r(s) = B² − B⁴/p² ≤ B².
Proof. Because 2B − 1 ≤ p, the integers in (−B, B) are distinct mod p, so N(r) = Σ_{(x,y)∈C_r} w(x)w(y).
Insert Lemma 8's expansion to get Σ_{h,k} ŵ(h)ŵ(k) S_r(h,k), then apply Lemma 5. ∎

**Lemma 10 (W is not concentrated).** Let T = ⌊√((p−1)/2)⌋ and D_p = max_{1≤a<p} r₂(a). For every r and s,
  W_r(s) ≤ D_p (B²/p)² + 2B²/T.
Proof. Fix m = 4s/r ≠ 0 and represent h and k in (−p/2, p/2). We bound the pairs (h, k) on the circle
h² + k² ≡ m in three groups.
- Pairs with |h|, |k| ≤ T. Here the integer h² + k² lies in [1, 2T²] ⊆ [1, p−1], so it equals the least
  positive residue of m. There are at most r₂ of that residue ≤ D_p such pairs, each of weight ≤ (B²/p)².
- Pairs with |h| > T. For each such h there are at most two k with k² ≡ m − h², and ŵ(k) ≤ B²/p. Lemma 8
  gives Σ_{|h|>T} ŵ(h) ≤ 2Σ_{h>T} p/(4h²) ≤ p/(2T), so this group contributes ≤ 2(B²/p)(p/(2T)) = B²/T.
- Pairs with |k| > T contribute ≤ B²/T in the same way. ∎

**Proposition 11 (= Theorem A(i)).** Fix ε ∈ (0, 1/12). For all sufficiently large primes p ≡ 3 (mod 4), every
r ≢ 0 (mod p) has two distinct a, b ∈ E with a ≡ b ≡ r (mod p) and a, b ≤ 2p^{5/3+2ε}. Since 2p^{5/3+2ε} < p²,
also a ≢ b (mod p²). Hence F*(p) ≤ 2p^{5/3+2ε}.
Proof.
1. Setup. Let B = ⌈p^{5/6+ε}⌉, so 2B − 1 ≤ p for large p. Let D' = max_{1≤a≤2B²} r₂(a); note D_p ≤ D'.
   By Lemma 7 with δ = ε/8, D' ≤ 4c_δ²(2B²)^{2δ} ≤ C_ε p^{ε/2}.
2. Error bound. By Hölder, then Lemmas 6, 9 and 10,
   |Σ_s W_r(s)Kl(s)| ≤ (Σ|Kl|⁴)^{1/4}(max W)^{1/4}(Σ W)^{3/4}
                     ≤ (3p³)^{1/4}(D'B⁴/p² + 2B²/T)^{1/4} B^{3/2}
                     ≤ (3D')^{1/4} p^{1/4} B^{5/2} + (6p³/T)^{1/4} B².
3. Turning a count into two distinct values. Any single integer a can contribute at most B²r₂(a) ≤ B²D' to
   N(r). So if N(r) > B²D', the pairs counted in N(r) take at least two distinct integer values a = x² + y².
   Each such value lies in E (since a ≡ r ≢ 0, a ≥ 1) and satisfies a ≤ 2(B−1)².
4. Checking the inequality. Since N(r) ≥ B⁴/p − |error|, it suffices to show
   (3D')^{1/4} p^{5/4} B^{−3/2} + (6p³/T)^{1/4} p B^{−2} + D' p B^{−2} < 1.
   With B ≥ p^{5/6+ε}, D' ≤ C_ε p^{ε/2} and T ≥ √p/2 (true for large p), the three terms are at most
   C p^{−11ε/8}, 12^{1/4} p^{−1/24−2ε} and C p^{−2/3−3ε/2}. All tend to 0, so the inequality holds for large p. ∎

**Proposition 12 (= Theorem B(i)).** Assume Weil's bound |Kl(s)| ≤ 2√p for s ≠ 0 (Weil 1948; cited, not
re-proved here; it is consistent with out/check_identities.txt, where max|Kl|/√p ≤ 1.995 for p ≤ 499). Then for
large p, F*(p) ≤ 6p^{3/2}.
Proof. Let B = ⌈√3·p^{3/4}⌉. By Lemma 9, N(r) ≥ B⁴/p − 2√p·B². This exceeds B²D' if B² > p(2√p + D'). That
holds because B² ≥ 3p^{3/2} and D' ≤ C p^{δ} < √p. Conclude as in step 3 above, with 2(B−1)² ≤ 6p^{3/2} < p². ∎

**Lemma 13 (primes 3 mod 4 are plentiful; PROOF.md Lemma 7, elementary, re-read).** For every δ ∈ (0,1) there
is y₀(δ) such that θ(y;4,3) = Σ_{q≤y, q≡3(4)} log q ≥ y^{1−δ} for y ≥ y₀(δ).

**Proof of Theorem A(ii).** Fix θ < 3/5. Choose ε, δ > 0 with (1−δ)/(5/3+2ε) > θ, and put
Y = (n/2)^{1/(5/3+2ε)}. Every prime p ≡ 3 (mod 4) with p₁(ε) ≤ p ≤ Y has F*(p) ≤ 2p^{5/3+2ε} ≤ n
(Proposition 11), so p | t by Lemma 3. These primes are distinct, so
log t ≥ θ(Y;4,3) − θ(p₁(ε);4,3) ≥ Y^{1−δ} − O_ε(1) > n^θ for n large (Lemma 13). ∎

**Proof of Theorem B(ii).** The same argument with Proposition 12 and Y = (n/6)^{2/3}. For the constant, the
prime number theorem for progressions gives θ(Y;4,3) ~ Y/2. ∎

**Proof of Proposition C.**
- First bullet: this is Lemma 3, which only uses LOC_p.
- Second bullet, setup. Suppose n < F*(p), so n < 5(p−1)²/4 ≤ (p−1)p². Then some nonzero class r mod p does not
  contain two elements of E ∩ [1, n] that are distinct mod p².
- Case 1: the class contains no element of E ∩ [1, n]. Put d = r.
- Case 2: its elements a₁, …, a_j are all ≡ c (mod p²). They are pairwise distinct mod p³, since their
  differences are nonzero multiples of p² of size < n < p³. Also j ≤ ⌈n/p²⌉ ≤ p − 1. So at least one of the p
  classes mod p³ lying over c contains no a_i; call it d.
- Choosing t. By CRT pick t ≥ 1 with t ≡ −d (mod p³), and with t ≡ q^{j_q} (mod q^{j_q+1}) for each
  q ∈ Q ∖ {p}, where q^{j_q} > n.
- Checking LOC. p ∤ t because d ≢ 0 (mod p). For a ∈ E ∩ [1, n] with a ≢ r (mod p), v_p(a+t) = 0. In Case 2,
  v_p(a_i + t) = v_p(a_i − d) = 2, because a_i ≡ d (mod p²) but not mod p³. For q ∈ Q ∖ {p},
  v_q(a + t) = v_q(a), which is even by Lemma 2, because a ≤ n < q^{j_q} = q^{v_q(t)}. ∎

**Proof of Proposition D.** Let Q₁ = {q ∈ Q : q ≤ n} and Q₂ = Q ∖ Q₁. Let M = ∏_{Q₁} q^{j_q+1}·∏_{Q₂} q³.
By CRT pick t₀ with t₀ ≡ q^{j_q} (mod q^{j_q+1}) for q ∈ Q₁, and t₀ ≡ q² − 1 (mod q³) for q ∈ Q₂.
Every t ≡ t₀ (mod M), t ≥ 1, satisfies LOC_q for all q ∈ Q:
- for q ∈ Q₁, v_q(a + t) = v_q(a), which is even;
- for q ∈ Q₂ and 2 ≤ a ≤ n, q ∤ a − 1, so v_q(a + t) = 0;
- for q ∈ Q₂ and a = 1, v_q(1 + t) = 2.
The gcd of the progression t₀ + MZ_{≥0} divides gcd(t₀, M) = ∏_{Q₁} q^{j_q}. Finally
log ∏_{q≤n} q^{j_q} ≤ Σ_{q≤n} log(qn) ≤ 2π(n) log n ≪ n by Chebyshev. ∎

**Proof of Lemma 15.**
- k odd with p^{k+1} ≤ n. Take a = p^{k+1}, which is in E. Then v_p(a + t) = k is odd, so a + t ∉ E by
  Lemma 2. Contradiction.
- k even with n ≥ p^k F*(p). Write t = p^k t' with p ∤ t', and let r = −t' mod p. Pick m₁, m₂ ∈ E ∩ [1, F*(p)]
  with m_i ≡ r (mod p) and m₁ ≢ m₂ (mod p²). Then a_i = p^k m_i ∈ E ∩ [1, n] by Lemma 2, so a_i + t ∈ E, and
  v_p(a_i + t) = k + v_p(m_i + t') must be even and ≥ k + 1, hence ≥ k + 2. That gives m₁ ≡ −t' ≡ m₂ (mod p²),
  a contradiction. ∎

## 3. Why each route stops where it does

1. **Prime powers (mod p², p³, …).** Lemma 15 gives v_p(t) ≥ 2 for p ≤ √n and p^{v_p(t)} ≥ n/F*(p). Proposition D
   bounds every prime-power gain by p^{v_p} ≤ pn, so the total gain is Σ_{p≤n} O(log n) = O(n), and the new
   information comes only from primes that are already forced. Restricted to p ≤ √n (the only primes the
   p²-lifting reaches with PROOF.md's witnesses), this is Σ_{p≤√n} O(log n) = O(√n). So prime powers improve
   constants, not the exponent 1/2. Primes above √n need new witnesses; that is what §2 supplies.
2. **Primes p ≡ 1 (mod 4) and p = 2.** E-membership involves only v_q for q ≡ 3 (mod 4) (Lemma 2 plus the
   converse, eq. (5) in Liu). Proposition D shows that D_Q has no such prime factor. No argument made of local
   conditions can force them into t. Gaussian integers help only through F_p(i) for p ≡ 3 (mod 4), which is
   how they are used in Lemmas 4–5.
3. **Averaging over p (large sieve and similar).** This cannot help. In the proof of Proposition C the classes
   −t mod p can be chosen independently for different p (CRT). So "most classes mod p have two witnesses" never
   forces p | t. Every nonzero class mod p has to be covered, which is exactly F*(p) ≤ n.
4. **The conic-in-a-box method itself.** The main term is ≈ B⁴/p and the error is Σ W_r(s)Kl(s), with
   ΣW ≈ B².
   - With only the fourth moment (Lemma 6), Hölder is optimal given the information. W is spread over about
     (p/B)² values, each of size ≈ (B²/p)². That gives ‖W‖_{4/3} ≈ p^{−1/2}B^{5/2} and error ≈ p^{3/4}·p^{−1/2}B^{5/2} = p^{1/4}B^{5/2}, which forces
     B > p^{5/6}, so F* ≲ p^{5/3}: the cap is θ = 3/5. Spreading W further makes it worse, by the
     uncertainty principle.
   - With Weil's pointwise bound the error is ≈ √p·B². That needs B > p^{3/4}, so F* ≲ p^{3/2}: the cap is
     θ = 2/3. This is the same "square-root barrier" as the 2/3 level of distribution for incomplete sums.
   - Going further needs cancellation in Σ_s W_r(s)Kl(s). That is a sum of Kloosterman sums Kl(r m/4) over the
     short, r₂-weighted range m ≤ (p/B)². Equivalently, it needs a nontrivial bound for the number of points of
     x² + y² ≡ r (mod p) in a box of side p^{1/2+o(1)}, for every r, or a Burgess-type bound for characters of
     F_{p²} restricted to boxes. I did not attempt these, and I did not check what the literature gives (see
     Sources not read).
5. **Global arguments.** The other half of the shift condition (a ∉ E ⇒ a + t ∉ E) and the condition at
   primes q ∤ t are global (they are about prime factorizations of numbers near t). One could try to compare
   densities: |E ∩ [t+1, t+n]| = |E ∩ [1, n]|. That would need E to be equidistributed in intervals of length
   n ≈ (log t)^{5/3}, which is far beyond anything known. INFERRED, not pursued.

## 4. What this does and does not show

- VERIFIED (proved in this file, with a numerical cross-check): Theorem A, the bound F*(p) ≤ p^{5/3+o(1)}, and
  hence log t > n^θ for every θ < 3/5. The only background used is PROOF.md Lemmas 1, 3, 4 (re-proved or
  restated here) and Lemma 7, which I re-read. All constants are ineffective only through c_δ and y₀(δ), which
  are explicit in principle. p₁(ε) and N_θ are not computed.
- VERIFIED conditional on a cited theorem: Theorem B (θ < 2/3) assumes Weil's Kloosterman bound. That is a
  classical theorem, not a conjecture, but I did not re-prove it or re-read a proof of it.
- VERIFIED: Propositions C and D and Lemma 15. These are statements about what local conditions can and cannot
  force. They are not statements about actual n-shifts, whose existence is open.
- NOT shown: existence of n-shifts (question (a) itself stays open, and every bound here is vacuous for n with no
  n-shift). Not shown: any upper bound on t_n. Not shown: an exponent above 2/3, or above 3/5 without Weil.
- INFERRED, not proved: F*(p) = p^{1+o(1)}. The numerics give F*(p)/(p(log p)^{3/2}) ≤ 1.75 (max 1.741; sampled values 1.09–1.29)
  for 1000 ≤ p ≤ 20000, and a heuristic coupon-collector argument with density ≈ 1/√log of E points the same way.
  If true, Proposition C would give every θ < 1, and Proposition D says that is the best possible for local
  methods.
- Lean: nothing formalized. The formal-conjectures statement of 675(a) is about existence only.
- Novelty: not found in the forum thread, Liu's note, PROOF.md, or the arXiv queries listed. That means
  "not found there", not "proved new". Liu's Remark 12 points at exactly this kind of improvement (E in
  progressions).

## 5. Numerics (all with python3 -I; Python 3.11.7, numpy 1.26.4; total < 5 minutes)

Reproduce from this folder:
```
python3 -I code/check_identities.py > out/check_identities.txt   # ~6 s
python3 -I code/check_count.py      > out/check_count.txt        # ~2 min
python3 -I code/fstar.py 20000      > out/fstar.txt              # ~1 min
python3 -I code/shift_check.py      > out/shift_check.txt        # ~5 s
```
- check_identities: exact checks for every listed p.
  - Lemma 4 trace–norm count and G = −Kl, for p ≤ 43.
  - Lemma 5 S_r(h,k) = −Kl(r(h²+k²)/4) for all r and all (h,k), for p ∈ {3,…,43}.
  - Lemma 6: Σ|Kl|⁴ ≤ p²(3p−5) for 21 primes up to 499. The ratio is ≈ 0.667, consistent with the
    Sato–Tate value 2p³. max|Kl|/√p ≤ 1.995.
  - Lemma 7: r₂ ≤ 4d², and primitive r₂* ≤ 4·2^ω, for all a ≤ 2·10⁵.
- check_count: for (p, B) up to (1019, 400), N(r) computed directly equals the Lemma 9 Fourier formula for
  every r. The true max error, the pointwise bound, the Hölder bound and the Lemma 10 bound are all respected.
  The true error is ≈ 0.57–1.12·√p·B², the square-root size that Weil predicts, while Lemma 10 is very lossy.
- fstar: F*(p) for all p ≡ 3 (mod 4) up to 20000 (e.g. F*(19991) = 750258). log F*/log p decreases from
  ≈ 1.53 (p ≈ 100) to ≈ 1.37 (p ≈ 2·10⁴). F*(p)/(p(log p)^{1.5}) ≤ 1.741 for all 1000 ≤ p ≤ 20000 (sampled values 1.09–1.29). The box
  threshold Bbox(p) (two values x²+y², 0 ≤ x,y < B, in every class) is ≈ 3.5–4.5·√p for p ≤ 4003.
- shift_check: every n-shift t ≤ 2·10⁷ for n ≤ 31 is divisible by every p with F*(p) ≤ n (3 from n = 5, 7 from
  n = 26). Lemma 15 holds for p ∈ {3, 7, 11} on all of them. (Least shifts agree with PROOF.md: 48, 2304,
  40320, 173376, 1761984, 10269504.)

## 6. Sources not read

- Weil's bound for Kloosterman sums (A. Weil, 1948) and its proofs (Stepanov's method, Iwaniec–Kowalski Ch. 11):
  not read. Used only in Theorem B.
- Literature on sums of two squares in arithmetic progressions (level of distribution, least element of E in a
  residue class), on small solutions of quadratic congruences (e.g. work of Heath-Brown, Cochrane), on points
  of conics in small boxes, and on Burgess bounds over F_{p²}. I recall that such results exist but did not read
  any. A result giving F*(p) ≤ p^{κ} with κ < 3/2 would improve Theorem B directly through Proposition C. The
  arXiv queries in refs/arxiv/ found nothing relevant, but they were narrow keyword searches.
- Davenport, *Multiplicative Number Theory* (PNT for progressions): not read; used only for the constant in
  Theorem B(ii).
- Ho Boon Suan's squarefree note, Zhong–Zhang, Nunes (forum, part (c)): not read; not used.
- Any private or unindexed work on 675(a) after 2026-05-09: unknown.

## Files

- code/check_identities.py, code/check_count.py, code/fstar.py, code/shift_check.py
- out/*.txt (outputs of the commands above)
- refs/web/page675.html, refs/web/forum675.html (+ .txt), fetched 2026-11-23; refs/arxiv/*.xml (queries)
