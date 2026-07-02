# FPGA Digital Interface Lab

Portfolio-safe FPGA/RTL practice inspired by communication-engineering internship work. The code is original and intentionally small: it demonstrates digital building blocks that often appear in entry-level FPGA board bring-up tasks without exposing any company-specific design.

## What Is Included

- `clock_divider.v`: parameterized counter divider with one-cycle tick output.
- `edge_detector.v`: rising/falling edge pulse detector.
- `seven_segment_scan.v`: four-digit seven-segment display scanner.
- `adc0809_reader.v`: ADC0809-style control FSM with `ALE`, `START`, `OE`, and `EOC` handshaking.
- `sim/digital_models.py`: Python reference models for deterministic behavior checks.
- `tests/test_digital_models.py`: smoke tests for interface timing and RTL source structure.

## Run

```bash
python tests/test_digital_models.py
```

## Portfolio Note

This project supports FPGA / hardware-development applications by showing RTL structure, finite-state-machine thinking, peripheral timing awareness, and clean public documentation. It is not copied from any internship repository.
