"""Run all reproducibility checks from the repository root."""

from __future__ import annotations

import subprocess
import sys

from tools.finite_model_check import verify_coordinate_competitor
from tools.verify_counterexample import (
    explicit_factor_three_parameters,
    render_report,
    verify_family,
)


def main() -> int:
    params = explicit_factor_three_parameters()
    print(render_report(params))
    if params.validate():
        return 1

    print("\nIndependent finite-distribution check")
    print("=====================================")
    finite = verify_coordinate_competitor()
    tolerance = finite["delta"] * 0 + __import__("decimal").Decimal("1e-70")
    print(f"I(Gamma;X2|X1) = {finite['I(Gamma;X2|X1)']}")
    print(f"I(Gamma;X1|X2) = {finite['I(Gamma;X1|X2)']}")
    if abs(finite["I(Gamma;X2|X1)"]) > tolerance:
        return 1
    if abs(finite["I(Gamma;X1|X2)"] - finite["delta"]) > tolerance:
        return 1

    print("\nAdditional parameter-search checks")
    print("==================================")
    for candidate in verify_family([(1, 1), (2, 3), (3, 3), (10, 7), (100, 100)]):
        print(
            f"PASS R={candidate.redundancy_constant}, "
            f"M={candidate.maximality_constant}, "
            f"delta={candidate.erasure_probability}, "
            f"n={candidate.block_length}"
        )

    print("\nRunning regression tests")
    print("========================")
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
