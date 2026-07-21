# Block-Erasure Counterexample

All random variables are finite. All logarithms are base \(2\), so entropy, mutual information, and KL divergence are measured in bits.

Write

\[
h_2(t)=-t\log_2t-(1-t)\log_2(1-t)
\]

for binary entropy. For \(p,q\in(0,1)\), write

\[
d_2(q\|p)
=q\log_2\frac qp+(1-q)\log_2\frac{1-q}{1-p}
\]

for binary KL divergence, with the standard lower-semicontinuous boundary conventions. In particular,

\[
d_2(q\|0)=+\infty\quad\text{for }q>0,
\qquad d_2(0\|0)=0.
\]

## Theorem

For every fixed finite \(R,M\geq0\), there exist finite random variables \(X_1,X_2\) and \(\varepsilon>0\) such that no latent variable \(\Omega\) can satisfy both

\[
I(\Omega;X_2\mid X_1)\leq R\varepsilon,
\qquad
I(\Omega;X_1\mid X_2)\leq R\varepsilon,
\tag{1}
\]

and

\[
I((X_1,X_2);\Gamma\mid\Omega)\leq M\varepsilon
\tag{2}
\]

for every latent variable \(\Gamma\) satisfying

\[
I(\Gamma;X_2\mid X_1)\leq\varepsilon,
\qquad
I(\Gamma;X_1\mid X_2)\leq\varepsilon.
\tag{3}
\]

Therefore no universal dimension-free theorem with errors bounded by fixed constant multiples of \(\varepsilon\) can hold. No approximate-determinism assumption on \(\Omega\) is needed for the contradiction.

When two latent variables are mentioned simultaneously, they may be sampled conditionally independently given \(X=(X_1,X_2)\). The competitors used below are deterministic functions of \(X\), so the proof is independent of this convention.

## Construction

Choose an integer \(n\geq1\) and an erasure probability \(0<\delta<1\), to be fixed below.

Let

\[
S=(S_1,\ldots,S_n)
\]

be uniformly distributed on \(\{0,1\}^n\). Let \(E\sim\operatorname{Bernoulli}(\delta)\) be independent of \(S\). Define

\[
X_1=S
\]

and

\[
X_2=
\begin{cases}
S,&E=0,\\
\bot,&E=1,
\end{cases}
\]

where \(\bot\) is a new erasure symbol. Set

\[
\varepsilon=\delta.
\]

Choose \(n\) so that

\[
n>\frac{R}{1-h_2(1/4)}.
\tag{4}
\]

If \(M>0\), choose \(\delta\) sufficiently small that

\[
\frac{M\delta}{2}<\frac14
\tag{5}
\]

and

\[
d_2\!\left(\frac14\middle\|\frac{M\delta}{2}\right)>R.
\tag{6}
\]

Such a positive \(\delta\) exists because, for fixed \(q=1/4\),

\[
d_2(q\|p)\longrightarrow+\infty
\qquad\text{as }p\downarrow0.
\]

If \(M=0\), choose any \(0<\delta<1\), for example \(\delta=1/2\). The proof below treats that boundary case directly.

## Step 1: each coordinate is an admissible competitor

For every \(j\in\{1,\ldots,n\}\), let

\[
\Gamma_j=S_j.
\]

Because \(S_j\) is a deterministic function of \(X_1=S\),

\[
I(S_j;X_2\mid X_1)=0.
\tag{7}
\]

Given \(X_2\), the bit \(S_j\) is known when \(E=0\), while on \(E=1\) it remains a fair bit. Hence

\[
H(S_j\mid X_2)=\delta.
\]

Since \(S_j\) is determined by \(X_1\),

\[
I(S_j;X_1\mid X_2)
=H(S_j\mid X_2)
=\delta
=\varepsilon.
\tag{8}
\]

Thus every \(\Gamma_j\) satisfies (3).

## Step 2: maximality makes every bit predictable from \(\Omega\)

Assume, for contradiction, that a variable \(\Omega\) satisfies (1) and (2).

Apply (2) to \(\Gamma_j=S_j\). Since \(S_j\) is a deterministic function of \(X=(X_1,X_2)\),

\[
I(X;S_j\mid\Omega)=H(S_j\mid\Omega).
\]

Therefore

\[
H(S_j\mid\Omega)\leq M\delta.
\tag{9}
\]

Let \(f_j(\Omega)\) be a Bayes-optimal estimator of \(S_j\), and put

\[
p_j=\Pr[f_j(\Omega)\neq S_j].
\]

For a binary variable, the posterior Bayes error is a number \(t\in[0,1/2]\), and the posterior entropy is \(h_2(t)\). Concavity of \(h_2\) gives

\[
h_2(t)\geq2t
\qquad(0\leq t\leq1/2).
\]

Averaging over \(\Omega\),

\[
H(S_j\mid\Omega)\geq2p_j.
\]

Together with (9),

\[
p_j\leq\frac{M\delta}{2}.
\tag{10}
\]

## Step 3: the information cannot disappear only on erasure

Conditioned on \(S\), the variables \(X_2\) and \(E\) determine one another. Consequently,

\[
I(\Omega;X_2\mid X_1)
=I(\Omega;E\mid S)
\leq R\delta.
\tag{11}
\]

Expand the conditional mutual information as conditional KL divergence:

\[
I(\Omega;E\mid S)
=
\sum_{e\in\{0,1\}}\Pr(E=e)\,
\mathbb E_S
D\!\left(
P_{\Omega\mid S,E=e}
\middle\|
P_{\Omega\mid S}
\right).
\]

All summands are nonnegative. Keeping only the \(E=1\) term in (11) and dividing by \(\delta>0\),

\[
\mathbb E_S
D\!\left(
P_{\Omega\mid S,E=1}
\middle\|
P_{\Omega\mid S}
\right)
\leq R.
\tag{12}
\]

Because \(S\) and \(E\) are independent, the distribution of \(S\) is unchanged by conditioning on \(E=1\). The KL chain rule therefore turns (12) into

\[
D\!\left(
P_{S,\Omega\mid E=1}
\middle\|
P_{S,\Omega}
\right)
\leq R.
\tag{13}
\]

For a fixed coordinate \(j\), define

\[
A_j=\mathbf 1\{f_j(\Omega)\neq S_j\},
\qquad
q_j=\Pr(A_j=1\mid E=1).
\]

Under \(P_{S,\Omega}\), the indicator \(A_j\) is Bernoulli with parameter \(p_j\); under \(P_{S,\Omega\mid E=1}\), it is Bernoulli with parameter \(q_j\). Data processing for KL divergence applied to the map \((S,\Omega)\mapsto A_j\) gives

\[
d_2(q_j\|p_j)\leq R.
\tag{14}
\]

We now prove

\[
q_j<\frac14.
\tag{15}
\]

If \(p_j=0\), then (14) is finite only if \(q_j=0\), so (15) follows. This covers every coordinate immediately when \(M=0\), because then (10) forces \(p_j=0\).

Suppose instead that \(p_j>0\). Then necessarily \(M>0\). If \(q_j\geq1/4\), equations (5), (6), and (10), together with monotonicity of binary KL divergence on the region \(0<p<q<1\), imply

\[
\begin{aligned}
d_2(q_j\|p_j)
&\geq d_2\!\left(\frac14\middle\|p_j\right)\\
&\geq d_2\!\left(\frac14\middle\|\frac{M\delta}{2}\right)\\
&>R,
\end{aligned}
\]

contradicting (14). Thus (15) holds for every \(j\).

## Step 4: on erasure, \(\Omega\) contains linearly many bits

Conditioned on \(E=1\), the estimator \(f_j(\Omega)\) predicts \(S_j\) with error \(q_j<1/4\). Binary Fano gives

\[
H(S_j\mid\Omega,E=1)
\leq h_2(q_j)
<h_2\!\left(\frac14\right),
\tag{16}
\]

where the strict inequality uses that \(h_2\) is strictly increasing on \([0,1/2]\).

Conditional entropy is subadditive, so

\[
H(S\mid\Omega,E=1)
\leq
\sum_{j=1}^n H(S_j\mid\Omega,E=1)
<
n\,h_2\!\left(\frac14\right).
\tag{17}
\]

Since \(S\) is uniform and independent of \(E\),

\[
H(S\mid E=1)=n.
\]

Therefore

\[
I(S;\Omega\mid E=1)
=H(S\mid E=1)-H(S\mid\Omega,E=1)
>
n\left(1-h_2\!\left(\frac14\right)\right).
\tag{18}
\]

## Step 5: contradiction with the second commonality bound

The value of \(X_2\) reveals whether erasure occurred. On \(E=0\), \(X_2=S\), so conditioning on \(X_2\) already determines \(S\). On \(E=1\), \(X_2=\bot\) is constant. Hence

\[
I(X_1;\Omega\mid X_2)
=\delta\,I(S;\Omega\mid E=1).
\tag{19}
\]

Combining (18) and (19),

\[
I(X_1;\Omega\mid X_2)
>
\delta n\left(1-h_2\!\left(\frac14\right)\right).
\tag{20}
\]

The choice of \(n\) in (4) now gives

\[
I(X_1;\Omega\mid X_2)
>R\delta
=R\varepsilon,
\]

contradicting (1). This proves the theorem.

## Explicit factor-\(3\) instance

Take

\[
R=M=3,
\qquad
\delta=\varepsilon=2^{-18},
\qquad
n=16.
\]

Equation (10) gives

\[
p_j\leq\frac{3\delta}{2}=3\cdot2^{-19}.
\]

The exact inequality formalized in `WentworthLorell/Constants.lean` is

\[
d_2\!\left(\frac14\middle\|3\cdot2^{-19}\right)>3.
\]

Numerically,

\[
d_2\!\left(\frac14\middle\|3\cdot2^{-19}\right)
=3.5424874417537\ldots.
\]

Also,

\[
16\left(1-h_2\!\left(\frac14\right)\right)>3,
\]

with numerical value

\[
16\left(1-h_2\!\left(\frac14\right)\right)
=3.0195500086538\ldots.
\]

Thus

\[
I(X_1;\Omega\mid X_2)>3\varepsilon,
\]

contradicting the proposed factor-\(3\) bound.

The numerical values and finite competitor identities can be checked with

```bash
python verify.py
```

The exact two numerical margins are also machine-checked by Lean in `WentworthLorell/Constants.lean`.

## What the theorem does not exclude

The argument rules out constants independent of the size of the distribution. It does not exclude bounds depending on \(n\), entropy, alphabet size, or additional structural assumptions, nor does it exclude nonlinear dependence on \(\varepsilon\).
