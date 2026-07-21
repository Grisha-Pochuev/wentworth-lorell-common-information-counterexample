import WentworthLorell.Constants

/-!
# Algebraic proof spine

This file formalizes the final contradiction once the information-theoretic
lemmas have supplied a lower bound on information in the erasure branch and the
exact decomposition of the second redundancy term.

It contains no axioms and no `sorry`.  The remaining work is to connect the
finite probability model to the hypotheses of these theorems.
-/

namespace WentworthLorell

noncomputable section

/-- General final contradiction.

If the erasure branch carries more than `n*c` units of information, if the
unconditional redundancy term is exactly `δ` times that branch information,
and if it is nevertheless bounded by `R*δ`, then `R < n*c` is impossible.
-/
theorem contradiction_from_erasure_branch
    (R δ c branchInfo redundancyInfo : ℝ) (n : ℕ)
    (hδ : 0 < δ)
    (hbranch : (n : ℝ) * c < branchInfo)
    (hdecomp : redundancyInfo = δ * branchInfo)
    (hupper : redundancyInfo ≤ R * δ)
    (hcoefficient : R < (n : ℝ) * c) : False := by
  rw [hdecomp] at hupper
  nlinarith

/-- The explicit factor-three contradiction after the branch-information
lower bound has been proved for `n = 16`.
-/
theorem explicit_factor_three_contradiction
    (δ branchInfo redundancyInfo : ℝ)
    (hδ : 0 < δ)
    (hbranch : 16 * (1 - binaryEntropyBits (1 / 4)) < branchInfo)
    (hdecomp : redundancyInfo = δ * branchInfo)
    (hupper : redundancyInfo ≤ 3 * δ) : False := by
  exact contradiction_from_erasure_branch
    3 δ (1 - binaryEntropyBits (1 / 4)) branchInfo redundancyInfo 16
    hδ hbranch hdecomp hupper explicit_entropy_margin

/-- The KL numerical certificate rules out an erasure-branch prediction error
of at least `1/4`, once the standard binary-KL monotonicity comparison has been
established.
-/
theorem erasure_error_lt_quarter_of_comparison
    (q : ℝ)
    (hKL : binaryKLBits q (3 / (2 : ℝ) ^ 19) ≤ 3)
    (hcomparison :
      1 / 4 ≤ q →
        binaryKLBits (1 / 4) (3 / (2 : ℝ) ^ 19) ≤
          binaryKLBits q (3 / (2 : ℝ) ^ 19)) :
    q < 1 / 4 := by
  by_contra hnot
  have hq : 1 / 4 ≤ q := le_of_not_gt hnot
  have hle := hcomparison hq
  have hstrict := explicit_kl_margin
  linarith

end

end WentworthLorell
