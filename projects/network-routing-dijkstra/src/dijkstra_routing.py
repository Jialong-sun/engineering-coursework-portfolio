import argparse
import heapq
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

Graph = Dict[str, Dict[str, float]]


@dataclass(frozen=True)
class Route:
    source: str
    target: str
    path: List[str]
    cost: float

    @property
    def reachable(self) -> bool:
        return math.isfinite(self.cost)


def default_sensor_graph() -> Graph:
    return {
        "1": {"2": 5, "4": 1, "5": 3},
        "2": {"1": 5, "3": 4, "4": 1, "6": 4},
        "3": {"2": 4, "6": 3},
        "4": {"1": 1, "2": 1, "5": 2, "6": 8},
        "5": {"1": 3, "4": 2, "6": 3},
        "6": {"2": 4, "3": 3, "4": 8, "5": 3},
    }


def validate_graph(graph: Graph) -> None:
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            if weight < 0:
                raise ValueError(f"Negative edge weight is not supported: {node}->{neighbor}")


def shortest_path(graph: Graph, source: str, target: str) -> Route:
    validate_graph(graph)
    if source not in graph:
        raise KeyError(f"Unknown source node: {source}")
    if target not in graph:
        raise KeyError(f"Unknown target node: {target}")

    distances = {node: math.inf for node in graph}
    previous: Dict[str, str | None] = {node: None for node in graph}
    distances[source] = 0.0
    queue: List[Tuple[float, str]] = [(0.0, source)]

    while queue:
        current_cost, node = heapq.heappop(queue)
        if current_cost > distances[node]:
            continue
        if node == target:
            break

        for neighbor, edge_cost in graph[node].items():
            candidate = current_cost + edge_cost
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))

    path = reconstruct_path(previous, source, target) if math.isfinite(distances[target]) else []
    return Route(source=source, target=target, path=path, cost=distances[target])


def reconstruct_path(previous: Dict[str, str | None], source: str, target: str) -> List[str]:
    path = [target]
    node = target
    while node != source:
        parent = previous[node]
        if parent is None:
            return []
        path.append(parent)
        node = parent
    return list(reversed(path))


def all_routes_from(graph: Graph, source: str) -> Iterable[Route]:
    for target in sorted(graph):
        if target != source:
            yield shortest_path(graph, source, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dijkstra routing on a weighted sensor graph.")
    parser.add_argument("--source", default="1")
    parser.add_argument("--target", default="6")
    parser.add_argument("--all", action="store_true", help="Print routes from source to every other node.")
    return parser.parse_args()


def print_route(route: Route) -> None:
    if not route.reachable:
        print(f"No route from {route.source} to {route.target}.")
        return
    print(f"Shortest path {route.source} -> {route.target}: {' -> '.join(route.path)}")
    print(f"Total cost: {route.cost:.2f}")


def main() -> None:
    args = parse_args()
    graph = default_sensor_graph()
    if args.all:
        for route in all_routes_from(graph, args.source):
            print_route(route)
    else:
        print_route(shortest_path(graph, args.source, args.target))


if __name__ == "__main__":
    main()
