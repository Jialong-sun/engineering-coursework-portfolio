# Signal Fourier Lab

This mini-project turns signal-and-systems coursework into a small reusable Python toolkit for Fourier analysis and LTI convolution experiments.

## What This Demonstrates

- Discrete Fourier transform implemented from first principles
- Dominant-frequency detection for sampled signals
- Linear convolution for LTI system response
- Deterministic signal generation and no third-party runtime dependencies

## Run

```powershell
python src/fourier_lab.py --samples 64 --sample-rate 64 --freq-a 5 --freq-b 13
```

Example output:

```text
Dominant bins:
5.00 Hz
13.00 Hz
```

## Test

```powershell
python tests/test_fourier_lab.py
```

## Portfolio Notes

This project is inspired by signal-and-systems and MATLAB Fourier-analysis coursework, rewritten as clean Python code suitable for a public engineering portfolio.
