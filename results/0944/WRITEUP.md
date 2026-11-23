# Erdős 944, quantitative form at k = 4: f_4(n) → ∞

Date: 2026-11-23. Folder: `erdos-work/attack/944/t1/prove/`.

## 0. Exact statement established

**Theorem A (no outside input except Skottová–Steiner's gluing idea, re-proved here).**
Let r ≥ 0. Suppose some (4,r)-graph has order N. Then a (4,r)-graph exists for **every** order
n ≥ N + (5N−3)(9N−5).

**Theorem B (answers the target, using one outside input).** f_4(n) → ∞ as n → ∞. More precisely,
for every r ≥ 1 let N_r be the order of any finite (4,r)-graph. Then f_4(n) ≥ r for all
n ≥ N_r + (5N_r−3)(9N_r−5).

The outside input is the existence of a finite (4,r)-graph for every r ≥ 1. This is the k = 4 branch of
the Kruer–Kohlmeyer Lean proof (Conjectures.io record e7afff2c…, SHA-256 8bf7cd0e…abecd5). Its kernel was
replayed by Conjectures.io and, independently, by Plasma's corpus. **I did not replay it myself**: a local
replay attempt was blocked by the session's permission system (see §6).

Definitions. Graphs are finite and simple. G − v deletes a vertex. G − F deletes edges F ⊆ E(G).
A **(k,r)-graph** is a finite graph G with χ(G) = k, χ(G − v) < k for every vertex v, and χ(G − F) = k
for every F ⊆ E(G) with |F| ≤ r. f_k(n) is the largest r ≥ 1 such that a (k,r)-graph on exactly n
vertices exists (0 if there is none). These definitions are as on erdosproblems.com/944 and in SkSt25,
Problem 1.1. A graph H is **k-critical** if χ(H) = k, and χ(H − v) < k and χ(H − e) < k for every
vertex v and every edge e. For c : V(G) → [k−1], an arbitrary map (not necessarily proper), write
Bad_G(c) = {uw ∈ E(G) : c(u) = c(w)} and μ_{k−1}(G) = min_c |Bad_G(c)|.

## 1. Prior-status check (done before investing)

- erdosproblems.com/944 (fetched 2026-11-23, `refs/page944.html.txt`) still says k = 4 is open "even
  the case k=4 and r=1", and gives the f_k(n) → ∞ question only for k ≥ 5 (SkSt25). VERIFIED (read).
- Forum thread 944 (`refs/forum944.html.txt`) has 4 comments (Kitamura r = 1 Lean, veljjanoski SAT,
  AlperTheKing 6-regular, Zach Hunter on constants). The proof-claims tab has 1 claim (Chan, k = 4 graph).
  None mentions f_4(n) → ∞. VERIFIED (read).
- Plasma `wiki/problems/graph_coloring/E0944/_index.md` and the Kruer–Kohlmeyer claim page
  (`refs/plasma_*.md`) mark the existence question proved. They state that the KK exposition "does not
  claim" the every-large-order assertion. VERIFIED (read).
- KK exposition `../../refs/kk944.txt` §1.1: "It does not claim the further assertion that suitable
  graphs exist at every sufficiently large prescribed order with robustness tending to infinity."
  VERIFIED (read).
- formal-conjectures origin/main (2207c54, 2026-11-21) `944.lean` has no f_k(n) variant. ryantuck/erdos-ai
  `conjectures/944.lean` only states the existence form. An arXiv search (`abs:"vertex-critical"`, newest 20,
  `refs/arxiv_search.xml`) found nothing on f_4. VERIFIED (read).

Conclusion: as far as these sources show, the quantitative k = 4 statement is not recorded as decided.
The deduction below is short. Someone may have noticed it without writing it down, so I make **no
priority claim**.

## 2. Lemmas and proofs

### Lemma 1 (bridge; KK Lemma 2.1, SkSt-style). Let k ≥ 2, r ≥ 0, and let G be a finite graph with at least one vertex. Then G is a (k,r)-graph if and only if (a) G − v is (k−1)-colourable for every v, and (b) μ_{k−1}(G) ≥ r + 1.

*Proof.* (⇒) (a) holds because χ(G − v) < k. For (b), suppose some c has |Bad_G(c)| ≤ r. Put
F = Bad_G(c). Then c is a proper (k−1)-colouring of G − F, so χ(G − F) ≤ k−1 < k, while |F| ≤ r. This
contradicts the definition.
(⇐) Fix v. Colour G − v with k−1 colours and give v a new colour. So χ(G) ≤ k. If G had a proper
(k−1)-colouring c, then Bad_G(c) = ∅, contradicting (b). So χ(G) = k, and χ(G − v) ≤ k−1 < k by (a).
Now let F ⊆ E(G) with |F| ≤ r. If c were a proper (k−1)-colouring of G − F, every monochromatic edge of c
in G would lie in F. Then |Bad_G(c)| ≤ r, contradicting (b). So χ(G − F) ≥ k. Also χ(G − F) ≤ χ(G) = k,
since G − F is a subgraph of G. ∎

### Lemma 2 (gluing; SkSt25 Lemma 2.1, re-proved in full). Let k ≥ 3 and r ≥ 0. Let H be k-critical with h vertices and t ≥ 1 edges, and let G_1, …, G_t be (k,r)-graphs of orders n_1, …, n_t (repetitions allowed; use disjoint copies). Then there is a (k,r)-graph of order h + Σ_{i=1}^t (n_i − 1).

*Construction.* Enumerate E(H) = {e_1, …, e_t} and orient each edge as e_i = u_i w_i. In each G_i pick a
vertex v_i and a proper (k−1)-colouring c_i of G_i − v_i; it exists by Lemma 1(a). Put
A_i = N_{G_i}(v_i) ∩ c_i^{-1}(1) and B_i = N_{G_i}(v_i) \ A_i. Let G have vertex set V(H) ⊔ ⨆_i (V(G_i) \ {v_i}).
Its edges are: all edges of each G_i − v_i; u_i x for x ∈ A_i; and w_i x for x ∈ B_i. **No** edge of H is kept.
So |V(G)| = h + Σ(n_i − 1). Note three facts:
(F1) every edge of G lies inside a single set W_i := (V(G_i) \ {v_i}) ∪ {u_i, w_i};
(F2) the edges of G inside W_i are exactly the edges of G_i − v_i together with u_i–A_i and w_i–B_i, because
the only edges between V(H) and V(G_i) \ {v_i} come from e_i, and V(H) is independent in G;
(F3) G[W_i] is the graph G'_i of SkSt.

*Robustness: μ_{k−1}(G) ≥ min_i μ_{k−1}(G_i).* Let c : V(G) → [k−1] be any map. Restricted to V(H), c is a
(k−1)-colouring of V(H). Since χ(H) = k it is not proper on H, so some edge e_i has c(u_i) = c(w_i) =: γ.
Define φ on V(G_i) by φ = c on V(G_i) \ {v_i} and φ(v_i) = γ. Map each monochromatic edge of φ in G_i to an
edge of Bad_G(c):
- an edge xy of G_i − v_i maps to itself. It is an edge of G and is monochromatic under c.
- an edge v_i x with φ(x) = γ: if x ∈ A_i, map it to u_i x, which is in E(G) with c(u_i) = γ = c(x).
  If x ∈ B_i, map it to w_i x, which is in E(G) with c(w_i) = γ = c(x).

This map is injective. On the first type it is the identity. On the second type x determines the image, and
A_i ∩ B_i = ∅. The images of the second type have an endpoint in V(H), so they differ from those of the
first type. Hence |Bad_{G_i}(φ)| ≤ |Bad_G(c)|, so |Bad_G(c)| ≥ μ_{k−1}(G_i) ≥ min_j μ_{k−1}(G_j). Since c
was arbitrary, the claim holds. With Lemma 1(b) for each G_i, this gives μ_{k−1}(G) ≥ r + 1.

*Two-point colourings.* Fix i and distinct colours α ≠ β in [k−1]. Extend c_i by u_i ↦ 2 and w_i ↦ 1. In
G[W_i] the neighbours of u_i are A_i (colour 1 ≠ 2) and the neighbours of w_i are B_i (colours ≠ 1), by (F2).
So the extension is a proper colouring of G[W_i] with k−1 colours. Here k−1 ≥ 2, so colours 1 and 2 exist.
Compose it with a permutation π of [k−1] such that π(2) = α and π(1) = β. The result is a proper
(k−1)-colouring ψ_i^{α,β} of G[W_i] with u_i ↦ α and w_i ↦ β.

*Vertex deletions: G − v is (k−1)-colourable for each v.* By (F1), a map on V(G) \ {v} is a proper
colouring of G − v as soon as it is proper on each G[W_i] \ {v}.
- Case v ∈ V(H). Let c_H be a proper (k−1)-colouring of H − v (H is k-critical). For each i with
  v ∉ e_i, the edge e_i lies in H − v, so c_H(u_i) ≠ c_H(w_i); use ψ_i^{c_H(u_i), c_H(w_i)} on W_i. For
  each i with v ∈ e_i, say v = w_i (the case v = u_i is symmetric), pick s ≠ c_H(u_i) and use
  ψ_i^{c_H(u_i), s} restricted to W_i \ {v}. These maps agree with c_H on V(H) \ {v}, so they fit together
  into one map on V(G) \ {v}. Each piece is proper on its G[W_i] \ {v}.
- Case v ∈ V(G_j) \ {v_j}. Let c_H be a proper (k−1)-colouring of H − e_j (H is k-critical). Since
  χ(H) = k, c_H(u_j) = c_H(w_j) =: γ. Let φ_j be a proper (k−1)-colouring of G_j − v (Lemma 1(a)).
  Permute its colours so that φ_j(v_j) = γ; note v_j ≠ v. On W_j \ {v} use c_H at u_j, w_j and φ_j
  elsewhere. Edges of G_j − v_j − v are proper because φ_j is. An edge u_j x with x ∈ A_j \ {v} has x
  adjacent to v_j in G_j − v, so φ_j(x) ≠ φ_j(v_j) = γ = c_H(u_j). The same holds for w_j x with
  x ∈ B_j \ {v}. For i ≠ j, e_i ∈ H − e_j, so c_H(u_i) ≠ c_H(w_i); use ψ_i^{c_H(u_i), c_H(w_i)}. All pieces
  agree with c_H on V(H).

So (a) and (b) of Lemma 1 hold for G, and G is a (k,r)-graph. ∎

(This is SkSt25's proof, refs/skst.txt lines ~206–277, with two typos there corrected: the order sum runs to
t, not t−1, and "[1,k−1]\{j}" should read "[1,t]\{j}". I also state robustness in the slightly stronger
μ-form, which is what T3 tests.)

### Lemma 3 (f_4(n) is well defined). No (4,r)-graph on n vertices has r ≥ (n−1)/3.

*Proof.* Take any vertex v and a proper 3-colouring of G − v. N(v) splits into three colour classes. The
smallest one, X with colour γ, has |X| ≤ deg(v)/3 ≤ (n−1)/3. Let F be the set of edges from v to X. Colour v
with γ. This is a proper 3-colouring of G − F, so χ(G − F) ≤ 3 < 4 with |F| ≤ (n−1)/3. ∎

So the set of admissible r at each n is finite and f_4(n) is a maximum. Also, a (4,r)-graph is a
(4,r')-graph for every r' ≤ r. Hence **f_4(n) ≥ r ⟺ some (4,r)-graph has order n** (for r ≥ 1).

### Lemma 4 (three 4-critical graphs). K4 (h = 4, t = 6), the wheel W6 = C5 + hub (h = 6, t = 10) and the Grötzsch graph (Mycielskian of C5; h = 11, t = 20) are 4-critical.

*Proof.* VERIFIED by exhaustive computation (test T1). For each graph the solver checks that G is not
3-colourable, that every G − v is 3-colourable, and that every G − e is 3-colourable. The solver is an
exact backtracking search, cross-checked against brute force over all 3^n maps on 300 random graphs
(T0). The edge lists are saved in `out/H_graphs.txt`.

By hand for K4 and W6: K4 needs 4 colours and K4 − v = K3, K4 − e is 3-colourable. W6: the rim C5 needs
3 colours and the hub sees all of them, so χ = 4. Deleting the hub leaves C5. Deleting a rim vertex leaves
hub + P4. Deleting a rim edge leaves hub + P5. Each is 3-colourable with the hub alone in colour 3. Deleting
the spoke hub–x: colour x with 3 and the rest of the rim 1,2,1,2; the hub gets 3. ∎

### Lemma 5 (Sylvester). If p, q ≥ 1 are coprime, every integer x ≥ (p−1)(q−1) is i·p + j·q with i, j ≥ 0.

*Proof.* Since gcd(p,q) = 1, the residues j·q mod p for j = 0, …, p−1 are pairwise distinct, so one of them
is ≡ x (mod p). Then p | x − jq and x − jq ≥ (p−1)(q−1) − (p−1)q = −(p−1) > −p, so x − jq = ip with
i ≥ 0. ∎

### Lemma 6 (semigroup). Let a ≥ 1, g1 = 3+5a, g2 = 5+9a, g3 = 10+19a, and let S be the additive monoid they generate. Every integer x ≥ (g1−1)(g2−1) = (2+5a)(4+9a) lies in S.

*Proof.* 9·g1 − 5·g2 = 2, so gcd(g1, g2) | 2.
*a even:* g1 is odd, so gcd(g1, g2) = 1, and Lemma 5 applies directly.
*a odd:* g1 and g2 are both even, so gcd(g1, g2) = 2. Then p = g1/2 and q = g2/2 are coprime. By Lemma 5
every even x ≥ 2(p−1)(q−1) = (g1−2)(g2−2)/2 is in ⟨g1, g2⟩; this number is an integer since g1−2 and
g2−2 are even. Also g3 = 10 + 19a is odd. So every x ≥ X0 := g3 + (g1−2)(g2−2)/2 lies in S. An even x is
handled directly. For an odd x, x − g3 is even and ≥ (g1−2)(g2−2)/2. Finally,
2(g1−1)(g2−1) − 2X0 = (16 + 76a + 90a²) − (23 + 62a + 45a²) = 45a² + 14a − 7 > 0 for a ≥ 1, so
X0 < (g1−1)(g2−1). ∎
(T4 confirms this exactly for N = a+1 = 2..80. The true Frobenius number is at most 0.703 times the bound.)

### Lemma 7 (order propagation) ⇒ Theorem A. Let G* be a (4,r)-graph of order N and a = N − 1 (N ≥ 4, so a ≥ 3). Let T = {m ≥ 0 : a (4,r)-graph of order m+1 exists}. Then a ∈ T, and for each H in Lemma 4 with parameters (h,t), m ∈ T ⇒ m + (h−1) + (t−1)a ∈ T.

*Proof.* a ∈ T is witnessed by G*. If m ∈ T, apply Lemma 2 with k = 4 and that H. Use G_1 = a
(4,r)-graph of order m+1 and G_2 = … = G_t = copies of G*. The result has order
h + m + (t−1)a, which is (m + (h−1) + (t−1)a) + 1. ∎

The increments for K4, W6 and Grötzsch are 3+5a, 5+9a and 10+19a. By induction on the number of summands,
a + S ⊆ T. Since (2+5a)(4+9a) = (5N−3)(9N−5), Lemma 6 gives the following for every
n ≥ N + (5N−3)(9N−5): n − N ∈ S, so n − 1 = a + (n − N) ∈ T. That is, a (4,r)-graph of order n exists.
This proves **Theorem A**. ∎

### Theorem B. f_4(n) → ∞.

*Proof.* Fix r ≥ 1. By the outside input (§3) there is a finite (4,r)-graph; let N_r be its order. By
Theorem A, a (4,r)-graph exists at every order n ≥ M_r := N_r + (5N_r−3)(9N_r−5). By Lemma 3,
f_4(n) ≥ r for all n ≥ M_r. Since r was arbitrary, f_4(n) → ∞. ∎

## 3. The outside input, and what I checked about it

Statement used: **for every r ≥ 1 there is a finite graph G with χ(G) = 4, χ(G−v) < 4 for every v, and
χ(G−F) = 4 for every F ⊆ E(G) with |F| ≤ r.**

- Source file `refs/kk_solution.lean`: 9,535 lines, 459,268 bytes. Its SHA-256 is
  8bf7cd0e83463e5f304ad848921c5078d57e8f3411050e705c69a69822abecd5, which matches the hash printed in the KK
  exposition and the size Plasma recorded. VERIFIED (computed).
- **Finiteness of the witness**, VERIFIED by reading source. `erdos944_four` (l. 5362) →
  `erdos944_four_of_periodic_rigidity` → … → `erdos944_four_from_arithmetic_conditions` (l. 3382). That
  lemma obtains `G : SimpleGraph (ZMod n)` with `[NeZero n]` from `erdos944_four_of_short_compatible`
  (statement at l. 2197–2204). It then transports G along `ULift (ZMod n) ≃ ZMod n`
  (`erdos944_universe_lift`, l. 2358–2363). So the vertex type is finite, with n ≥ 1 elements.
- **Predicate match**, INFERRED from reading definitions; I did not machine-check it. The predicate
  `Erdos944.SimpleGraph.IsErdos944 G 4 r` (formal-conjectures `944.lean`; `IsCritical` and
  `IsCriticalEdges` in `FormalConjecturesForMathlib/.../Coloring/Vertex.lean`) says three things:
  χ(G) = 4; χ(⊤.deleteVerts{v}) < χ(G) for each v, and ⊤.deleteVerts{v} is G − v; and every edge set whose
  deletion lowers χ has `ncard` > r. On a finite vertex type, every F ⊆ E(G) is a finite set and `ncard` is
  its size, so |F| ≤ r forces χ(G − F) ≥ χ(G) = 4. So a witness on a finite type is a (4,r)-graph as defined
  in §0. Plasma's claim page records the same check.
- **Correctness of the k = 4 branch**: NOT checked by me. It rests on Conjectures.io's kernel acceptance and
  Plasma's rebuild and kernel replay from an empty environment (Lean v4.34.1; axioms propext,
  Classical.choice and Quot.sound only), as recorded on the Plasma claim page. Plasma notes that it traced
  only the reduction chain of the k = 4 branch by reading; the rest rests on the kernel.

## 4. Code, outputs, reproduction

- `code/mu.c`: an exact 3-colouring solver. It does backtracking for colourability and branch and bound
  for μ_3, with colour-permutation symmetry breaking.
- `code/tests.py` runs these tests:
  - T0: solver vs brute force.
  - T1: Lemma 4.
  - T2: 44 random gluings of 4-critical pieces (orders 35–64). Each glued graph has order h + Σ(n_i−1)
    and is 4-vertex-critical.
  - T3: the robustness half of Lemma 2 in μ-form, μ(glue) ≥ min μ(G_i), on 41 cases. The pieces include
    the apex graphs v + K_{m,m,m}, which have μ = m. The informative cases have all pieces with μ ≥ 2,
    and there μ(glue) = 2, 2, 2, 3.
  - T4: Lemma 6 for N = 2..80.
  - T5: the first iteration of Lemma 7 from W6 (orders 34 and 56).
- Outputs: `out/tests.log` (also `out/tests.stdout`) and `out/H_graphs.txt`.
- Reproduce:
  `cd attack/944/t1/prove/code && cc -O2 -o mu mu.c && python3 -I tests.py ../out`
  (about 18 s; ends with "ALL TESTS PASSED").

Toy-setting caveat: no small (4,r)-graph with r ≥ 1 is available. SkSt Prop 5.1 forces at least 5r+6
vertices, and the known (4,1) examples have 48 or more vertices. So the tests check the two halves of
Lemma 2 separately: vertex-criticality on 4-critical pieces (r = 0), and the μ-inequality on non-critical
pieces with μ up to 3. The proofs do not depend on the tests.

## 5. What this does and does not show

Does show:
- Theorem A, unconditionally. One (4,r)-graph of order N gives (4,r)-graphs at all orders
  ≥ N + (5N−3)(9N−5) = O(N²). The proof is complete and elementary; its pieces are SkSt's gluing lemma,
  three small 4-critical graphs and a Frobenius-number bound.
- Theorem B (f_4(n) → ∞, Erdős's quantitative question for k = 4), given the KK existence theorem.

Does not show:
- Any growth rate for f_4. The bound is f_4(n) ≥ r once n ≥ M_r = O(N_r²). N_r comes from a
  Chinese-remainder construction in the KK file and I did not extract it, so I claim nothing like
  f_4(n) ≥ n^c (scout's Target B). An explicit polynomial bound on N_r would give such a rate via Theorem A.
- Anything about the KK k = 4 proof beyond what §3 lists. I did not replay its kernel or read its argument.
  If that proof were wrong, Theorem B would be unproved, though Theorem A would still hold.
- No priority claim. The deduction is short. It reuses SkSt's Theorem 2.3 bootstrapping idea, adapted so
  that a single base graph is enough instead of a congruence family.

## 6. Notes on process

- I attempted a local Lean replay of the KK file: a wrapper importing the built FormalConjecturesForMathlib
  on the local v4.33.1 toolchain. The session's permission system refused to run it, since it would have
  executed downloaded code. I did not run it, I deleted the wrapper, and no replay is claimed.
- I wrote nothing outside this folder, and posted, committed or pushed nothing.

## 7. Sources not read

- The KK Lean file beyond the declarations cited in §3 (about 30 lines around each), in particular
  `exists_cyclic_integer_data`, `cyclic_data_periodic_rigidity` and the whole k = 4 non-colourability argument.
- The Conjectures.io record and verification pages, and Plasma's replay receipt page (I read only Plasma's
  summary of them).
- SkSt25 §3 (upper bound), §4 and the appendices (the k ≥ 5 construction), and any arXiv version after v1.
- Erdős [Er89e] (Ann. Discrete Math. 41) and the other original sources; the Chan and Kitamura Lean files;
  the veljjanoski/erdos944 repository; arXiv:2606.18462.
