import WentworthLorell.Constants

/-!
# Lean formalization of the Wentworth–Lorell counterexample

This is the entry point for the machine-checked development.

`WentworthLorell.Constants` proves the two strict numerical margins used by the
explicit factor-three counterexample without decimal approximations.
Additional files formalize the finite block-erasure construction and the
general information-theoretic contradiction.
-/

namespace WentworthLorell

#check explicit_entropy_margin
#check explicit_kl_margin

end WentworthLorell
