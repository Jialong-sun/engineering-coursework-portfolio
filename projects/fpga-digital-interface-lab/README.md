# FPGA Digital Interface Lab

Portfolio-safe FPGA/RTL practice grounded in documented communication-engineering internship topics. The code is original and intentionally small: it demonstrates digital building blocks that often appear in entry-level FPGA board bring-up tasks without exposing any company-specific design.

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

This project supports FPGA / hardware-development applications by showing RTL structure, finite-state-machine thinking, peripheral timing awareness, and clean public documentation. The source evidence mentions Verilog HDL, LED timing, clock division, seven-segment dynamic scanning, ADC0809 timing/interface design, UART/IIC learning, Quartus II, and ModelSim. This repository contains only original public-safe practice code, not internship or company code.
