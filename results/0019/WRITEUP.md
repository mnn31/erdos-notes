# Erdős #19, the [Er78] function m_k at n = 3, k = 5: m_5(3) = 12

## Statement established (PROVED)

**Theorem.** Let G be a finite simple graph whose edge set is the union of m pairwise
edge-disjoint triangles. If χ(G) ≥ 8, then m ≥ 12. Also, K_9 is the union of 12 pairwise
edge-disjoint triangles (the Steiner triple system STS(9)), and χ(K_9) = 9 ≥ 8. So

  **m_5(3) = 12.**

Here m_k(n) is the least m such that some edge-disjoint union of m copies of K_n has
chromatic number at least n + k. This is the definition on erdosproblems.com/19, which
attributes it to [Er78] (VERIFIED: read in refs/page19.html). For n = 3 and k = 5 the
threshold is χ ≥ 8.

Corollary (also PROVED). The answer is still 12 if "at least 8" is read as "exactly 8".
The lower bound covers that case, and check C2 below gives 12 edge-disjoint triangles whose
union has χ exactly 8.

Since m_5(3) ≤ m_6(3) and m_6(3) = 12, this shows m_5(3) = m_6(3) = 12. (The scout gave
m_6(3) = 12. It also follows directly: χ ≥ 9 needs at least 36 edges, and K_9 = STS(9) has 36.)

## Status check before working (VERIFIED)
- Problem page (refs/page19.html, fetched 2026-11-23): defines m_k and quotes Erdős as
  having no plausible conjecture. It gives no values.
- Forum thread (refs/forum19.html, 8 comments): none of them mention m_k.
- Plasma E0019 page (refs/plasma_E0019_index.md): it cites [Er78] but says nothing about m_k.
- formal-conjectures `ErdosProblems/19.lean` (origin/main): no m_k variant.
- One web search ("edge-disjoint triangles union chromatic number 8 minimum number of triangles
  Erdős m_k Faber Lovász"): nothing on m_k values.
- The argument below is elementary: critical subgraphs, complements and degree parity. It could
  be folklore. I found no source for it, but I make **no novelty claim**.

## Notation
Graphs are finite and simple. χ is the chromatic number and δ is the minimum degree. For S ⊆ V,
G[S] is the induced subgraph. A "triangle decomposition" of G is a partition of E(G) into
edge sets of triangles.

## Lemmas

**Lemma 0 (even degrees).** If E(G) is the union of pairwise edge-disjoint triangles
T_1, …, T_m, then every vertex has even degree, and |E(G)| = 3m.

*Proof.* The edge sets E(T_i) partition E(G), and each E(T_i) has 3 edges, so |E(G)| = 3m.
Fix a vertex v. Every edge at v lies in exactly one T_i. A triangle containing v holds exactly
2 edges at v, and a triangle not containing v holds none. So deg(v) = 2·#{i : v ∈ T_i}. ∎

**Lemma 1 (dense subgraph).** If χ(G) ≥ c ≥ 1, then G has a subgraph H with χ(H) ≥ c and
δ(H) ≥ c − 1. Also |V(H)| ≥ c.

*Proof.* G is finite and is itself a subgraph with χ ≥ c. So among subgraphs H with χ(H) ≥ c
we can pick one with |V(H)| + |E(H)| minimal. Suppose some v ∈ V(H) has deg_H(v) ≤ c − 2.
Then H − v is a smaller subgraph, so χ(H − v) ≤ c − 1 by minimality. Take a proper colouring
of H − v with colours {1, …, c−1}. The neighbours of v use at most c − 2 of these colours, so
v can get a colour none of them uses. That is a proper (c−1)-colouring of H, contradicting
χ(H) ≥ c. Therefore δ(H) ≥ c − 1. Any graph has χ ≤ its number of vertices (give each vertex
its own colour), so |V(H)| ≥ χ(H) ≥ c. ∎

**Lemma 2 (8 vertices).** If H has exactly 8 vertices and χ(H) ≥ 8, then H = K_8.

*Proof.* Suppose u ≠ v are non-adjacent. Give u and v colour 1 and give the other 6 vertices
distinct colours 2, …, 7. This is a proper 7-colouring, since the only repeated colour is on a
non-adjacent pair. That contradicts χ(H) ≥ 8, so every pair is adjacent. ∎
(Computation C3: χ(K_8 − e) = 7.)

**Lemma 3 (9 vertices).** If H has exactly 9 vertices, δ(H) ≥ 7 and |E(H)| ≤ 33, then χ(H) ≤ 6.

*Proof.* Let H̄ be the complement on the same 9 vertices. Then deg_{H̄}(v) = 8 − deg_H(v) ≤ 1
for every v, so H̄ is a matching M. Its size is |M| = C(9,2) − |E(H)| = 36 − |E(H)| ≥ 3. The
two endpoints of each edge of M are non-adjacent in H, and the |M| pairs are disjoint. Give each
pair its own colour, and give each of the 9 − 2|M| unmatched vertices its own colour. This is a
proper colouring with |M| + (9 − 2|M|) = 9 − |M| ≤ 6 colours. ∎
(Computation C4: all 66,045 graphs on 9 labelled vertices with 32 or 33 edges were checked.
The 2,205 with δ ≥ 7 have maximum χ = 6.)

**Lemma 4 (parity around a K_8).** Let G have all degrees even, and let S ⊆ V(G) with
|S| = 8 and G[S] = K_8. Then |E(G)| ≥ 36.

*Proof.* G is simple and G[S] is complete, so the edges of G with both ends in S are exactly the
28 edges of K_8. For v ∈ S, let f(v) be the number of edges at v whose other end lies outside S.
Then deg_G(v) = 7 + f(v). This is even, so f(v) is odd and in particular f(v) ≥ 1. An edge
with exactly one end in S is counted once in Σ_{v∈S} f(v), so there are Σ_{v∈S} f(v) ≥ 8 such
edges. None of them is among the 28 edges inside S. Hence |E(G)| ≥ 28 + 8 = 36. ∎
(Computation `parity_k8`: K_8 plus any set of at most t extra edges, on 8 + 2t vertices,
which covers every placement up to isomorphism. For t = 2 and t = 5, none of the 742 and
244,548,276 edge sets checked makes all degrees even. As control cases, (c,t) = (4,3) and
(6,5) also give 0, while (4,4) gives 176 all-even sets, matching the analogous bound C(c,2)+c.)

## Main proof

*Lower bound.* Let G be the union of m pairwise edge-disjoint triangles with χ(G) ≥ 8. Suppose
m ≤ 11. By Lemma 0, |E(G)| = 3m ≤ 33 and all degrees of G are even. By Lemma 1 with c = 8,
there is a subgraph H with χ(H) ≥ 8, δ(H) ≥ 7 and |V(H)| ≥ 8. By the handshake identity,
7|V(H)| ≤ Σ deg_H = 2|E(H)| ≤ 2|E(G)| ≤ 66, so |V(H)| ≤ 9.
- If |V(H)| = 9, then |E(H)| ≤ 33, so Lemma 3 gives χ(H) ≤ 6. This contradicts χ(H) ≥ 8.
- If |V(H)| = 8, Lemma 2 gives H = K_8. So with S = V(H), G[S] contains every pair and
  G[S] = K_8. Lemma 4 then gives |E(G)| ≥ 36 > 33, a contradiction.

So m ≥ 12.

*Upper bound.* Take the 9 points of the affine plane AG(2,3), i.e. Z_3², and its 12 lines. Each
pair of points lies on exactly one line, so the 12 lines are pairwise edge-disjoint triangles
whose union is K_9, and χ(K_9) = 9 ≥ 8. Computation C1 checks this exactly, and the triangles
are saved in out/objects.json under "sts9".

*Exactly 8.* Computation C2 gives 12 edge-disjoint triangles: a triangle decomposition of
K_8 minus the perfect matching {01, 23, 45, 67}, plus the four triangles {0,1,8}, {2,3,9},
{4,5,10}, {6,7,11}. Their union contains K_8 and has χ = 8, computed exactly. The object is
saved in out/objects.json under "chi_exactly_8_example". ∎

## Toy-setting / analogue tests (consistency, not part of the proof)
- C5: the 7-vertex analogue of the Lemma 2 + 3 step for c = 4 and c = 6. Every graph in the
  networkx graph atlas (all graphs on ≤ 7 vertices) with χ ≥ c and ≤ C(c,2)+c−3 edges contains
  K_c. That is 9 graphs for c = 4 and 5 for c = 6, with 0 exceptions.
- The same template gives m_3(3) ≥ 7: χ ≥ 6 forces K_6 (with ≤ 20 edges the dense subgraph has
  ≤ 8 vertices. On 7 vertices the complement is a matching, so χ ≥ 6 forces K_6. On 8 vertices
  the graph is 5-regular, its complement is 2-regular, and then χ ≤ 4). Parity then needs
  ≥ 21 edges. This matches the scout's brute-force value m_3(3) = 7 (K_7 = Fano). I checked it
  by hand and only partly by code (C5 covers the 7-vertex case, parity_k8 the parity part).

## Code and reproduction
Directory: attack/19/t1/prove

```
cd attack/19/t1/prove/code
cc -O2 -o parity_k8 parity_k8.c
bash -c 'for a in "4 3" "4 4" "6 5" "8 2" "8 5"; do ./parity_k8 $a; done' > ../out/parity_k8.txt
python3 -I checks.py        # writes ../out/checks.txt and ../out/objects.json
```
Outputs: out/parity_k8.txt (about 4 s total) and out/checks.txt (about 1 s). Chromatic numbers
are exact, computed by exhaustive backtracking. The decomposition checks assert pairwise
edge-disjointness and the exact union edge set.

## What this does and does not show
- DOES: it proves m_5(3) = 12, under both the "χ ≥ 8" reading (the page's wording) and the
  "χ = 8" reading. The proof is self-contained and uses only Lemmas 0–4, each proved above and
  each also checked by exhaustive computation in its own finite range. Lemmas 2 and 3 are proved
  by hand, and the computer checks are redundant confirmation. Lemma 4's count is proved by hand,
  and `parity_k8` only confirms it for at most 5 extra edges.
- DOES NOT: it says nothing about m_k(3) for k = 7, 8, … or about m_k(n) for n ≥ 4, and nothing
  about Erdős's general question of how m_k behaves. For k = 7 (χ ≥ 10) the same template gives
  a lower bound, but I did not write it up or check it. K_10 minus a perfect matching has no
  triangle decomposition (10 ≢ 0, 2 mod 6), so the matching upper-bound construction is not
  available there and the true value needs a separate search. This value is a small case. I
  found no source for it, but given how elementary it is, it may be known or folklore. It
  should not be presented as a new result without that caveat.
- The reduction rests on Erdős's definition as quoted on the page: "edge-disjoint union of m_k
  copies of K_n ... chromatic number at least n+k". I did not read [Er78] itself.

## Sources not read
- [Er78] Erdős, Problems and results in combinatorial analysis and graph theory (the original
  definition of m_k). Only the erdosproblems.com paraphrase was read.
- Hindman [Hi81], KKKMO21/KKKMO24, Kahn [Ka92]: not needed for this argument, not read.
- Gallai/Dirac results on critical graphs with few edges: mentioned in the brief, not used. The
  argument avoids them through Lemmas 1–3.
- ryantuck/erdos-ai was not searched beyond its top-level listing.
