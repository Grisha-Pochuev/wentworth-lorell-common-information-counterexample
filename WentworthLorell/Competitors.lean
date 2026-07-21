import WentworthLorell.Distribution
import WentworthLorell.FiniteInformation

/-!
# Coordinate competitors

This file records the exact theorem interface needed for the first step of the
counterexample proof.  The concrete proofs will be filled in only after the
pushforward distributions of `(Gamma_j, X₁, X₂)` are implemented and compiled.

There are deliberately no axioms and no `sorry` declarations here.  The file
contains definitions and theorem statements expressed as predicates, so later
proof files can depend on a stable interface without pretending that the bridge
has already been verified.
-/

namespace WentworthLorell

noncomputable section

/-- The two information bounds required for a coordinate to be an
`epsilon`-common variable. -/
structure IsEpsilonCommonCoordinate (epsilon leftInfo rightInfo : ℝ) : Prop where
  left_nonnegative : 0 ≤ leftInfo
  right_nonnegative : 0 ≤ rightInfo
  left_bound : leftInfo ≤ epsilon
  right_bound : rightInfo ≤ epsilon

/-- Exact target values for a coordinate competitor in the block-erasure
model: the first conditional mutual information is zero and the second is the
erasure probability. -/
def CoordinateCompetitorIdentity (delta leftInfo rightInfo : ℝ) : Prop :=
  leftInfo = 0 ∧ rightInfo = delta

/-- Exact coordinate identities imply the required common-variable bounds. -/
theorem coordinate_identity_implies_common
    (delta leftInfo rightInfo : ℝ)
    (hdelta : 0 ≤ delta)
    (h : CoordinateCompetitorIdentity delta leftInfo rightInfo) :
    IsEpsilonCommonCoordinate delta leftInfo rightInfo := by
  rcases h with ⟨rfl, rfl⟩
  exact {
    left_nonnegative := le_rfl
    right_nonnegative := hdelta
    left_bound := hdelta
    right_bound := le_rfl
  }

end

end WentworthLorell
