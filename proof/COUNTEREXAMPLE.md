# Block-erasure counterexample

All information quantities are measured in bits. Write

```text
h2(t) = -t log2(t) - (1-t) log2(1-t)
```

for binary entropy.

## Theorem

Let `R, M < infinity` be fixed nonnegative constants. Then there are finite random variables `X1, X2` and a number `epsilon > 0` for which no latent variable `Omega` satisfies both:

```text
I(Omega ; X2 | X1) <= R epsilon,
I(Omega ; X1 | X2) <= R epsilon,
```

and

```text
I((X1, X2) ; Gamma | Omega) <= M epsilon
```

for every latent variable `Gamma` satisfying

```text
I(Gamma ; X2 | X1) <= epsilon,
I(Gamma ; X1 | X2) <= epsilon.
```

In particular, adding any bound on `H(Omega | X1, X2)` cannot make a universal dimension-free linear theorem true.

## Construction

Choose an integer `n` and an erasure probability `delta` later.

Let

```text
S = (S1, ..., Sn)
```

be uniformly distributed on `{0,1}^n`. Let `E` be independent of `S`, with

```text
P(E = 1) = delta.
```

Define

```text
X1 = S,
```

and

```text
X2 = S     when E = 0,
X2 = bottom when E = 1,
```

where `bottom` is an erasure symbol not in `{0,1}^n`.

Set

```text
epsilon = delta.
```

## Step 1: every coordinate bit is an allowed epsilon-redund

For each `j`, take

```text
Gamma_j = Sj.
```

Since `Sj` is a deterministic function of `X1 = S`,

```text
I(Gamma_j ; X2 | X1) = 0.
```

Given `X2`, the bit `Sj` is known unless erasure occurred. On erasure, it remains a fair bit. Therefore

```text
I(Gamma_j ; X1 | X2)
  = H(Sj | X2)
  = delta
  = epsilon.
```

Thus every `Gamma_j` is an admissible competitor.

## Step 2: maximality forces Omega to predict every bit

Assume for contradiction that an `Omega` satisfying the stated bounds exists.

Applying maximality to `Gamma_j = Sj` gives

```text
I((X1, X2) ; Sj | Omega) <= M delta.
```

Because `Sj` is a deterministic function of `X = (X1, X2)`,

```text
I(X ; Sj | Omega) = H(Sj | Omega).
```

Hence

```text
H(Sj | Omega) <= M delta.                 (1)
```

Let `f_j(Omega)` be a Bayes-optimal predictor of `Sj` from `Omega`, and let

```text
p_j = P(f_j(Omega) != Sj).
```

For a binary variable, binary entropy lies above the chord joining `(0,0)` and `(1/2,1)`, so

```text
h2(t) >= 2t    for 0 <= t <= 1/2.
```

Averaging this inequality over posterior probabilities gives

```text
H(Sj | Omega) >= 2 p_j.
```

Together with (1),

```text
p_j <= M delta / 2.                       (2)
```

## Step 3: Omega cannot hide all bit information only on erasure

Given `S`, the value of `X2` is equivalent to the erasure bit `E`. Therefore

```text
I(Omega ; X2 | X1) = I(Omega ; E | S) <= R delta.     (3)
```

The conditional mutual information has the KL expansion

```text
I(Omega ; E | S)
  = sum_e P(E=e) E_S D(P(Omega | S,E=e) || P(Omega | S)).
```

Keeping only the nonnegative `E=1` term and using the independence of `S` and `E`, (3) yields

```text
D(P(S,Omega | E=1) || P(S,Omega)) <= R.               (4)
```

For each `j`, map `(S,Omega)` to the error indicator

```text
A_j = 1{f_j(Omega) != Sj}.
```

Let

```text
q_j = P(A_j = 1 | E=1).
```

By data processing for KL divergence, (4) implies

```text
d2(q_j || p_j) <= R,                                  (5)
```

where `d2` is binary KL divergence in bits.

Choose `delta` so small that

```text
M delta / 2 < 1/4
```

and

```text
d2(1/4 || M delta/2) > R.                             (6)
```

Such a positive `delta` always exists because the left side of (6) tends to infinity as `delta` tends to zero.

If `q_j >= 1/4`, then by (2), monotonicity of binary KL divergence for `p < q`, and (6),

```text
d2(q_j || p_j)
  >= d2(1/4 || M delta/2)
  > R,
```

contradicting (5). Consequently,

```text
q_j < 1/4                                                (7)
```

for every coordinate `j`.

## Step 4: on erasure, Omega contains a linear amount of information

Under `E=1`, the estimator `f_j(Omega)` predicts `Sj` with error below `1/4`. Fano's inequality for a binary variable gives

```text
H(Sj | Omega, E=1) <= h2(q_j) < h2(1/4).
```

By conditional subadditivity,

```text
H(S | Omega, E=1)
  <= sum_j H(Sj | Omega, E=1)
  < n h2(1/4).
```

Since `S` is uniform and independent of `E`,

```text
H(S | E=1) = n.
```

Therefore

```text
I(S ; Omega | E=1)
  = H(S | E=1) - H(S | Omega,E=1)
  > n (1 - h2(1/4)).                                  (8)
```

## Step 5: contradiction with the second redundancy bound

When `E=0`, `X2=S`, so `S` is already known from `X2`. When `E=1`, `X2=bottom` is constant. Because `E` is determined by `X2`,

```text
I(X1 ; Omega | X2)
  = delta I(S ; Omega | E=1).
```

Using (8),

```text
I(X1 ; Omega | X2)
  > delta n (1 - h2(1/4)).                            (9)
```

Now choose

```text
n > R / (1 - h2(1/4)).                                (10)
```

Then (9) gives

```text
I(X1 ; Omega | X2) > R delta = R epsilon,
```

contradicting the assumed redundancy bound on `Omega`.

This proves the theorem.

## Explicit constants for the factor-3 proposal

Take

```text
R = M = 3,
delta = epsilon = 2^-18,
n = 16.
```

From (2),

```text
p_j <= 3 * 2^-19.
```

The binary KL barrier is

```text
d2(1/4 || 3 * 2^-19)
  = 3.5424874417...
  > 3.
```

Also,

```text
1 - h2(1/4)
  = 0.1887218755...,
```

so

```text
16 * (1 - h2(1/4))
  = 3.0195500086...
  > 3.
```

Thus no `Omega` can satisfy the factor-3 redundancy and maximality requirements for this finite distribution. The determinism constant is irrelevant.
