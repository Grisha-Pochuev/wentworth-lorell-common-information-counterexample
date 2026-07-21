# Precise problem statement

All random variables below are finite. All entropies, mutual informations, and KL divergences are measured in bits.

Let

```text
X = (X1, X2).
```

A latent variable `Gamma`, represented by a conditional distribution `P(Gamma | X)`, is an `epsilon`-redund over `X1, X2` when

```text
I(Gamma ; X2 | X1) <= epsilon,
I(Gamma ; X1 | X2) <= epsilon.
```

These are the mutual-information forms of the two approximate Markov diagrams used by Wentworth and Lorell.

The proposed maximal-redund theorem asks for universal finite constants

```text
C_red, C_max, C_det
```

such that, for every finite joint distribution `P(X1, X2)` and every `epsilon >= 0`, there exists a latent variable `Omega` satisfying all three groups of conditions below.

## 1. Omega is itself approximately redundant

```text
I(Omega ; X2 | X1) <= C_red epsilon,
I(Omega ; X1 | X2) <= C_red epsilon.
```

## 2. Omega is approximately maximal among epsilon-redunds

For every latent `Gamma` with

```text
I(Gamma ; X2 | X1) <= epsilon,
I(Gamma ; X1 | X2) <= epsilon,
```

one has

```text
I(X ; Gamma | Omega) <= C_max epsilon.
```

When `Omega` and `Gamma` are considered jointly, they may be conditionally resampled independently given `X`. In the counterexample, the competitors are deterministic functions of `X`, so this convention causes no ambiguity.

## 3. Omega is approximately determined by X

```text
H(Omega | X) <= C_det epsilon.
```

The bounty post states that small constants such as 2 or 3 would definitely count as reasonable and that the bounds should be global rather than only asymptotic.

## Exact case

At `epsilon = 0`, construct a bipartite graph whose left vertices are values of `X1`, whose right vertices are values of `X2`, and whose edges are the support pairs with positive probability. The connected-component label is a deterministic maximal redund.

The open question is whether a dimension-free, linearly stable approximate analogue always exists.

## What the counterexample proves

The proof in this repository establishes the following stronger negative statement.

> For every fixed finite `R` and `M`, there exist finite `X1, X2` and `epsilon > 0` such that no `Omega` can satisfy both the two `R epsilon` redundancy bounds and the `M epsilon` maximality bound for all competing `epsilon`-redunds.

No assumption on `H(Omega | X)` is used. Therefore no choice of `C_det` repairs the dimension-free linear statement.

## Primary source

John Wentworth and David Lorell, “Does An (Approximately) Deterministic Maximal Redund Always Exist?”, 6 May 2025, edited 22 August 2025:

https://www.lesswrong.com/posts/sCNdkuio62Fi9qQZK/usd500-usd500-bounty-problem-does-an-approximately
