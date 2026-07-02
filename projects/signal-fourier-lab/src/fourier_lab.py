import argparse
import cmath
import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class SpectrumPeak:
    frequency_hz: float
    magnitude: float


def generate_composite_signal(
    samples: int,
    sample_rate_hz: float,
    components: Sequence[Tuple[float, float]],
) -> List[float]:
    if samples <= 0:
        raise ValueError("samples must be positive.")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive.")

    signal = []
    for n in range(samples):
        t = n / sample_rate_hz
        value = sum(amplitude * math.sin(2 * math.pi * frequency * t) for frequency, amplitude in components)
        signal.append(value)
    return signal


def dft(signal: Sequence[float]) -> List[complex]:
    size = len(signal)
    if size == 0:
        raise ValueError("signal must not be empty.")

    spectrum = []
    for k in range(size):
        total = 0j
        for n, sample in enumerate(signal):
            angle = -2 * math.pi * k * n / size
            total += sample * cmath.exp(1j * angle)
        spectrum.append(total)
    return spectrum


def dominant_frequencies(
    signal: Sequence[float],
    sample_rate_hz: float,
    count: int = 2,
) -> List[SpectrumPeak]:
    if count < 1:
        raise ValueError("count must be at least 1.")
    spectrum = dft(signal)
    half = len(spectrum) // 2
    peaks = []
    for k in range(1, half + 1):
        frequency = k * sample_rate_hz / len(spectrum)
        magnitude = abs(spectrum[k]) / len(spectrum)
        peaks.append(SpectrumPeak(frequency_hz=frequency, magnitude=magnitude))
    return sorted(peaks, key=lambda peak: peak.magnitude, reverse=True)[:count]


def convolve(signal: Sequence[float], impulse_response: Sequence[float]) -> List[float]:
    if not signal or not impulse_response:
        raise ValueError("signal and impulse_response must not be empty.")

    output = [0.0] * (len(signal) + len(impulse_response) - 1)
    for i, sample in enumerate(signal):
        for j, impulse in enumerate(impulse_response):
            output[i + j] += sample * impulse
    return output


def moving_average_impulse(taps: int) -> List[float]:
    if taps < 1:
        raise ValueError("taps must be at least 1.")
    return [1.0 / taps] * taps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Small Fourier-analysis and LTI-convolution lab.")
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--sample-rate", type=float, default=64.0)
    parser.add_argument("--freq-a", type=float, default=5.0)
    parser.add_argument("--freq-b", type=float, default=13.0)
    parser.add_argument("--taps", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    signal = generate_composite_signal(
        samples=args.samples,
        sample_rate_hz=args.sample_rate,
        components=[(args.freq_a, 1.0), (args.freq_b, 0.5)],
    )
    peaks = dominant_frequencies(signal, sample_rate_hz=args.sample_rate, count=2)
    filtered = convolve(signal, moving_average_impulse(args.taps))

    print("Dominant bins:")
    for peak in peaks:
        print(f"{peak.frequency_hz:.2f} Hz")
    print(f"Filtered output length: {len(filtered)}")


if __name__ == "__main__":
    main()
