import Shannon.Entropy.Properties

/-!
# Exact analytic certificates for the explicit counterexample

The human-readable proof uses the numerical inequalities

* `16 * (1 - h₂(1/4)) > 3`, and
* `d₂(1/4 || 3 * 2⁻¹⁹) > 3`.

This file proves them without decimal approximations.  Logarithms are natural
inside the definitions and division by `log 2` converts to bits.
-/

namespace WentworthLorell

noncomputable section

open Real

/-- Binary entropy measured in bits. -/
def binaryEntropyBits (p : ℝ) : ℝ :=
  (-p * Real.log p - (1 - p) * Real.log (1 - p)) / Real.log 2

/-- Binary KL divergence measured in bits. -/
def binaryKLBits (q p : ℝ) : ℝ :=
  (q * Real.log (q / p) + (1 - q) * Real.log ((1 - q) / (1 - p))) / Real.log 2

lemma log_two_pos : 0 < Real.log 2 := Real.log_pos (by norm_num)

/-- The exact integer inequality behind the entropy margin. -/
lemma entropy_integer_certificate : (2 : ℝ) ^ 19 < (3 : ℝ) ^ 12 := by
  norm_num

/-- Taking logarithms of the integer certificate. -/
lemma entropy_log_certificate : 19 * Real.log 2 < 12 * Real.log 3 := by
  have h := Real.log_lt_log (by positivity : (0 : ℝ) < (2 : ℝ) ^ 19)
    entropy_integer_certificate
  simpa [Real.log_pow] using h

lemma log_quarter : Real.log (1 / 4 : ℝ) = -2 * Real.log 2 := by
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_one]
  norm_num [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]

lemma log_three_quarters : Real.log (3 / 4 : ℝ) = Real.log 3 - 2 * Real.log 2 := by
  rw [Real.log_div (by norm_num) (by norm_num)]
  norm_num [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]

/-- Closed form for the entropy at `1/4`. -/
lemma binaryEntropyBits_quarter :
    binaryEntropyBits (1 / 4) = 2 - (3 / 4) * (Real.log 3 / Real.log 2) := by
  rw [binaryEntropyBits]
  norm_num [log_quarter, log_three_quarters]
  field_simp [ne_of_gt log_two_pos]
  ring

/-- Exact Lean proof of `16 * (1 - h₂(1/4)) > 3`. -/
theorem explicit_entropy_margin :
    3 < 16 * (1 - binaryEntropyBits (1 / 4)) := by
  rw [binaryEntropyBits_quarter]
  have hlog := entropy_log_certificate
  have h2 := log_two_pos
  field_simp [ne_of_gt h2]
  nlinarith

/-- A simple strict lower bound used for the KL certificate. -/
lemma one_lt_log_thirtytwo_thirds : 1 < Real.log (32 / 3 : ℝ) := by
  have h := Real.lt_log_one_add_of_pos (show (0 : ℝ) < 29 / 3 by norm_num)
  norm_num at h ⊢
  nlinarith

lemma first_kl_log :
    Real.log ((1 / 4 : ℝ) / (3 / (2 : ℝ) ^ 19)) =
      17 * Real.log 2 - Real.log 3 := by
  have hratio : ((1 / 4 : ℝ) / (3 / (2 : ℝ) ^ 19)) = (2 : ℝ) ^ 17 / 3 := by
    norm_num
  rw [hratio, Real.log_div (by positivity) (by norm_num), Real.log_pow]
  norm_num

/-- Exact Lean proof of the KL margin used by the factor-three instance. -/
theorem explicit_kl_margin :
    3 < binaryKLBits (1 / 4) (3 / (2 : ℝ) ^ 19) := by
  let p : ℝ := 3 / (2 : ℝ) ^ 19
  have hp : 0 < p := by dsimp [p]; positivity
  have hp1 : p < 1 := by dsimp [p]; norm_num
  have hr : 0 < (1 - (1 / 4 : ℝ)) / (1 - p) := by positivity
  have hsecond := Real.one_sub_inv_le_log_of_pos hr
  have hlog : 1 < 5 * Real.log 2 - Real.log 3 := by
    have h32 := one_lt_log_thirtytwo_thirds
    have hrewrite : Real.log (32 / 3 : ℝ) = 5 * Real.log 2 - Real.log 3 := by
      rw [show (32 : ℝ) = 2 ^ 5 by norm_num, Real.log_div (by positivity) (by norm_num),
        Real.log_pow]
      norm_num
    rwa [hrewrite] at h32
  rw [binaryKLBits]
  change 3 < ((1 / 4 : ℝ) * Real.log ((1 / 4 : ℝ) / p) +
    (1 - (1 / 4 : ℝ)) * Real.log ((1 - (1 / 4 : ℝ)) / (1 - p))) / Real.log 2
  rw [show p = 3 / (2 : ℝ) ^ 19 by rfl, first_kl_log]
  have h2 := log_two_pos
  have hsecond' :
      -(1 / 3 : ℝ) + 4 * p / 3 ≤
        Real.log ((1 - (1 / 4 : ℝ)) / (1 - p)) := by
    convert hsecond using 1 <;> field_simp [ne_of_gt hp, ne_of_gt (sub_pos.mpr hp1)] <;> ring
  apply (lt_div_iff₀ h2).2
  nlinarith

end

end WentworthLorell
