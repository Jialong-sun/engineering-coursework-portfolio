import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import dijkstra_routing  # noqa: E402


def assert_valid_path(graph, path, expected_source, expected_target) -> None:
    assert path[0] == expected_source
    assert path[-1] == expected_target
    for source, target in zip(path, path[1:]):
        assert target in graph[source]


def test_default_shortest_path() -> None:
    graph = dijkstra_routing.default_sensor_graph()
    route = dijkstra_routing.shortest_path(
        graph,
        source="1",
        target="6",
    )

    assert route.reachable
    assert route.cost == 6
    assert_valid_path(graph, route.path, "1", "6")


def test_all_routes_from_source() -> None:
    routes = list(dijkstra_routing.all_routes_from(dijkstra_routing.default_sensor_graph(), "1"))

    assert len(routes) == 5
    assert all(route.reachable for route in routes)


def test_unreachable_target() -> None:
    graph = {
        "1": {"2": 1},
        "2": {"1": 1},
        "3": {},
    }

    route = dijkstra_routing.shortest_path(graph, source="1", target="3")

    assert not route.reachable
    assert route.path == []
    assert math.isinf(route.cost)


def test_negative_weight_rejected() -> None:
    graph = {"1": {"2": -1}, "2": {}}

    try:
        dijkstra_routing.shortest_path(graph, source="1", target="2")
    except ValueError as exc:
        assert "Negative edge" in str(exc)
    else:
        raise AssertionError("Expected negative edge weight to be rejected.")


if __name__ == "__main__":
    test_default_shortest_path()
    test_all_routes_from_source()
    test_unreachable_target()
    test_negative_weight_rejected()
    print("Dijkstra routing tests passed.")
