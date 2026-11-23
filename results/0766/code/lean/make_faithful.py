# Builds Erdos766Faithful.lean: the verbatim formal-conjectures origin/main 766.lean with
# (i) the module header made non-module (`module`, `public import`, `@[expose] public section` removed),
# (ii) the helper lemmas of Erdos766PartsII.lean inserted before parts.ii,
# (iii) the `sorry` of parts.ii replaced by the proof. Nothing else is changed.
import sys
src, proof, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()
p = open(proof).read()
helpers = p[p.index("section\nvariable {n k : ℕ}"):p.index("end\n\ntheorem erdos_766.parts.ii")+4]
s = s.replace("module\n\npublic import FormalConjecturesUtil", "import FormalConjecturesUtil", 1)
s = s.replace("@[expose] public section\n", "", 1)
stmt = """theorem erdos_766.parts.ii :
    ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
      StrictMonoOn (forcingNumber n k) (Set.Ioc k (k ^ 2 / 4)) := by
  sorry"""
assert s.count(stmt) == 1
newproof = """theorem erdos_766.parts.ii :
    ∀ k : ℕ, ∀ᶠ n : ℕ in atTop,
      StrictMonoOn (forcingNumber n k) (Set.Ioc k (k ^ 2 / 4)) := by
  intro k
  rw [Filter.eventually_atTop]
  exact ⟨k, fun n hn => (forcingNumber_strictMonoOn_Iic hn).mono (Ioc_subset_Iic_choose k)⟩"""
anchor = "/--\nFor fixed $k$ and large $n$ is $f(n;k,l)$ a strictly monotone function of $l$?"
assert s.count(anchor) == 1
s = s.replace(anchor, helpers + "\n\n" + anchor, 1)
s = s.replace(stmt, newproof, 1)
s += "\n#print axioms Erdos766.erdos_766.parts.ii\n"
open(out, "w").write(s)
