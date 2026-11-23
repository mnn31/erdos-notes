# Erdős #30, lead 2 (Sidon-adjacent): Ding's residue-class and weighted sums for every n, under RH

Written 22 Nov 2026. Verdict: **the lead survives as stated.** Every step is either proved here or cited by theorem number, and for each citation I checked the source text and its hypotheses. Two caveats. It is a short consequence of known conditional remarks (see "Credit"). It is not a result about #30's actual question.

## Final statement

Notation. S_n (= h(n) on erdosproblems.com and in the Lean file) is the largest size of a Sidon subset of [1,n] = {1,...,n}. "Sidon" means all sums a+b, taken over unordered pairs with a = b allowed, are distinct.

**Theorem (RH).** Assume the Riemann Hypothesis for ζ. Fix integers m ≥ 1, 0 ≤ r < m and s, l ≥ 0. Let n ≥ 3, and let S = {a_1 < ... < a_t} ⊂ [1,n] be a Sidon set with t = S_n, meaning maximum cardinality, not just inclusion-maximal. Then

  Σ_{1≤i≤t, a_i ≡ r (mod m)} i^s a_i^l = n^{l+(s+1)/2} / (m(s+l+1)) + O_{s,l,m}( n^{l+s/2+3/8} (log n)^{3/2} ).

Special case s = 0, l = 1:

  Σ_{a∈S, a≡r (mod m)} a = n^{3/2}/(2m) + O_m( n^{11/8} (log n)^{3/2} )   for every n ≥ 3.

- Hypothesis used: **RH** for ζ only. The argument uses no Dirichlet L-function and no other L-function, so "GRH for Dirichlet L-functions" is not needed beyond its ζ case.
- If the Alpöge Lean theorem for RH (as described in the brief, Mathlib's `RiemannHypothesis`) is accepted, the Theorem is **unconditional**. I did not check that Lean development myself. The brief reports it as certified.
- Comparison with what is known without RH (Ding, arXiv:2606.15041v2):
  - Corollary 5 gives error O(n^{l+s/2+61/160} log n) for all n. For s = 0, l = 1 that is O(n^{221/160} log n).
  - Theorem 6 gives O(n^{l+s/2+3/8} log n), but only outside an exceptional set of O(N^{4/5+ε}) integers n ≤ N.
  - Under RH the exponent of Theorem 6 holds for **every** n ≥ 3. The cost is a factor (log n)^{1/2}.

## Lemmas

### Lemma 1 (Bose set; proved here)
For every prime p there is a Sidon set A ⊂ [1, p^2−1] with |A| = p. Hence S_n ≥ p whenever p^2 − 1 ≤ n.

Proof.
- Let θ generate the cyclic group F_{p^2}^×, which has order p^2−1. Then θ ∉ F_p, because every element of F_p^× has order dividing p−1 < p^2−1.
- Put A = {a ∈ [1, p^2−1] : θ^a − θ ∈ F_p}.
- Size of A. The map a ↦ θ^a is a bijection from [1,p^2−1] to F_{p^2}^×. For each x ∈ F_p we have θ + x ≠ 0, since otherwise θ = −x ∈ F_p. So each θ + x equals θ^a for exactly one a ∈ [1,p^2−1]. Hence |A| = p.
- Sidon property. Suppose a+b = c+d with a,b,c,d ∈ A. Write θ^a = θ+x, θ^b = θ+y, θ^c = θ+u, θ^d = θ+v with x,y,u,v ∈ F_p. Then (θ+x)(θ+y) = (θ+u)(θ+v), so (x+y−u−v)θ + (xy−uv) = 0.
- If x+y ≠ u+v, then θ ∈ F_p, a contradiction. So x+y = u+v, and then xy = uv.
- So x,y and u,v are the roots, with multiplicity, of the same monic quadratic over the field F_p. Hence {x,y} = {u,v} as multisets.
- Since x determines a uniquely in [1,p^2−1], we get {a,b} = {c,d}. ∎

(This is Bose's construction. Balasubramanian–Dutta, arXiv:2409.01986v4, Theorem B, state the same fact. Ding's Lemma 10 proof uses it as "Singer's construction gives S_n ≥ p_j" for p_j^2 − 1 ≤ n.) Numerically checked: for all primes p ≤ 40 the set has size p, lies in [1,p^2−1] and is Sidon (`check_numeric.py`).

### Lemma 2 (upper bound; cited)
For every N ≥ 1, S_N ≤ N^{1/2} + N^{1/4} + 1. A weaker form, S_N ≤ N^{1/2} + O(N^{1/4}), is all we use.

Sources and what I checked:
- **Read:** Ortega–Prendiville, JTNB 35 (2023), eq. (1.1) with its proof in Appendix A. For S inside an interval of length N they show |S| ≤ N^{1/2} + H N^{−1/2} + N H^{−1} + 1 and take H ≈ N^{3/4}. That gives N^{1/2} + O(N^{1/4}) for all N, with no extra hypotheses.
- **Read as secondary statements only:** the constant-1 form is attributed to Erdős–Turán/Lindström [Li69] on erdosproblems.com/30, in O'Bryant's survey §4.1, and as `erdos_30.variants.lindstrom` (a statement with `sorry`) in formal-conjectures. I did not read Lindström 1969 itself.

### Lemma 3 (RH prime in a short interval; cited)
Assume RH. For every real x ≥ 2 there is a prime in (x − (4/π)√x log x, x].

- Source: Dudek, arXiv:1402.6417v2, Theorem 2. Read: the hypothesis is RH for ζ.
- What the proof uses (read §2.1): the Riemann–von Mangoldt explicit formula for ψ, summed over the nontrivial zeros of ζ only.
- Independent corroboration (read): Carneiro–Milinovich–Soundararajan, arXiv:1708.04122v2, Theorem 5. Under RH, for x ≥ 4 there is a prime in [x, x + (22/25)√x log x]. The same paper's intro says this gives p_{n+1} − p_n ≤ (22/25)√p_n log p_n for p_n > 3.
- Classical form: Cramér 1920, p_{n+1} − p_n = O(√p_n log p_n). I know it only through Dudek's restatement (his Theorem 1) and did not read Cramér.
- Numeric sanity check (not a proof): for consecutive primes below 10^7, the ratio (p_{k+1} − p_k)/((4/π)√p_{k+1} log p_{k+1}) is at most 0.437.

### Lemma 4 (RH: maximal Sidon size within n^{1/4} log n)
Assume RH. For every n ≥ 3:
- −(2/π)(n+1)^{1/4} log(n+1) < S_n − √n ≤ n^{1/4} + 1;
- hence |1 − S_n/√n| ≤ C n^{−1/4} log n with an absolute constant C;
- and S_n ≤ 3√n.

Proof.
- Put y = √(n+1) ≥ 2. By Lemma 3 there is a prime p with y − (4/π)√y log y < p ≤ y.
- Then p^2 ≤ n+1, so p^2 − 1 ≤ n, and Lemma 1 gives S_n ≥ p.
- Since √y log y = (n+1)^{1/4} · ½ log(n+1), we get S_n ≥ p > √(n+1) − (2/π)(n+1)^{1/4} log(n+1) ≥ √n − (2/π)(n+1)^{1/4} log(n+1).
- The upper side is Lemma 2.
- For n ≥ 3, both (n+1)^{1/4} log(n+1) and n^{1/4} + 1 are ≪ n^{1/4} log n. Dividing by √n gives the second claim.
- Finally, n^{1/4} + 1 ≤ 2√n for n ≥ 1, so S_n ≤ 3√n. ∎

Numeric sanity check: for all n < 10^{12}, taking p = the largest prime with p^2 ≤ n+1, the quantity √n − p is at most 0.41 · (2/π)(n+1)^{1/4} log(n+1). The worst case of each prime interval was checked.

(Lemma 4 also gives the two-sided h(N) = √N + O(N^{1/4} log N) under RH. That is Lead A in ../SCREEN.md and is not this lead.)

### Lemma 5 (Fourier uniformity; cited)
For every Sidon set S ⊂ [1,N]:

  ‖1̂_S − (|S|/N) 1̂_{[N]}‖_∞ ≪ N^{1/2} ( |1 − |S|/N^{1/2}| + N^{−1/4} )^{1/2}.

Here f̂(α) = Σ f(x) e(αx) and [N] = {1,...,N}.

- Source: Ortega–Prendiville, "Extremal Sidon sets are Fourier uniform…", J. Théor. Nombres Bordeaux 35 (2023) 115–134, doi:10.5802/jtnb.1239, **Theorem 6.3, eq. (6.1)**.
- The only hypothesis is "S ⊂ [N] a Sidon set". Their Definition 1.1 and the definition [N] := {1,...,N} match Ding's conventions.
- I checked the absolute-value bars by viewing the rendered PDF page (journal p. 128). This settles the screener's least-trusted step: the bars are present in O-P (6.1) and also in Ding (1.2) and (2.1), checked on the rendered pages of arXiv:2606.15041v2.
- The proof of Theorem 6.3 in O-P is given as a modification of their Theorem 1.2 that uses Cilleruelo's Theorem 6.1. I cite it as a refereed published theorem and did not re-derive it.

### Lemma 6 (L^1 bound for progressions; cited)
For every arithmetic progression P ⊂ [1,n], ∫_T |1̂_P(α)| dα ≪ log(2n).

- Source: Ortega–Prendiville, Lemma 3.2, which gives ≪ log|P| for every arithmetic progression P ⊂ Z. I read the statement and the full proof: the pointwise bound min(|P|, 1/‖α‖) plus a dyadic decomposition.
- Use |P| ≤ n. The case |P| ≤ 1 is trivial (the integral is at most 1). This is Ding's Lemma 8.

### Lemma 7 (Ding's Theorem 4; cited, proof re-checked line by line)
Let m ≥ 1, 0 ≤ r < m and s,l ≥ 0 be fixed integers. Let S = {a_1<…<a_t} ⊂ [1,n] be **any** Sidon set, and put Φ = Φ(S,n) := n^{1/2}(|1 − t/n^{1/2}| + n^{−1/4})^{1/2}. Then

  Σ_{i: a_i≡r (m)} i^s a_i^l = t^{s+1} n^l/(m(s+l+1)) + O_{s,l,m}( t^s n^l Φ log(2n) ).

This is Ding, arXiv:2606.15041v2, Theorem 4, eq. (1.7). Its only hypothesis is that S ⊂ [1,n] is Sidon; no size condition is needed. I re-checked the proof:

- **Lemma 9** (discrepancy on progressions: |S∩P| = (t/n)|P| + O(Φ log 2n)) follows from Parseval/orthogonality for finitely supported functions, together with Lemma 5 (sup-norm) and Lemma 6 (L^1 norm). Correct.
- **Theorem 1** (power sums over S∩P) follows by Abel summation. The error is at most E(n^l + Σ_{k<n}((k+1)^l − k^l)) ≤ 2n^l E. Correct.
- **Rank of a_i.** i = |S∩[1,a_i]| = (t/n)a_i + O(E), by Lemma 9 applied to the interval [1,a_i]. With y_i = t a_i/n, both i and y_i lie in [0,t], so |i^s − y_i^s| ≤ s t^{s−1}|i − y_i|. Summing over at most t indices gives error t^s n^l E. Correct.
- **Back to the progression.** Apply Theorem 1 with exponent s+l, then multiply by t^s/n^s. The error is t^s n^l E. Correct.
- **(2.9)**, sums of powers in a residue class: Σ_{a≤n, a≡r(m)} a^k = n^{k+1}/(m(k+1)) + O_{k,m}(n^k). This holds because for increasing f, f(a) ≤ (1/m)∫_a^{a+m} f ≤ f(a+m), so the sum is (1/m)∫_0^n x^k dx up to O(m·n^k + (n+m)^{k+1} − n^{k+1}).
- **The leftover error** after multiplying (2.9) by t^{s+1}/n^{s+1} is O(t^{s+1}n^{l−1}) ≤ O(t^s n^l). This is absorbed because Φ ≥ n^{3/8} ≥ 1 and t ≤ n. Correct.

Numeric sanity check (not a proof): on Bose sets with p ∈ (20,400) and n = p^2−1, for (s,l,m,r) ∈ {(0,1,3,1), (1,1,4,2), (0,2,5,0), (2,0,3,2)}, the ratio |LHS − main| / (t^s n^l Φ log 2n) is at most 0.022.

## Proof of the Theorem
Assume RH, let n ≥ 3, and let t = S_n.

1. By Lemma 4, |1 − t/√n| ≤ C n^{−1/4} log n. So Φ ≤ n^{1/2}((C+1) n^{−1/4} log n)^{1/2} ≪ n^{3/8}(log n)^{1/2}.
2. By Lemma 7, using t ≤ 3√n (Lemma 4) and log(2n) ≤ 2 log n for n ≥ 2:
   Σ_{a_i≡r} i^s a_i^l = t^{s+1} n^l/(m(s+l+1)) + O_{s,l,m}( n^{s/2} n^l n^{3/8}(log n)^{1/2} log n ).
3. Main-term replacement. By the identity t^{s+1} − n^{(s+1)/2} = (t − √n) Σ_{j=0}^{s} t^j n^{(s−j)/2}, together with t ≤ 3√n and Lemma 4:
   |t^{s+1} − n^{(s+1)/2}| ≤ (s+1) 3^s n^{s/2} |t − √n| ≪_s n^{s/2+1/4} log n.
   After multiplying by n^l/(m(s+l+1)), this is O(n^{l+s/2+1/4} log n), which is smaller than the error in step 2.
4. Combining steps 2 and 3 proves the Theorem. The case s = 0, l = 1 is the displayed special case. ∎

The general-l, s = 0 case gives the RH version of Ding's Corollary 3 for maximal sets: Σ_{a∈S, a≡r} a^l = n^{l+1/2}/(m(l+1)) + O(n^{l+3/8}(log n)^{3/2}).

## What this does and does not show

- **Not #30.** Erdős #30 asks whether h(N) = √N + O_ε(N^ε). Its Lean form is `erdos_30` in FormalConjectures/ErdosProblems/30.lean, together with `erdos_30.variants.O_one`. This lead says nothing about the upper side of h(N) and does not touch either Lean statement. It concerns how maximum-size Sidon sets are distributed in residue classes. That is a Sidon-adjacent question from Ding's papers and is not on erdosproblems.com/30.
- **What RH supplies.** RH enters only through Lemma 4: maximal Sidon sets have size √n − O(n^{1/4} log n) for every n. Everything else is unconditional and already in Ding / Ortega–Prendiville.
- **The log loss.** The error is n^{l+s/2+3/8}(log n)^{3/2}, which is weaker by (log n)^{1/2} than Ding's almost-all Theorem 6. RH does not give the exact n^{1/4} size defect, because of the log in Cramér's bound.
- **Better result for m = 1 (inferred).** For the plain sum over all of S (m = 1, s = 0, l = 1) a better RH bound follows by another route. Ding II (arXiv:2205.01084v2), Corollary 1.2, says that Σ_{i≤t} a_i = ½nt + O(n^{5/4}(n^{1/2} − t)^{1/2}) when t < n^{1/2} − n^{1/4}. I read the statement but not its proof. Plugging in Lemma 4 gives Σ_{a∈S} a = ½n^{3/2} + O(n^{11/8}(log n)^{1/2}) for all n under RH. So the residue-class and weighted versions are where the Theorem above adds something, not the m = 1 sum.
- **What would sharpen it.** Improving the log power, or removing it, would need either an improvement of Cramér's RH gap bound or a better Fourier-uniformity exponent (Ding, Remark 11). Neither is provided here.

## Credit

- The whole analytic engine is Ding (arXiv:2606.15041v2, Theorem 4) and Ortega–Prendiville (JTNB 2023, Theorem 6.3 and Lemma 3.2).
- The RH input is Cramér's theorem (1920), in Dudek's explicit form (arXiv:1402.6417, Theorem 2). Carneiro–Milinovich–Soundararajan (Theorem 5) give it with a better constant.
- The step "a prime-gap bound gives a size defect, which gives sum asymptotics" is already in the literature in conditional form:
  - Balasubramanian–Dutta (arXiv:2409.01986v4, remark after Lemma 2) note that p_{k+1} − p_k ≪ √p_k would give L ≪ n^{1/4}.
  - Ding II (intro) recalls that Ding 2021 obtained O(n^{11/8}) under S_n = n^{1/2} + O(n^{1/4}).
  - None of the papers I read state the RH version. I grepped for "Riemann", "hypothes" and "Cram" in Ding 2026, Ding II and B-D, and they contain no RH statement.
- Novelty is therefore of the "nobody wrote it down" kind: a routine substitution. It should be presented as a remark, not a theorem.
- Rival check (22 Nov 2026):
  - Plasma `wiki/problems/additive_bases/E0030/_index.md`: no RH, residue-class or Ding content. Plasma's tree has no Ding-Sidon, Ortega–Prendiville or Balasubramanian–Dutta Sidon entries. Its only Ding/Balasubramanian entries are on additive complements of squares.
  - ryantuck/erdos-ai `fable-review/30.md`: no hit for RH or residue classes.
  - erdosproblems.com/forum/thread/30: only upper-bound constants (Hou–Zhao and follow-ups).
  - arXiv web search for "Balasubramanian Dutta Sidon" returns only 2409.01986.

## Sources not read
- Balasubramanian–Dutta, the J. Number Theory 279 (2026) journal version. I read only arXiv v4.
- Ding 2021 (IJNT 17), "Sum of elements in finite Sidon sets". I know its conditional n^{11/8} remark only from Ding II's intro.
- The proof of Ding II, Corollary 1.2 (used only in the inferred m = 1 remark).
- Cilleruelo, "Gaps in dense Sidon sets" (input to O-P Theorem 6.3). Not re-derived.
- Cramér 1920; Lindström 1969; Erdős–Turán 1941; Singer 1938; Bose 1942. Lemma 1 is proved here, so Bose is not load-bearing.
- The Alpöge Lean RH development (taken from the brief, not checked).
- Journal versions of Dudek and of Carneiro–Milinovich–Soundararajan. I read only the arXiv versions.

Files: refs/ holds the PDFs and extracted text of O-P, Dudek, CMS, B-D and Ding II. Ding 2026 is in ../refs/. `check_numeric.py` runs the numeric checks (`python3 -I check_numeric.py`, about 1 minute).
