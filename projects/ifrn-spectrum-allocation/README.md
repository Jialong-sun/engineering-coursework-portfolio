# IFRN Spectrum Allocation

Small, dependency-free Python simulator for interference-aware frequency reuse in an M-cell network. It is based on the same engineering theme as a 5G+/B5G spectrum-allocation research exercise, but the code and examples are rewritten from scratch for a public portfolio.

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

The project is useful for communications, robotics connectivity, intelligent hardware, and autonomous-system roles because it turns a network-planning concept into a runnable engineering model with metrics.
