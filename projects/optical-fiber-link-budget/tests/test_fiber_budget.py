import sys
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import fiber_budget  # noqa: E402


def test_link_budget_margin() -> None:
    budget = fiber_budget.LinkBudget(
        tx_power_dbm=0,
        length_km=25,
        fiber_loss_db_per_km=0.22,
        connectors=2,
        connector_loss_db=0.5,
        splices=4,
        splice_loss_db=0.05,
        receiver_sensitivity_dbm=-24,
        system_margin_db=1,
    )

    assert abs(budget.total_loss_db - 7.7) < 1e-12
    assert abs(budget.received_power_dbm + 7.7) < 1e-12
    assert abs(budget.margin_db - 16.3) < 1e-12
    assert budget.passes


def test_fbg_wavelength_shift() -> None:
    shifted = fiber_budget.fbg_wavelength_shift_nm(
        center_wavelength_nm=1550,
        strain_microstrain=1000,
        temperature_delta_c=13,
    )

    assert abs(shifted - 1551.33) < 1e-12


def test_argument_validation() -> None:
    args = Namespace(
        tx_dbm=0,
        length_km=-1,
        fiber_loss_db_km=0.22,
        connectors=2,
        connector_loss_db=0.5,
        splices=4,
        splice_loss_db=0.05,
        rx_sensitivity_dbm=-24,
        system_margin_db=1,
    )

    try:
        fiber_budget.build_budget(args)
    except ValueError as exc:
        assert "length_km" in str(exc)
    else:
        raise AssertionError("Expected negative length to be rejected.")


if __name__ == "__main__":
    test_link_budget_margin()
    test_fbg_wavelength_shift()
    test_argument_validation()
    print("Fiber budget tests passed.")
