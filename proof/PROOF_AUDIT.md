# Proof audit

This file isolates every load-bearing step in the block-erasure proof.

## Quantifiers

The negative theorem has the correct order:

```text
for every fixed finite R,M
there exist finite X1,X2 and epsilon>0
such that no Omega satisfies the required properties.
```

This is exactly what is needed to rule out universal dimension-free constants.

## Competitor variables

For `Gamma_j = Sj`:

```text
I(Sj ; X2 | X1) = 0
```

because `Sj` is determined by `X1`.

Also:

```text
I(Sj ; X1 | X2)
  = H(Sj | X2) - H(Sj | X1,X2)
  = delta - 0
  = delta.
```

The erasure symbol makes `E` observable from `X2`, and on `E=1` the bit is uniform.

## Maximality conversion

Since `Sj` is a deterministic function of `X=(X1,X2)`,

```text
I(X ; Sj | Omega)
  = H(Sj | Omega) - H(Sj | X,Omega)
  = H(Sj | Omega).
```

No conditional-resampling convention affects this identity.

## Entropy-to-error conversion

For each posterior `t = P(Sj=1 | Omega=omega)`, Bayes error is `min(t,1-t)`. Concavity of binary entropy gives

```text
h2(t) >= 2 min(t,1-t).
```

Averaging yields

```text
H(Sj | Omega) >= 2 p_j.
```

This direction is important. It is not an invalid reversal of Fano's inequality.

## KL change of measure

Because `X1=S`, and because `(S,X2)` determines `E` while `(S,E)` determines `X2`,

```text
I(Omega ; X2 | X1) = I(Omega ; E | S).
```

The exact expansion is

```text
I(Omega ; E | S)
 = (1-delta) E_S D(P(Omega|S,E=0) || P(Omega|S))
 + delta     E_S D(P(Omega|S,E=1) || P(Omega|S)).
```

The second expectation equals

```text
D(P(S,Omega|E=1) || P(S,Omega))
```

because `S` and `E` are independent. Dividing the `E=1` term by `delta` is therefore valid.

## Data processing target

The deterministic map

```text
(S,Omega) -> 1{f_j(Omega) != Sj}
```

turns the conditional-erasure distribution into `Bernoulli(q_j)` and the unconditional distribution into `Bernoulli(p_j)`. KL data processing gives the binary divergence bound directly.

## Monotonicity used in the barrier

For `0 < p < q < 1`, binary KL divergence satisfies:

- at fixed `p`, `d2(q||p)` increases with `q` for `q>p`;
- at fixed `q`, `d2(q||p)` decreases with `p` for `p<q`.

Thus `q_j >= 1/4` and `p_j <= M delta/2 < 1/4` imply

```text
d2(q_j||p_j) >= d2(1/4 || M delta/2).
```

## Use of Fano

Fano is applied only after an explicit estimator with conditional error `q_j<1/4` has been obtained. For a binary target,

```text
H(Sj | Omega,E=1) <= h2(q_j).
```

No independence of the bits conditional on `Omega` is assumed. Only subadditivity is used:

```text
H(S | Omega,E=1) <= sum_j H(Sj | Omega,E=1).
```

## Final conditional mutual information identity

Since `X2` itself reveals whether erasure occurred,

```text
I(S ; Omega | X2)
 = (1-delta)*0 + delta*I(S ; Omega | E=1).
```

On the non-erasure branch, conditioning on `X2=S` leaves no uncertainty in `S`.

## Edge cases

- `delta>0` is chosen, so division by `delta` is valid.
- `delta` is chosen small enough that `M delta/2 < 1/4`.
- If a Bayes error `p_j` is zero, finite KL in the erasure branch forces `q_j=0`, which is even stronger.
- The alphabets are finite: `S` has `2^n` values, `X2` has `2^n+1` values, and each competitor is binary.
- No restriction on the alphabet of `Omega` is needed beyond the finite-variable setting of the problem.
- The determinism error `H(Omega|X)` is never invoked.

## Scope of the conclusion

The proof excludes universal constants multiplying the competitor error. It does not exclude bounds that grow with `n`, `H(X)`, alphabet size, or another structural parameter.
