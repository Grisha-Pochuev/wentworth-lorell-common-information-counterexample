import WentworthLorell.BlockErasure
import WentworthLorell.Distribution
import WentworthLorell.FiniteInformation
import WentworthLorell.Competitors
import WentworthLorell.Constants
import WentworthLorell.ProofSpine

/-!
# Lean formalization of the Wentworth–Lorell counterexample

This is the entry point for the formal development.

Prepared modules:

* `BlockErasure`: the exact finite deterministic construction;
* `Distribution`: the uniform block and independent Bernoulli erasure law;
* `FiniteInformation`: finite three-variable marginals and conditional mutual information;
* `Competitors`: the exact interface for coordinate common variables;
* `Constants`: exact analytic certificates for the explicit factor-three margins;
* `ProofSpine`: the final contradiction assembled without axioms or `sorry`.

The remaining formalization work is to prove the information-theoretic bridge
lemmas connecting an arbitrary candidate `Omega` to the hypotheses in
`ProofSpine`. The project has deliberately not been labelled complete before
those lemmas compile under Lean.
-/

namespace WentworthLorell

-- These checks make every prepared module part of the compilation audit.
#check secondObservation_isNone
#check hiddenDistribution_independent
#check conditionalMutualInfo
#check coordinate_identity_implies_common
#check explicit_entropy_margin
#check explicit_kl_margin
#check explicit_factor_three_contradiction

end WentworthLorell
