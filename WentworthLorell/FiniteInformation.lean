import Shannon.Entropy.Properties

/-!
# Finite conditional information

The external `Shannon` dependency provides finite probability distributions,
Shannon entropy, conditional entropy, the entropy chain rule, nonnegativity, and
subadditivity.  This file adds the three-variable marginals and the entropy
formula for conditional mutual information used by the counterexample.

The ambient joint distribution is stored on `((A × B) × C)`.
-/

namespace WentworthLorell

noncomputable section

open Shannon

variable {A B C : Type} [Fintype A] [Fintype B] [Fintype C]

/-- Reorder `(A,B,C)` as `(A,C,B)`. -/
def acbEquiv : ((A × B) × C) ≃ ((A × C) × B) where
  toFun x := ((x.1.1, x.2), x.1.2)
  invFun x := ((x.1.1, x.2), x.1.2)
  left_inv := by
    rintro ⟨⟨a, b⟩, c⟩
    rfl
  right_inv := by
    rintro ⟨⟨a, c⟩, b⟩
    rfl

/-- Reorder `(A,B,C)` as `(B,C,A)`. -/
def bcaEquiv : ((A × B) × C) ≃ ((B × C) × A) where
  toFun x := ((x.1.2, x.2), x.1.1)
  invFun x := ((x.2, x.1.1), x.1.2)
  left_inv := by
    rintro ⟨⟨a, b⟩, c⟩
    rfl
  right_inv := by
    rintro ⟨⟨b, c⟩, a⟩
    rfl

/-- The `(A,B)` marginal of a distribution on `(A,B,C)`. -/
def marginalAB (p : ProbDist ((A × B) × C)) : ProbDist (A × B) :=
  marginalFst p

/-- The `C` marginal of a distribution on `(A,B,C)`. -/
def marginalC (p : ProbDist ((A × B) × C)) : ProbDist C :=
  marginalSnd p

/-- The `(A,C)` marginal, obtained by relabeling and taking a first marginal. -/
def marginalAC (p : ProbDist ((A × B) × C)) : ProbDist (A × C) :=
  marginalFst (relabelProb (acbEquiv (A := A) (B := B) (C := C)) p)

/-- The `(B,C)` marginal, obtained by relabeling and taking a first marginal. -/
def marginalBC (p : ProbDist ((A × B) × C)) : ProbDist (B × C) :=
  marginalFst (relabelProb (bcaEquiv (A := A) (B := B) (C := C)) p)

/-- Conditional mutual information in natural-log units:

`I(A;B | C) = H(A,C) + H(B,C) - H(C) - H(A,B,C)`.

The choice of natural rather than base-two logarithms multiplies every
information quantity by the same positive constant and therefore does not
change any zero statement or linear contradiction.
-/
def conditionalMutualInfo (p : ProbDist ((A × B) × C)) : ℝ :=
  entropyNat (marginalAC p) + entropyNat (marginalBC p) -
    entropyNat (marginalC p) - entropyNat p

@[simp] theorem conditionalMutualInfo_eq (p : ProbDist ((A × B) × C)) :
    conditionalMutualInfo p =
      entropyNat (marginalAC p) + entropyNat (marginalBC p) -
        entropyNat (marginalC p) - entropyNat p := rfl

/-- The existing finite entropy chain rule, specialized to the grouping
`(A,B)` followed by `C`. -/
theorem entropyABC_chain_rule (p : ProbDist ((A × B) × C)) :
    entropyNat p = entropyNat (marginalAB p) + condEntropy p := by
  simpa [marginalAB] using chain_rule p

/-- Conditional entropy of `C` given `(A,B)` is nonnegative. -/
theorem condEntropyC_given_AB_nonneg (p : ProbDist ((A × B) × C)) :
    0 ≤ condEntropy p :=
  condEntropy_nonneg p

end

end WentworthLorell
