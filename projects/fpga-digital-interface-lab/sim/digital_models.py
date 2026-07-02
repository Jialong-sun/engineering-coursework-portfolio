"""Reference models for small FPGA digital-interface blocks."""

from __future__ import annotations

from dataclasses import dataclass


SEGMENT_ACTIVE_LOW = {
    0x0: "1000000",
    0x1: "1111001",
    0x2: "0100100",
    0x3: "0110000",
    0x4: "0011001",
    0x5: "0010010",
    0x6: "0000010",
    0x7: "1111000",
    0x8: "0000000",
    0x9: "0010000",
    0xA: "0001000",
    0xB: "0000011",
    0xC: "1000110",
    0xD: "0100001",
    0xE: "0000110",
    0xF: "0001110",
}


def edge_pulses(samples: list[int]) -> tuple[list[int], list[int]]:
    """Return one-cycle rising and falling edge pulses for a binary sequence."""

    previous = 0
    rising: list[int] = []
    falling: list[int] = []
    for value in samples:
        bit = 1 if value else 0
        rising.append(1 if bit and not previous else 0)
        falling.append(1 if previous and not bit else 0)
        previous = bit
    return rising, falling


def seven_segment_pattern(value: int) -> str:
    """Return active-low seven-segment pattern for one hexadecimal digit."""

    return SEGMENT_ACTIVE_LOW[value & 0xF]


@dataclass
class Adc0809ReaderModel:
    """Cycle-level behavioral model of the ADC0809 reader FSM."""

    setup_cycles: int = 4
    state: str = "IDLE"
    setup_count: int = 0
    sample: int = 0

    def tick(self, start: bool, eoc: bool, adc_data: int) -> dict[str, int | str]:
        ale = 0
        start_conv = 0
        oe = 0
        busy = 1 if self.state != "IDLE" else 0
        done = 0

        if self.state == "IDLE":
            busy = 0
            if start:
                ale = 1
                busy = 1
                self.setup_count = 0
                self.state = "LATCH"
        elif self.state == "LATCH":
            ale = 1
            if self.setup_count >= self.setup_cycles - 1:
                self.setup_count = 0
                self.state = "START"
            else:
                self.setup_count += 1
        elif self.state == "START":
            start_conv = 1
            self.state = "WAIT_LOW"
        elif self.state == "WAIT_LOW":
            if not eoc:
                self.state = "WAIT_HIGH"
        elif self.state == "WAIT_HIGH":
            if eoc:
                self.state = "READ"
        elif self.state == "READ":
            oe = 1
            done = 1
            busy = 0
            self.sample = adc_data & 0xFF
            self.state = "IDLE"

        return {
            "state": self.state,
            "ale": ale,
            "start_conv": start_conv,
            "oe": oe,
            "busy": busy,
            "done": done,
            "sample": self.sample,
        }
