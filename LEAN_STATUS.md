# Lean formalization status

This branch contains a prepared Lean 4 formalization project. It has **not yet been compiled**, because all available GitHub Actions runner capacity is currently reserved for another project.

## Prepared

- Lean 4.28 toolchain pinned in `lean-toolchain`.
- The finite-entropy dependency pinned to an exact commit in `lakefile.toml`.
- `WentworthLorell/BlockErasure.lean`: deterministic block-erasure construction.
- `WentworthLorell/Distribution.lean`: uniform block and independent Bernoulli erasure distribution.
- `WentworthLorell/FiniteInformation.lean`: finite three-variable marginals and conditional mutual information.
- `WentworthLorell/Constants.lean`: exact, non-decimal certificates for both factor-three numerical margins.
- `WentworthLorell/ProofSpine.lean`: final contradiction logic without axioms or `sorry`.
- `--no-sorries` enabled for the Lean library.

## Still required for a complete formal proof

The remaining mathematical bridge must formalize, for an arbitrary finite latent variable `Omega`:

1. maximality implies a small conditional entropy for every coordinate bit;
2. small binary conditional entropy gives a low-error predictor;
3. the first redundancy condition yields the erasure-branch KL bound;
4. KL data processing bounds predictor error on the erasure branch;
5. binary Fano and conditional subadditivity give the branch-information lower bound;
6. the second redundancy condition equals the erasure probability times the branch information.

Only after these lemmas are proved and `lake build` succeeds with `--no-sorries` should this branch be described as a complete Lean verification.

## Later verification command

```bash
lake update
lake build
```

No GitHub Actions workflow is present, so this branch cannot consume runner capacity automatically.
