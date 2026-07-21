import Shannon.Entropy.Properties

/-!
# Lean formalization of the Wentworth–Lorell counterexample

This file is the entry point for the machine-checked development.
The first milestone checks that the external finite-entropy library is pinned
and available reproducibly. The counterexample theorem is developed in the
files under `WentworthLorell/`.
-/

namespace WentworthLorell

open Shannon

example {α : Type} [Fintype α] (p : ProbDist α) :
    0 ≤ entropyNat p :=
  entropyNat_nonneg p

end WentworthLorell
