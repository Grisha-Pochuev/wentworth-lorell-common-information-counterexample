import WentworthLorell.BlockErasure
import Shannon.Entropy.Joint

/-!
# Probability distribution of the block-erasure model

This file defines the concrete finite probability distribution used in the
counterexample.  The hidden bit block is uniform, the erasure flag is
Bernoulli with parameter `δ`, and the two are independent by construction.
-/

namespace WentworthLorell

noncomputable section

open Shannon

/-- Uniform probability distribution on an arbitrary nonempty finite type. -/
def uniformOn (α : Type) [Fintype α] [Nonempty α] : ProbDist α := by
  refine ⟨fun _ => 1 / (Fintype.card α : ℝ), ?_⟩
  constructor
  · intro _
    positivity
  · have hcard : (Fintype.card α : ℝ) ≠ 0 := by
      exact_mod_cast Fintype.card_ne_zero
    simp [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, hcard]

/-- Uniform distribution on all `n`-bit strings. -/
def uniformBitBlock (n : ℕ) : ProbDist (BitBlock n) :=
  uniformOn (BitBlock n)

/-- Bernoulli distribution on the erasure flag, where `true` has mass `δ`. -/
def erasureDistribution (δ : ℝ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) : ProbDist Bool := by
  refine ⟨fun e => if e then δ else 1 - δ, ?_⟩
  constructor
  · intro e
    cases e <;> simp [hδ0, hδ1]
  · norm_num

/-- Joint hidden-state distribution: a uniform bit block independent of the
Bernoulli erasure flag. -/
def hiddenDistribution (n : ℕ) (δ : ℝ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) :
    ProbDist (HiddenState n) :=
  prodDist (uniformBitBlock n) (erasureDistribution δ hδ0 hδ1)

/-- The bit block and erasure flag are independent by construction. -/
theorem hiddenDistribution_independent
    (n : ℕ) (δ : ℝ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1) :
    IsIndependent (hiddenDistribution n δ hδ0 hδ1) := by
  intro s e
  simp [hiddenDistribution, IsIndependent, marginalFst_prodDist, marginalSnd_prodDist]

/-- Every hidden state has the expected product mass. -/
theorem hiddenDistribution_apply
    (n : ℕ) (δ : ℝ) (hδ0 : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (s : BitBlock n) (e : Bool) :
    hiddenDistribution n δ hδ0 hδ1 (s, e) =
      uniformBitBlock n s * erasureDistribution δ hδ0 hδ1 e := rfl

end

end WentworthLorell
