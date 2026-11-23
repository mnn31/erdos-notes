# Erdős 675(a), angle 2: trying to DISPROVE the translation property for sums of two squares

Date: 2026-11-23. Folder: `grh2/675/existence/angle2/`. Nothing here was committed, pushed or posted.

## Outcome in one paragraph

The disproof attempt fails, and the reasons can be stated precisely. (1) There is **no local obstruction**:
for every n and every finite set of primes, t = (product of large prime powers) meets every local condition
(Lemma A). (2) Any disproof would also **refute Dickson's prime k-tuples conjecture**, because Dickson's
conjecture implies that E has the translation property (Theorem F, proved in full below). (3) Exact computation
finds the least n-shift t_n for **every n <= 52**, and t_53 > 10^16. log t_n grows roughly linearly in n
(about 0.7 n), which fits the heuristic expectation t_n = exp(n^{1+o(1)}). The data show no sign that shifts stop
existing. (4) An explicit polynomial family gives infinitely many n-shifts for n <= 7 (Lemma G). Unconditional
existence for all n is still open, and so is question (a).

## Exact statements established (all rigorous unless marked)

Notation. E = { m >= 1 : m = x^2 + y^2, x, y in Z }. For n >= 1, t >= 1 is an **n-shift** if, for all 1 <= a <= n,
a in E iff a + t in E. S_n = E ∩ [1, n]. "q" always denotes a prime q ≡ 3 (mod 4). oddpart(m) = m / 2^{v_2(m)}.

**Theorem (this note).**
1. (No local obstruction; Lemma A.) For every n >= 1 and every finite set P of primes, every positive multiple t of
   M_P = ∏_{p in P} p^{e_p} (where p^{e_p} > n) satisfies v_p(a + t) = v_p(a) for all p in P and all 1 <= a <= n.
   In particular, for every y, t is an n-shift for the truncated set E_y = { m >= 1 : v_q(m) even for all q <= y }.
2. (Dickson implies (a); Theorem F.) If Dickson's conjecture holds, then for every n there are infinitely many
   n-shifts, and these include t = M_n s with M_n = 4 ∏_{p <= n} p^{e_p}. Hence E has the translation property.
   Contrapositive: a disproof of 675(a) would disprove Dickson's conjecture.
3. (Computation; Lemmas C1, C2.) The least n-shifts are as listed in Table 1 for every 1 <= n <= 52, and t_53 > 10^16.
   In particular E has the n-translation property for every n <= 52.
4. (Polynomial family; Lemma G.) For every integer v ≡ 0 (mod 21), v >= 21, t(v) = 4v^2(v^2 - 1) is a 7-shift.
   So there are infinitely many n-shifts for every n <= 7.

**Outcome label: PARTIAL.** These are weaker rigorous results. Question (a) is neither proved nor disproved.

## Prior work checked (to avoid redoing it)

VERIFIED (read 2026-11-23, saved in `refs/`):
- `refs/page675.html(.txt)` and `refs/forum675.html(.txt)`: the problem page and its 7 forum comments. The only
  post about part (a) is Liu's (09 May 2026), giving a lower bound t > exp(n^c) for c < 1/10. Liu says explicitly
  that he does not address existence. The other posts concern part (c), the squarefree case (Ho Boon Suan, an
  improvement by "aditya", Tao's and Sothanaphan's checks), plus a typo report. Nobody discusses existence for E
  or a possible disproof.
- Liu's note (`../../refs/erdos675a.txt`, read in full). Remark 3: "We do not prove part (a)". Its Lemmas 6-7 are
  divisibility constraints only.
- `../../PROOF.md`. It strengthens the lower bound to c < 1/2, unconditionally. Its "What this does and does not
  show" says existence stays open.
- OEIS: searches for `1,3,3,16,48,48,48,96,2304` and `3,16,48,96,2304,40320,173376` return "No results"
  (`refs/oeis_search1.txt`, `refs/oeis_search2.txt`). So the sequence t_n below does not appear to be recorded in OEIS.

## Lemmas and proofs

Classical inputs (cited, not re-proved): **(Fermat–Euler)** m >= 1 is in E iff v_q(m) is even for every prime
q ≡ 3 (mod 4). **(Brahmagupta)** E is closed under multiplication. The direction "m in E implies v_q(m) even" is
re-proved in `../../PROOF.md` Lemma 1, by descent.

**Lemma A (no local obstruction).** Let n >= 1, let P be a finite set of primes, and for p in P let e_p be the
least integer with p^{e_p} > n. If M_P | t, then v_p(a + t) = v_p(a) for every p in P and every 1 <= a <= n.
Consequently:
(i) for every y, every positive multiple of M_y := ∏_{q <= y} q^{e_q} is an n-shift for E_y;
(ii) if 2 in P and 2^{e_2} > 4n, then also oddpart(a + t) ≡ oddpart(a) (mod 4) for all a <= n.

Proof. Since 1 <= a <= n < p^{e_p}, we have v_p(a) < e_p <= v_p(t), so v_p(a + t) = v_p(a) (ultrametric
inequality). For (i): membership in E_y depends only on the v_q with q <= y, and these are unchanged. For (ii):
write a = 2^k a', so k = v_2(a). Then 2^k <= n, so 2^{k+2} <= 4n < 2^{e_2}, and 2^{k+2} | t. Hence
a + t = 2^k (a' + t/2^k) with t/2^k ≡ 0 (mod 4). ∎

Remark A'. t = 0 satisfies every condition in the definition of an n-shift. Lemma A shows that t can be made
p-adically as close to 0 as we like, at any finite set of primes at once, while staying >= 1. So no obstruction
that is local at finitely many primes (congruences, p-adic or 2-adic parity conditions) can rule out n-shifts.
Also, t is an n-shift for E iff it is an n-shift for E_y with y = n + t, because E ∩ [1, n+t] = E_y ∩ [1, n+t].
So the true set of n-shifts is { t : t in T_{n, n+t} }, where T_{n,y} is the set of n-shifts for E_y. Each
T_{n,y} contains the multiples of M_y and so has positive density. The intersection is a sieve problem with
infinitely many primes and no finite-level obstruction.

**Lemma B (density zero).** For every n >= 1 the set of n-shifts has upper density 0. So existence cannot come
from a positive-density argument.

Proof. 1 is in S_n, so every n-shift t has t + 1 in E, hence v_q(t + 1) is even for every q (Fermat–Euler,
easy direction). Fix y and J. The set of t with v_q(t+1) not in {1, 3, ..., 2J-1} for all q <= y is periodic
modulo ∏_{q <= y} q^{2J}. By CRT its density is ∏_{q <= y} (1 - Σ_{j odd < 2J} (q^{-j} - q^{-j-1})). As J -> ∞
this tends to ∏_{q <= y} q/(q+1). Since Σ_{q ≡ 3 (4)} 1/q diverges (`../../PROOF.md` Lemma 6), the product tends to
0 as y -> ∞. ∎

**Lemma C1 (necessary conditions used to prune the search).** If t is an n-shift and a is in S_n, then
(i) v_q(a + t) is even for every prime q ≡ 3 (mod 4), and (ii) oddpart(a + t) ≡ 1 (mod 4).

Proof. a + t is in E. Part (i) is the easy direction of Fermat–Euler. For (ii): by (i), oddpart(a+t) is a product of
primes ≡ 1 (mod 4) times even powers of primes ≡ 3 (mod 4), and each such factor is ≡ 1 (mod 4). ∎

**Lemma C2 (the search is exhaustive).** `code/lshift.c` scans t in increasing order. It discards t only when
t mod 2^{e2} 3^{e3} 7^{e7} 11^{e11} violates C1 (i) or (ii) **on residues where the valuation is determined**, or
when some a in S_n and some prime q ≡ 3 (mod 4), 19 <= q <= 3000, have q || a + t. Both rules are necessary
conditions by C1, so no n-shift is ever discarded. Every surviving t is then tested exactly for all a <= 80 with
`isE`. `isE` implements Fermat–Euler: trial division up to the cube root of the cofactor; the cofactor then has
at most two prime factors, decided by Miller–Rabin (deterministic bases for 64 bits), a perfect-square test, the
residue mod 4, and Pollard rho if needed.

Independent cross-checks:
- `code/brute.c` builds E by enumerating x^2 + y^2. It does no factoring and uses no wheel. It recomputes
  t_1..t_36 for all t <= 10^9, and the values agree exactly (`out/brute_1e9.txt`).
- `code/verify_shifts.py` recomputes L(t) = the largest n for which t is an n-shift, for every record t, using
  `sympy.factorint` (`out/verify_shifts.txt`). It agrees with `lshift` in every case.

**Table 1 (least n-shifts t_n; VERIFIED by computation).** t_n is nondecreasing, so the table lists only the jumps:

| n | t_n | factorisation | L(t_n), and first failure a |
|---|---|---|---|
| 1 | 1 | 1 | 1 (a=2) |
| 2-3 | 3 | 3 | 3 (a=4) |
| 4 | 16 | 2^4 | 4 (a=5) |
| 5-7 | 48 | 2^4·3 | 7 (a=8) |
| 8 | 96 | 2^5·3 | 8 (a=9) |
| 9-12 | 2304 | 2^8·3^2 | 12 (a=13) |
| 13-16 | 40320 | 2^7·3^2·5·7 | 16 (a=17) |
| 17 | 173376 | 2^6·3^2·7·43 | 17 (a=18) |
| 18-24 | 1761984 | 2^6·3^2·7·19·23 | 24 (a=25) |
| 25-31 | 10269504 | 2^6·3^4·7·283 | 31 (a=32) |
| 32-36 | 755048448 | 2^13·3^2·7^2·11·19 | 36 (a=37) |
| 37-39 | 87196919040 | 2^8·3^3·5·7^2·11·31·151 | 39 (a=40) |
| 40 | 159488372736 | 2^12·3^5·7·11·2081 | 40 (a=41) |
| 41-44 | 3993737134464 | 2^7·3^2·7·11·17·31·37·2309 | 44 (a=45) |
| 45-48 | 34647247514880 | 2^8·3^4·5·7·11·13·47·7103 | 48 (a=49) |
| 49-51 | 2312113913214336 | 2^7·3^3·7^2·11·1241214179 | 51 (a=52) |
| 52 | 7504125968199168 | 2^9·3^3·7^2·11·19^2·31^2·2903 | 52 (a=53) |
| 53 | > 10^16 | (none found in [1, 10^16]) | — |

The values for n <= 31 match `../../PROOF.md`. Every listed failure is of the form "a in E, a + t not in E".
3 | t_n for n >= 5, 7 | t_n for n >= 13, and 11 | t_n for n >= 32. These are all consistent with the
divisibility lemmas in PROOF.md (which give sufficient thresholds only).

**Theorem F (Dickson's conjecture implies 675(a)).**
Dickson's conjecture: if f_i(s) = b_i + c_i s (1 <= i <= k, c_i >= 1) and for every prime p some s has
p ∤ ∏ f_i(s), then infinitely many s >= 1 make every f_i(s) prime.

Claim: under it, for every n >= 1 there are infinitely many n-shifts.

Proof. For each prime p <= n let e_p be least with p^{e_p} > n, and put M = 4 ∏_{p <= n} p^{e_p}. For a in S_n,
v_p(a) < e_p for all p <= n, so M/a is an integer divisible by every prime p <= n, and by 8.
Put f_a(s) = 1 + (M/a) s for a in S_n.
Admissibility: for p <= n we have p | M/a, so f_a(s) ≡ 1 (mod p). For p > n we have p ∤ M/a, so f_a vanishes mod p
on exactly one class, and the k = |S_n| <= n < p forms remove at most k < p classes.
Dickson then gives infinitely many s >= 1 with every f_a(s) prime. Fix one and set t = Ms >= 1.
(1) a in S_n: a + t = a · f_a(s), and f_a(s) is a prime ≡ 1 (mod 4) because 4 | M/a. So f_a(s) is in E (Fermat), and
a + t is in E (Brahmagupta).
(2) 1 <= a <= n, a not in E: by Fermat–Euler some q ≡ 3 (mod 4) has v_q(a) odd. Then q <= n, and by Lemma A
v_q(a + t) = v_q(a) is odd, so a + t is not in E.
So t is an n-shift. Different s give different t. ∎

Remark F'. The proof uses only that every f_a(s) is in E, not that it is prime. So the translation property
follows from the weaker "E-tuples" statement: for every admissible finite family of linear forms in ONE variable,
some s puts all values in E. By Lemma E below, that is again a sieve statement about the 3-mod-4 primes.

**Lemma E (mod-4 parity).** Let m be odd with m ≡ 1 (mod 4), and suppose every prime factor q ≡ 3 (mod 4) of m
satisfies q > sqrt(m). Then m is in E.

Proof. Two such factors, counted with multiplicity, would multiply to more than m, so there is at most one.
Primes ≡ 1 (mod 4) contribute 1 mod 4, so m ≡ (-1)^{(number of 3-mod-4 factors)} (mod 4). Since m ≡ 1, that number
is even, hence 0. Fermat–Euler then gives m in E. ∎
So the n-shift problem along t = Ms reduces to this: find s for which none of the |S_n| forms f_a(s) has a prime
factor q ≡ 3 (mod 4) with q <= f_a(s)^{1/2}. That is a sieve of dimension |S_n|/2 run up to the square root.

**Lemma G (infinitely many 7-shifts).** Let t = 4v^2(v^2 - 1) with v ≡ 0 (mod 21) and v >= 21. Then t is a
7-shift.

Proof. The following are identities in Z[v]:
t+1 = (2v^2-1)^2, t+2 = (2v^2-1)^2 + 1, t+4 = (2-2v^2)^2 + (2v)^2, t+5 = (2v^2-1)^2 + 2^2.
These values are >= 1, so they lie in E. Next, 3 | v gives 9 | t, so v_3(t+3) = v_3(t+6) = 1, which is odd.
And 7 | v gives 49 | t, so v_7(t+7) = 1. So t+3, t+6, t+7 are not in E. Finally 1, 2, 4, 5 are in E and 3, 6, 7
are not, and t >= 1. ∎
`code/family7.py` checks the identities symbolically. It also confirms numerically that L(t(21k)) >= 7 for
k <= 300, with values 7, 8 and 12 occurring (`out/family7.txt`).

## INFERRED (heuristic or from memory; not proved here)

- **Size of t_n.** A Hardy–Littlewood-type model predicts #{n-shifts <= X} ≈ 𝔖_n X (log X)^{-|S_n|/2}, with
  𝔖_n > 0 (Lemma A gives positive local factors, and for q > n the factor is about 1 - |S_n|/(q+1) > 0). Setting
  this count to 1 gives log t_n ≈ (|S_n|/2) log log t_n, which means t_n = exp(n^{1+o(1)}). The data in Table 1 give
  ln t_n / n ≈ 0.70 at n = 52 (ln t_52 ≈ 36.55), and the ratio rises slowly, consistent with this model.
  At n = 49 the model's crude count gives log X ≈ 39, against the actual 35.4.
- **Sieve limits.** The reduction in Lemma E needs a lower-bound sieve of dimension κ = |S_n|/2 run up to
  x^{1/2}. From memory (not re-read): the sifting limit β_κ exceeds 2 for κ > 1, so the standard
  (Diamond–Halberstam–Richert / Iwaniec) sieves reach only x^{1/β_κ} < x^{1/2} once |S_n| >= 3. Unconditional
  existence of one-variable k-tuples in E for k >= 3 is, to my knowledge, not known in general, and here k ~ n/sqrt(log n) -> ∞.
- **Two variables do not help.** Finite-complexity results (from memory: Matthiesen on linear correlations of
  sums-of-two-squares representation functions; Harpaz–Skorobogatov–Wittenberg via Green–Tao–Ziegler) would give
  (λ, μ) with λ + aμ in E for all a in S_n. The translation problem needs μ = 1, which brings back a single
  variable, i.e. infinite complexity.
- **Polynomial families.** From memory: Stein's theorem says a non-composite polynomial T in several variables has
  T + a reducible for fewer than deg T values of a. So multivariable polynomial families reduce to one-variable
  ones. A probe over P = A v^2 + B v + C (|coefficients| small) found that P^2 + m is a polynomial norm only for
  m a square plus at most two extra values in 0..40 (`code/polyfam_probe.py`, `out/polyfam_probe.txt`; top 15
  of the 250 polynomials tried are listed). Its norm test does not check the leading coefficient's class carefully, so it is exploratory only. This fits the expectation that a fixed polynomial covers only a thin set of offsets, so any polynomial
  approach would need families that change with n.

## Where each route breaks (the "gap")

1. **Local / congruence obstruction (disproof):** impossible, by Lemma A. Every finite set of local conditions is
   met by the multiples of M_P.
2. **Forced divisibility (Liu / PROOF.md style), pushed to a contradiction (disproof):** every constraint comes from
   a <= n, so it fixes t modulo an n-dependent modulus. Lemma A shows that all such constraints are met at once by
   multiples of M_P. Such arguments give lower bounds on t (now exp(n^{1/2-ε})) and can never give a contradiction.
3. **Density / upper-bound sieve (disproof):** these give #{t <= X} ≪_n X (log X)^{-|S_n|/2}, which is an upper
   bound and never zero. Lemma B shows the set has density 0 anyway. Proving the set empty would need a global
   argument that uses t >= 1 (t = 0 satisfies everything). By Theorem F, such an argument would also refute
   Dickson's conjecture.
4. **Numerics (disproof):** n-shifts exist for every n <= 52, and the growth of t_n matches the heuristic that
   they exist for all n. Nothing suggests a breakdown. Exact search past n = 52 is limited by t_53 > 10^16.
5. **Existence, unconditionally:** this needs one-variable |S_n|-tuples in E with |S_n| -> ∞, beyond the reach of
   sieve methods (INFERRED above). Polynomial identities work only up to n = 7 here (Lemma G). Two-variable
   (finite-complexity) results do not apply because the shift has coefficient 1.

## What this does and does not show

- Does show: no local or congruence obstruction exists. 675(a) holds if Dickson's conjecture holds. The exact least
  shifts are known for n <= 52 (so the n-translation property holds for n <= 52), and t_53 > 10^16. There are
  infinitely many n-shifts for n <= 7.
- Does NOT show: that E has the translation property, or that it fails. Theorem F is conditional. The minimality in
  Table 1 relies on the correctness of `lshift.c`. That program was cross-checked by an independent brute force up
  to 10^9 (n <= 36), and every reported t was re-verified with sympy. Minimality for 37 <= n <= 52, and the bound
  t_53 > 10^16, rest on `lshift.c` alone, whose pruning uses only the necessary conditions of Lemma C1.
- Novelty: Theorem F and Table 1 were not found on the forum, in Liu's note or in OEIS. Theorem F is a short
  argument and is quite possibly folklore. Novelty is "not found in these places", not "new".
- Lean: `erdos_675.parts.i` in formal-conjectures (per PROOF.md) states only the existence claim. Nothing here
  proves or refutes it.

## Reproduce

All commands are run from `grh2/675/existence/angle2/`. clang -O3 on macOS; Python 3.11 with sympy 1.14.
```
clang -O3 -march=native -o code/lshift code/lshift.c -lm
clang -O3 -o code/brute code/brute.c
code/brute 1000000000 > out/brute_1e9.txt                                   # ~20 s
code/lshift 80 100000000000000 3000 1 1 > out/lshift_upto_1e14.txt 2> out/lshift_upto_1e14.err   # ~1 min
code/run_segments.sh 49 100000000000001 10000000000000000 10 out/seg       # 10 parallel jobs, ~12 min wall
python3 -I code/combine_segments.py > out/least_shifts_table.txt
python3 -I code/verify_shifts.py   > out/verify_shifts.txt
python3 -I code/family7.py         > out/family7.txt
python3 -I code/polyfam_probe.py > out/polyfam_probe.txt                     # exploratory, a few minutes
```
`lshift NMAX XMAX Q0 NSTART TSTART` prints the least n-shift >= TSTART for each n >= NSTART, up to XMAX.

## Sources not read

- Dickson (1904) on simultaneous primes in linear forms: the conjecture is stated here in its standard form; the
  original was not read.
- Stein (1989) / Lorenzini on reducible fibres; Matthiesen (sums of two squares in linear forms);
  Harpaz–Skorobogatov–Wittenberg (2014); Hooley and Indlekofer on consecutive sums of two squares;
  Iwaniec and Diamond–Halberstam–Richert on sieve limits. All are used only in the INFERRED section.
- Ho Boon Suan's squarefree note: not read, and not load-bearing.
- arXiv was not searched for "k-tuples of sums of two squares" or "translation property". A known unconditional
  result there would bear on route 5.
- The proof-claims tab and history pages were not re-fetched; per `../../PROOF.md` the only claim concerns part (b).
