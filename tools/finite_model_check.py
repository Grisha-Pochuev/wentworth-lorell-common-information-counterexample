"""Independent finite-distribution check of the coordinate competitors."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Callable, Hashable, Iterable

from tools.verify_counterexample import PRECISION, log2

getcontext().prec = PRECISION
State = tuple[int, int | str, int]
Distribution = dict[State, Fraction]


def block_erasure_joint(n: int, delta: Fraction, coordinate: int = 0) -> Distribution:
    """Return P(X1, X2, Gamma_j) for Gamma_j equal to one bit of X1."""

    if n <= 0:
        raise ValueError("n must be positive")
    if not (Fraction(0) < delta < Fraction(1)):
        raise ValueError("delta must lie in (0,1)")
    if not (0 <= coordinate < n):
        raise ValueError("coordinate is outside the bit block")

    distribution: defaultdict[State, Fraction] = defaultdict(Fraction)
    p_s = Fraction(1, 2**n)
    for s in range(2**n):
        gamma = (s >> coordinate) & 1
        distribution[(s, s, gamma)] += p_s * (1 - delta)
        distribution[(s, "bottom", gamma)] += p_s * delta
    return dict(distribution)


def marginal(
    distribution: Distribution,
    key: Callable[[State], Hashable],
) -> dict[Hashable, Fraction]:
    result: defaultdict[Hashable, Fraction] = defaultdict(Fraction)
    for state, probability in distribution.items():
        result[key(state)] += probability
    return dict(result)


def entropy(probabilities: Iterable[Fraction]) -> Decimal:
    total = Decimal(0)
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
    """Compute I(A;B|C)=H(A,C)+H(B,C)-H(C)-H(A,B,C)."""

    ac = marginal(distribution, lambda state: (a(state), c(state)))
    bc = marginal(distribution, lambda state: (b(state), c(state)))
    cc = marginal(distribution, c)
    abc = marginal(distribution, lambda state: (a(state), b(state), c(state)))
    return entropy(ac.values()) + entropy(bc.values()) - entropy(cc.values()) - entropy(abc.values())


def verify_coordinate_competitor(n: int = 4, delta: Fraction = Fraction(1, 8)) -> dict[str, Decimal]:
    distribution = block_erasure_joint(n=n, delta=delta)
    x1 = lambda state: state[0]
    x2 = lambda state: state[1]
    gamma = lambda state: state[2]
    return {
        "I(Gamma;X2|X1)": conditional_mutual_information(distribution, gamma, x2, x1),
        "I(Gamma;X1|X2)": conditional_mutual_information(distribution, gamma, x1, x2),
        "delta": Decimal(delta.numerator) / Decimal(delta.denominator),
    }


if __name__ == "__main__":
    values = verify_coordinate_competitor()
    for name, value in values.items():
        print(f"{name} = {value}")
