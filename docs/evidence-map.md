# Evidence Map

This repository is a curated public portfolio, not a raw archive. The private source materials were checked locally before publication, and the public code was either refactored, rewritten, or built as a clearly labeled extension from verified coursework, internship, research, and thesis evidence.

No raw certificates, reports, screenshots, student IDs, classmates' names, company documents, or original coursework PDFs/DOCX files are included here.

## Claim Levels

- **Direct rewrite**: a public, cleaned implementation based on an existing code artifact or very specific lab task.
- **Theme rewrite**: original public code based on a documented project/report topic, not copied from the source file.
- **Portfolio extension**: an original mini-project that extends a verified learning theme; it should not be described as a completed original assignment.

## Project-to-Evidence Mapping

| Public project | Claim level | Local evidence checked | Evidence-supported boundary |
|---|---|---|---|
| `java-student-grade-manager` | Direct rewrite | Java experiment source tree containing GUI system classes, loader classes, sample score data, and a program-interface screenshot. | Supports Java GUI, object-oriented design, file loading, table/query workflow, and basic desktop data management. |
| `wireless-sensor-network-mst` | Direct rewrite | WSN assignment Python script using NetworkX to generate a connected random network and compute a minimum spanning tree with Prim/NetworkX logic. | Supports WSN topology generation, MST reduction, graph metrics, and visualization. |
| `network-routing-dijkstra` | Portfolio extension | Same WSN graph/topology coursework used above. No separate raw Dijkstra assignment was found in the checked materials. | Supports graph-algorithm extension only. The README must describe this as a WSN-themed public extension, not as a direct assignment rewrite. |
| `signal-fourier-lab` | Direct/theme rewrite | Signal-and-systems MATLAB reports covering Fourier analysis, sampling theorem verification, frequency spectra, continuous-time LTI analysis, convolution, and frequency-domain methods. | Supports Fourier/DFT, sampling, spectrum analysis, and LTI/convolution experiments. |
| `optical-fiber-link-budget` | Theme rewrite | Optical communication experiment report covering optical fiber transmission, 1310/1550 nm links, optical power, extinction ratio, APC, connectors, insertion loss, return loss, WDM, and CMI optical transmission. | Supports optical link-budget style calculations and optical communication engineering units. The FBG sensor part is a public reading-based extension, not a direct lab result. |
| `analog-rc-filter-tool` | Portfolio extension | Analog electronics course-design report around a superheterodyne transistor radio, circuit assembly, soldering, bias/debugging, and radio-frequency circuit principles. | Supports analog-circuit practice and frequency-response intuition. The RC filter calculator is an original public extension, not a raw coursework deliverable. |
| `fpga-digital-interface-lab` | Theme rewrite | Siemens internship summary documenting FPGA design/R&D internship, Verilog HDL practice, LED blinking, stopwatch, clock division, seven-segment dynamic scanning, ADC0809 timing/interface design, UART/IIC learning, Quartus II, and ModelSim verification. | Supports public-safe RTL blocks for timing, display scanning, edge detection, and ADC0809-style control. The code is original and must not be described as company code. |
| `thermal-control-fuzzy-pid` | Theme rewrite | Undergraduate thesis and evaluation materials on meter-wave solar radio spectrometer analog-receiver temperature stabilization with NTC sensing, TEC cooling/heating, thermal module, fuzzy PID control, dynamic response, and measured stability targets. | Supports TEC plant/control simulation, fuzzy-style PID scheduling, saturation, settling, ripple, and hardware-control framing. The Python model is illustrative, not calibrated raw lab data. |
| `ifrn-spectrum-allocation` | Theme rewrite | 5G+ frequency-allocation research reference letter documenting weekly network simulations, Matlab/Octave programming, final project theme "M-Cell IFRN Network", comparison under different settings, and successful technical work. | Supports M-cell IFRN/frequency-allocation simulation theme and trade-off metrics. The public Python code is a dependency-free remake, not the original Matlab/Octave submission. |
| `coursework-notes` | Summary rewrite | Course folders and reports spanning signal systems, WSN, IoT, optical communication, deep learning, analog circuits, data training, and engineering practice. | Supports high-level learning notes only; raw reports are intentionally excluded. |

## Wording Rules

- Use "rewritten", "public-safe", "derived from", "inspired by", or "extension" when the public code is not the exact original deliverable.
- Avoid implying that internship/company code, private reports, or raw assignment files were uploaded.
- Avoid claiming measured hardware results inside a simulation README unless those exact metrics are clearly separated as source-material evidence.
- Keep the repository strong through runnable code, tests, CI, and clean documentation rather than inflated claims.
