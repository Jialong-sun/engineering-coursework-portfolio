# Engineering Coursework Portfolio

[![Portfolio CI](https://github.com/Jialong-sun/engineering-coursework-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/Jialong-sun/engineering-coursework-portfolio/actions/workflows/ci.yml)

Curated undergraduate engineering coursework and mini-projects by **Jialong Sun**.

This repository is intentionally **not** a raw homework archive. It keeps only portfolio-friendly materials: runnable source code, anonymized sample data, concise documentation, and rewritten engineering notes.

Raw documents containing student IDs, classmates' names, course handouts, personal files, screenshots with private data, or assignment-only wording have been excluded.

## Engineering Signals

- CI workflow under `.github/workflows/ci.yml` checks the Python simulations/calculators, Java project, and FPGA-interface reference models.
- Python project includes a deterministic smoke test for graph generation and MST behavior.
- Dijkstra routing project includes shortest-path tests for reachable, unreachable, and invalid-weight cases.
- Signal/Fourier, optical-link, analog-filter, thermal-control, and spectrum-allocation projects include deterministic engineering-unit tests.
- FPGA digital-interface project includes Verilog modules plus Python behavioral checks for edge detection, display scanning, and ADC0809-style timing.
- Java project includes Maven/JUnit tests for CSV loading and sample-data validation.
- Each project has its own README with run commands and portfolio notes.

## Recruiter Quick Scan

This portfolio supports applications for FPGA, hardware, embedded systems, communications, robotics, and intelligent hardware roles. It highlights:

- software engineering discipline: readable code, modular structure, explicit run instructions, and clean public documentation;
- engineering modeling ability: graph-based wireless sensor network simulation and MST topology reduction;
- system thinking: coursework coverage across communications, IoT, signal systems, optical communication, deep learning, and electronic circuits;
- privacy and professionalism: source files are curated, anonymized, and separated from raw class materials.

## Highlighted Projects

| Project | Focus | Why It Matters |
|---|---|---|
| `java-student-grade-manager` | Java Swing, file parsing, GUI table query, statistics | Demonstrates object-oriented programming, desktop UI, data loading, sorting, and basic software architecture. |
| `wireless-sensor-network-mst` | Python, NetworkX, random graph generation, minimum spanning tree | Demonstrates wireless sensor network topology modeling, graph algorithms, parameterized experiments, and visualization. |
| `network-routing-dijkstra` | Python, Dijkstra, priority queue, shortest-path routing | Demonstrates routing-oriented graph algorithms for sensor-network-style weighted topologies. |
| `signal-fourier-lab` | Python, DFT, LTI convolution, moving-average filtering | Demonstrates DSP fundamentals without relying on black-box libraries. |
| `optical-fiber-link-budget` | Python, dB/dBm, fiber attenuation, FBG wavelength shift | Demonstrates optical communication link budgeting and sensing-model intuition. |
| `analog-rc-filter-tool` | Python, RC cutoff, low/high-pass frequency response | Demonstrates analog electronics modeling and engineering-unit calculation. |
| `fpga-digital-interface-lab` | Verilog, digital interfaces, ADC0809-style FSM, seven-segment scan | Demonstrates internship-relevant RTL structure, timing awareness, and board-bring-up fundamentals. |
| `thermal-control-fuzzy-pid` | Python, TEC plant model, fuzzy-style PID, saturation | Demonstrates hardware closed-loop control modeling related to receiver temperature stabilization. |
| `ifrn-spectrum-allocation` | Python, M-cell network, reuse factor, SINR/fairness metrics | Demonstrates research-style communication-network simulation and trade-off analysis. |
| `coursework-notes` | Signal systems, optical communication, IoT, deep learning, analog circuits | Summarizes engineering foundations without exposing raw homework. |

## Repository Structure

```text
.
|-- projects/
|   |-- java-student-grade-manager/
|   |-- wireless-sensor-network-mst/
|   |-- network-routing-dijkstra/
|   |-- signal-fourier-lab/
|   |-- optical-fiber-link-budget/
|   |-- analog-rc-filter-tool/
|   |-- fpga-digital-interface-lab/
|   |-- thermal-control-fuzzy-pid/
|   |-- ifrn-spectrum-allocation/
|   `-- coursework-notes/
|-- docs/
|   |-- resume-github-blurb.md
|   |-- github-upload-steps.md
|   `-- portfolio-selection-notes.md
|-- .github/workflows/ci.yml
|-- LICENSE
`-- .gitignore
```

## Suggested Resume Line

```text
GitHub: https://github.com/Jialong-sun/engineering-coursework-portfolio
```

## Notes

The goal of this repository is to show engineering habits and technical breadth without overwhelming reviewers with raw coursework files. Each included project has its own README and can be reviewed independently.
