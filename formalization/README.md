# Formalization boundary and Lean roadmap

A full proof-assistant formalization is desirable, but this repository does not claim to contain one yet.

## Why a tiny arithmetic Lean file is not enough

The load-bearing content is not merely

```text
3.019550008... > 3.
```

A faithful formalization must connect:

1. finite probability distributions;
2. conditional entropy and conditional mutual information;
3. KL divergence and its conditional expansion;
4. data processing for KL divergence;
5. Bayes-optimal binary prediction;
6. the entropy/error inequality `H >= 2 p_error`;
7. binary Fano;
8. conditional entropy subadditivity;
9. the block-erasure construction.

Formalizing only the decimal margins would verify the least controversial part and risk overstating the assurance obtained.

## Proposed Lean spine

A useful staged formalization would be:

### Stage 1: finite distribution construction

Define finite types for `S`, `E`, `X1`, and `X2`, and prove the exact identities for each competitor `Gamma_j=Sj`.

### Stage 2: information-theoretic library bridge

Identify or build reusable definitions and lemmas for finite Shannon entropy, conditional mutual information, and KL divergence with base-2 normalization.

### Stage 3: predictor lemmas

Formalize Bayes error for a binary variable and prove:

```text
H(B | Y) >= 2 * p_error(B | Y).
```

Formalize binary Fano in the direction used here.

### Stage 4: change of measure

Prove the erasure-branch KL bound and apply data processing to the error indicator.

### Stage 5: assemble the theorem

Formalize the general quantifier statement for arbitrary fixed finite `R` and `M`, then derive the explicit `R=M=3` corollary.

## Present source of truth

Until that spine is complete, the source of truth is the human-readable proof plus the independent audit and deterministic arithmetic verifier.

Contributions toward a full Lean formalization are welcome.
