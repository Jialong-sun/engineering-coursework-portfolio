# Thermal Control Fuzzy PID

Compact simulation of a TEC-based thermal control loop. The project is inspired by a receiver temperature-stabilization design, but the model and code are original public-portfolio materials.

## What It Demonstrates

- first-order thermal plant modeling;
- PID control with fuzzy-style gain scheduling;
- actuator saturation and anti-windup;
- settling-time and steady-state-ripple metrics.

## Run

```bash
python tests/test_thermal_control.py
python src/thermal_control.py
```

## Portfolio Note

This project is useful for hardware, embedded-control, robotics, and intelligent-hardware roles because it connects physical plant intuition with deterministic simulation and testable control metrics.
