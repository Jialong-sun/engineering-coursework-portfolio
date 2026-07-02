import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import fourier_lab  # noqa: E402


def test_detects_dominant_frequencies() -> None:
    signal = fourier_lab.generate_composite_signal(
        samples=64,
        sample_rate_hz=64,
        components=[(5, 1.0), (13, 0.5)],
    )

    peaks = fourier_lab.dominant_frequencies(signal, sample_rate_hz=64, count=2)
    frequencies = sorted(round(peak.frequency_hz) for peak in peaks)

    assert frequencies == [5, 13]


def test_convolution_length_and_values() -> None:
    output = fourier_lab.convolve([1, 2, 3], [0.5, 0.5])

    assert output == [0.5, 1.5, 2.5, 1.5]


def test_moving_average_impulse_sums_to_one() -> None:
    impulse = fourier_lab.moving_average_impulse(4)

    assert len(impulse) == 4
    assert abs(sum(impulse) - 1.0) < 1e-12


if __name__ == "__main__":
    test_detects_dominant_frequencies()
    test_convolution_length_and_values()
    test_moving_average_impulse_sums_to_one()
    print("Fourier lab tests passed.")
