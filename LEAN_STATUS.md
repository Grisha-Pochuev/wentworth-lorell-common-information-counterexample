# Lean formalization status

The prepared Lean 4 project compiles successfully on GitHub with Lean 4.28.0 and the dependency revisions pinned in this repository.

## Machine-checked now

- deterministic block-erasure construction;
- uniform block distribution and independent Bernoulli erasure distribution;
- finite three-variable marginals and the entropy formula used for conditional mutual information;
- the elementary coordinate-competitor interface;
- exact, non-decimal proofs of both factor-three numerical margins;
- the final algebraic contradiction once the information-theoretic bridge hypotheses are supplied.

The project is compiled with `-DwarningAsError=true`. Therefore a use of `sorry` in the project would fail the build, as would any other Lean warning.

## Not yet a complete formalization of the full counterexample theorem

The following bridge remains to be formalized for an arbitrary finite latent variable `Omega`:

1. maximality implies a small conditional entropy for every coordinate bit;
2. small binary conditional entropy gives a low-error predictor;
3. the first redundancy condition yields the erasure-branch KL bound;
4. KL data processing bounds predictor error on the erasure branch;
5. binary Fano and conditional subadditivity give the branch-information lower bound;
6. the second redundancy condition equals the erasure probability times the branch information.

Consequently, the current Lean code is a compiled and checked proof spine, not yet a machine-checked proof of every information-theoretic step in `PROOF.md`.

## Reproduce

```bash
lake update
lake build
```

The first fully successful strict build was GitHub Actions run `29847167109` in draft pull request #4.
