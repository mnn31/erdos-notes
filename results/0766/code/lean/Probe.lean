import Mathlib
open scoped SimpleGraph
example : True := by
  trivial
#check @Set.exists_subset_card_eq
#check @Set.ncard_insert_of_notMem
#check @Set.Subsingleton.preimage
#check @Set.ncard_le_one_iff_subsingleton
#check @Set.ncard_union_le
#check @SimpleGraph.edgeSet_sup
#check @SimpleGraph.edgeSet_edge_of_ne
#check @SimpleGraph.edge_adj
#check @SimpleGraph.Copy
#check @SimpleGraph.comap_adj
#check @strictMonoOn_Iic_of_lt_succ
#check @Set.nonempty_of_ncard_ne_zero
#check @Sym2.mem_diagSet
#check @SimpleGraph.not_isDiag_of_mem_edgeSet
