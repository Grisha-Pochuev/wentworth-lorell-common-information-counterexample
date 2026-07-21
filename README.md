# A Block-Erasure Counterexample to Approximately Deterministic Maximal Common Information

> **Current status:** a complete self-contained counterexample proof is included in this repository. The arithmetic checks pass automatically. External review and acceptance by the bounty authors are still pending.

This repository is part of my personal project **The Open Mathematics Project**.

The idea of the project is simple: mathematical work should be open, readable, reusable, and independently checkable. A result should not appear only as a final claim. The definitions, proof, numerical margins, verification scripts, limitations, and remaining review status should all be visible.

This repository studies the Wentworth–Lorell bounty problem:

> Does every pair of finite random variables admit an approximately deterministic maximal redund with errors bounded by universal constant multiples of the allowed redundancy error?

The original bounty page is:

- John Wentworth and David Lorell, **“Does An (Approximately) Deterministic Maximal Redund Always Exist?”**  
  https://www.lesswrong.com/posts/sCNdkuio62Fi9qQZK/usd500-usd500-bounty-problem-does-an-approximately

As of the authors' 22 August 2025 edit, the remaining advertised bounty is **$500**.

## The problem in ordinary language

Suppose two observers, `X1` and `X2`, each contain nearly the same information about some hidden feature `Gamma`.

The hoped-for theorem says that there should be one master variable `Omega` with three properties:

1. `Omega` is itself nearly recoverable from either observer;
2. `Omega` contains essentially everything that any other approximately shared variable contains;
3. `Omega` is almost determined by the observed pair `(X1, X2)`.

In the exact zero-error case, such a master variable exists. It is the connected-component label in the bipartite support graph of the joint distribution. The bounty asks whether this exact construction has a stable approximate analogue with dimension-free linear error bounds.

Why is this interesting? A positive theorem would provide a canonical summary of shared information. In the natural-latents programme, that could simplify comparisons between different probabilistic models and help explain when two different representations are really talking about the same underlying feature.

## Main result claimed here

The proposed dimension-free linear theorem is false.

For every pair of fixed finite constants `R` and `M`, there are finite random variables `X1, X2` and an error tolerance `epsilon` for which no variable `Omega` can simultaneously satisfy:

```text
I(Omega ; X2 | X1) <= R epsilon,
I(Omega ; X1 | X2) <= R epsilon,
```

and, for every competing `epsilon`-redund `Gamma`,

```text
I((X1, X2) ; Gamma | Omega) <= M epsilon.
```

The approximate-determinism requirement is not used. Therefore the obstruction is stronger than needed: maximality and approximate redundancy already conflict.

## The counterexample in one picture

Let `S = (S1, ..., Sn)` be a uniformly random `n`-bit string.

- `X1` always sees all of `S`.
- `X2` sees all of `S` with probability `1 - epsilon`.
- With probability `epsilon`, `X2` sees only an erasure symbol `⊥`.

Each individual bit `Sj` is an allowed approximate redund:

```text
I(Sj ; X2 | X1) = 0,
I(Sj ; X1 | X2) = epsilon.
```

So a maximal `Omega` must preserve almost every bit `Sj`. But on the rare erasure branch, `X2` knows none of the string. If `Omega` still preserves all `n` bits there, then

```text
I(X1 ; Omega | X2)
```

is of order `n epsilon`, not merely a fixed constant times `epsilon`.

The rigorous proof shows that `Omega` cannot hide its information only on the erasure branch without violating its other redundancy condition. This is the key step.

## Explicit failure of the proposed factor 3

All information quantities are measured in bits. Take

```text
R = 3,
M = 3,
epsilon = 2^-18,
n = 16.
```

The proof gives

```text
I(X1 ; Omega | X2)
  > epsilon * 16 * (1 - h2(1/4))
  = epsilon * 3.019550008...
  > 3 epsilon.
```

Thus the factor-3 version cannot hold. The same construction defeats every fixed finite pair of constants after choosing a smaller erasure probability and a larger block length.

## Current verification level

| Layer | Status | Where |
|---|---|---|
| Popular explanation | complete | this README |
| Exact problem statement | complete | `docs/PROBLEM_STATEMENT.md` |
| General counterexample theorem | complete draft | `proof/COUNTEREXAMPLE.md` |
| Line-by-line proof audit | complete | `proof/PROOF_AUDIT.md` |
| High-precision numerical margins | automated | `python run_checks.py` |
| Regression tests | automated | `tests/test_verifier.py` |
| GitHub Actions verification | configured | `.github/workflows/verify.yml` |
| Full proof-assistant formalization | not yet complete | `formalization/README.md` |
| Independent human review | pending | external |
| Bounty-author acceptance | pending | external |

The distinction between a complete proof draft and an accepted solution is intentional. The repository records what has been proved internally and what still depends on external review.

## Reproduce the checks

No external Python packages are required. Python 3.11 or later is recommended.

```bash
python run_checks.py
```

The command:

1. recomputes the binary-entropy constant at high precision;
2. verifies the KL-divergence barrier used on the erasure branch;
3. verifies the explicit `R = M = 3`, `epsilon = 2^-18`, `n = 16` contradiction;
4. independently enumerates a small finite block-erasure distribution and recomputes the competitor mutual informations;
5. runs independent regression tests;
6. searches for valid parameters for several other fixed constants.

The script does **not** replace the proof. It checks every numerical and parameter-selection claim on which the explicit instance depends. The information-theoretic deductions are laid out separately in the proof and audit files.

## Repository layout

```text
README.md                    Popular introduction and current status.
START_HERE.md                Short navigation for reviewers.
run_checks.py                One-command reproducibility entry point.
docs/PROBLEM_STATEMENT.md    Precise formulation of the bounty problem.
docs/REPRODUCIBILITY.md      What is and is not mechanically checked.
proof/COUNTEREXAMPLE.md      Full general proof.
proof/PROOF_AUDIT.md         Dependency and edge-case audit.
tools/verify_counterexample.py
                             High-precision arithmetic verifier.
tools/finite_model_check.py  Independent finite-distribution enumeration.
tests/test_verifier.py       Independent regression tests.
formalization/README.md      Honest formalization boundary and Lean roadmap.
.github/workflows/verify.yml Automatic verification on GitHub.
```

## Why no pretend Lean proof?

A useful formal proof must cover conditional entropy, conditional mutual information, KL divergence, data processing, Bayes error, and Fano's inequality in one coherent probability library. Formalizing only the decimal inequality `3.01955 > 3` would add little confidence while looking more impressive than it is.

For now the source of truth is:

- a self-contained mathematical proof;
- a separate proof audit;
- a deterministic high-precision arithmetic check;
- automatic tests on every commit.

The exact boundary and a staged Lean plan are recorded in `formalization/README.md`.

## Limitations

This counterexample rules out bounds of the form

```text
constant * epsilon
```

with constants independent of the alphabet size or block length.

It does not rule out:

- bounds depending on dimension or entropy;
- nonlinear bounds in the allowed redundancy error;
- positive theorems under additional structural assumptions;
- restricted distribution classes motivated by applications.

Those remain legitimate directions after the dimension-free linear conjecture fails.

## Project philosophy

This repository follows the spirit of **The Open Mathematics Project**:

- explain the problem before presenting machinery;
- separate theorem, computation, and speculation;
- publish exact assumptions and constants;
- make checks easy to rerun;
- record limitations and external-review status honestly;
- prefer small independent verifiers to trust in a large exploratory system;
- make it possible for another person to correct, reuse, or continue the work.

The proof was developed in an AI-assisted mathematical workflow and is maintained by **Grisha Pochuev**. The purpose of the repository is precisely to make the result assessable without trusting the process that produced it.

## Acknowledgements

A public comment by **Thane Ruthenis** on the original bounty post suggested the broad obstruction of combining many approximately redundant pieces until any maximal object accumulates too much non-redundant information. This repository gives a concrete block-erasure distribution and a complete quantitative proof of that obstruction. Attribution of conceptual and technical contributions should remain visible in any bounty discussion.

## License

The code and original exposition in this repository are released under the MIT License. Mathematical facts and theorem statements are, of course, not owned by the repository.

## Telegram

**The Open Mathematics Project on Telegram:** _public channel link to be inserted once its exact URL is supplied._
