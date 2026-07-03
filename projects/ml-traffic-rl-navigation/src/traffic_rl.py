"""Q-learning route planning for a small traffic-navigation grid.

The module is a dependency-free public remake of the RL side of a course
project that combined LSTM traffic forecasts with Q-learning navigation.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable


Action = int
State = int
Forecast = list[list[list[float]]]


ACTION_DELTAS: dict[Action, tuple[int, int]] = {
    0: (-1, 0),  # north
    1: (1, 0),  # south
    2: (0, -1),  # west
    3: (0, 1),  # east
}


@dataclass(frozen=True)
class TrainingConfig:
    episodes: int = 500
    max_steps: int = 100
    learning_rate: float = 0.1
    discount: float = 0.95
    epsilon_start: float = 0.5
    epsilon_min: float = 0.05
    epsilon_decay: float = 0.99
    distance_weight: float = 0.1
    congestion_weight: float = 0.5
    seed: int = 7


@dataclass(frozen=True)
class RouteResult:
    path: list[State]
    total_reward: float
    reached_goal: bool


class TrafficGridEnv:
    """A 3x4 road grid with congestion-aware rewards."""

    def __init__(
        self,
        rows: int = 3,
        cols: int = 4,
        start_state: State = 0,
        goal_state: State | None = None,
        forbidden_moves: set[tuple[State, Action]] | None = None,
        terminal_reward: float = 200.0,
        boundary_penalty: float = -10.0,
        wrong_direction_penalty: float = -20.0,
    ) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive")
        self.rows = rows
        self.cols = cols
        self.num_states = rows * cols
        self.num_actions = len(ACTION_DELTAS)
        self.start_state = start_state
        self.goal_state = self.num_states - 1 if goal_state is None else goal_state
        self.forbidden_moves = forbidden_moves or set()
        self.terminal_reward = terminal_reward
        self.boundary_penalty = boundary_penalty
        self.wrong_direction_penalty = wrong_direction_penalty
        self._validate_state(self.start_state)
        self._validate_state(self.goal_state)

    def _validate_state(self, state: State) -> None:
        if state < 0 or state >= self.num_states:
            raise ValueError(f"state {state} is outside the grid")

    def to_pos(self, state: State) -> tuple[int, int]:
        self._validate_state(state)
        return divmod(state, self.cols)

    def to_state(self, row: int, col: int) -> State:
        return row * self.cols + col

    def is_valid_move(self, state: State, action: Action) -> bool:
        row, col = self.to_pos(state)
        d_row, d_col = ACTION_DELTAS[action]
        next_row = row + d_row
        next_col = col + d_col
        return 0 <= next_row < self.rows and 0 <= next_col < self.cols

    def next_state(self, state: State, action: Action) -> State:
        if not self.is_valid_move(state, action):
            return state
        row, col = self.to_pos(state)
        d_row, d_col = ACTION_DELTAS[action]
        return self.to_state(row + d_row, col + d_col)

    def manhattan_to_goal(self, state: State) -> int:
        row, col = self.to_pos(state)
        goal_row, goal_col = self.to_pos(self.goal_state)
        return abs(goal_row - row) + abs(goal_col - col)

    def step(
        self,
        state: State,
        action: Action,
        forecast: Forecast,
        distance_weight: float,
        congestion_weight: float,
    ) -> tuple[State, float, bool]:
        if action not in ACTION_DELTAS:
            raise ValueError(f"unknown action {action}")
        if not self.is_valid_move(state, action):
            return state, self.boundary_penalty, False
        if (state, action) in self.forbidden_moves:
            return state, self.wrong_direction_penalty, False

        next_state = self.next_state(state, action)
        if next_state == self.goal_state:
            return next_state, self.terminal_reward, True

        congestion = discounted_congestion(forecast[state][action], congestion_weight)
        distance = self.manhattan_to_goal(next_state) * distance_weight
        reward = -(congestion + distance)
        return next_state, reward, False


def discounted_congestion(values: Iterable[float], discount: float) -> float:
    """Aggregate multi-step predicted flow into one route-planning penalty."""

    total = 0.0
    weight = 1.0
    for value in values:
        total += max(0.0, float(value)) * weight
        weight *= discount
    return total


def make_demo_forecast(
    num_states: int = 12,
    num_actions: int = 4,
    horizon: int = 12,
    busy_corridor: set[tuple[State, Action]] | None = None,
) -> Forecast:
    """Create deterministic directional traffic forecasts.

    The shape mirrors the course report's RL input idea: each state-action pair
    receives a 12-step forecast from the prediction layer.
    """

    busy_corridor = busy_corridor or {(1, 3), (5, 1), (9, 3)}
    forecast: Forecast = []
    for state in range(num_states):
        state_values: list[list[float]] = []
        for action in range(num_actions):
            base = 0.15 + 0.02 * ((state + action) % 5)
            if (state, action) in busy_corridor:
                base += 0.65
            trend = [base + 0.015 * math.sin(step / 2.0 + state) for step in range(horizon)]
            state_values.append(trend)
        forecast.append(state_values)
    return forecast


def initialize_q_table(num_states: int, num_actions: int) -> list[list[float]]:
    return [[0.0 for _ in range(num_actions)] for _ in range(num_states)]


def choose_action(
    q_table: list[list[float]],
    state: State,
    epsilon: float,
    rng: random.Random,
    valid_actions: list[Action],
) -> Action:
    if rng.random() < epsilon:
        return rng.choice(valid_actions)
    values = q_table[state]
    return max(valid_actions, key=lambda action: (values[action], -action))


def valid_actions(env: TrafficGridEnv, state: State) -> list[Action]:
    return [action for action in ACTION_DELTAS if env.is_valid_move(state, action)]


def train_q_learning(
    env: TrafficGridEnv,
    forecast: Forecast,
    config: TrainingConfig = TrainingConfig(),
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(config.seed)
    q_table = initialize_q_table(env.num_states, env.num_actions)
    episode_rewards: list[float] = []
    epsilon = config.epsilon_start

    for _ in range(config.episodes):
        state = env.start_state
        total_reward = 0.0
        for _step in range(config.max_steps):
            actions = valid_actions(env, state)
            action = choose_action(q_table, state, epsilon, rng, actions)
            next_state, reward, done = env.step(
                state,
                action,
                forecast,
                config.distance_weight,
                config.congestion_weight,
            )
            future = 0.0 if done else max(q_table[next_state][a] for a in valid_actions(env, next_state))
            target = reward + config.discount * future
            q_table[state][action] += config.learning_rate * (target - q_table[state][action])
            total_reward += reward
            state = next_state
            if done:
                break
        episode_rewards.append(total_reward)
        epsilon = max(config.epsilon_min, epsilon * config.epsilon_decay)

    return q_table, episode_rewards


def greedy_route(
    env: TrafficGridEnv,
    q_table: list[list[float]],
    forecast: Forecast,
    config: TrainingConfig = TrainingConfig(),
) -> RouteResult:
    state = env.start_state
    path = [state]
    total_reward = 0.0
    for _ in range(config.max_steps):
        actions = valid_actions(env, state)
        action = max(actions, key=lambda a: (q_table[state][a], -a))
        next_state, reward, done = env.step(
            state,
            action,
            forecast,
            config.distance_weight,
            config.congestion_weight,
        )
        total_reward += reward
        path.append(next_state)
        state = next_state
        if done:
            return RouteResult(path, total_reward, True)
    return RouteResult(path, total_reward, False)


def train_demo() -> RouteResult:
    env = TrafficGridEnv()
    forecast = make_demo_forecast()
    config = TrainingConfig(episodes=650, seed=11)
    q_table, _rewards = train_q_learning(env, forecast, config)
    return greedy_route(env, q_table, forecast, config)


def main() -> None:
    result = train_demo()
    print("greedy path:", " -> ".join(str(state) for state in result.path))
    print(f"reached goal: {result.reached_goal}")
    print(f"total reward: {result.total_reward:.2f}")


if __name__ == "__main__":
    main()
