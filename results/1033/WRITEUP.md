# Erdős 1033: how far the butterfly improvement over Fan's construction extends

Outcome: **PROVED.** The proof is computer-assisted: an exact-arithmetic sign check, described in Lemma 7.

## 0. Status check (done before starting)

- erdosproblems.com/1033 (fetched 2026-11-23, saved as `refs/page.html`) and its forum thread (`refs/forum.html`,
  9 comments, 27 Jun to 7 Aug 2026). VERIFIED: nobody discusses edge densities α > 1/4. The thread covers the butterfly
  construction (rickyc, GPT), Wouter CvB's optimisation at α = 1/4 (value 1.463877...), and RealBelgian's flag-algebra
  lower bounds.
- Plasma AI pages for E1033 (`refs/plasma_*.md`). VERIFIED: they cover only the α = 1/4 problem (the 183/125
  certificate and the Wouter claim). Nothing on general density.
- Wouter CvB's note (`../../refs/wouter_note.pdf`, read in full). It treats only α = 1/4.
- A quick arXiv API search ("degree sum" + triangle) found nothing relevant.

Conclusion: as far as I could find, the target is not already decided.

Note: the brief points to `t1/prove/../SCOUT.md`. That file does not exist. The scout notes were at
`attack/1033/SCOUT.md` and were read there (target T2 in that file is this task).

## 1. Statement established

**Setup.** A *butterfly blow-up* has these parameters:
- part weights x = (x_a, x_b, x_c, x_d, x_e) with x_i ≥ 0 and Σ x_i = 1;
- densities f = f_ac ∈ [0,1] and g = f_de ∈ [0,1].

The pairs ab, bc, ad, ae are complete. The pair ac has density f and the pair de has density g. The normalised
edge density and normalised degrees are

D = x_a x_b + x_b x_c + f x_a x_c + x_a x_d + x_a x_e + g x_d x_e,

d_a = x_b + f x_c + x_d + x_e, d_b = x_a + x_c, d_c = x_b + f x_a, d_d = x_a + g x_e, d_e = x_a + g x_d.

A triangle type is *present* if all its weights and its partial density are positive:
- type abc: x_a, x_b, x_c, f > 0;
- type ade: x_a, x_d, x_e, g > 0.

The two possible triangle degree sums are S_abc = d_a + d_b + d_c and S_ade = d_a + d_d + d_e. Define
τ(blow-up) as the maximum of S over the present types. For 1/4 < α ≤ 1/3 define

B(α) = inf{ τ : D ≥ α }    (the optimal butterfly blow-up at edge density α),
U(α) = 4√(3α) − 2          (Fan's construction).

Lemma 4 shows that using D = α instead of D ≥ α gives the same B. Every blow-up with D > 1/4 has a triangle
(Lemma 3).

**Theorem.** Let T_b ≈ 0.46502058891446675131420 be the unique root in (93/200, 1) of

p8(T) = 1761T⁸ + 15288T⁷ + 40795T⁶ + 11790T⁵ − 59967T⁴ + 75924T³ − 72279T² + 32886T − 5238.

Set α_b = (T_b + 3)²/48 ≈ **0.25013266003335745803180494801**. Equivalently, α_b is the largest real root of the
irreducible octic

457278898176A⁸ − 466300901376A⁷ + 181754989888A⁶ − 30906363888A⁵ + 1134475329A⁴ + 285053348A³ − 22147578A² − 988332A + 37249.

The threshold sum t_b = U(α_b) = 1 + T_b ≈ 1.465020588914466751 is a root of
1761y⁸ + 1200y⁷ − 16913y⁶ − 10548y⁵ + 81198y⁴ + 54256y³ − 437568y² + 552192y − 230816.

Then:
- (i) B(α) < U(α) for every α ∈ (1/4, α_b);
- (ii) B(α) = U(α) for every α ∈ (α_b, 1/3].

So the target quantity is exactly α_b:

sup{α ≥ 1/4 : B(α) < U(α)} = α_b.

Part (ii) follows from a stronger inequality (Proposition 8). Every butterfly blow-up with a triangle satisfies

D ≤ max(α_b, (τ + 2)²/48).

At α_b, the optimal butterfly is attained both by Fan's blow-up and by a Wouter-type blow-up (Lemma 9 has both).
This is a first-order crossing. The Wouter branch does not merge into Fan's family; it crosses it.

## 2. Reductions (all elementary, full proofs)

From here on write T = t − 1, where t is a triangle-sum level, and set M_F(T) = (T+3)²/48. Then
U(α) ≤ 1+T ⟺ α ≤ M_F(T), and M_F is strictly increasing for T > −3.

**Lemma 1 (Fan's construction is a butterfly blow-up).** Let 1/4 < α ≤ 1/3 and set k = 2√(α/3). Take
x_b = 1 − k, x_a = x_c = k/2, x_d = x_e = 0, f = 4(α − k(1−k))/k² and g = 0. Then f ∈ [0,1], D = α, and τ = U(α).
Hence B(α) ≤ U(α).

*Proof.* We have D = x_b(x_a + x_c) + f x_a x_c = k(1−k) + f k²/4 = α. Only type abc is present, and

S_abc = 2x_b + x_a + x_c + f(x_a + x_c) = 2 − k + fk.

Substituting fk = 4(α − k + k²)/k gives S_abc = 2 − k + 4α/k − 4 + 4k = 3k + 4α/k − 2. Since 3k = 2√(3α) and
4α/k = 4α/(2√(α/3)) = 2√(3α), this equals 4√(3α) − 2 = U(α).

For the bounds on f:
- f ≤ 1 ⟺ α ≤ k − 3k²/4 = 2√(α/3) − α ⟺ α ≤ 1/3.
- f ≥ 0 ⟺ α ≥ k(1−k) = 2√(α/3) − 4α/3 ⟺ √α ≥ 6/(7√3) ⟺ α ≥ 36/147 ≈ 0.245.

Both hold. f > 0 and x_a, x_b, x_c > 0, so type abc is present. ∎

**Lemma 2 (reduced coordinates).** Write s = x_d + x_e and u = g s ∈ [0, s]. Using Σx = 1:

- S_abc = 1 + x_b + f(x_a + x_c)
- S_ade = 1 + x_a − (1−f)x_c + u
- D = x_a x_b + x_b x_c + f x_a x_c + x_a s + g x_d x_e

If type ade is present, replace (x_d, x_e) by (s/2, s/2) and keep g. Then S_abc and S_ade are unchanged, the
presence of each type is unchanged, and D does not decrease. After the replacement the last term of D becomes u s/4.

*Proof.* First, S_abc = (x_b + f x_c + s) + (x_a + x_c) + (x_b + f x_a) = (x_a + x_b + x_c + s) + x_b + f(x_a + x_c).

Second, S_ade = (x_b + f x_c + s) + 2x_a + g s = (x_a + x_b + x_c + s) + x_a − x_c + f x_c + u.

S_abc involves only x_a, x_b, x_c, f (and s through Σx = 1). S_ade involves d and e only through s and u = g s. So
neither sum changes. AM–GM gives x_d x_e ≤ s²/4, so D does not decrease. The weights stay positive, so presence is
unchanged. ∎

In the coordinates (a, b, c, s, u) := (x_a, x_b, x_c, s, u) with a + b + c + s = 1, the program uses:

- D = ab + bc + fac + as + us/4
- C1: T − b − f(a+c) ≥ 0   (S_abc ≤ 1+T)
- C2: T − a + (1−f)c − u ≥ 0   (S_ade ≤ 1+T)
- bounds: a, b, c ≥ 0, s − u ≥ 0, u ≥ 0.

For fixed (f, T), the following polytopes are subsets of R⁵:

| name | constraints | used for |
|---|---|---|
| P_both(f,T) | a,b,c,u ≥ 0, s−u ≥ 0, C1, C2 | both types present |
| P_abc(f,T) | the same with u = 0 and without C2 | only abc present |
| P_b0(f,T) | without C1, with b = 0 | only ade present (b = 0) |
| P_c0(f,T) | without C1, with c = 0 | only ade present (c = 0) |
| P_f0(T) | without C1, f = 0 | only ade present (f = 0) |

Let v_•(f,T) be the maximum of D over the corresponding polytope (−∞ if it is empty).

**Lemma 3.**
- (a) Every butterfly blow-up has D ≤ 1/3.
- (b) A blow-up with no present triangle type has D ≤ 1/4.

*Proof.* (a) The colouring {a}, {b, d}, {c, e} is a proper 3-colouring of the butterfly. Hence
D ≤ X₁X₂ + X₁X₃ + X₂X₃ ≤ 1/3, where X_i are the colour-class weights.

(b) The butterfly's only cycles are the two triangles, because a is a cut vertex. So if no type is present, the
support graph (parts of positive weight joined by pairs of positive density) is a forest, and in particular
bipartite with sides of weights Y, 1 − Y. Then D ≤ Y(1−Y) ≤ 1/4. ∎

**Lemma 4 (≥α vs =α).** For α > 1/4 the infimum defining B(α) does not change if D ≥ α is replaced by D = α.

*Proof.* Take a blow-up with D ≥ α. Lower g continuously to 0, then lower f continuously to 0. Along the way
S_ade is non-increasing in g and S_abc is non-increasing in f. Types can only disappear, so τ does not increase. At
f = g = 0 no type is present, so D ≤ 1/4 < α by Lemma 3(b). D is continuous along the path, so by the intermediate
value theorem some point has D = α and τ no larger. ∎

**Lemma 5 (bounding by the polytopes).** Take any blow-up with at least one present type, and let T = τ − 1.
Then D ≤ max over the applicable programs of v_•(f, T), where f = f_ac, and:

- both types present ⇒ D ≤ v_both(f, T);
- only abc present ⇒ D ≤ v_abc(f, T);
- only ade present ⇒ D ≤ max(v_b0(f, T), v_c0(f, T), v_f0(T)).

Moreover, every v_• is non-decreasing in T.

*Proof.*
- **Both present.** Apply Lemma 2. The point (a, b, c, s, u) satisfies C1 and C2 because both sums are ≤ τ = 1+T.
- **Only abc present.** Then a > 0, and ade is absent, so x_d = 0, x_e = 0 or g = 0. In each case g x_d x_e = 0, so
  D = ab + bc + fac + as. This is the value at the point with u = 0, which satisfies C1.
- **Only ade present.** Then a > 0 and abc is absent, so b = 0, c = 0 or f = 0. Symmetrise d and e (Lemma 2). This
  keeps b, c, f fixed and keeps ade present. The point satisfies C2 and lies in P_b0, P_c0 or P_f0 respectively.

Monotonicity: the polytopes grow with T. ∎

**Lemma 6 (strict feasibility and lower semicontinuity).** Fix ε = 1/100. For every f ∈ [0,1] and
T ∈ [93/200, 1], the following points satisfy every non-forced inequality of the respective polytope strictly:

- (ε, ε, ε, 1−3ε, (1−3ε)/10) for P_both and P_f0;
- (ε, ε, ε, 1−3ε, 0) for P_abc;
- (ε, 0, ε, 1−2ε, (1−2ε)/10) for P_b0;
- (ε, ε, 0, 1−2ε, (1−2ε)/10) for P_c0.

Consequently each v_• is finite and lower semicontinuous on [0,1] × [93/200, 1].

*Proof.* Check P_both; the others are the same computation.
- a, b, c > 0.
- s − u = (9/10)(1−3ε) > 0 and u > 0.
- C1: T − ε − 2fε ≥ 0.465 − 0.03 > 0.
- C2: T − ε + (1−f)ε − u ≥ 0.465 − 0.01 − 0.097 > 0.

For P_b0 and P_c0 the C2 slack is ≥ 0.465 − 0.01 − 0.098 > 0.

Lower semicontinuity: let x* be a maximiser at (f*, T*), and let x₀ be the point above. For λ ∈ (0,1] the point
x_λ = (1−λ)x* + λx₀ satisfies the forced equalities. Each non-forced constraint is affine in x, so
g_i(x_λ; f*, T*) ≥ λ g_i(x₀; f*, T*) > 0. The constraint functions are continuous in (f, T), so x_λ is feasible for
all (f, T) near (f*, T*).

Hence liminf_{(f,T)→(f*,T*)} v(f,T) ≥ D_{f*}(x_λ) for every λ, using continuity of D in (x, f). Letting λ → 0 gives
liminf ≥ v(f*, T*). ∎

**Lemma 5′ (face lemma).** Fix one of the programs and a parameter point where its polytope P is non-empty. Then
v = max D(x_A), where the maximum runs over all active sets A of size ≤ 4 that:
- contain the forced constraints;
- have a Lagrange system L_A (stationarity of D − μ₀(a+b+c+s−1) − Σ_{i∈A} μ_i g_i, plus a+b+c+s = 1 and g_i = 0
  for i ∈ A) whose x-part has a unique generic solution x_A(f,T), a rational function;
- have x_A defined and lying in P at the given parameter point.

*Proof.* Every such x_A lies in P, so the maximum is ≤ v.

Conversely, P is compact and D is continuous, so maximisers exist. Choose one, x*, in a face F of P of minimal
dimension. Let I(F) be the set of inequalities tight on F. Then aff F = {a+b+c+s = 1, g_i = 0 for i ∈ I(F)} (the
standard description of the affine hull of a polyhedral face).

The relative interior of F is open in aff F and contained in P, so x* is a local maximum of D on aff F. Since aff F
is affine, x* is a stationary point of D|aff F (Lagrange's condition needs no constraint qualification here). Let S
be the set of stationary points of D on aff F. S is an affine subspace, the solution set of a linear system.

D is constant on S. Indeed, for x, y ∈ S we have ∇D(x)·(y−x) = 0, and H(y−x) = ∇D(y) − ∇D(x) is orthogonal to the
direction space of aff F. So D(y) − D(x) = ∇D(x)·(y−x) + ½(y−x)ᵀH(y−x) = 0.

If dim S > 0, a line in S through x* leaves the bounded set F at a point of a proper face. That point is also a
maximiser, contradicting minimality. So S = {x*}.

Choose A ⊆ I(F) containing the forced constraints such that {1} ∪ {∇g_i : i ∈ A} is a basis of
span({1} ∪ {∇g_i : i ∈ I(F)}). Then |A| ≤ 4. For j ∈ I(F) \ A, the function g_j − λ₀(a+b+c+s−1) − Σ_{i∈A} λ_i g_i
has zero gradient, so it is constant, and evaluating at x* shows the constant is 0. Hence A defines the same affine
set aff F.

L_A therefore has x-solution set S = {x*}, with independent constraint rows. That makes the coefficient matrix K_A
nonsingular at (f, T), so det K_A ≢ 0. Sympy's generic solution x_A over Q(f,T) equals Cramer's rule, so its reduced
denominator divides det K_A. Therefore x_A is defined at (f, T) and equals x*. ∎

The enumeration is in `code/qpfaces.py`. Active sets whose system is generically inconsistent or not uniquely
solvable in x have det K_A ≡ 0, so they can never occur as A. For every enumerated A, the code substitutes the
solution back into all equations of L_A and asserts they reduce to 0 exactly.

## 3. The computer-assisted step

**Lemma 7 (exact cell certificate).** Let • ∈ {both, abc, b0, c0} and let A be any enumerated active set.

Consider the open box (f, T) ∈ (0,1) × (T_b, 1). Decompose it cylindrically, adapted to:
- all irreducible factors over Q of the numerators and denominators of the coordinates of x_A;
- the constraint values g_i(x_A) (all inequalities of the program);
- Δ_A := M_F(T) − D(x_A);
- f and f − 1.

The decomposition is a Collins projection with respect to f. Its critical T-values are the real roots in (0,1) of:
- the leading coefficients in f;
- the discriminants in f;
- all pairwise resultants in f;
- the pure-T factors;
- p8 (so that T_b is a cell boundary).

On every open 2D cell (sector), the following implication holds:

[x_A defined and x_A ∈ P_•] ⇒ Δ_A ≥ 0.

The same statement holds for P_f0 in one dimension (cells of (T_b, 1) cut at the real roots of all factors).

*Verification.* `code/cadcheck.py`, driven by `code/run_relaxed.py` and `code/run_f0.py`, does the following:
- isolates all real roots exactly with sympy (Sturm/Descartes isolation with rational endpoints, refined until
  intervals from distinct irreducibles are disjoint);
- picks one rational sample T* in each gap above T_b. "Above T_b" is decided exactly by Sturm counting of p8 roots
  in (93/200, T*);
- at each T*, isolates the roots in f of every factor and picks a rational sample f* in every gap;
- evaluates every quantity at (f*, T*) in exact rational arithmetic.

Delineability: over a T-interval free of critical values, every factor keeps its f-degree and its simple roots. Its
roots in (0,1) move continuously and never meet each other or the lines f = 0, 1, because the resultants with f and
f − 1 are included. Hence every polynomial has constant sign on each sector, and the sample decides the whole
sector. The code asserts that no resultant or projection polynomial vanishes identically.

Results (`out/cad_*.out`): **0 failures** in every family.

| family | active sets with unique KKT point | 2D cells checked |
|---|---|---|
| both | 84 | 639 |
| abc | 22 | 100 |
| b0 | 23 | 55 |
| c0 | 19 | 26 |
| f0 | 44 | 60 (1D) |

Negative control: lowering the T-cut to 46/100 (below T_b). The checker then reports failures, exactly 3, all on the
Wouter face A = {C1, C2}, at T ≈ 0.4612, 0.4620, 0.4632 (`out/negcontrol_relaxed_cut046.out`). So it does detect the
known violation below T_b.

**Proposition 8 (main inequality).** For each family •, every f ∈ [0,1] and every T ∈ [T_b, 1]:
v_•(f,T) ≤ M_F(T). Consequently every butterfly blow-up with a triangle satisfies D ≤ max(α_b, (τ+2)²/48).

*Proof.* Fix •. For each A, the union of its sector cells is open and dense in the box. Let O be the intersection of
these unions over the finitely many A; O is also open and dense.

For (f, T) ∈ O, Lemma 5′ writes v_•(f,T) as a maximum of D(x_A) over the A with x_A defined and feasible. Lemma 7
says each such value is ≤ M_F(T). So v_• ≤ M_F on O.

The set {v_• − M_F > 0} is relatively open in [0,1] × [T_b,1]: v_• is lower semicontinuous (Lemma 6) and M_F is
continuous. This open set misses the dense set O, so it is empty. (For f0 the same argument runs in T alone.)

Now take a blow-up with a triangle and τ = 1 + T. There are three cases.
- If T ∈ [T_b, 1], Lemma 5 gives D ≤ M_F(T) = (τ+2)²/48.
- If T < T_b, monotonicity in T gives D ≤ max_• v_•(f, T_b) ≤ M_F(T_b) = α_b.
- If T > 1, Lemma 3(a) gives D ≤ 1/3 < (τ+2)²/48. ∎

**Proof of Theorem (ii).** Let α ∈ (α_b, 1/3] and take any blow-up with D ≥ α. Then D > 1/4, so it has a triangle
(Lemma 3b). Proposition 8 gives α ≤ D ≤ max(α_b, (τ+2)²/48), and since α > α_b we get (τ+2)²/48 ≥ α, that is
τ ≥ √(48α) − 2 = U(α). So B(α) ≥ U(α). Lemma 1 gives the reverse inequality. ∎

## 4. The Wouter branch and the existence part

**Lemma 9 (exact branch, crossing, f_b).** For the face A = {C1, C2} (`out/branch.out`):

- a = −(4Tf² − 4Tf − 8T + f³ + 4f² + 17f + 2)/Q(f)
- c = (Tf³ − 5Tf² − 12Tf − 12T + 5f² + f + 6)/Q(f)
- s = −4f(Tf² − 3Tf − 10T + f² + 7f + 4)/Q(f)
- u = −4(10Tf + 4T + f³ − 2f² − 3f − 2)/Q(f)
- b = T − f(a+c)

Here Q(f) = f⁴ − 6f³ − 11f² − 36f + 4. The value is

V_W(f,T) = −(T²f² − 4T²f + 4T² + 4Tf² + 6Tf − 4T + f³ + f² + 7f)/Q(f),

and

M_F − V_W = (f−1) N(f,T) / (48 Q(f)),

where N = T²(f³ − 5f² + 32f − 196) + T(6f³ − 30f² + 96f + 168) + 9f³ + 3f² − 48f − 36.

Then:
- Res_f(N, ∂_f N) = 384 (T+3)² p8(T).
- The degree-1 subresultant gives f_b = 2(401T⁴ + 1908T³ + 1146T² − 2484T + 693)/(71T⁴ + 564T³ + 1578T² + 1908T − 1305)
  at T = T_b, so f_b ≈ 0.44672110252553525362.
- Reducing modulo p8 shows that N(f_b, T_b) = 0 and ∂_f N(f_b, T_b) = 0 exactly.

Cross-check: with "= M_F" replaced by "= 1/4", the same machinery yields a resultant divisible by Wouter's
degree-7 polynomial P(y) at y = 1 + T (VERIFIED in code). This reproduces his 1.463877226961...

The crossing blow-up at α_b (`out/threshold_numbers.out`) is:

| parameter | value |
|---|---|
| x_a | 0.4265951873466 |
| x_b | 0.2426660278016 |
| x_c | 0.0711528703470 |
| x_d = x_e | 0.1297929572524 |
| f_ac | 0.4467211025255 |
| f_de | 0.2996802941869 |

Both triangle sums equal t_b and the density is α_b. Fan's blow-up at α_b is x_b = 0.42249656851,
x_a = x_c = 0.28875171574, f_ac = 0.07363422983.

**Proposition 10 (existence below α_b).** Fix f = f_b and let T ∈ [T₁, T_b], where T₁ = 4635/10000.
- (a) x_W(f_b, T) has all coordinates > 0 and 0 < u < s.
- (b) Δ_W(f_b, T) := M_F(T) − V_W(f_b,T) < 0 for T ∈ [T₁, T_b).
- (c) α(T) := V_W(f_b, T) is continuous, with α(T₁) < 1/4 and α(T_b) = α_b.

*Proof.* The values are computed with exact rational interval arithmetic on a rational enclosure of T_b of width
10⁻⁶⁰ (`code/branch.py`, `out/branch.out`).

(a) For fixed f, the coordinates are affine in T. They are certified strictly positive at both T₁ and T_b, as is
s − u, so they are positive on the whole segment.

(b) N(f_b, ·) is a quadratic with roots T_b and A₀/(A₂T_b) ∈ [0.6599, 0.6600], which lies outside [T₁, T_b]. So
Δ_W(f_b, ·) has one sign on [T₁, T_b). Its value at T₁ is certified < 0 (≈ −4.26·10⁻⁵). Q(f_b) is certified ≠ 0.

(c) α(T₁) ∈ [0.24995573, 0.24995574] < 1/4. At T_b, N(f_b, T_b) = 0, so Δ_W = 0 and α(T_b) = M_F(T_b) = α_b. ∎

**Proof of Theorem (i).** Let α ∈ (1/4, α_b). By (c) and the intermediate value theorem there is T ∈ (T₁, T_b)
with α(T) = α. Take the blow-up with:
- x_a, x_b, x_c, s, u from x_W(f_b, T);
- x_d = x_e = s/2;
- f_ac = f_b and f_de = u/s ∈ (0,1).

Both triangle types are present, both sums equal 1 + T because C1 and C2 are identically active on this face, and
D = α. By (b), α > M_F(T), so U(α) > 1 + T ≥ B(α). ∎

Theorem (i) and (ii) together give sup{α ≥ 1/4 : B(α) < U(α)} = α_b. (At α = 1/4, under any convention, the value
is ≤ α_b.) ∎

**Remark (graphs; standard, sketched only).** Realise a blow-up on N vertices with near-regular bipartite graphs of
the prescribed densities on ac and de, as in Wouter's note. This gives, for each α ∈ (1/4, α_b), graphs with ≥ αN²
edges in which every triangle has degree sum ≤ (B(α) + o(1))N < (4√(3α) − 2)N. In words, Fan's upper construction
for f(n, e) is beaten throughout this density window. This remark is not part of the established statement.

## 5. What this does and does not show

Does:
- Determines exactly the edge-density window in which blow-ups of the butterfly beat Fan's construction:
  (1/4, α_b), with α_b ≈ 0.2501326600 algebraic of degree 8.
- Shows the butterfly family gives nothing better than Fan for α ∈ (α_b, 1/3]. This is proved over all butterfly
  blow-ups: all part weights, d ≠ e allowed, both partial densities free, and triangle types counted only when
  present.

Does not:
- Say anything about graphs that are not butterfly blow-ups. Neither h(n) nor the general Δ₃(n, m) is determined.
  Fan's construction may well be beatable for α > α_b by other templates.
- Address the lower bound side (Fan's 21/16, RealBelgian's claimed flag-algebra bounds).

Trust base of Lemma 7:
- sympy's exact factorisation, resultants, subresultants, root isolation (`Poly.intervals`, `refine_root`,
  `count_roots`) and linear solving over Q(f,T);
- the correctness of my ~200-line driver.

The CAD-lite check uses only rational sample points and exact rational arithmetic; no floating point enters any
sign decision. Independent numerical cross-checks (`out/crosscheck.out`, not part of the proof):
- multistart SLSQP agrees with the face-enumeration value at 150 random (f, T), with maximum excess 1.4·10⁻¹⁴;
- 20000 random blow-ups plus 300 Nelder–Mead searches in the original 7-parameter space found no violation of
  D ≤ max(α_b, (τ+2)²/48). The best value was +1.1·10⁻¹⁶, which is rounding at Fan points.
- The scout's SLSQP numbers (gain at 0.25013, none at 0.25014) agree with α_b = 0.2501327.

Impact: small. This is an exact value inside the general-density variant recorded on the problem page, and it
documents how far the only known improvement over Fan extends.

## 6. Reproduce

From `attack/1033/t1/prove/code` (Python 3.11, sympy 1.14, scipy 1.17,
mpmath 1.3):

```
python3 -I run_relaxed.py relaxed     > ../out/cad_relaxed.out      # ~65 s
python3 -I run_relaxed.py abc_only    > ../out/cad_abc_only.out
python3 -I run_relaxed.py ade_only_b0 > ../out/cad_ade_only_b0.out
python3 -I run_relaxed.py ade_only_c0 > ../out/cad_ade_only_c0.out
python3 -I run_f0.py                  > ../out/cad_f0.out
python3 -I branch.py                  > ../out/branch.out           # alpha_b, f_b, existence certificate
python3 -I threshold_numbers.py       > ../out/threshold_numbers.out
NEGCONTROL_CUT=46/100 python3 -I run_relaxed.py relaxed > ../out/negcontrol_relaxed_cut046.out
python3 -I crosscheck.py              > ../out/crosscheck.out       # numerical only
```

(`-I` ignores PYTHONPATH and the current directory, so each script inserts its own directory into the path.)

## 7. Sources

Read: the erdosproblems.com page and forum thread for 1033; Plasma's E1033 index and both claim pages; Wouter CvB's
note; the scout file and `refs/bfly_slsqp.py`.

Sources not read:
- Fan 1988 (J. Graph Theory 12): its §2 bound f(n, e) < 4√(3e) − 2n + 5 is taken from Plasma's summary. My
  normalisation U(α) = 4√(3α) − 2 is re-derived independently in Lemma 1.
- Erdős–Laskar 1985, Bollobás–Nikiforov 2005, Faudree 1992.
- Plasma's L113 certificate pages.
- RealBelgian's flag-algebra work (no note available).
- The ChatGPT transcripts linked in the thread.
- ryantuck/erdos-ai (only the top-level listing was seen).
