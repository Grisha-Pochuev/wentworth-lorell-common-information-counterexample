# Reproducibility

## One-command check

From the repository root, run:

```bash
python run_checks.py
```

Python 3.11 or later is recommended. No third-party packages are required.

## What is checked mechanically

The verifier uses Python's standard-library `decimal` module at high precision. It checks:

1. the value of `1 - h2(1/4)`;
2. the explicit binary-KL barrier for `R=M=3` and `delta=2^-18`;
3. the strict final inequality for `n=16`;
4. automatic parameter selection for several other constants;
5. regression tests for monotonicity-relevant parameter conditions and exact construction identities.

## What remains a mathematical proof obligation

The script does not attempt to enumerate all possible latent variables `Omega`. That would be neither finite in a useful fixed alphabet nor a proof of the general statement.

Instead, the proof reduces every possible `Omega` to standard information-theoretic inequalities:

- maximality implies small conditional entropy for every bit;
- small binary conditional entropy implies a low-error Bayes predictor;
- conditional mutual information supplies a KL change-of-measure bound;
- KL data processing controls predictor failure on the erasure branch;
- Fano and subadditivity force linear information on that branch;
- the second redundancy condition is contradicted.

Those deductions are written in `proof/COUNTEREXAMPLE.md` and audited individually in `proof/PROOF_AUDIT.md`.

## Continuous verification

The GitHub Actions workflow runs the same command on pushes and pull requests. A green workflow means the repository's executable arithmetic and regression checks agree with the committed proof parameters.

It does not mean the bounty authors have accepted the mathematical argument.
