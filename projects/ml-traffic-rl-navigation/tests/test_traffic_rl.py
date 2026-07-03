import pathlib
import sys


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from traffic_rl import (  # noqa: E402
    TrafficGridEnv,
    TrainingConfig,
    discounted_congestion,
    greedy_route,
    make_demo_forecast,
    train_q_learning,
)


def test_discounted_congestion_uses_future_steps() -> None:
    assert discounted_congestion([1.0, 1.0, 1.0], 0.5) == 1.75


def test_environment_penalizes_congested_direction() -> None:
    env = TrafficGridEnv()
    forecast = make_demo_forecast(busy_corridor={(0, 3)})
    _, east_reward, _ = env.step(0, 3, forecast, distance_weight=0.1, congestion_weight=0.5)
    _, south_reward, _ = env.step(0, 1, forecast, distance_weight=0.1, congestion_weight=0.5)
    assert east_reward < south_reward


def test_environment_penalizes_forbidden_direction() -> None:
    env = TrafficGridEnv(forbidden_moves={(0, 3)})
    forecast = make_demo_forecast()
    next_state, reward, done = env.step(0, 3, forecast, distance_weight=0.1, congestion_weight=0.5)

    assert next_state == 0
    assert reward == env.wrong_direction_penalty
    assert not done


def test_training_learns_route_to_goal() -> None:
    env = TrafficGridEnv()
    forecast = make_demo_forecast()
    config = TrainingConfig(episodes=650, seed=23)
    q_table, rewards = train_q_learning(env, forecast, config)
    route = greedy_route(env, q_table, forecast, config)

    assert len(q_table) == 12
    assert len(q_table[0]) == 4
    assert len(rewards) == config.episodes
    assert route.reached_goal
    assert route.path[0] == env.start_state
    assert route.path[-1] == env.goal_state
    assert len(route.path) <= 8


if __name__ == "__main__":
    test_discounted_congestion_uses_future_steps()
    test_environment_penalizes_congested_direction()
    test_environment_penalizes_forbidden_direction()
    test_training_learns_route_to_goal()
    print("ml-traffic-rl-navigation checks passed")
