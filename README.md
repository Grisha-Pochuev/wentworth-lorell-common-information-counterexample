# A Block-Erasure Counterexample to Approximately Deterministic Maximal Common Information

> **Result:** the dimension-free linear version of the Wentworth–Lorell problem is false. This repository contains a complete mathematical proof, an independent finite numerical verifier, and a compiled Lean proof spine for the exact construction and numerical certificates.

## What is the problem?

Suppose two observations, \(X_1\) and \(X_2\), both contain almost the same information about some latent variable \(\Gamma\).

The proposed theorem asks whether there is always one distinguished latent variable \(\Omega\) that simultaneously has three properties:

1. \(\Omega\) is itself approximately recoverable from either observation;
2. \(\Omega\) contains essentially all information carried by every other approximately shared latent variable;
3. \(\Omega\) is almost determined by the observed pair \((X_1,X_2)\).

In the exact zero-error case, such a variable exists: it is the connected-component label of the bipartite support graph of the joint distribution. The question is whether this construction has a stable approximate analogue with errors bounded by universal constant multiples of the original approximation error.

A positive result would give a canonical summary of the information genuinely shared by two observations. The counterexample here shows that no such summary can satisfy dimension-independent linear bounds in full generality.

## Precise formulation

All random variables are finite, and all information quantities are measured in bits.

A latent variable \(\Gamma\) is an \(\varepsilon\)-common variable for \(X_1,X_2\) when

\[
I(\Gamma;X_2\mid X_1)\leq\varepsilon,
\qquad
I(\Gamma;X_1\mid X_2)\leq\varepsilon.
\]

The proposed conclusion asks for universal constants \(C_{\rm red},C_{\rm max},C_{\rm det}<\infty\) such that, for every \(X_1,X_2\) and every \(\varepsilon\geq0\), there is a latent variable \(\Omega\) satisfying

\[
I(\Omega;X_2\mid X_1),
\ I(\Omega;X_1\mid X_2)
\leq C_{\rm red}\varepsilon,
\]

\[
I((X_1,X_2);\Gamma\mid\Omega)
\leq C_{\rm max}\varepsilon
\]

for every \(\varepsilon\)-common variable \(\Gamma\), and

\[
H(\Omega\mid X_1,X_2)
\leq C_{\rm det}\varepsilon.
\]

## Main theorem proved here

For every fixed finite pair of constants \(R,M\geq0\), there exist finite random variables \(X_1,X_2\) and \(\varepsilon>0\) such that no latent variable \(\Omega\) can satisfy both

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

The approximate-determinism condition is not used. Thus the obstruction is stronger than required: approximate maximality and approximate commonality already contradict one another.

The full argument, including the boundary case \(M=0\), is in [`PROOF.md`](PROOF.md).

## Counterexample idea

Let

\[
S=(S_1,\ldots,S_n)
\]

be a uniformly random \(n\)-bit string.

- \(X_1\) always reveals the complete string \(S\).
- With probability \(1-\varepsilon\), \(X_2\) also reveals \(S\).
- With probability \(\varepsilon\), \(X_2\) shows only an erasure symbol.

Each bit \(\Gamma_j=S_j\) is an admissible \(\varepsilon\)-common variable:

\[
I(S_j;X_2\mid X_1)=0,
\qquad
I(S_j;X_1\mid X_2)=\varepsilon.
\]

If \(\Omega\) is approximately maximal, it must retain enough information to predict every bit \(S_j\). The other commonality condition prevents \(\Omega\) from discarding all of this information only on the rare erasure event. Consequently, on that event \(\Omega\) still carries a positive constant fraction of all \(n\) bits.

This forces

\[
I(X_1;\Omega\mid X_2)
\geq c\,n\varepsilon
\]

for an absolute constant \(c>0\), contradicting any bound of the form \(R\varepsilon\) when \(n\) is large enough.

## Explicit finite instance

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
d_2\!\left(\frac14\,\middle\|\,\frac{3\varepsilon}{2}\right)
=3.5424874417\ldots>3
\]

and

\[
16\left(1-h_2\!\left(\frac14\right)\right)
=3.0195500086\ldots>3.
\]

Therefore every candidate \(\Omega\) violates at least one required inequality.

## Reproduce the numerical checks

Only Python's standard library is required.

```bash
python verify.py
```

The script:

- recomputes the entropy and binary-divergence constants at high precision;
- verifies the strict inequalities for the explicit \(R=M=3\) instance;
- independently enumerates a small block-erasure distribution and checks the two conditional mutual informations for a coordinate competitor;
- verifies that suitable parameters are found for several other fixed constants.

The script checks the finite construction and all numerical margins. The general reduction applying to every possible \(\Omega\) is the mathematical proof in `PROOF.md`.

## Lean verification

The Lean project is pinned to Lean `4.28.0` and to exact revisions of its dependencies. Reproduce the build with

```bash
lake update
lake build
```

The project compiles with all Lean warnings treated as errors. A use of `sorry` would therefore fail the build.

Lean currently checks:

- the deterministic block-erasure construction;
- the finite hidden-state distribution and its independence structure;
- finite conditional-information definitions;
- exact non-decimal proofs of the two factor-3 numerical margins;
- the final contradiction once the information-theoretic bridge hypotheses are supplied.

It does **not yet** formalize every information-theoretic bridge for an arbitrary latent variable \(\Omega\): Bayes prediction from conditional entropy, the erasure-branch KL bound, KL data processing, binary Fano, conditional subadditivity, and the final erasure decomposition still need to be connected in Lean.

The exact boundary is recorded in [`LEAN_STATUS.md`](LEAN_STATUS.md). Thus the human proof is complete, while the Lean development is currently a compiled proof spine rather than a complete formal proof of every line.

## Files

```text
README.md                  Problem, significance, result, and reproduction.
PROOF.md                   Complete information-theoretic proof.
verify.py                  Standalone numerical and finite-model verifier.
LEAN_STATUS.md             Exact status of the Lean formalization.
lean-toolchain             Pinned Lean version.
lakefile.toml              Pinned Lean dependencies and strict compiler settings.
WentworthLorell.lean       Lean entry point.
WentworthLorell/           Lean definitions, certificates, and proof spine.
LICENSE                    MIT license.
```

## Scope of the result

The counterexample rules out universal dimension-independent bounds of the form

\[
\text{constant}\times\varepsilon.
\]

It does not rule out:

- bounds depending on dimension, entropy, or alphabet size;
- nonlinear dependence on \(\varepsilon\);
- positive results under additional structural assumptions.

## Repository philosophy

The aim is to make the result readable and independently checkable:

- explain the problem before presenting the technical proof;
- separate the mathematical argument from numerical and formal verification;
- state constants and assumptions explicitly;
- keep reproduction commands simple;
- record exactly what has been proved and what remains unformalized.

Telegram: https://t.me/let_people_dance
