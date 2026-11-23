/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/
import FormalConjecturesUtil

/-!
# Erdős Problem 766

*References:*
- [erdosproblems.com/766](https://www.erdosproblems.com/766)
- [Er64c] Erdős, P., *Extremal problems in graph theory*. Theory of Graphs and its Applications
  (Proc. Sympos. Smolenice, 1963) (1964), 29-36.
  [PDF](https://www.renyi.hu/~p_erdos/1964-06.pdf)
-/


open Filter
open scoped SimpleGraph

namespace Erdos766

/-- $f(n;k,l)$ in the sense of [Er64c], where it is called $f_1(n;k,l)$: the least $m$ such that
every graph with $n$ vertices and $m$ edges contains at least one graph with $k$ vertices and
$l$ edges as a (not necessarily induced) subgraph. There is no graph with $n$ vertices and more
than $\binom{n}{2}$ edges, so the set is nonempty. -/
noncomputable def forcingNumber (n k l : ℕ) : ℕ :=
  sInf {m : ℕ | ∀ G : SimpleGraph (Fin n), G.edgeSet.ncard = m →
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l ∧ H ⊑ G}

/-- If every graph with $n$ vertices and $m$ edges contains a graph with $k$ vertices and $l$
edges, then $f(n;k,l) \leq m$. -/
@[category API, AMS 5]
theorem forcingNumber_le {n k l m : ℕ} (h : ∀ G : SimpleGraph (Fin n), G.edgeSet.ncard = m →
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l ∧ H ⊑ G) : forcingNumber n k l ≤ m :=
  Nat.sInf_le h

/-- For $k \leq n$ every graph on $n$ vertices contains the empty graph on $k$ vertices, so
$f(n;k,0) = 0$. -/
@[category test, AMS 5]
theorem forcingNumber_zero {n k : ℕ} (hkn : k ≤ n) : forcingNumber n k 0 = 0 :=
  Nat.eq_zero_of_le_zero <| forcingNumber_le fun _ _ ↦
    ⟨⊥, by simp, SimpleGraph.bot_isContained_iff_card_le.2 (by simpa using hkn)⟩

/-- $f(n;k,l) \leq \mathrm{ex}(n;G) + 1$ for every graph $G$ with $k$ vertices and $l$ edges,
since a graph with more than $\mathrm{ex}(n;G)$ edges contains $G$. Here $\mathrm{ex}(n;G)$ is
`SimpleGraph.extremalNumber n G`, the maximum number of edges of a graph on $n$ vertices with no
copy of $G$. -/
@[category test, AMS 5]
theorem forcingNumber_le_extremalNumber_add_one (n : ℕ) {k l : ℕ} (G : SimpleGraph (Fin k))
    (h : G.edgeSet.ncard = l) : forcingNumber n k l ≤ SimpleGraph.extremalNumber n G + 1 := by
  classical
  refine forcingNumber_le fun G' hG' ↦ ⟨G, h, ?_⟩
  refine SimpleGraph.IsContained.of_extremalNumber_lt_card_edgeFinset ?_
  rw [Fintype.card_fin, ← Set.ncard_coe_finset, SimpleGraph.coe_edgeFinset, hG']
  exact Nat.lt_succ_self _

/-- The function of erdosproblems.com: the minimum of $\mathrm{ex}(n;G)$ over all graphs $G$ with
$k$ vertices and $l$ edges. In [Er64c] the least $m$ such that every graph with $n$ vertices and
$m$ edges contains one fixed graph with $k$ vertices and $l$ edges is called $f_2(n;k,l)$, so
this is $f_2(n;k,l) - 1$. The value is in `ℕ∞` and is `⊤` when no such graph $G$ exists. -/
noncomputable def minExtremalNumber (n k l : ℕ) : ℕ∞ :=
  ⨅ (G : SimpleGraph (Fin k)) (_ : G.edgeSet.ncard = l), (SimpleGraph.extremalNumber n G : ℕ∞)

/-- The minimum is at most $\mathrm{ex}(n;G)$ for every graph $G$ with $k$ vertices and $l$
edges. -/
@[category API, AMS 5]
theorem minExtremalNumber_le (n : ℕ) {k l : ℕ} (G : SimpleGraph (Fin k))
    (h : G.edgeSet.ncard = l) : minExtremalNumber n k l ≤ SimpleGraph.extremalNumber n G :=
  iInf₂_le G h

/-- There is no graph with $0$ vertices and $1$ edge, so the minimum is `⊤`. -/
@[category test, AMS 5]
theorem minExtremalNumber_zero_one (n : ℕ) : minExtremalNumber n 0 1 = ⊤ := by
  simp [minExtremalNumber, Set.eq_empty_of_isEmpty]

def erdos_766.parts.i.answer : ℕ → ℕ → ℕ → ℝ := sorry

/--
Let $f(n;k,l)=\min \mathrm{ex}(n;G)$, where $G$ ranges over all graphs with $k$ vertices and $l$
edges.

Give good estimates for $f(n;k,l)$ in the range $k<l\leq k^2/4$.

In [Er64c, p. 33] this question is asked for $f_1(n;k,l)$ (`Erdos766.forcingNumber`), which
forces at least one graph with $k$ vertices and $l$ edges rather than one fixed graph; we follow
the source. The question for the function of erdosproblems.com is
`Erdos766.erdos_766.variants.minExtremalNumber_estimate`.
-/
@[category research open, question value, AMS 5]
theorem erdos_766.parts.i :
    ∀ k l : ℕ, k < l → l ≤ k ^ 2 / 4 →
      (fun n ↦ (forcingNumber n k l : ℝ)) =Θ[atTop] erdos_766.parts.i.answer k l := by
  sorry

section
variable {n k : ℕ}

/-- Lemma A: a contained graph with at least `l` edges yields a contained graph with exactly
`l` edges. -/
lemma exists_card_eq_of_isContained {l : ℕ} {G : SimpleGraph (Fin n)}
    {H₀ : SimpleGraph (Fin k)} (h : H₀ ⊑ G) (hl : l ≤ H₀.edgeSet.ncard) :
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l ∧ H ⊑ G := by
  obtain ⟨t, ht, htl⟩ := Set.exists_subset_card_eq hl
  have hdiag : t \ Sym2.diagSet = t := by
    ext e
    simp only [Set.mem_sdiff, Sym2.mem_diagSet]
    exact ⟨fun h => h.1, fun h => ⟨h, H₀.not_isDiag_of_mem_edgeSet (ht h)⟩⟩
  refine ⟨SimpleGraph.fromEdgeSet t, ?_, ?_⟩
  · rw [SimpleGraph.edgeSet_fromEdgeSet, hdiag, htl]
  · refine SimpleGraph.IsContained.mono_left ?_ h
    rw [SimpleGraph.fromEdgeSet_le, hdiag]
    exact ht

/-- Lemma B: if `H'` (with `l+1` edges) is contained in `G` plus one edge, then some graph on
`Fin k` with `l` edges is contained in `G`. -/
lemma exists_of_isContained_sup_edge {l : ℕ} {G : SimpleGraph (Fin n)} {u v : Fin n}
    {H' : SimpleGraph (Fin k)} (h : H' ⊑ G ⊔ SimpleGraph.edge u v)
    (hl : H'.edgeSet.ncard = l + 1) :
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l ∧ H ⊑ G := by
  obtain ⟨f⟩ := h
  let H₀ : SimpleGraph (Fin k) := H' ⊓ G.comap f
  have hH₀ : H₀ ⊑ G := ⟨⟨⟨f, fun {a b} hab => hab.2⟩, f.injective⟩⟩
  have hsub : H'.edgeSet ⊆ H₀.edgeSet ∪ (Sym2.map f) ⁻¹' {s(u, v)} := by
    intro e he
    induction e using Sym2.ind with
    | h a b =>
      have hab : H'.Adj a b := he
      have hf := f.toHom.map_adj hab
      rcases hf with hG | hE
      · left
        exact ⟨hab, hG⟩
      · right
        rw [SimpleGraph.edge_adj] at hE
        simp only [Set.mem_preimage, Sym2.map_mk, Set.mem_singleton_iff]
        rcases hE.1 with ⟨h1, h2⟩ | ⟨h1, h2⟩
        · have h1' : f a = u := h1
          have h2' : f b = v := h2
          rw [h1', h2']
        · have h1' : f a = v := h1
          have h2' : f b = u := h2
          rw [h1', h2', Sym2.eq_swap]
  have hP : ((Sym2.map f) ⁻¹' {s(u, v)}).ncard ≤ 1 :=
    Set.ncard_le_one_iff_subsingleton.2
      ((Set.subsingleton_singleton).preimage (Sym2.map.injective f.injective))
  have h1 : H'.edgeSet.ncard ≤ H₀.edgeSet.ncard + 1 :=
    calc H'.edgeSet.ncard ≤ (H₀.edgeSet ∪ (Sym2.map f) ⁻¹' {s(u, v)}).ncard :=
          Set.ncard_le_ncard hsub
      _ ≤ H₀.edgeSet.ncard + ((Sym2.map f) ⁻¹' {s(u, v)}).ncard := Set.ncard_union_le _ _
      _ ≤ H₀.edgeSet.ncard + 1 := by omega
  exact exists_card_eq_of_isContained hH₀ (by omega)

/-- Number of edges after adding a non-edge. -/
lemma ncard_edgeSet_sup_edge {G : SimpleGraph (Fin n)} {u v : Fin n} (huv : u ≠ v)
    (hn : ¬ G.Adj u v) :
    (G ⊔ SimpleGraph.edge u v).edgeSet.ncard = G.edgeSet.ncard + 1 := by
  rw [SimpleGraph.edgeSet_sup, SimpleGraph.edgeSet_edge_of_ne huv, Set.union_singleton]
  exact Set.ncard_insert_of_notMem hn

/-- Every graph on `Fin n` has at most `n.choose 2` edges. -/
lemma ncard_edgeSet_le (G : SimpleGraph (Fin n)) : G.edgeSet.ncard ≤ n.choose 2 := by
  classical
  have := G.card_edgeFinset_le_card_choose_two
  rw [Fintype.card_fin] at this
  rw [← SimpleGraph.coe_edgeFinset, Set.ncard_coe_finset]
  exact this

lemma ncard_edgeSet_top (k : ℕ) : (⊤ : SimpleGraph (Fin k)).edgeSet.ncard = k.choose 2 := by
  classical
  rw [← SimpleGraph.coe_edgeFinset, Set.ncard_coe_finset,
    SimpleGraph.card_edgeFinset_top_eq_card_choose_two, Fintype.card_fin]

lemma top_isContained_top (hkn : k ≤ n) :
    (⊤ : SimpleGraph (Fin k)) ⊑ (⊤ : SimpleGraph (Fin n)) :=
  ⟨⟨⟨Fin.castLE hkn, fun {a b} hab => by
      simp only [SimpleGraph.top_adj] at hab ⊢
      exact (Fin.castLE_injective hkn).ne hab⟩, Fin.castLE_injective hkn⟩⟩

/-- Lemma E (the key step): for `k ≤ n` and `l + 1 ≤ k.choose 2`,
`forcingNumber n k l < forcingNumber n k (l + 1)`. -/
lemma forcingNumber_lt_succ (hkn : k ≤ n) {l : ℕ} (hl : l + 1 ≤ k.choose 2) :
    forcingNumber n k l < forcingNumber n k (l + 1) := by
  set S := {m : ℕ | ∀ G : SimpleGraph (Fin n), G.edgeSet.ncard = m →
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l + 1 ∧ H ⊑ G} with hS
  have hne : n.choose 2 + 1 ∈ S := by
    intro G hG
    have := ncard_edgeSet_le G
    omega
  have hmem : forcingNumber n k (l + 1) ∈ S := Nat.sInf_mem ⟨_, hne⟩
  set m' := forcingNumber n k (l + 1) with hm'
  have hpos : m' ≠ 0 := by
    intro h0
    rw [h0] at hmem
    obtain ⟨H, hH, ⟨f⟩⟩ := hmem ⊥ (by simp)
    obtain ⟨e, he⟩ := Set.nonempty_of_ncard_ne_zero (s := H.edgeSet) (by omega)
    induction e using Sym2.ind with
    | h a b => exact (f.toHom.map_adj he : (⊥ : SimpleGraph (Fin n)).Adj (f a) (f b))
  have hle : forcingNumber n k l ≤ m' - 1 := by
    apply Nat.sInf_le
    intro G hG
    by_cases htop : ∀ u v : Fin n, u ≠ v → G.Adj u v
    · have hGtop : G = ⊤ := by
        ext u v
        simp only [SimpleGraph.top_adj]
        exact ⟨G.ne_of_adj, htop u v⟩
      subst hGtop
      exact exists_card_eq_of_isContained (top_isContained_top hkn)
        (by rw [ncard_edgeSet_top]; omega)
    · push Not at htop
      obtain ⟨u, v, huv, hnadj⟩ := htop
      obtain ⟨H', hH', hc⟩ := hmem (G ⊔ SimpleGraph.edge u v)
        (by rw [ncard_edgeSet_sup_edge huv hnadj, hG]; omega)
      exact exists_of_isContained_sup_edge hc hH'
  omega

/-- For `k ≤ n`, `l ↦ forcingNumber n k l` is strictly increasing on `[0, k.choose 2]`. -/
theorem forcingNumber_strictMonoOn_Iic (hkn : k ≤ n) :
    StrictMonoOn (forcingNumber n k) (Set.Iic (k.choose 2)) := by
  apply strictMonoOn_Iic_of_lt_succ
  intro m hm
  rw [Order.succ_eq_add_one]
  exact forcingNumber_lt_succ hkn (by omega)

lemma Ioc_subset_Iic_choose (k : ℕ) : Set.Ioc k (k ^ 2 / 4) ⊆ Set.Iic (k.choose 2) := by
  intro l ⟨hkl, hl⟩
  simp only [Set.mem_Iic]
  rw [Nat.le_div_iff_mul_le (by norm_num)] at hl
  rw [Nat.choose_two_right, Nat.le_div_iff_mul_le (by norm_num)]
  rcases k with _ | j
  · simp at hl
    omega
  · simp only [Nat.add_sub_cancel]
    nlinarith

end


/--
For fixed $k$ and large $n$ is $f(n;k,l)$ a strictly monotone function of $l$?

As in `Erdos766.erdos_766.parts.i`, $f$ is $f_1$ of [Er64c], and we use the range
$k<l\leq k^2/4$ in which the question is asked there; here `k ^ 2 / 4` is $\lfloor k^2/4\rfloor$.
The question for the function of erdosproblems.com is
`Erdos766.erdos_766.variants.minExtremalNumber_strictMonoOn`.
-/
@[category research open, question, AMS 5]
theorem erdos_766.parts.ii :
    ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
      StrictMonoOn (forcingNumber n k) (Set.Ioc k (k ^ 2 / 4)) := by
  intro k
  rw [Filter.eventually_atTop]
  exact ⟨k, fun n hn => (forcingNumber_strictMonoOn_Iic hn).mono (Ioc_subset_Iic_choose k)⟩

/--
Dirac and Erdős proved independently that when $l=\lfloor k^2/4\rfloor+1$
$$f(n;k,l)\leq \lfloor n^2/4\rfloor+1.$$

[Er64c, p. 34] states this for every $k \leq n$. We assume $k \geq 3$, since for $k \leq 2$ there
is no graph with $k$ vertices and $\lfloor k^2/4\rfloor+1$ edges.
-/
@[category research solved, AMS 5]
theorem erdos_766.variants.dirac_erdos (n k : ℕ) (hk : 3 ≤ k) (hkn : k ≤ n) :
    forcingNumber n k (k ^ 2 / 4 + 1) ≤ n ^ 2 / 4 + 1 := by
  sorry

def erdos_766.variants.minExtremalNumber_estimate.answer : ℕ → ℕ → ℕ → ℝ := sorry

/--
The estimate question of `Erdos766.erdos_766.parts.i` for the function
$\min \mathrm{ex}(n;G)$ of erdosproblems.com (`Erdos766.minExtremalNumber`).
-/
@[category research open, question value, AMS 5]
theorem erdos_766.variants.minExtremalNumber_estimate :
    ∀ k l : ℕ, k < l → l ≤ k ^ 2 / 4 →
      (fun n ↦ ((minExtremalNumber n k l).toNat : ℝ)) =Θ[atTop]
        erdos_766.variants.minExtremalNumber_estimate.answer k l := by
  sorry

/--
The monotonicity question of `Erdos766.erdos_766.parts.ii` for the function
$\min \mathrm{ex}(n;G)$ of erdosproblems.com (`Erdos766.minExtremalNumber`).
-/
@[category research open, question, AMS 5]
theorem erdos_766.variants.minExtremalNumber_strictMonoOn :
    ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
      StrictMonoOn (minExtremalNumber n k) (Set.Ioc k (k ^ 2 / 4)) := by
  sorry

end Erdos766

#print axioms Erdos766.erdos_766.parts.ii
