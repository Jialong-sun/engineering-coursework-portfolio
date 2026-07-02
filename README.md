# Engineering Coursework Portfolio

Curated undergraduate engineering coursework and mini-projects by **Jialong Sun**.

This repository is intentionally **not** a raw homework archive. It keeps only portfolio-friendly materials: runnable source code, anonymized sample data, concise documentation, and rewritten engineering notes.

Raw documents containing student IDs, classmates' names, course handouts, personal files, screenshots with private data, or assignment-only wording have been excluded.

## Engineering Signals

- CI workflow under `.github/workflows/ci.yml` checks the Python simulation and Java project.
- Python project includes a deterministic smoke test for graph generation and MST behavior.
- Java project includes a non-GUI smoke test for CSV loading and sample-data validation.
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
| `coursework-notes` | Signal systems, optical communication, IoT, deep learning, analog circuits | Summarizes engineering foundations without exposing raw homework. |

## Repository Structure

```text
.
|-- projects/
|   |-- java-student-grade-manager/
|   |-- wireless-sensor-network-mst/
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
GitHub: https://github.com/<your-username>/engineering-coursework-portfolio
```

## Notes

The goal of this repository is to show engineering habits and technical breadth without overwhelming reviewers with raw coursework files. Each included project has its own README and can be reviewed independently.
