import argparse
import random
from dataclasses import dataclass
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import networkx as nx
except ModuleNotFoundError as exc:
    missing = exc.name or "required package"
    raise SystemExit(
        f"Missing dependency: {missing}. Run `pip install -r requirements.txt` first."
    ) from exc


@dataclass(frozen=True)
class NetworkSummary:
    nodes: int
    original_edges: int
    mst_edges: int
    attempts: int
    original_total_length: float
    mst_total_length: float


def validate_args(args: argparse.Namespace) -> None:
    if args.nodes < 2:
        raise ValueError("--nodes must be at least 2.")
    if args.area_size <= 0:
        raise ValueError("--area-size must be positive.")
    if args.radius_ratio <= 0:
        raise ValueError("--radius-ratio must be positive.")
    if not 0 <= args.edge_probability <= 1:
        raise ValueError("--edge-probability must be between 0 and 1.")
    if args.max_attempts < 1:
        raise ValueError("--max-attempts must be at least 1.")


def generate_random_network(
    num_nodes: int,
    area_size: float,
    communication_radius: float,
    edge_probability: float,
    seed: int | None = None,
    max_attempts: int = 2_000,
) -> tuple["nx.Graph", int]:
    rng = random.Random(seed)

    for attempt in range(1, max_attempts + 1):
        graph = nx.Graph()
        for node in range(1, num_nodes + 1):
            graph.add_node(
                node,
                pos=(rng.uniform(0, area_size), rng.uniform(0, area_size)),
            )

        for i in range(1, num_nodes + 1):
            for j in range(i + 1, num_nodes + 1):
                x1, y1 = graph.nodes[i]["pos"]
                x2, y2 = graph.nodes[j]["pos"]
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                if distance <= communication_radius and rng.random() < edge_probability:
                    graph.add_edge(i, j, weight=distance)

        if nx.is_connected(graph):
            return graph, attempt

    raise RuntimeError(
        "Failed to generate a connected graph. "
        "Try increasing --radius-ratio, --edge-probability, or --max-attempts."
    )


def total_edge_weight(graph: "nx.Graph") -> float:
    return sum(data["weight"] for _, _, data in graph.edges(data=True))


def summarize_network(graph: "nx.Graph", mst: "nx.Graph", attempts: int) -> NetworkSummary:
    return NetworkSummary(
        nodes=graph.number_of_nodes(),
        original_edges=graph.number_of_edges(),
        mst_edges=mst.number_of_edges(),
        attempts=attempts,
        original_total_length=total_edge_weight(graph),
        mst_total_length=total_edge_weight(mst),
    )


def draw_graph(ax, graph: "nx.Graph", title: str, area_size: float) -> None:
    pos = nx.get_node_attributes(graph, "pos")
    nx.draw(
        graph,
        pos,
        ax=ax,
        node_size=95,
        width=0.8,
        with_labels=True,
        font_size=7,
    )
    ax.set_title(title)
    ax.set_xlim(0, area_size)
    ax.set_ylim(0, area_size)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")


def print_summary(summary: NetworkSummary) -> None:
    print(f"Nodes: {summary.nodes}")
    print(f"Original edges: {summary.original_edges}")
    print(f"MST edges: {summary.mst_edges}")
    print(f"Generation attempts: {summary.attempts}")
    print(f"Original total link length: {summary.original_total_length:.2f}")
    print(f"MST total link length: {summary.mst_total_length:.2f}")


def run(args: argparse.Namespace) -> None:
    validate_args(args)
    radius = args.radius_ratio * args.area_size
    graph, attempts = generate_random_network(
        args.nodes,
        args.area_size,
        radius,
        args.edge_probability,
        seed=args.seed,
        max_attempts=args.max_attempts,
    )
    mst = nx.minimum_spanning_tree(graph)
    summary = summarize_network(graph, mst, attempts)
    print_summary(summary)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    draw_graph(
        axes[0],
        graph,
        f"Initial Topology\nLinks: {summary.original_edges} | Attempts: {summary.attempts}",
        args.area_size,
    )
    draw_graph(
        axes[1],
        mst,
        f"Minimum Spanning Tree\nLinks: {summary.mst_edges}",
        args.area_size,
    )
    fig.tight_layout()

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=180)
        print(f"Saved figure to {output}")
    else:
        plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wireless sensor network topology and MST simulation."
    )
    parser.add_argument("--nodes", type=int, default=80)
    parser.add_argument("--area-size", type=float, default=100)
    parser.add_argument("--radius-ratio", type=float, default=1 / 3)
    parser.add_argument("--edge-probability", type=float, default=0.8)
    parser.add_argument("--max-attempts", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", type=str, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
