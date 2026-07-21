# Lean proof dependency map

The intended machine-checked proof follows the human proof in `PROOF.md`.

```text
Block-erasure model
        |
        v
Coordinate competitors are epsilon-common
        |
        v
Maximality gives H(S_j | Omega) <= M epsilon
        |
        v
Bayes predictor error p_j <= M epsilon / 2
        |
        v
Redundancy gives KL(erasure branch || unconditional) <= R
        |
        v
Data processing gives d2(q_j || p_j) <= R
        |
        v
Exact KL certificate forces q_j < 1/4
        |
        v
Binary Fano + subadditivity
        |
        v
I(S ; Omega | erasure) > n(1-h2(1/4))
        |
        v
Exact entropy certificate and erasure decomposition
        |
        v
Contradiction with I(X1 ; Omega | X2) <= R epsilon
```

## File ownership

- `BlockErasure.lean`: deterministic variables and erasure identities.
- `Distribution.lean`: the finite probability law.
- `FiniteInformation.lean`: entropy-based conditional-information definitions.
- `Constants.lean`: exact logarithmic certificates.
- `ProofSpine.lean`: final contradiction once the bridge lemmas are available.

The next implementation file should be `WentworthLorell/Competitors.lean`, proving the two exact information identities for each coordinate competitor under the block-erasure distribution.
