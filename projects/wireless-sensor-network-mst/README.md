# Wireless Sensor Network Topology and MST Simulation

This mini-project generates a random connected wireless sensor network, visualizes its topology, and computes a minimum spanning tree (MST) using NetworkX.

## What This Demonstrates

- Random graph modeling for wireless sensor networks
- Communication-radius-based link generation
- Connectivity checking
- Minimum spanning tree calculation
- Matplotlib visualization
- Parameter validation, deterministic seeds, and basic experiment metrics

## Run

```powershell
pip install -r requirements.txt
python src/wsn_mst.py --nodes 80 --area-size 100 --radius-ratio 0.33 --seed 42 --output outputs/wsn_mst.png
```

The script prints topology metrics and saves a figure comparing the original network with its MST.

Example output:

```text
Nodes: 80
Original edges: <computed at runtime>
MST edges: 79
Generation attempts: <computed at runtime>
Original total link length: <computed at runtime>
MST total link length: <computed at runtime>
```

## Test

```powershell
pip install -r requirements.txt
python tests/test_wsn_mst.py
```

## Portfolio Notes

This project came from wireless sensor network coursework and has been cleaned into a reusable script with arguments, deterministic seeds, and output support.
