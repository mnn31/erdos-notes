import Mathlib

/-!
Proof of `Erdos766.erdos_766.parts.ii` (formal-conjectures origin/main 2207c54d, file
FormalConjectures/ErdosProblems/766.lean). The definition `forcingNumber` below is copied verbatim
from that file; the final theorem has verbatim the statement of `erdos_766.parts.ii`.
-/

open Filter
open scoped SimpleGraph

namespace Erdos766

noncomputable def forcingNumber (n k l : ℕ) : ℕ :=
  sInf {m : ℕ | ∀ G : SimpleGraph (Fin n), G.edgeSet.ncard = m →
    ∃ H : SimpleGraph (Fin k), H.edgeSet.ncard = l ∧ H ⊑ G}

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

theorem erdos_766.parts.ii :
    ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
      StrictMonoOn (forcingNumber n k) (Set.Ioc k (k ^ 2 / 4)) := by
  intro k
  rw [Filter.eventually_atTop]
  exact ⟨k, fun n hn => (forcingNumber_strictMonoOn_Iic hn).mono (Ioc_subset_Iic_choose k)⟩

end Erdos766

#print axioms Erdos766.erdos_766.parts.ii
