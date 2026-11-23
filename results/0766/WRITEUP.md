# Erdős 766, `erdos_766.parts.ii` (the f_1 reading): proved, and the proof is elementary

Date: 2026-11-23. Outcome: **PROVED**, with a Lean 4 / Mathlib proof checked against a verbatim copy of the
formal-conjectures file (axioms: `propext`, `Classical.choice`, `Quot.sound` only).

## 0. Exact statement established

Notation. Write `f(n;k,l)` for `Erdos766.forcingNumber n k l` (formal-conjectures origin/main `2207c54d`,
`FormalConjectures/ErdosProblems/766.lean`):

    f(n;k,l) = sInf { m : every G on Fin n with exactly m edges contains (⊑, an injective
                          homomorphism, not necessarily induced) some H on Fin k with exactly l edges }.

**Theorem.** For all natural numbers `k ≤ n` and every `l` with `l + 1 ≤ C(k,2)`,
`f(n;k,l) < f(n;k,l+1)`. So for `n ≥ k` the map `l ↦ f(n;k,l)` is strictly increasing on
`{0, 1, …, C(k,2)}`. Since `⌊k²/4⌋ ≤ C(k,2)`, this gives, verbatim, the Lean statement

    theorem erdos_766.parts.ii :
        ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
          StrictMonoOn (forcingNumber n k) (Set.Ioc k (k ^ 2 / 4))

with the explicit threshold `n ≥ k`. Remark 6 shows that for `k ≥ 6` this threshold is sharp: for `n < k` the
function is constant.

So the answer to the question as formalized is **yes**. The proof takes one line on paper (add one edge to an
extremal graph), which strongly suggests that the f_1 reading is not what Erdős meant (see Section 4).

## 1. Status check before investing (done 2026-11-23)

VERIFIED, read in source text (copies in `refs/`):
- erdosproblems.com/766 (curl): OPEN; 0 comments, 0 proof claims; "Formalised statement? Yes". The forum thread is empty.
- formal-conjectures origin/main `2207c54d` (2026-11-21): `erdos_766.parts.ii` is tagged
  `@[category research open, question, AMS 5]` and its proof is `sorry` (copy: `refs/766.lean.origin_main_2207c54d`).
- formal-conjectures PRs mentioning 766: #6964 (adds the file, merged) and #8091 (open; links a proof of
  `variants.dirac_erdos` only). Issue #930 (closed) is the request for the formalization. None of them proves
  `parts.ii` or notes that it is easy. I read the #8091 body and grepped the #6964 comments for
  "monoton|strict|trivial".
- Plasma `wiki/problems/extremal_graph_theory/E0766/_index.md` (updated 2026-10-08) and the library page
  `conjecture_p33.md`. Both say that the two readings are nondecreasing in l, that "the question is strictness",
  and that it is open in both readings. Neither gives the argument below.
- ryantuck/erdos-ai `deepmind/reviews/766.md`, `deepmind/ai-review/766.md`, `deepmind/deepmind/766.lean`: these
  review an older min-ex formalization and contain no proof of strictness.

Conclusion: no source I read decides `parts.ii`. Novelty is beside the point here, because the argument is
elementary; see Section 4.

## 2. Lemmas and proofs

Throughout, graphs are simple, `e(G) = |E(G)|`, and `[k] = Fin k`. `S_l = S_l(n,k)` is the set whose infimum
defines `f(n;k,l)`. "H ⊑ G" means that there is an injective map `φ : V(H) → V(G)` with
`ab ∈ E(H) ⇒ φ(a)φ(b) ∈ E(G)` (Mathlib `SimpleGraph.Copy` / `IsContained`).

**Lemma 1 (shrinking).** If `H₀` is a graph on `[k]` with `H₀ ⊑ G` and `l ≤ e(H₀)`, then some graph `H` on `[k]`
has `e(H) = l` and `H ⊑ G`.

*Proof.* Choose `T ⊆ E(H₀)` with `|T| = l`, which is possible because `l ≤ |E(H₀)|`. Let `H` be the graph on `[k]`
with edge set `T`. The elements of `T` are edges of `H₀`, so none of them is a loop, and therefore `E(H) = T` and
`e(H) = l`. Since `T ⊆ E(H₀)`, `H` is a subgraph of `H₀` on the same vertex set. The injective map `φ`
witnessing `H₀ ⊑ G` therefore also witnesses `H ⊑ G`: if `ab ∈ E(H)` then `ab ∈ E(H₀)`, so `φ(a)φ(b) ∈ E(G)`. ∎
(Lean: `exists_card_eq_of_isContained`.)

**Lemma 2 (one added edge costs at most one edge).** Let `u ≠ v` be non-adjacent in `G`, and let `G⁺ = G + uv`.
If `H'` is a graph on `[k]` with `e(H') = l+1` and `H' ⊑ G⁺`, then some graph `H` on `[k]` has `e(H) = l` and
`H ⊑ G`.

*Proof.* Let `φ` witness `H' ⊑ G⁺`. Let `H₀` be the graph on `[k]` whose edges are the edges `ab` of `H'` with
`φ(a)φ(b) ∈ E(G)`. Then `φ` witnesses `H₀ ⊑ G`, because it is injective and maps every edge of `H₀` into `E(G)`
by definition. Take an edge `ab ∈ E(H') \ E(H₀)`. Then `φ(a)φ(b) ∈ E(G⁺) \ E(G) = {uv}`, so `{φ(a),φ(b)} = {u,v}`.
The map `φ` is injective, so the induced map on unordered pairs `{a,b} ↦ {φ(a),φ(b)}` is injective
(`Sym2.map.injective`), and at most one unordered pair of `[k]` is sent to `{u,v}`. Hence `|E(H') \ E(H₀)| ≤ 1`,
so `e(H₀) ≥ e(H') − 1 = l`. Lemma 1 applied to `H₀` gives `H`. ∎ (Lean: `exists_of_isContained_sup_edge`. Lean
uses the inclusion `E(H') ⊆ E(H₀) ∪ map⁻¹{uv}` and `ncard_union_le`.)

**Lemma 3 (basic facts about `S_l`).**
(a) `e(G) ≤ C(n,2)` for every graph `G` on `[n]`, so `C(n,2)+1 ∈ S_l` for every `l`, `S_l ≠ ∅`, and
`f(n;k,l) ∈ S_l` (least element of a nonempty set of naturals).
(b) If `l ≥ 1` then `0 ∉ S_l`.
(c) If `G` is a graph on `[n]` with exactly `m` edges and `G` is not complete, then there are `u ≠ v` with `uv ∉ E(G)`
and `e(G + uv) = m + 1`.

*Proof.* (a) `E(G)` is a subset of the `C(n,2)` two-element subsets of `[n]`. No graph has exactly `C(n,2)+1`
edges, so the defining condition of `S_l` holds vacuously at `m = C(n,2)+1`. `Nat.sInf_mem` gives the last claim.
(b) The empty graph on `[n]` has 0 edges. If `H ⊑` empty graph with `e(H) = l ≥ 1`, pick `ab ∈ E(H)`. Then
`φ(a)φ(b)` would be an edge of the empty graph, which is impossible.
(c) If every pair `u ≠ v` were adjacent, `G` would be complete. For the non-edge `uv`,
`E(G + uv) = E(G) ∪ {uv}` with `uv ∉ E(G)`, so the count rises by exactly 1. ∎
(Lean: `ncard_edgeSet_le`, the `hpos` block, `ncard_edgeSet_sup_edge`.)

**Lemma 4 (complete graphs).** If `k ≤ n`, then `K_k ⊑ K_n` and `e(K_k) = C(k,2)`.

*Proof.* The inclusion `Fin.castLE : [k] → [n]` is injective, and it maps distinct vertices to distinct vertices,
that is, edges of `K_k` to edges of `K_n`. The count is standard (`card_edgeFinset_top_eq_card_choose_two`). ∎

**Theorem 5 (key step).** If `k ≤ n` and `l + 1 ≤ C(k,2)`, then `f(n;k,l) < f(n;k,l+1)`.

*Proof.* Let `m' = f(n;k,l+1)`. By Lemma 3(a), `m' ∈ S_{l+1}`, and by Lemma 3(b), `m' ≥ 1`. We show `m' − 1 ∈ S_l`.
Let `G` be any graph on `[n]` with exactly `m' − 1` edges.
- If `G = K_n`: by Lemma 4, `K_k ⊑ G` and `e(K_k) = C(k,2) ≥ l + 1 > l`. Lemma 1 gives `H` with `e(H) = l` and
  `H ⊑ G`.
- Otherwise, by Lemma 3(c), `G⁺ = G + uv` has exactly `m'` edges for some non-edge `uv`. Since `m' ∈ S_{l+1}`,
  some `H'` on `[k]` with `e(H') = l+1` has `H' ⊑ G⁺`. Lemma 2 gives `H` with `e(H) = l` and `H ⊑ G`.

So `m' − 1 ∈ S_l`, hence `f(n;k,l) = inf S_l ≤ m' − 1 < m'`. ∎ (Lean: `forcingNumber_lt_succ`.)

**Corollary 6 (the Lean statement).** For `n ≥ k`, `l ↦ f(n;k,l)` is strictly increasing on `[0, C(k,2)]`.
(Theorem 5 plus induction; Lean uses `strictMonoOn_Iic_of_lt_succ`.) Also `Ioc k ⌊k²/4⌋ ⊆ [0, C(k,2)]`: if
`k < l` and `4l ≤ k²`, then `k ≥ 1`, and `2l ≤ k²/2 ≤ k(k−1)` because `k²/2 ≤ k² − k` holds exactly when `k ≥ 2`.
Here `k = 1` is impossible, since `4l ≤ 1` would force `l = 0`, contradicting `l > 1`. So `l ≤ k(k−1)/2 = C(k,2)`.
Hence `erdos_766.parts.ii` holds with "eventually" witnessed by `N₀ = k`. ∎
(Lean: `forcingNumber_strictMonoOn_Iic`, `Ioc_subset_Iic_choose`, `erdos_766.parts.ii`.)

**Remark 7 (the threshold `n ≥ k` is sharp for k ≥ 6; paper proof only, not in Lean).** If `n < k`, then no
graph on `[k]`, not even the empty one, is ⊑ a graph on `[n]`, because there is no injection `[k] → [n]`. So
`S_l = {m : no graph on [n] has m edges} = {m ≥ C(n,2)+1}` and `f(n;k,l) = C(n,2)+1` for every `l`. For
`k ≥ 6` the interval `Ioc k ⌊k²/4⌋` contains at least two points (`k+1 ≤ ⌊k²/4⌋`), so strict monotonicity fails
for every `n < k`. (For `k ≤ 5` the interval has at most one point and the statement holds for every `n`.)
The program in `out/` only covers `k ≤ n`, so it does not test this remark.

**Remark 8 (paper only).** For `n ≥ k` the strict increase extends one step further:
`f(n;k,C(k,2)) ≤ C(n,2) < C(n,2)+1 = f(n;k,C(k,2)+1)`. Here `K_n ⊇ K_k` gives `C(n,2) ∈ S_{C(k,2)}`, and no
graph on `[k]` has `C(k,2)+1` edges. This matches the last entry of every row in `out/`.

## 3. Computation (sanity checks only; the proof does not depend on them)

`code/f1_all.c` enumerates every labelled graph on `n ≤ 8` vertices and computes `f(n;k,l)` for all `k ≤ n` and
`0 ≤ l ≤ C(k,2)+1` in two independent ways:
(A) directly from the definition (the least `m` such that the minimum over all `m`-edge graphs of
"max edges spanned by a k-set" is at least `l`; this uses the fact, for `k ≤ n`, that some `k`-vertex `l`-edge
graph is ⊑ G iff some k-set spans at least l edges);
(B) as `1 + max{e(G) : every k-set spans ≤ l−1 edges}`.
It checks that A = B and that the result is strictly increasing in `l` on `0..C(k,2)+1`.
Result: all checks passed for n = 1..8 (`out/f1_all_n1to7.txt`, `out/f1_all_n8.txt`). The n = 7, 8, k = 6 rows
match the scout's independent `f1_bruteforce.c` output exactly
(n=7: 1,2,3,5,6,8,9,10,12,13,15,16,17,19,20; n=8: 1,2,3,5,7,9,11,13,15,17,19,21,22,25,26 for l = 1..15).

Reproduce:

    cd attack/766/t1/prove/code
    cc -O2 -o f1_all f1_all.c
    for n in 1 2 3 4 5 6 7; do ./f1_all $n; done > ../out/f1_all_n1to7.txt
    ./f1_all 8 > ../out/f1_all_n8.txt          # about 30 s

### Lean verification

- `code/lean/Erdos766PartsII.lean`: standalone (`import Mathlib`). It contains the `forcingNumber` definition
  copied verbatim, the lemmas above, and `erdos_766.parts.ii` with its verbatim statement. Checked with
  `cd formal-conjectures && lake env lean <path>/code/lean/Erdos766PartsII.lean`
  (Lean v4.33.1, that checkout's Mathlib). Output in `out/lean_standalone.txt`: no errors and no warnings,
  `'Erdos766.erdos_766.parts.ii' depends on axioms: [propext, Classical.choice, Quot.sound]`.
- `code/lean/Erdos766Faithful.lean`: generated by `code/lean/make_faithful.py` from the verbatim origin/main file
  `refs/766.lean.origin_main_2207c54d`. The only changes are these: the `module` / `public import` /
  `@[expose] public section` header is replaced by a plain `import FormalConjecturesUtil`; the helper lemmas are
  inserted before `parts.ii`; and the `sorry` of `parts.ii` is replaced by the proof (`diff` of the two files
  confirms this). All other declarations, including the `@[category research open, question, AMS 5]` attribute
  and the definition, are untouched. Checked with
  `cd wt/fc-675 && lake env lean <path>/code/lean/Erdos766Faithful.lean`. That
  worktree is at `4a3ca808`, which contains origin/main `2207c54d` as an ancestor and has a built
  `FormalConjecturesUtil` with the `question` attribute. Output in `out/lean_faithful.txt`: exit 0. The only
  warnings are `sorry` in the other, untouched declarations (parts.i and its answer, dirac_erdos, the two minEx
  variants), and `parts.ii` depends only on `[propext, Classical.choice, Quot.sound]`.
- Regenerate the faithful file:
  `python3 -I code/lean/make_faithful.py refs/766.lean.origin_main_2207c54d code/lean/Erdos766PartsII.lean code/lean/Erdos766Faithful.lean`.
- `out/sha256.txt` has the checksums. `code/lean/Probe.lean` was only used to look up lemma names.

## 4. What this does and does not show

Does show (VERIFIED: paper proof plus a Lean kernel check):
- `Erdos766.erdos_766.parts.ii` as stated in formal-conjectures origin/main is **true**, with `N₀ = k`, and in the
  stronger form "strictly increasing on all of `0..C(k,2)` for every `n ≥ k`". The `research open` tag on it is
  therefore inaccurate. Its content is an elementary observation.

Does not show:
- Nothing about `erdos_766.variants.minExtremalNumber_strictMonoOn` (the erdosproblems.com function
  `min_G ex(n;G)`, which is f_2 − 1). The add-an-edge argument does not transfer (INFERRED). For f_2 the monotone
  direction holds because a graph with `l+1` edges contains one with `l` edges. Strictness would need, for the
  minimizing `l`-edge graph `G`, that `ex(n;G') > ex(n;G)` for every `l+1`-edge `G'`, and adding an edge to a
  host does not give that. This variant remains open as far as I know.
- Nothing about `parts.i` (estimates) or `dirac_erdos`.
- INFERRED, not verified: because the f_1 question is settled by a one-line argument, Erdős (who wrote "I cannot
  even prove that ... f(n;k,l) is a strictly monotone function of l", Er64c p. 33, as quoted by Plasma) very
  probably did not mean the literal f_1 strictness. Plausible intended readings are f_2 (erdosproblems.com's
  `min ex`), or strictness at the level of orders of magnitude, for example `f(n;k,l+1)/f(n;k,l) → ∞` or
  `f(n;k,l+1) − f(n;k,l) → ∞` as `n → ∞`. I have not read Er64c itself, only Plasma's quotation of it. Nothing
  here bears on those readings. The formal-conjectures formalization of `parts.ii` (and Plasma's statement that
  the f_1 reading is open) should be revisited. Under the literal reading, the question has the answer "yes".
- Nothing is claimed to be new. The argument is folklore-level, and I found no written record of it in the
  sources I read.

## 5. Sources not read

- Er64c itself (Erdős, *Extremal problems in graph theory*, 1964): not opened. The definitions of f_1, f_2, f_3
  and the p. 33 sentence are taken from Plasma's quotation (`refs/plasma_*conjecture_p33.md`). The Lean
  definition was read directly and the proof is about it, so this does not affect the PROVED claim. It only
  affects the "intended reading" discussion.
- MathSciNet, zbMATH, Google Scholar, and an arXiv search for later treatments of f_1(n;k,l) monotonicity: not
  searched.
- formal-conjectures PR #6964 review thread: grepped only, not read in full. Issue #930: not opened.
- Plasma library pages theorem_p31 / theorem_p34 and the Dirac 1963 pages: not read (not needed).
