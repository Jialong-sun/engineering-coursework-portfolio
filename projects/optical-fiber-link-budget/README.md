# Optical Fiber Link Budget and FBG Sensor Model

This mini-project converts optical-communication coursework themes into a small command-line model for fiber link margin and FBG wavelength shift.

## What This Demonstrates

- Optical link budget calculation in dB/dBm
- Connector, splice, and fiber attenuation modeling
- Receiver sensitivity margin estimation
- FBG strain/temperature wavelength-shift model
- Pure Python implementation with deterministic tests

## Run

```powershell
python src/fiber_budget.py --tx-dbm 0 --length-km 25 --fiber-loss-db-km 0.22 --connectors 2 --splices 4 --rx-sensitivity-dbm -24
```

Example output:

```text
Received power: -7.70 dBm
System margin: 16.30 dB
FBG shift: 1.330 nm
```

## Test

```powershell
python tests/test_fiber_budget.py
```

## Portfolio Notes

This project is inspired by optical fiber communication coursework and FBG-related technical reading, rewritten as an engineering calculator rather than a raw report.
