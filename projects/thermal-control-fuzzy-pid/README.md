# Thermal Control Fuzzy PID

Compact simulation of a TEC-based thermal control loop. The project is derived from a documented receiver temperature-stabilization thesis theme, but the model and code are original public-portfolio materials rather than calibrated raw experimental data.

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

This project is useful for hardware, embedded-control, robotics, and intelligent-hardware roles because it connects physical plant intuition with deterministic simulation and testable control metrics. The source evidence supports TEC cooling/heating, temperature sensing, fuzzy PID control, dynamic response, and receiver temperature-stability framing.
