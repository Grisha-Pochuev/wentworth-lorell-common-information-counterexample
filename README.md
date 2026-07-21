# A Block-Erasure Counterexample to Approximately Deterministic Maximal Common Information

> **Result:** the dimension-free linear version of the Wentworth–Lorell problem is false. This repository contains a complete mathematical counterexample proof, an independent finite verifier, and a compiled Lean proof spine.

## The problem

All random variables are finite and information quantities are measured in bits.

A latent variable \(\Gamma\) is \(\varepsilon\)-common for observations \(X_1,X_2\) when

\[
I(\Gamma;X_2\mid X_1)\leq\varepsilon,
\qquad
I(\Gamma;X_1\mid X_2)\leq\varepsilon.
\]

The proposed theorem asks whether universal finite constants
\(C_{\rm red},C_{\rm max},C_{\rm det}\) always allow a latent variable \(\Omega\) satisfying

\[
I(\Omega;X_2\mid X_1),
\ I(\Omega;X_1\mid X_2)
\leq C_{\rm red}\varepsilon,
\]

\[
I((X_1,X_2);\Gamma\mid\Omega)
\leq C_{\rm max}\varepsilon
\]

for every \(\varepsilon\)-common \(\Gamma\), together with

\[
H(\Omega\mid X_1,X_2)
\leq C_{\rm det}\varepsilon.
\]

## Main theorem

For every fixed finite pair \(R,M\geq0\), there exist finite random variables \(X_1,X_2\) and \(\varepsilon>0\) such that no latent variable \(\Omega\) can satisfy both

\[
I(\Omega;X_2\mid X_1),
\ I(\Omega;X_1\mid X_2)
\leq R\varepsilon
\]

and

\[
I((X_1,X_2);\Gamma\mid\Omega)
\leq M\varepsilon
\]

for every \(\varepsilon\)-common variable \(\Gamma\).

The approximate-determinism condition is not used. Thus approximate maximality and approximate commonality already contradict one another.

The complete argument, including the boundary case \(M=0\), is in [`PROOF.md`](PROOF.md).

## Counterexample idea

Let \(S=(S_1,\ldots,S_n)\) be a uniformly random \(n\)-bit string. Let \(E\) be an independent Bernoulli erasure flag with probability \(\delta\), and define

\[
X_1=S,
\qquad
X_2=
\begin{cases}
S,&E=0,\\
\bot,&E=1.
\end{cases}
\qquad
\varepsilon=\delta.
\]

Every coordinate \(\Gamma_j=S_j\) is an admissible competitor:

\[
I(S_j;X_2\mid X_1)=0,
\qquad
I(S_j;X_1\mid X_2)=\delta.
\]

Approximate maximality then makes every bit predictable from \(\Omega\). The other commonality inequality prevents all of that information from disappearing only on the rare erasure event. On that event, \(\Omega\) must retain a positive constant fraction of all \(n\) bits, forcing

\[
I(X_1;\Omega\mid X_2)
>\delta n\left(1-h_2\!\left(\frac14\right)\right).
\]

For sufficiently large \(n\), this contradicts any fixed bound \(R\varepsilon\).

## Explicit factor-3 instance

The proposed factor \(3\) already fails for

\[
R=M=3,
\qquad
\varepsilon=2^{-18},
\qquad
n=16.
\]

The proof gives

\[
d_2\!\left(\frac14\middle\|3\cdot2^{-19}\right)
=3.5424874417\ldots>3
\]

and

\[
16\left(1-h_2\!\left(\frac14\right)\right)
=3.0195500086\ldots>3.
\]

Therefore every candidate \(\Omega\) violates at least one required inequality.

## Reproduce the finite and numerical checks

Only Python's standard library is required:

```bash
python verify.py
```

The script:

- recomputes the entropy and binary-KL constants at high precision;
- verifies the strict inequalities for the explicit factor-3 instance;
- independently enumerates a small block-erasure distribution;
- checks both conditional mutual informations for a coordinate competitor;
- finds valid parameters for several other fixed constants.

The script checks the construction and numerical margins. The universal argument for every possible \(\Omega\) is the proof in `PROOF.md`.

## Lean verification

The Lean project is pinned to Lean `4.28.0` and exact dependency revisions. Reproduce the build with

```bash
lake update
lake build
```

All project warnings are treated as errors, so any use of `sorry` would fail the build.

Lean currently checks:

- the deterministic block-erasure construction;
- the finite hidden-state distribution and its independence structure;
- finite conditional-information definitions;
- exact non-decimal proofs of both factor-3 numerical margins;
- the final algebraic contradiction once the bridge hypotheses are supplied.

The Lean development is not yet a machine-checked proof of every line of `PROOF.md`. The remaining bridge for an arbitrary finite \(\Omega\) consists of:

1. deriving small coordinate entropy from maximality;
2. converting binary conditional entropy into Bayes prediction error;
3. extracting the erasure-branch KL bound;
4. applying KL data processing to the prediction-error indicator;
5. combining binary Fano with conditional subadditivity;
6. proving the final erasure decomposition of conditional mutual information.

Thus the mathematical proof is complete, while Lean currently provides a compiled and checked proof spine.

## Files

```text
README.md                  Problem, result, construction, and reproduction.
PROOF.md                   Complete information-theoretic proof.
verify.py                  Standalone numerical and finite-model verifier.
lean-toolchain             Pinned Lean version.
lakefile.toml              Pinned dependencies and strict compiler settings.
WentworthLorell.lean       Lean entry point.
WentworthLorell/           Lean definitions, certificates, and proof spine.
LICENSE                    MIT license.
```

## Scope

The counterexample rules out universal dimension-independent bounds of the form

\[
\text{constant}\times\varepsilon.
\]

It does not rule out bounds depending on dimension, entropy, alphabet size, additional structural assumptions, or nonlinear dependence on \(\varepsilon\).

## Repository philosophy

The repository is intended to be readable and independently checkable:

- the problem is explained before the technical proof;
- the mathematical argument is separated from numerical and formal verification;
- constants and assumptions are explicit;
- reproduction commands are short;
- the exact boundary of the Lean formalization is stated openly.

Telegram: https://t.me/let_people_dance
