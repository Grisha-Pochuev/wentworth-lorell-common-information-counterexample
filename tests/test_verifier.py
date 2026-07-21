from __future__ import annotations

import unittest
from decimal import Decimal

from fractions import Fraction

from tools.finite_model_check import verify_coordinate_competitor
from tools.verify_counterexample import (
    ONE,
    TWO,
    binary_entropy,
    binary_kl,
    choose_parameters,
    construction_identities,
    explicit_factor_three_parameters,
)


class CounterexampleVerifierTests(unittest.TestCase):
    def test_binary_entropy_quarter(self) -> None:
        gap = ONE - binary_entropy(ONE / Decimal(4))
        self.assertGreater(gap, Decimal("0.1887218755"))
        self.assertLess(gap, Decimal("0.1887218756"))

    def test_explicit_factor_three_parameters(self) -> None:
        params = explicit_factor_three_parameters()
        self.assertEqual(params.validate(), [])
        self.assertGreater(params.kl_barrier, Decimal(3))
        self.assertGreater(params.final_coefficient, Decimal(3))

    def test_construction_identities(self) -> None:
        delta = ONE / (TWO ** 18)
        identities = construction_identities(delta)
        self.assertEqual(identities["I(Sj;X2|X1)"], Decimal(0))
        self.assertEqual(identities["I(Sj;X1|X2)"], delta)
        self.assertEqual(identities["epsilon"], delta)

    def test_binary_kl_barrier_is_strict(self) -> None:
        params = explicit_factor_three_parameters()
        direct = binary_kl(ONE / Decimal(4), Decimal(3) / (TWO ** 19))
        self.assertEqual(direct, params.kl_barrier)
        self.assertGreater(direct, Decimal("3.54"))

    def test_parameter_search_for_multiple_constants(self) -> None:
        for r, m in [(1, 1), (2, 3), (3, 3), (10, 7), (100, 100)]:
            with self.subTest(R=r, M=m):
                params = choose_parameters(r, m)
                self.assertEqual(params.validate(), [])

    def test_independent_finite_distribution_check(self) -> None:
        values = verify_coordinate_competitor(n=4, delta=Fraction(1, 8))
        self.assertLess(abs(values["I(Gamma;X2|X1)"]), Decimal("1e-70"))
        self.assertLess(
            abs(values["I(Gamma;X1|X2)"] - values["delta"]),
            Decimal("1e-70"),
        )

    def test_zero_maximality_constant(self) -> None:
        params = choose_parameters(5, 0)
        self.assertEqual(params.validate(), [])


if __name__ == "__main__":
    unittest.main()
