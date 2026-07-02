import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FrequencyResponse:
    frequency_hz: float
    cutoff_hz: float
    magnitude_db: float
    phase_deg: float


def cutoff_frequency_hz(resistance_ohm: float, capacitance_f: float) -> float:
    if resistance_ohm <= 0:
        raise ValueError("resistance_ohm must be positive.")
    if capacitance_f <= 0:
        raise ValueError("capacitance_f must be positive.")
    return 1.0 / (2 * math.pi * resistance_ohm * capacitance_f)


def lowpass_response(resistance_ohm: float, capacitance_f: float, frequency_hz: float) -> FrequencyResponse:
    cutoff = cutoff_frequency_hz(resistance_ohm, capacitance_f)
    ratio = frequency_hz / cutoff
    magnitude = 1 / math.sqrt(1 + ratio * ratio)
    phase = -math.degrees(math.atan(ratio))
    return FrequencyResponse(frequency_hz, cutoff, to_db(magnitude), phase)


def highpass_response(resistance_ohm: float, capacitance_f: float, frequency_hz: float) -> FrequencyResponse:
    cutoff = cutoff_frequency_hz(resistance_ohm, capacitance_f)
    ratio = frequency_hz / cutoff
    magnitude = ratio / math.sqrt(1 + ratio * ratio)
    phase = 90 - math.degrees(math.atan(ratio))
    return FrequencyResponse(frequency_hz, cutoff, to_db(magnitude), phase)


def to_db(linear_magnitude: float) -> float:
    if linear_magnitude <= 0:
        return -math.inf
    return 20 * math.log10(linear_magnitude)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="First-order RC filter response calculator.")
    parser.add_argument("--mode", choices=["lowpass", "highpass"], default="lowpass")
    parser.add_argument("--resistance", type=float, default=10_000)
    parser.add_argument("--capacitance", type=float, default=1e-8)
    parser.add_argument("--frequency", type=float, default=1_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == "lowpass":
        response = lowpass_response(args.resistance, args.capacitance, args.frequency)
    else:
        response = highpass_response(args.resistance, args.capacitance, args.frequency)

    print(f"Cutoff frequency: {response.cutoff_hz:.2f} Hz")
    print(f"Magnitude: {response.magnitude_db:.2f} dB")
    print(f"Phase: {response.phase_deg:.2f} deg")


if __name__ == "__main__":
    main()
