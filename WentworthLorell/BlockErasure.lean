import Mathlib

/-!
# The finite block-erasure construction

This file formalizes the deterministic part of the counterexample: the hidden
bit block, the erasure flag, the two observations, and elementary identities
showing exactly what the second observation reveals.

No probabilistic or information-theoretic claims are made here. Those are
layered on top of this construction in later files.
-/

namespace WentworthLorell

/-- An `n`-bit string. -/
abbrev BitBlock (n : ℕ) := Fin n → Bool

/-- The first observation always reveals the full block. -/
def firstObservation {n : ℕ} (s : BitBlock n) : BitBlock n := s

/-- The second observation either reveals the full block or returns an erasure. -/
def secondObservation {n : ℕ} (erased : Bool) (s : BitBlock n) : Option (BitBlock n) :=
  if erased then none else some s

/-- The `j`th coordinate competitor. -/
def coordinate {n : ℕ} (j : Fin n) (s : BitBlock n) : Bool := s j

@[simp] theorem firstObservation_eq {n : ℕ} (s : BitBlock n) :
    firstObservation s = s := rfl

@[simp] theorem secondObservation_erased {n : ℕ} (s : BitBlock n) :
    secondObservation true s = none := by
  simp [secondObservation]

@[simp] theorem secondObservation_visible {n : ℕ} (s : BitBlock n) :
    secondObservation false s = some s := by
  simp [secondObservation]

/-- The output itself determines whether erasure occurred. -/
theorem secondObservation_isNone {n : ℕ} (erased : Bool) (s : BitBlock n) :
    (secondObservation erased s).isNone = erased := by
  cases erased <;> simp [secondObservation]

/-- A visible observation is exactly the original block. -/
theorem secondObservation_eq_some_iff {n : ℕ}
    (erased : Bool) (s t : BitBlock n) :
    secondObservation erased s = some t ↔ erased = false ∧ s = t := by
  cases erased <;> simp [secondObservation]

/-- Erasure is the only way the second observation can be `none`. -/
theorem secondObservation_eq_none_iff {n : ℕ}
    (erased : Bool) (s : BitBlock n) :
    secondObservation erased s = none ↔ erased = true := by
  cases erased <;> simp [secondObservation]

/-- On the non-erasure branch the second observation determines every bit. -/
theorem coordinate_of_visible_observation {n : ℕ}
    (j : Fin n) (s t : BitBlock n)
    (h : secondObservation false s = some t) :
    coordinate j s = coordinate j t := by
  have hst : s = t := by
    simpa [secondObservation] using h
  simpa [coordinate, hst]

/-- The complete finite hidden state used by the probability model. -/
abbrev HiddenState (n : ℕ) := BitBlock n × Bool

/-- First observed variable as a deterministic function of the hidden state. -/
def X₁ {n : ℕ} (z : HiddenState n) : BitBlock n := z.1

/-- Second observed variable as a deterministic function of the hidden state. -/
def X₂ {n : ℕ} (z : HiddenState n) : Option (BitBlock n) :=
  secondObservation z.2 z.1

/-- Erasure flag recovered from the second observation. -/
def erasureFromX₂ {n : ℕ} (x : Option (BitBlock n)) : Bool := x.isNone

@[simp] theorem erasureFromX₂_X₂ {n : ℕ} (z : HiddenState n) :
    erasureFromX₂ (X₂ z) = z.2 := by
  exact secondObservation_isNone z.2 z.1

end WentworthLorell
