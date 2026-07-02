# Analog RC Filter Tool

This mini-project models first-order RC low-pass and high-pass filters, turning analog-circuit coursework themes into a small frequency-response calculator.

## What This Demonstrates

- RC cutoff-frequency calculation
- Low-pass and high-pass transfer functions
- Magnitude and phase response in engineering units
- Pure Python implementation with deterministic tests

## Run

```powershell
python src/rc_filter.py --mode lowpass --resistance 10000 --capacitance 1e-8 --frequency 1000
```

Example output:

```text
Cutoff frequency: 1591.55 Hz
Magnitude: -1.45 dB
Phase: -32.14 deg
```

## Test

```powershell
python tests/test_rc_filter.py
```

## Portfolio Notes

This project is inspired by analog electronics and circuit-design coursework. It complements the digital/DSP projects by showing circuit-level modeling intuition.
