# Erdős 1131, n = 4: exact minimum of I (attempted disproof; outcome: the target is TRUE, proved)

## Statement established

Let n = 4. For -1 <= x_1 < x_2 < x_3 < x_4 <= 1 let l_k be the Lagrange basis polynomials and
I(x) = int_{-1}^{1} sum_k l_k(x)^2 dx. Let t* be the unique real root of 21t^3 + 9t^2 + 3t - 1
(t* = 0.18547209365357910332..., it lies in (0,1)). Then

    min I = I*_4 = (140 t*^2 - 112 t* + 92 + 8/t*) / (105 (1 - t*)^2) = 1.71075810740114490363...,

and the minimum is attained **only** at (x_1,x_2,x_3,x_4) = (-1, -sqrt t*, sqrt t*, 1)
(sqrt t* = 0.43066471140967552383...).

So the scout's target is TRUE; no counterexample exists. The value agrees with the upper end
of mzn's certified bracket [1.710738107401, 1.710758107402] (forum, 14 Aug 2026).

Notation. T = {(u,v): -1 < u < v < 1}; I(u,v) := I(-1,u,v,1); S(x) = sum_k l_k(x)^2.

## Lemma 1 (endpoint reduction; valid for every n >= 2)

Let x_1 < ... < x_n in [-1,1], a = x_1, b = x_n, L = b - a, and suppose (a,b) != (-1,1).
Let y_k = phi(x_k) with phi(x) = -1 + 2(x-a)/L. Then I(x) > min(2, I(y)).

*Proof.* phi is affine with positive slope 2/L, so y_i - y_j = (2/L)(x_i - x_j) and
phi(x) - y_j = (2/L)(x - x_j); every factor ratio in l_k is unchanged, so l^y_k(phi(x)) = l^x_k(x)
and S_y(phi(x)) = S_x(x). Substituting y = phi(x), dy = (2/L)dx:
I(y) = (2/L) A with A := int_a^b S_x(x) dx.
Let O = [-1,1] \ [a,b]; it has measure 2 - L > 0. For x > b, each factor (x - x_j)/(b - x_j)
(j < n) of l_n(x) exceeds 1 because x - x_j > b - x_j > 0, so S_x(x) >= l_n(x)^2 > 1. For x < a,
each factor (x - x_j)/(a - x_j) = (x_j - x)/(x_j - a) (j > 1) of l_1(x) exceeds 1, so S_x(x) > 1.
S_x is continuous and > 1 on O, hence int_O S_x > 2 - L. So I(x) = A + int_O S_x > A + 2 - L.
- If A <= L: A + (2 - L) >= A + (2 - L)A/L = 2A/L = I(y), so I(x) > I(y).
- If A > L: I(x) > L + 2 - L = 2. ∎

## Lemma 2 (explicit formula, exact computation)

For (u,v) in T,
I(u,v) = 4 P(u,v) / (105 (1-u^2)^2 (1-v^2)^2 (v-u)^2), with P the degree-10 polynomial printed
in out/verify_output.txt. In the coordinates z = (v-u)^2, w = (u+v)^2,
I(u,v) = (256/105) G(z,w), G = N(z,w) / (z E(z,w)^2), E = (w-z)^2 - 8(w+z) + 16 = 16(1-u^2)(1-v^2).

*Proof.* Each ∫ l_k^2 is the exact integral of a polynomial; computed symbolically (sympy) and
cross-checked at 20 random rational (u,v) against an independent pure-Python Fraction
implementation (exact equality). Evenness of the numerator in s = u+v and in d = v-u separately,
the identity for E, and I = (256/105) G are verified as polynomial identities. (code/verify.py,
Steps 1 and 3.) ∎

On T: z = (v-u)^2 in (0,4), and -2 < u+v < 2 so w in [0,4); E > 0 and z > 0, so G is a rational
function with non-vanishing denominator on the image of T.

## Lemma 3 (the symmetric family)

I(-1,-sqrt t, sqrt t, 1) = (140t^2 - 112t + 92 + 8/t)/(105(1-t)^2) =: J(t) for t in (0,1), and
J'(t) = 8(21t^3 + 9t^2 + 3t - 1)/(105 t^2 (1-t)^3). The cubic c(t) = 21t^3+9t^2+3t-1 has
c'(t) = 63t^2 + 18t + 3 with negative discriminant (324 - 756) and positive leading coefficient,
so c is strictly increasing on R; c(0) = -1 < 0 < 32 = c(1). Hence J' = 0 on (0,1) exactly at t*.
Also J(3/16) = 91076/53235 < 2. (Identities verified exactly; Sturm count confirms one root in [0,1].) ∎

## Lemma 4 (coercivity: a minimizer over T exists)

For (u,v) in T, l_u(x) = (x+1)(x-v)(x-1) / ((u+1)(u-v)(u-1)) and
∫_{-1}^1 ((x^2-1)(x-v))^2 dx = 16/105 + (16/15) v^2 >= 16/105 (odd cross term integrates to 0;
verified exactly). So I(u,v) >= ∫ l_u^2 >= (16/105) / ((1+u)^2 (v-u)^2 (1-u)^2), and symmetrically
I(u,v) >= ∫ l_v^2 >= (16/105) / ((1+v)^2 (v-u)^2 (1-v)^2).
If I(u,v) <= 2 then (1+u)^2(v-u)^2(1-u)^2 >= 8/105, and since 0 < 1-u <= 2,
(1+u)(v-u) >= c := sqrt(8/105)/2 > 0; likewise (1-v)(v-u) >= c.
Let K = {(u,v) in [-1,1]^2 : u <= v, (1+u)(v-u) >= c, (1-v)(v-u) >= c}. K is closed and bounded,
hence compact, and every point of K has 1+u > 0, v-u > 0, 1-v > 0, so K ⊂ T. Every point of
T \ K has I > 2. K is nonempty: it contains (-sqrt3/4, sqrt3/4), where I = J(3/16) < 2.
I is continuous on K, so it attains its minimum on K at some Q; for p in T \ K,
I(p) > 2 > J(3/16) >= I(Q). So Q minimizes I over the open set T, hence grad I(Q) = 0. ∎

## Lemma 5 (the only critical point of I in T is (-sqrt t*, sqrt t*))

With z = (v-u)^2, w = (u+v)^2 and I = (256/105) G(z,w) (Lemma 2), the chain rule gives
dI/du + dI/dv = (256/105) · 4(u+v) G_w and dI/dv - dI/du = (256/105) · 4(v-u) G_z.
So grad I = 0 at a point of T iff G_z = 0 and (u+v = 0 or G_w = 0) (using v - u > 0).

*Case u+v = 0.* Then (u,v) = (-sqrt t, sqrt t), t = v^2 in (0,1), and z = 4t, w = 0, so
J(t) = (256/105) G(4t, 0) and J'(t) = (1024/105) G_z(4t,0). Thus G_z = 0 iff J'(t) = 0 iff t = t*
(Lemma 3). This point is indeed critical (G_w term is multiplied by u+v = 0).

*Case u+v != 0.* Then w0 = (u+v)^2 in (0,4) and z0 = (v-u)^2 in (0,4) satisfy G_w = G_z = 0.
Exactly (verified), G_w = Gw_num/(z E^3), G_z = Gz_num/(z^2 E^3) with Gw_num = (1/8) a(z,w),
Gz_num = (1/8) b(z,w) for the integer polynomials a (deg_z 5, LC_z = 119) and b (deg_z 6,
LC_z = -21) printed in out/verify_output.txt. Since z0 > 0 and E > 0, a(z0,w0) = b(z0,w0) = 0.
Both leading coefficients in z are nonzero constants, so the resultant R(w) = Res_z(a,b) specialises
correctly at w0 and R(w0) = 0 (common root z0). Exactly,
R(w) = -1544734672188080128 · w^3 (w-4)^6 (49w^2 - 84w + 64) · R10(w)   (out/resultant_factors.txt),
the factorization re-multiplies to R, and R1 := R/(w^3(w-4)^6) satisfies R1(0) != 0, R1(4) != 0 and
has **no real root in [0,4]** (exact Sturm count = 0; independently, exact real-root isolation puts
all real roots of R1 in negative intervals). So R has no root in (0,4): contradiction. ∎

## Theorem (main)

*Proof.* By Lemma 4, I attains a minimum on T at a critical point; by Lemma 5 that point is
P* = (-sqrt t*, sqrt t*), and any (u,v) in T with I(u,v) = min_T I is a minimizer, hence
critical, hence equal to P*. So min_T I = J(t*) =: I*, attained only at P*, and I* <= J(3/16) < 2.
Now take any x_1 < ... < x_4 in [-1,1]. If x_1 = -1 and x_4 = 1, then I(x) >= I* with equality iff
x = (-1, -sqrt t*, sqrt t*, 1). Otherwise Lemma 1 gives I(x) > min(2, I(y)) with y having both
endpoints, so I(x) > min(2, I*) = I*. ∎

## Code and reproduction

- code/verify.py — all exact checks (run with sympy 1.14.0; uses `sympy`, `mpmath`, `fractions`).
- out/verify_output.txt — full output: 38 PASS, 0 FAIL.
- out/resultant_factors.txt — the exact factorization of Res_z(a,b).
- Reproduce: `cd attack/1131/t1/disprove && python3 -I code/verify.py`
  (about 2 seconds).
- code/explore*.py — exploratory scripts, not load-bearing.

Load-bearing computer steps (all exact rational/polynomial arithmetic): the formula for I(u,v);
the change of coordinates; the derivative identities; the resultant, its factorization and the
Sturm/real-root-isolation counts; J'(t) and J(3/16). Floats appear only in lines tagged [sanity]
(40-digit value of I*, and a 0.005 grid over T whose best value 1.710764 sits at (-0.43,0.43)).

## What this does and does not show

- VERIFIED (proof above + exact computation): the exact value of I*_4 and uniqueness of the
  minimizer (-1, -sqrt t*, sqrt t*, 1). This answers the problem's first question ("what is the
  minimal value") for n = 4 only.
- VERIFIED: Lemma 1 holds for every n: any node set not containing both ±1 has I > min(2, value of
  its rescaling). Combined with any configuration of value < 2 (e.g. ESVV94's upper bound, read on
  the problem page only), the infimum for each n is approached only by node sets containing ±1.
  This is an elementary observation and is quite possibly already in ESVV94 / BrTo97 (not read).
- NOT shown: anything for n >= 5 (Target B), or about the asymptotic 2 - c/n.
- Trust assumptions: correctness of sympy's integrate (cross-checked independently), resultant,
  factor_list (re-multiplied), count_roots (Sturm) and intervals (two independent root-count
  methods agree). A fully independent re-run in another CAS was not done.
- Novelty: NOT established. BrTo97 (numerical) likely reports the n = 4 optimum to ~6 digits and
  may well identify the symmetric configuration; the closed form via the cubic may or may not be
  in the literature. The exact derivative and the formula J(t) are elementary.

## Sources read

erdosproblems.com/1131 and forum thread (refs/page.html, refs/forum.html, fetched 2026-11-23;
problem still open, last edited 23 Jan 2026; forum posting suspended); Plasma pages
wiki/problems/polynomials/E1131/_index.md and wiki/research/erdos_1131/* (refs/plasma_*);
../SCOUT.md (found at attack/1131/SCOUT.md, not at t1/SCOUT.md).

## Sources not read

Brutman–Toledano 1997 (Comput. Math. Appl. 34(12), 37–47) — the most likely prior source of the
n = 4 optimum; ESVV94; Szabados 1966; Erdős 1961/1995; Fejér 1932; Price/GPT-5.5 Pro write-up;
Rafik's preprints; ryantuck/erdos-ai; arXiv search not performed.
