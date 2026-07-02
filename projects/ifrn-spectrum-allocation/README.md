# IFRN Spectrum Allocation

Small, dependency-free Python simulator for interference-aware frequency reuse in an M-cell network. It is based on a documented 5G+/B5G frequency-allocation research exercise whose final project theme was M-cell IFRN network simulation, but the code and examples are rewritten from scratch for a public portfolio.

## What It Demonstrates

- hex-grid cellular topology generation;
- reuse-factor channel assignment;
- co-channel interference scoring;
- SINR, spectral-efficiency, and Jain fairness metrics;
- deterministic sweep tests for architecture trade-off thinking.

## Run

```bash
python tests/test_ifrn_allocator.py
python src/ifrn_allocator.py
```

## Portfolio Note

The project is useful for communications, robotics connectivity, intelligent hardware, and autonomous-system roles because it turns a network-planning concept into a runnable engineering model with metrics. It is a public Python remake, not the original Matlab/Octave submission.
