# ML Traffic RL Navigation

Clean public remake of the reinforcement-learning route-planning part of a machine-learning group project: **Intelligent Traffic Congestion Prediction and Navigation System using LSTM and Reinforcement Learning**.

The checked PDF report describes a cascade architecture where an LSTM module predicts directional traffic flow for the next 12 five-minute steps, and a Q-learning agent uses those predicted congestion values plus a Manhattan-distance heuristic to choose a route on a simplified 3x4 urban road network.

## Evidence Boundary

- Source evidence: the submitted machine-learning group report by Jialong Sun and teammates.
- Public reference: [`YuweiZhang-002/Navigation-System-based-on-LSTM-and-Q-Learning`](https://github.com/YuweiZhang-002/Navigation-System-based-on-LSTM-and-Q-Learning), which is linked in the report.
- License status checked: the reference repository is public but has no explicit license.
- This project therefore does **not** copy the collaborator repository. It is an original, dependency-free implementation of the RL concepts documented in the report.

## What This Demonstrates

- 3x4 grid traffic-navigation environment with 12 intersection states.
- Q-table-based reinforcement learning with epsilon-greedy exploration.
- Bellman update using learning rate, discount factor, and future reward estimate.
- Reward function combining terminal reward, boundary penalty, forbidden-direction penalty, directional congestion penalty, and Manhattan-distance penalty.
- Deterministic synthetic forecast interface that mirrors the report's LSTM-to-RL data shape.
- Unit-style tests for reward sensitivity, policy learning, and route extraction.

## Run

```bash
python tests/test_traffic_rl.py
python src/traffic_rl.py
```

Example output:

```text
greedy path: 0 -> 4 -> 5 -> 6 -> 7 -> 11
reached goal: True
total reward: 197.43
```

## Portfolio Note

This project is useful for robotics, autonomous systems, intelligent transportation, and embedded-AI applications because it turns a prediction-driven decision-making idea into a compact, testable control policy. It is intentionally smaller than the original coursework system, but it keeps the key RL design decisions visible and reviewable.
