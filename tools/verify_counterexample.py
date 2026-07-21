"""High-precision arithmetic verifier for the block-erasure counterexample.

This module checks the numerical margins used by the proof.  It deliberately
uses only Python's standard library.  It does not replace the information-
theoretic proof in proof/COUNTEREXAMPLE.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR, getcontext, localcontext
from typing import Iterable

PRECISION = 90
getcontext().prec = PRECISION
ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
FOUR = Decimal(4)


def d(value: int | str | Decimal) -> Decimal:
    """Convert a value to Decimal without introducing binary float error."""

    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def log2(x: Decimal) -> Decimal:
    if x <= ZERO:
        raise ValueError("log2 is defined here only for positive Decimal values")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return x.ln() / TWO.ln()


def binary_entropy(p: Decimal) -> Decimal:
    """Binary entropy h2(p), in bits."""

    p = d(p)
    if p < ZERO or p > ONE:
        raise ValueError("p must lie in [0,1]")
    if p == ZERO or p == ONE:
        return ZERO
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return -(p * log2(p) + (ONE - p) * log2(ONE - p))


def binary_kl(q: Decimal, p: Decimal) -> Decimal:
    """Binary KL divergence d2(q || p), in bits."""

    q = d(q)
    p = d(p)
    if not (ZERO <= q <= ONE and ZERO <= p <= ONE):
        raise ValueError("p and q must lie in [0,1]")
    if p == ZERO:
        return ZERO if q == ZERO else Decimal("Infinity")
    if p == ONE:
        return ZERO if q == ONE else Decimal("Infinity")

    with localcontext() as ctx:
        ctx.prec = PRECISION
        first = ZERO if q == ZERO else q * log2(q / p)
        second = ZERO if q == ONE else (ONE - q) * log2((ONE - q) / (ONE - p))
        return first + second


@dataclass(frozen=True)
class Parameters:
    redundancy_constant: Decimal
    maximality_constant: Decimal
    erasure_probability: Decimal
    block_length: int

    @property
    def predictor_error_bound(self) -> Decimal:
        return self.maximality_constant * self.erasure_probability / TWO

    @property
    def entropy_gap(self) -> Decimal:
        return ONE - binary_entropy(ONE / FOUR)

    @property
    def kl_barrier(self) -> Decimal:
        return binary_kl(ONE / FOUR, self.predictor_error_bound)

    @property
    def final_coefficient(self) -> Decimal:
        return d(self.block_length) * self.entropy_gap

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.redundancy_constant < ZERO:
            errors.append("redundancy constant must be nonnegative")
        if self.maximality_constant < ZERO:
            errors.append("maximality constant must be nonnegative")
        if not (ZERO < self.erasure_probability < ONE):
            errors.append("erasure probability must lie in (0,1)")
        if self.block_length <= 0:
            errors.append("block length must be positive")
        predictor_bound = self.predictor_error_bound
        if not (ZERO <= predictor_bound < ONE / FOUR):
            errors.append("predictor error bound is not in [0,1/4)")
        elif not self.kl_barrier > self.redundancy_constant:
            errors.append("KL barrier does not exceed redundancy constant")
        if not self.final_coefficient > self.redundancy_constant:
            errors.append("final coefficient does not exceed redundancy constant")
        return errors


def explicit_factor_three_parameters() -> Parameters:
    return Parameters(
        redundancy_constant=d(3),
        maximality_constant=d(3),
        erasure_probability=ONE / (TWO ** 18),
        block_length=16,
    )


def choose_parameters(
    redundancy_constant: int | str | Decimal,
    maximality_constant: int | str | Decimal,
    *,
    max_power: int = 10000,
) -> Parameters:
    """Find dyadic delta=2^-k and the smallest valid block length.

    The proof guarantees that a choice exists for every finite nonnegative R,M.
    This routine turns that existence argument into a deterministic parameter
    search for review and regression testing.
    """

    r = d(redundancy_constant)
    m = d(maximality_constant)
    if r < ZERO or m < ZERO:
        raise ValueError("constants must be nonnegative")

    gap = ONE - binary_entropy(ONE / FOUR)
    n = int((r / gap).to_integral_value(rounding=ROUND_FLOOR)) + 1

    if m == ZERO:
        return Parameters(r, m, ONE / TWO, n)

    for power in range(1, max_power + 1):
        delta = ONE / (TWO ** power)
        candidate = Parameters(r, m, delta, n)
        if not candidate.validate():
            return candidate

    raise RuntimeError(f"no dyadic parameter found through 2^-{max_power}")


def construction_identities(delta: Decimal) -> dict[str, Decimal]:
    """Exact information identities for a coordinate competitor, in bits."""

    delta = d(delta)
    if not (ZERO < delta < ONE):
        raise ValueError("delta must lie in (0,1)")
    return {
        "I(Sj;X2|X1)": ZERO,
        "I(Sj;X1|X2)": delta,
        "epsilon": delta,
    }


def render_report(params: Parameters) -> str:
    ids = construction_identities(params.erasure_probability)
    lines = [
        "Block-erasure counterexample verification",
        "===========================================",
        f"R                          = {params.redundancy_constant}",
        f"M                          = {params.maximality_constant}",
        f"delta = epsilon            = {params.erasure_probability}",
        f"n                          = {params.block_length}",
        f"I(Sj;X2|X1)                = {ids['I(Sj;X2|X1)']}",
        f"I(Sj;X1|X2)                = {ids['I(Sj;X1|X2)']}",
        f"Bayes error upper bound    = {params.predictor_error_bound}",
        f"d2(1/4 || error bound)     = {params.kl_barrier}",
        f"1 - h2(1/4)                = {params.entropy_gap}",
        f"n * (1 - h2(1/4))          = {params.final_coefficient}",
    ]
    errors = params.validate()
    if errors:
        lines.append("RESULT: FAIL")
        lines.extend(f"  - {error}" for error in errors)
    else:
        lines.append("RESULT: PASS")
    return "\n".join(lines)


def verify_family(cases: Iterable[tuple[int, int]]) -> list[Parameters]:
    params: list[Parameters] = []
    for r, m in cases:
        candidate = choose_parameters(r, m)
        errors = candidate.validate()
        if errors:
            raise AssertionError(f"invalid parameters for R={r}, M={m}: {errors}")
        params.append(candidate)
    return params


if __name__ == "__main__":
    explicit = explicit_factor_three_parameters()
    print(render_report(explicit))
    if explicit.validate():
        raise SystemExit(1)
