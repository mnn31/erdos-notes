# Erdős #838 — convex subsets of the Erdős–Szekeres sets, and an upper constant below 1

Date: 2026-11-23. Status of the target: **established** (rigorous; one lemma, Lemma 13, is
computer-assisted by outward-rounded interval arithmetic and is used only for the ratio
optimisation, not for the main bound).

## 0. Statement established

All logarithms are base 2 unless written `ln`. `f(n)` is as on erdosproblems.com/838: the least
number of convex subsets (subsets in convex position; empty set, singletons and pairs included, as
in the formal-conjectures file — this changes counts by at most `1+n+n^2` and does not matter) over
all `n`-point sets in the plane with no three on a line.

For integers `i, j >= 0` let `𝓔(i,j)` be the Erdős–Szekeres family defined in §2 (in the usual
`(a,b)` notation, `E(a,b)` = `𝓔(a-2,b-2)`: no `a`-cup, no `b`-cap, `|E(a,b)| = C(a+b-4,a-2)`).
Let `c(i,j)` = number of nonempty convex-position subsets of a member of `𝓔(i,j)` (it does not
depend on the member, Theorem A). Put

    γ(ρ) = [Φ(ρ) + ρ²Φ(1/ρ)] / φ(ρ)²,   φ(x) = (1+x)log(1+x) − x log x,   Φ(y) = ∫_0^y φ.

**Theorem.**
1. (Exact recursion, Theorem A.) `c(i,j) = c(i−1,j) + c(i,j−1) + u(i−1,j)·v(i,j−1)` with
   `u(i,j) = u(i−1,j)(1+s(i,j−1)) + u(i,j−1)`, `v(i,j) = v(i,j−1)(1+s(i−1,j)) + v(i−1,j)`,
   `s(i,j) = C(i+j,i)`, and `s=u=v=c=1` when `i=0` or `j=0`.
2. (Balanced ES constant, Theorem B.) For `k >= 2`,
   `2I(k−1)² − (2k−2)log(2k) <= log c(k,k) <= 2Ik² + 10k + 2`, `I = 2 − 1/(2 ln 2)`. Hence
   `c_ES := lim_m log C(E(m,m)) / (log|E(m,m)|)² = I/2 = 1 − 1/(4 ln 2) = 0.6393262397…`
3. (Answer to the question, Theorem C.)
   `limsup_n log f(n)/(log n)² <= 1 − 1/(4 ln 2) ≈ 0.63933 < 1`;
   explicitly, for `n >= 3`, `log f(n) <= (1/2 − 1/(8 ln 2))(log n + log(2 log n + 1) + 2)² + 10 log n + 13`.
   In natural logs: `limsup ln f(n)/(ln n)² <= 1/ln 2 − 1/(4 (ln 2)²) ≈ 0.92235` (previously `1/ln 2 ≈ 1.4427`).
4. (Other aspect ratios, Theorem D + Lemma 13.) If `i, j → ∞` with `i/j → ρ ∈ (0,∞)` then
   `log c(i,j)/(log s(i,j))² → γ(ρ)`; `γ(ρ) = γ(1/ρ)` and `γ(ρ) > γ(1) = 1 − 1/(4 ln 2)` for every
   `ρ ≠ 1` (computer-assisted). So within the ES family the balanced shape is optimal and no aspect
   ratio improves on `1 − 1/(4 ln 2)`.
5. (2^{k−2}-point set, Corollary E.) Any `n = 2^{k−2}`-point set in general position that contains a
   member of `𝓔(⌊(k−2)/2⌋, ⌈(k−2)/2⌉)` has at least `2^{(1−1/(4 ln 2) − o(1))(log n)²}` convex subsets.
   So, *provided* the classical `2^{k−2}`-point Erdős–Szekeres set contains such a balanced block (it
   is usually described as a union of blocks from `𝓔(i,k−2−i)`, `0<=i<=k−2` — recalled, not read
   in a source here), it cannot beat the `E(m,m)` constant.

The forum/Plasma state of the art (base 2) was `1/4 <= liminf <= limsup <= 1`; item 3 improves the
upper constant `1` to `1 − 1/(4 ln 2)`. Novelty: no prior count found (see §6), but the literature
search was short.

---

## 1. Conventions and chain facts

Point sets have pairwise distinct `x`-coordinates; list them by increasing `x`. `σ(p,q)` is the
slope of `pq`. A sequence `c_0 < c_1 < … < c_t` (by `x`) is a **cup** if
`σ(c_0,c_1) < σ(c_1,c_2) < … < σ(c_{t−1},c_t)` and a **cap** if the slopes strictly decrease. Sets
of size `<= 2` are both. A set `S` is in **convex position** if no `s∈S` lies in `conv(S∖{s})`.
This property is inherited by subsets (`conv(S'∖{s}) ⊆ conv(S∖{s})` for `S' ⊆ S`).

**Lemma 1 (mediant).** If `x_1 < x_2 < x_3` then
`σ(p_1,p_3) = [(x_2−x_1)σ(p_1,p_2) + (x_3−x_2)σ(p_2,p_3)]/(x_3−x_1)`, so `σ(p_1,p_3)` lies
between `σ(p_1,p_2)` and `σ(p_2,p_3)`, strictly if these differ. Moreover `p_2` is strictly below
the line `p_1p_3` iff `σ(p_1,p_2) < σ(p_1,p_3)` iff `σ(p_1,p_2) < σ(p_2,p_3)`.

*Proof.* `y_3−y_1 = (y_2−y_1)+(y_3−y_2)`; divide by `x_3−x_1`. The line `p_1p_3` at `x_2` has height
`y_1 + σ(p_1,p_3)(x_2−x_1)`, and `x_2−x_1>0`, giving the first equivalence; the second follows from
the weighted-average formula. ∎

**Lemma 2 (sub-chains, chords).** (a) Every subset of a cup is a cup; every subset of a cap is a cap.
(b) If `c_0<…<c_t` is a cup, every `c_k` with `0<k<t` lies strictly below the line `c_0c_t`;
for a cap, strictly above.

*Proof.* (a) Removing an endpoint keeps the remaining slopes. Removing `c_k`, `0<k<t`, replaces
`σ(c_{k−1},c_k), σ(c_k,c_{k+1})` by `σ(c_{k−1},c_{k+1})`, which by Lemma 1 lies strictly between
them; so the new slope sequence is still strictly increasing. Induct on the number of removed points.
(b) By Lemma 2(a), `c_0,c_k,c_t` is a cup, i.e. `σ(c_0,c_k) < σ(c_k,c_t)`; apply Lemma 1. Caps are
symmetric. ∎

**Lemma 3 (convex position = lower cup + upper cap).** Let `S` (distinct `x`, no three collinear,
`|S|>=2`) have leftmost point `p` and rightmost point `q`; let `S⁻`, `S⁺` be the points strictly
below, strictly above the line `pq` (so `S = {p,q} ⊔ S⁻ ⊔ S⁺`). Then `S` is in convex position iff
`K⁻ := {p}∪S⁻∪{q}` is a cup and `K⁺ := {p}∪S⁺∪{q}` is a cap.

*Proof.* (⇒) Write `K⁻ = c_0=p < c_1 < … < c_t=q`. Suppose for some `0<k<t` the slopes fail,
i.e. `σ(c_{k−1},c_k) > σ(c_k,c_{k+1})` (equality is excluded by non-collinearity). By Lemma 1, `c_k`
is strictly above the segment `c_{k−1}c_{k+1}`; let `A` be the point of that segment with
`x = x_{c_k}`. Since `c_k ∈ S⁻` and `x_p < x_{c_k} < x_q`, `c_k` is strictly below the point `B` of
the segment `pq` with the same `x`. So `c_k ∈ [A,B] ⊆ conv{c_{k−1},c_{k+1},p,q} ⊆ conv(S∖{c_k})`,
contradicting convex position. So `K⁻` is a cup; `K⁺` is a cap by the mirror argument.

(⇐) Let `F` (resp. `G`) be the piecewise-linear interpolation of `K⁻` (resp. `K⁺`) on
`[x_p,x_q]`. `F` is convex (slopes increase), `G` concave, and both agree with the line `ℓ = pq` at
`x_p, x_q`; hence `F <= ℓ <= G`, and every point `z` of `S` satisfies `F(x_z) <= y_z <= G(x_z)`.
*Endpoints:* `S∖{p}` lies in the open half-plane `x > x_p`, so `p ∉ conv(S∖{p})`; same for `q`.
*Interior point `s = c_k` of `K⁻`* (`0<k<t`): pick `μ` with
`σ(c_{k−1},c_k) < μ < σ(c_k,c_{k+1})` and let `λ(x) = y_s + μ(x−x_s)`. For `x > x_s`,
`F(x)−F(x_s) = ∫_{x_s}^x F' >= σ(c_k,c_{k+1})(x−x_s) > μ(x−x_s)` because `F'` is non-decreasing;
symmetrically for `x < x_s`. Hence every `z ∈ S∖{s}` (which has `x_z ≠ x_s`) satisfies
`y_z >= F(x_z) > λ(x_z)`: `S∖{s}` lies in an open half-plane not containing `s`, so
`s ∉ conv(S∖{s})`. Interior points of `K⁺` are symmetric (use `G`). ∎

## 2. The Erdős–Szekeres family and the exact recursion

**Definition.** `𝓔(i,j)` for `i=0` or `j=0`: all one-point sets. For `i,j>=1`: all sets `P = L ∪ R`
with `L ∈ 𝓔(i−1,j)`, `R ∈ 𝓔(i,j−1)` and
- (P1) every `x`-coordinate in `R` exceeds every `x`-coordinate in `L`;
- (P2) every slope `σ(l,r)`, `l∈L`, `r∈R`, exceeds every slope between two points of `L` and every
  slope between two points of `R`.

(This is the "far up-right translate" construction; `E(a,b) = 𝓔(a−2,b−2)`.)

**Lemma 4 (existence, general position).** For all `i,j` there is `P ∈ 𝓔(i,j)` with integer
coordinates. Every `P ∈ 𝓔(i,j)` has distinct `x`-coordinates, no three collinear points, and
`|P| = C(i+j,i)`.

*Proof.* Existence by induction: given integer `L, R`, shift `R` right by an integer `X` so that
(P1) holds, let `M⁺ >= 0` bound all internal slopes, `D = max(x_r−x_l)` and `Δ = max|y_r−y_l|` over
`l∈L` and shifted `r`, and shift up by an integer `Y > M⁺D + Δ`. Then each cross slope has numerator
`> M⁺D` and denominator in `(0,D]`, so it exceeds `M⁺`. Distinct `x`: induction and (P1). No three
collinear: triples inside `L` or `R` by induction; a triple `l_1<l_2` in `L`, `r` in `R` would need
`σ(l_1,l_2) = σ(l_1,r)`, but the latter is a cross slope and is larger by (P2); a triple `l`,
`r_1<r_2` would need `σ(l,r_1) = σ(r_1,r_2)`, again impossible. Size: `C(i−1+j,i−1)+C(i+j−1,i) =
C(i+j,i)`. ∎

**Lemma 5 (chains crossing the split).** Let `P = L∪R ∈ 𝓔(i,j)`, `i,j>=1`.
(a) A cup of `P` meeting both `L` and `R` contains exactly one point of `R` (its last point).
(b) If `A` is a cup of `L` and `r∈R`, then `A∪{r}` is a cup.
(c) A cap of `P` meeting both `L` and `R` contains exactly one point of `L` (its first point).
(d) If `l∈L` and `B` is a cap of `R`, then `{l}∪B` is a cap.

*Proof.* By (P1), in any chain the `L`-points precede the `R`-points. (a) If a cup had two
`R`-points, let `l` be its last `L`-point and `r_1<r_2` the next two points (both in `R`); then
`σ(l,r_1) > σ(r_1,r_2)` by (P2), contradicting increasing slopes. (b) The slopes inside `A` increase,
and the last slope `σ(a_last, r)` is a cross slope, larger than the internal `σ(a_{last−1},a_last)`
by (P2). (c), (d): mirror images (for (c), if `l_1<l_2` are the last two `L`-points and `r` the next
point, a cap needs `σ(l_1,l_2) > σ(l_2,r)`, contradicting (P2)). ∎

**Lemma 6 (crossing convex sets).** For `P = L∪R ∈ 𝓔(i,j)`, `i,j>=1`, the map `(A,B) ↦ A∪B` is a
bijection from {nonempty cups `A ⊆ L`} × {nonempty caps `B ⊆ R`} onto {convex-position `S ⊆ P` with
`S∩L ≠ ∅ ≠ S∩R`}.

*Proof.* *Well defined.* Let `S = A∪B`, `p` = first point of `A` (the leftmost of `S`, by (P1)),
`q` = last point of `B`. By Lemma 5(b), `A∪{q}` is a cup from `p` to `q`, so by Lemma 2(b) every
point of `A∖{p}` is strictly below the line `pq`; by Lemma 5(d), `{p}∪B` is a cap, so every point of
`B∖{q}` is strictly above. Hence `S⁻ = A∖{p}`, `S⁺ = B∖{q}`, `K⁻ = A∪{q}` is a cup and
`K⁺ = {p}∪B` a cap; `S` is in convex position by Lemma 3 (`P` is in general position, Lemma 4).
*Injective:* `A = S∩L`, `B = S∩R`. *Surjective:* let `S` be convex with both parts nonempty; its
leftmost `p` is in `L` and rightmost `q` in `R` (P1). By Lemma 3, `K⁻` is a cup containing `p∈L`
and `q∈R`, so by Lemma 5(a) `K⁻∩R = {q}`; thus `S⁻ ⊆ L`. Likewise `K⁺∩L = {p}` (Lemma 5(c)), so
`S⁺ ⊆ R`. Therefore `S∩L = {p}∪S⁻ = K⁻∖{q}`, a nonempty cup (Lemma 2(a)), and
`S∩R = K⁺∖{p}`, a nonempty cap, and `S` is their union. ∎

**Theorem A (recursion).** For `P ∈ 𝓔(i,j)` let `s,u,v,c` be the numbers of points, nonempty cups,
nonempty caps and nonempty convex-position subsets. They depend only on `(i,j)`, equal 1 when
`i=0` or `j=0`, and for `i,j>=1`:

    s(i,j) = s(i−1,j) + s(i,j−1) = C(i+j,i)
    u(i,j) = u(i−1,j)·(1 + s(i,j−1)) + u(i,j−1)
    v(i,j) = v(i,j−1)·(1 + s(i−1,j)) + v(i−1,j)
    c(i,j) = c(i−1,j) + c(i,j−1) + u(i−1,j)·v(i,j−1).

*Proof.* Base: one point. Cups of `P`: those inside `L` (`u(L)`), inside `R` (`u(R)`), and those
meeting both, which by Lemma 5(a),(b) and Lemma 2(a) are exactly `A∪{r}` with `A` a nonempty cup of
`L` and `r∈R` (bijectively: `r` is the unique `R`-point, `A` the rest), `u(L)·|R|` of them. Caps:
mirror. Convex subsets: inside `L`, inside `R`, or meeting both — counted by Lemma 6. Induction on
`i+j` gives independence of the realization. ∎

*Computation (VERIFIED, `code/brute.py`, `out/brute.txt`):* for two independent random integer
realizations of each of `(i,j) ∈ {(1,1),(1,2),(2,1),(2,2),(1,5),(5,1),(2,3),(3,2),(3,3),(2,4),
(4,2),(3,4),(4,3),(2,6),(6,2),(1,8),(8,1)}` (up to 35 points), (P1),(P2) and general position were
checked exactly and the brute-force numbers of cups, caps and convex subsets (exhaustive hereditary
DFS, exact integer orientation tests, convex position tested by hull size) equal the recursion,
e.g. `c(3,3) = 10951` (20 points), `c(3,4) = 354653` (35 points).

## 3. Bounds and asymptotics

Let `h(a,b) = (a+b)log(a+b) − a log a − b log b` (`0 log 0 = 0`) for `a,b >= 0`. Facts:
`h(a,b) = (a+b)H(a/(a+b))` (binary entropy), so `0 <= h(a,b) <= a+b`; `h` is symmetric, homogeneous
of degree 1, `h(x,1) = φ(x)`, continuous, and strictly increasing in each argument on `(0,∞)`
(`∂h/∂a = log((a+b)/a) > 0`).

**Lemma 7 (binomials).** For integers `0 <= t <= N`:
`2^{h(t,N−t)}/(N+1) <= C(N,t) <= 2^{h(t,N−t)}`.

*Proof.* With `π = t/N` (trivial if `t ∈ {0,N}`), the terms `b_m = C(N,m)π^m(1−π)^{N−m}` sum to 1,
and `C(N,t)π^t(1−π)^{N−t} = C(N,t)2^{−h(t,N−t)}`. So `C(N,t) <= 2^{h}`. The ratio
`b_{m+1}/b_m = (N−m)π/((m+1)(1−π))` is decreasing in `m`, `> 1` at `m = t−1` (equals
`(N−t+1)/(N−t)`) and `< 1` at `m = t` (equals `t/(t+1)`), so `b_t` is the largest of the `N+1` terms
and `b_t >= 1/(N+1)`. ∎

**Lemma 8 (Riemann sums).** For integers `J >= 1`, `M >= 0`:
`∫_0^M h(x,J)dx <= Σ_{t=1}^M h(t,J) <= ∫_0^M h(x,J)dx + h(M+1,J)`, and `∫_0^M h(x,J)dx = J²Φ(M/J)`.

*Proof.* `h(·,J)` is increasing, so `∫_{t−1}^t h <= h(t,J) <= ∫_t^{t+1} h`; sum and use
`∫_1^{M+1} <= ∫_0^M + ∫_M^{M+1} <= ∫_0^M + h(M+1,J)`. The last identity: substitute `x = Jy` and use
`h(Jy,J) = Jφ(y)`. ∎

Define, for `a,b>0`, `Q(a,b) = ∫_0^a h(x,b)dx + ∫_0^b h(a,y)dy`. It is continuous and homogeneous
of degree 2, and `Q(ρ,1) = Φ(ρ) + ρ²Φ(1/ρ) =: N(ρ)` (by Lemma 8's identity and symmetry of `h`).
Closed form (checked symbolically in `code/gamma_min.py`):
`Φ(y) = [(1+y)²/2·ln(1+y) − (1+y)²/4 + 1/4 − y²/2·ln y + y²/4]/ln 2`, so
`I := Φ(1) = 2 − 1/(2 ln 2) = 1.27865…`.

**Lemma 9 (product bounds).** For all `i,j >= 0`, with `Π_u(i,j) = ∏_{t=1}^i (1+s(t,j))` and
`Π_v(i,j) = ∏_{t=1}^j (1+s(i,t))`:
(a) `u(i,j) <= 2^{i+j}Π_u(i,j)`, `v(i,j) <= 2^{i+j}Π_v(i,j)`, `c(i,j) <= 4^{i+j}Π_u(i,j)Π_v(i,j)`;
(b) for `i,j >= 1`: `u(i,j) >= ∏_{t=1}^i s(t,j−1)`, `v(i,j) >= ∏_{t=1}^j s(i−1,t)`, and
`c(i,j) >= u(i−1,j)v(i,j−1) >= ∏_{t=1}^{i−1} s(t,j−1) · ∏_{t=1}^{j−1} s(i−1,t)`.

*Proof.* `s(t,j)` is non-decreasing in each argument (Pascal), so `Π_u, Π_v` are non-decreasing in
each of `i, j` (all factors `>= 1`). (a) Induction on `i+j`; base values are 1. Step:
`u(i,j) <= 2^{i+j−1}[Π_u(i−1,j)(1+s(i,j−1)) + Π_u(i,j−1)] <= 2^{i+j−1}[Π_u(i,j)+Π_u(i,j)]`, using
`1+s(i,j−1) <= 1+s(i,j)`. `v` is symmetric. For `c`: each of the three terms of Theorem A is at most
`4^{i+j−1}Π_u(i,j)Π_v(i,j)` (by induction/the `u,v` bounds and monotonicity), and `3 <= 4`.
(b) From Theorem A, `u(t,j) >= u(t−1,j)s(t,j−1)` for `t,j >= 1`; iterate from `u(0,j) = 1`.
Similarly `v(i,t) >= v(i,t−1)s(i−1,t)`. The bound on `c` keeps only the cross term. ∎

**Theorem B (balanced case).** For `k >= 2`:
`2I(k−1)² − (2k−2)log(2k) <= log c(k,k) <= 2Ik² + 10k + 2`, and
`2k − log(2k+1) <= log s(k,k) <= 2k`. Consequently
`lim_k log c(k,k)/(log s(k,k))² = I/2 = 1 − 1/(4 ln 2)`, i.e. `c_ES = 1 − 1/(4 ln 2)`.

*Proof.* It is the case `i=j=k` of the general bounds
(U) `log c(i,j) <= Q(i,j) + 5(i+j) + 2` for `i,j >= 1`;
(L) `log c(i,j) >= Q(i−1,j−1) − (i+j−2)log(i+j)` for `i,j >= 2`.
(U): by Lemma 9(a) and Lemma 7, `log c <= 2(i+j) + Σ_{t<=i}(1 + h(t,j)) + Σ_{t<=j}(1 + h(i,t))`
(`log(1+s) <= 1+log s`), and Lemma 8 bounds the sums by `Q(i,j) + h(i+1,j) + h(i,j+1)`, with
`h(i+1,j), h(i,j+1) <= i+j+1`.
(L): by Lemma 9(b) and Lemma 7, `log c >= Σ_{t=1}^{i−1}[h(t,j−1) − log(t+j)] +
Σ_{t=1}^{j−1}[h(i−1,t) − log(i+t)]`; apply the lower half of Lemma 8 and `t+j, i+t <= i+j−1 < i+j`.
For `i=j=k`: `Q(k,k) = 2k²Φ(1) = 2Ik²`. `s(k,k) = C(2k,k)` with `h(k,k) = 2k` and Lemma 7.
Dividing, both bounds give `2Ik²(1+O(log k/k))/(4k²(1+O(log k/k)))` → `I/2`. ∎

*Computation (VERIFIED, `code/asym.py`, `out/asym.txt`):* exact big-integer evaluation; all
inequalities of Lemma 9 and (U),(L) hold for `0 <= i,j <= 45`; the Theorem B sandwich holds for all
`k <= 200`; the ratio is 0.6438 (k=40), 0.6405 (k=200), and (float, k=2000) 0.63952, decreasing
towards `0.639326`. This matches the scout's independent log-space values (0.6398 at m=640).

**Theorem C (upper bound for f).** For `n >= 3`,
`log f(n) <= (I/2)(log n + log(2 log n + 1) + 2)² + 10 log n + 13`; hence
`limsup log f(n)/(log n)² <= 1 − 1/(4 ln 2) < 1`.

*Proof.* Let `k` be least with `C(2k,k) >= n`; `n >= 3` forces `k >= 2`, and
`2^{2k−2}/(2k−1) <= C(2k−2,k−1) < n` (Lemma 7), so `k < log n + 1` and
`2k < log n + log(2k−1) + 2 <= log n + log(2 log n + 1) + 2`. Take `P ∈ 𝓔(k,k)` (Lemma 4: general
position) and any `n`-point `Q ⊆ P`. `Q` has no three collinear points, and each convex-position
subset of `Q` is one of `P`, so `f(n) <= c(k,k) + 1` (the `+1` is the empty set). By Theorem B,
`log f(n) <= 2Ik² + 10k + 3 = (I/2)(2k)² + 10k + 3`; insert the bounds on `2k` and `k`. ∎

## 4. Other aspect ratios and the 2^{k−2} set

**Theorem D.** If `i,j → ∞` with `i/j → ρ ∈ (0,∞)`, then
`log c(i,j)/(log s(i,j))² → γ(ρ) = N(ρ)/φ(ρ)²`.

*Proof.* By (U),(L), homogeneity and continuity of `Q`:
`Q(i,j) = j²Q(i/j,1) = j²(N(ρ)+o(1))` and `Q(i−1,j−1) = (j−1)²Q((i−1)/(j−1),1) = j²(N(ρ)+o(1))`;
the error terms are `O((i+j)log(i+j)) = o(j²)`. By Lemma 7,
`log s(i,j) = h(i,j) + O(log(i+j)) = j(φ(ρ)+o(1))`, and `φ(ρ) > 0`. ∎

**Lemma 10 (symmetry).** `φ(1/ρ) = φ(ρ)/ρ` and `γ(1/ρ) = γ(ρ)`.

*Proof.* `φ(1/ρ) = h(1/ρ,1) = h(1,ρ)/ρ = φ(ρ)/ρ`, and
`N(1/ρ) = Φ(1/ρ) + Φ(ρ)/ρ² = N(ρ)/ρ²`; divide. ∎

**Lemma 11 (monotonicity).** `N` and `φ` are strictly increasing on `(0,∞)`.

*Proof.* `φ' = log((1+x)/x) > 0`. `N(ρ) = Q(ρ,1) = ∫_0^ρ h(x,1)dx + ∫_0^1 h(ρ,y)dy`; the first term
has derivative `h(ρ,1) > 0`, the second is increasing since `h` is increasing in its first
argument. ∎

**Lemma 12 (large ρ).** For `ρ >= 20`, `γ(ρ) >= 1.1 > γ(1)`.

*Proof.* `N(ρ) >= Φ(ρ) >= ∫_1^ρ φ >= (ρ−1)φ(1) = 2(ρ−1)`, and
`φ(ρ) = log(1+ρ) + ρ log(1+1/ρ) <= log(1+ρ) + 1/ln 2`. So `γ(ρ) >= q(ρ) := 2(ρ−1)/(log(1+ρ)+1/ln 2)²`.
`q(20) = 38/(4.3923+1.4427)² = 1.116`. With `D(ρ) = log(1+ρ)+1/ln 2` (so `D' = 1/((1+ρ)ln 2)`
and `D >= 5.83` for `ρ >= 20`), `(ln q)' = 1/(ρ−1) − 2/((1+ρ) ln 2 · D) >= 1/(ρ−1) − 0.495/(1+ρ) > 0`
for `ρ >= 20`; so `q` increases on `[20,∞)` and `q >= 1.116`. ∎

**Lemma 13 (minimum at ρ=1; computer-assisted).** `γ(ρ) > γ(1)` for all `ρ ∈ (0,∞)∖{1}`.

*Proof.* By Lemma 10 assume `ρ > 1`; Lemma 12 covers `ρ >= 20`.
(i) `ρ ∈ [1.05, 20]`: by Lemma 11, on any `[a,b]`, `γ >= N(a)/φ(b)²`. `code/gamma_min.py` covers
`[1.05,20]` by 133 intervals on each of which the outward-rounded interval value of `N(a)/φ(b)²`
exceeds the interval upper bound of `γ(1)` (mpmath `iv`, 120-bit precision).
(ii) `ρ ∈ (1, 1.05)`: put `g(t) = γ(e^t)`. `g` is even (Lemma 10) and smooth, so `g'(0) = 0`. The
script evaluates the symbolic `g''` (sympy) in interval arithmetic on 400 subintervals covering
`[0, ln 1.05]` and gets `g'' >= 0.2779 > 0` throughout. Hence `g' > 0` and `g(t) > g(0)` on
`(0, ln 1.05]`. ∎

*(Computation VERIFIED: `out/gamma_min.txt` says `ALL OK`; `out/gamma.txt` also shows the float
table `γ(0.5)=0.7088, γ(0.8)=0.6463, γ(0.9)=0.6409, γ(1)=0.6393`, and a log-grid minimum at ρ=1.)*

**Corollary E.** Let `P_k` be a point set in general position with `|P_k| = 2^{k−2}` containing a
member of `𝓔(i_k,j_k)`, `i_k = ⌊(k−2)/2⌋`, `j_k = ⌈(k−2)/2⌉`. Then
`liminf log C(P_k)/(log|P_k|)² >= 1 − 1/(4 ln 2)`, where `C` counts convex subsets.

*Proof.* `C(P_k) >= c(i_k,j_k)` (convex position is intrinsic). By Theorem D with `ρ = 1`,
`log c(i_k,j_k) = (γ(1)+o(1))(log s(i_k,j_k))²`, and by Lemma 7
`log s(i_k,j_k) = k − 2 − O(log k) = log|P_k| − O(log k)`. ∎

## 5. What this does and does not show

Does show (rigorously, modulo the interval-arithmetic computation in Lemma 13 which is used only for
item 4):
- The exact recursion for the number of convex subsets of every realization of the ES sets
  `E(a,b)`, the value `c_ES = 1 − 1/(4 ln 2)` for `E(m,m)`, and the general-shape limit `γ(ρ)`.
- `limsup log₂ f(n)/(log₂ n)² <= 1 − 1/(4 ln 2) ≈ 0.6393`, improving the recorded upper constant 1
  (Erdős 1978/1981 crude count `Σ_{j<k}C(n,j)`, as also restated on the forum and Plasma page).
  Current recorded window becomes `1/4 <= liminf <= limsup <= 0.6393`.
- Within the ES family `𝓔(i,j)`, no aspect ratio does better; sets containing a balanced ES block of
  size `n^{1−o(1)}` (in particular, if the classical `2^{k−2}` set is such, that set) do no better.

Does not show:
- Existence of `lim log f(n)/(log n)²` (part of the question) — still open.
- Any improvement of the lower constant `1/4`.
- That ES-type sets are near-optimal for `f(n)`; other constructions (e.g. Horton-type, or
  different "far" placements of non-ES blocks) could have fewer convex subsets. A natural next step
  is to reoptimize the recursive construction itself: in `P = L∪R` with (P1),(P2), crossing convex
  sets number `u(L)v(R)` for *any* blocks, so one may choose block sizes/shapes to minimize `c`
  subject to `|P| = n` — the ES choice `L = 𝓔(i−1,j)`, `R = 𝓔(i,j−1)` was not shown optimal.
- The structure of the classical `2^{k−2}`-point set (used only as a hypothesis in Corollary E) was
  recalled, not read in a source here.
- Novelty: only a short literature search was done (below). It is plausible this computation is
  known to experts or appears somewhere not indexed by keyword.

## 6. Sources read / checked

- erdosproblems.com/838 and forum thread 838 (fetched 2026-11-23; `refs/page838.html`,
  `refs/forum838.html`): statement; comments by nsingh (lower 1/8) and Zeraoulia Rafik
  (`1/4 <= liminf <= limsup <= 1`, base 2), "standard check believed this to be correct" (N. Sothanaphan).
- Erdős, *Some more problems on elementary geometry*, Austral. Math. Soc. Gaz. 5 (1978) 52–54
  (`refs/er78c.pdf`, OCR in `refs/er78c_ocr.txt`): the upper bound of (2) is the crude count over a
  set with no large convex subset; no finer count of convex subsets of the ES set.
- Plasma AI pages (`refs/plasma_*.md`): E0838 index; research page `convex_subsets.md` (upper
  constant 1, "next test is a construction controlling all convex sizes"); library page for Erdős
  1981 display (4) (`n^{(1+o(1))log n/log 2}`).
- formal-conjectures `FormalConjectures/ErdosProblems/838.lean` (origin/main): parts i, ii open; counts
  empty set, singletons, pairs.
- ryantuck/erdos-ai: only formalization reviews for 838 (`refs/rt_*.md`), no mathematics.
- arXiv API keyword searches ("number of convex subsets", "convex subsets" + "general position",
  "number of convex polygons", "Erdos and Hammer", "Erdos-Szekeres" + "number of convex") and
  OpenAlex searches: nothing on counting all convex subsets of ES sets or improving the constant.

## 7. Sources not read

- Erdős 1981 (Szeged proceedings) original pages — only Plasma's account of display (4) was read.
- Erdős–Szekeres 1935/1961 original papers and the Morris–Soifer survey (structure of the
  `2^{k−2}` set taken from memory, flagged in Corollary E).
- Suk 2017; Holmsen–Mojarrad–Pach–Tardos 2020 (only relevant for the lower bound; not used).
- Literature on counting convex polygons/holes in specific point sets (Valtr, Pór–Valtr, Bárány,
  Aichholzer et al.), Google Scholar / MathSciNet searches — not done.

## 8. Reproduce

    cd attack/838/t1/prove
    python3 -I code/brute.py      > out/brute.txt      # ~2 min; brute force vs recursion
    python3 -I code/asym.py 200   > out/asym.txt       # ~1 min; exact bounds + ratio tables
    python3 -I code/gamma.py      > out/gamma.txt      # gamma(rho) table, closed form check
    python3 -I code/gamma_min.py  > out/gamma_min.txt  # interval-arithmetic proof of Lemma 13

(Python 3.11, sympy 1.14, mpmath 1.3.)
