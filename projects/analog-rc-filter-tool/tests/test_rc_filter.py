import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import rc_filter  # noqa: E402


def test_cutoff_frequency() -> None:
    cutoff = rc_filter.cutoff_frequency_hz(10_000, 1e-8)

    assert abs(cutoff - 1591.5494309189535) < 1e-9


def test_lowpass_at_cutoff_is_minus_three_db() -> None:
    cutoff = rc_filter.cutoff_frequency_hz(10_000, 1e-8)
    response = rc_filter.lowpass_response(10_000, 1e-8, cutoff)

    assert abs(response.magnitude_db + 3.010299956639812) < 1e-9
    assert abs(response.phase_deg + 45.0) < 1e-12


def test_highpass_at_cutoff_is_minus_three_db() -> None:
    cutoff = rc_filter.cutoff_frequency_hz(10_000, 1e-8)
    response = rc_filter.highpass_response(10_000, 1e-8, cutoff)

    assert abs(response.magnitude_db + 3.010299956639812) < 1e-9
    assert abs(response.phase_deg - 45.0) < 1e-12


if __name__ == "__main__":
    test_cutoff_frequency()
    test_lowpass_at_cutoff_is_minus_three_db()
    test_highpass_at_cutoff_is_minus_three_db()
    print("RC filter tests passed.")
