# Sensor Network Routing with Dijkstra

This mini-project implements Dijkstra shortest-path routing on a weighted graph, using a small wireless-sensor-network-style topology as the default example.

It is a public portfolio extension of documented WSN graph/topology coursework. It complements the directly rewritten MST project; it should not be read as a separate raw Dijkstra assignment upload.

## What This Demonstrates

- Shortest-path routing fundamentals
- Weighted adjacency-list graph modeling
- Priority-queue-based Dijkstra implementation
- Path reconstruction and unreachable-node handling
- Pure Python implementation with no third-party dependencies

## Run

```powershell
python src/dijkstra_routing.py --source 1 --target 6
```

Example output:

```text
Shortest path 1 -> 6: 1 -> 4 -> 2 -> 6
Total cost: 6.00
```

## Test

```powershell
python tests/test_dijkstra_routing.py
```

## Portfolio Notes

This project is an original extension from the wireless-sensor-network graph theme and rewritten into a reusable routing module. It complements the MST topology project by showing a second graph-algorithm workflow: shortest-path routing rather than topology reduction.
