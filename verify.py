"""Reproduce the numerical checks for the block-erasure counterexample.

Run from the repository root:

    python verify.py

Only the Python standard library is used. This script checks the exact
finite construction identities and the numerical inequalities used by the
explicit R = M = 3 example. The general information-theoretic argument is
given in PROOF.md.
"""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_FLOOR, getcontext, localcontext
from fractions import Fraction
from typing import Callable, Hashable

PRECISION = 90
getcontext().prec = PRECISION

D0 = Decimal(0)
D1 = Decimal(1)
D2 = Decimal(2)
D4 = Decimal(4)


def dec(value: int | str | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def log2(x: Decimal) -> Decimal:
    if x <= D0:
        raise ValueError("log2 requires x > 0")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return x.ln() / D2.ln()


def binary_entropy(p: Decimal) -> Decimal:
    p = dec(p)
    if not D0 <= p <= D1:
        raise ValueError("p must lie in [0,1]")
    if p in (D0, D1):
        return D0
    return -(p * log2(p) + (D1 - p) * log2(D1 - p))


def binary_kl(q: Decimal, p: Decimal) -> Decimal:
    """Binary KL divergence d2(q || p), in bits."""
    q = dec(q)
    p = dec(p)
    if not (D0 <= q <= D1 and D0 <= p <= D1):
        raise ValueError("p and q must lie in [0,1]")
    if p == D0:
        return D0 if q == D0 else Decimal("Infinity")
    if p == D1:
        return D0 if q == D1 else Decimal("Infinity")

    first = D0 if q == D0 else q * log2(q / p)
    second = D0 if q == D1 else (D1 - q) * log2((D1 - q) / (D1 - p))
    return first + second


State = tuple[int, int | str, int]
Distribution = dict[State, Fraction]


def block_erasure_distribution(
    n: int,
    delta: Fraction,
    coordinate: int = 0,
) -> Distribution:
    """Return P(X1, X2, Gamma_j) for Gamma_j equal to one bit of X1."""
    if n <= 0:
        raise ValueError("n must be positive")
    if not Fraction(0) < delta < Fraction(1):
        raise ValueError("delta must lie in (0,1)")
    if not 0 <= coordinate < n:
        raise ValueError("coordinate is outside the block")

    result: defaultdict[State, Fraction] = defaultdict(Fraction)
    p_s = Fraction(1, 2**n)
    for s in range(2**n):
        gamma = (s >> coordinate) & 1
        result[(s, s, gamma)] += p_s * (1 - delta)
        result[(s, "erasure", gamma)] += p_s * delta
    return dict(result)


def marginal(
    distribution: Distribution,
    key: Callable[[State], Hashable],
) -> dict[Hashable, Fraction]:
    result: defaultdict[Hashable, Fraction] = defaultdict(Fraction)
    for state, probability in distribution.items():
        result[key(state)] += probability
    return dict(result)


def entropy(probabilities: list[Fraction] | tuple[Fraction, ...]) -> Decimal:
    total = D0
    for probability in probabilities:
        if probability == 0:
            continue
        p = Decimal(probability.numerator) / Decimal(probability.denominator)
        total -= p * log2(p)
    return total


def conditional_mutual_information(
    distribution: Distribution,
    a: Callable[[State], Hashable],
    b: Callable[[State], Hashable],
    c: Callable[[State], Hashable],
) -> Decimal:
    """Compute I(A;B|C) = H(A,C)+H(B,C)-H(C)-H(A,B,C)."""
    ac = marginal(distribution, lambda state: (a(state), c(state)))
    bc = marginal(distribution, lambda state: (b(state), c(state)))
    cc = marginal(distribution, c)
    abc = marginal(distribution, lambda state: (a(state), b(state), c(state)))
    return (
        entropy(list(ac.values()))
        + entropy(list(bc.values()))
        - entropy(list(cc.values()))
        - entropy(list(abc.values()))
    )


def check_finite_competitor() -> tuple[Decimal, Decimal, Decimal]:
    """Enumerate a small model and recompute both competitor CMIs."""
    delta_fraction = Fraction(1, 8)
    distribution = block_erasure_distribution(n=4, delta=delta_fraction)

    x1 = lambda state: state[0]
    x2 = lambda state: state[1]
    gamma = lambda state: state[2]

    first = conditional_mutual_information(distribution, gamma, x2, x1)
    second = conditional_mutual_information(distribution, gamma, x1, x2)
    delta = Decimal(delta_fraction.numerator) / Decimal(delta_fraction.denominator)
    return first, second, delta


def choose_parameters(r: Decimal, m: Decimal) -> tuple[Decimal, int]:
    """Find a dyadic erasure probability and a valid block length."""
    if r < D0 or m < D0:
        raise ValueError("constants must be nonnegative")

    gap = D1 - binary_entropy(D1 / D4)
    n = int((r / gap).to_integral_value(rounding=ROUND_FLOOR)) + 1

    if m == D0:
        return D1 / D2, n

    for power in range(1, 10001):
        delta = D1 / (D2**power)
        p_bound = m * delta / D2
        if p_bound < D1 / D4 and binary_kl(D1 / D4, p_bound) > r:
            return delta, n
    raise RuntimeError("parameter search failed unexpectedly")


def main() -> None:
    r = Decimal(3)
    m = Decimal(3)
    delta = D1 / (D2**18)
    n = 16

    quarter = D1 / D4
    error_bound = m * delta / D2
    entropy_gap = D1 - binary_entropy(quarter)
    kl_barrier = binary_kl(quarter, error_bound)
    final_coefficient = Decimal(n) * entropy_gap

    assert error_bound < quarter
    assert kl_barrier > r
    assert final_coefficient > r

    first, second, enumerated_delta = check_finite_competitor()
    tolerance = Decimal("1e-70")
    assert abs(first) < tolerance
    assert abs(second - enumerated_delta) < tolerance

    for r_int, m_int in [(1, 1), (2, 3), (3, 3), (10, 7), (100, 100)]:
        candidate_delta, candidate_n = choose_parameters(
            Decimal(r_int),
            Decimal(m_int),
        )
        p_bound = Decimal(m_int) * candidate_delta / D2
        gap = D1 - binary_entropy(quarter)
        assert p_bound < quarter
        assert binary_kl(quarter, p_bound) > Decimal(r_int)
        assert Decimal(candidate_n) * gap > Decimal(r_int)

    print("Block-erasure counterexample: reproducibility check")
    print("===================================================")
    print(f"R = M                         : {r}")
    print(f"delta = epsilon               : {delta}")
    print(f"n                             : {n}")
    print(f"Bayes-error upper bound       : {error_bound}")
    print(f"d2(1/4 || error bound)        : {kl_barrier}")
    print(f"1 - h2(1/4)                   : {entropy_gap}")
    print(f"n * (1 - h2(1/4))             : {final_coefficient}")
    print()
    print("Independent finite enumeration:")
    print(f"I(Gamma; X2 | X1)             : {first}")
    print(f"I(Gamma; X1 | X2)             : {second}")
    print(f"erasure probability           : {enumerated_delta}")
    print()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
