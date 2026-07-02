import sys
from argparse import Namespace
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import wsn_mst  # noqa: E402


def test_connected_network_and_mst() -> None:
    graph, attempts = wsn_mst.generate_random_network(
        num_nodes=12,
        area_size=100,
        communication_radius=70,
        edge_probability=0.9,
        seed=7,
        max_attempts=100,
    )
    mst = nx.minimum_spanning_tree(graph)
    summary = wsn_mst.summarize_network(graph, mst, attempts)

    assert nx.is_connected(graph)
    assert summary.nodes == 12
    assert summary.mst_edges == summary.nodes - 1
    assert summary.mst_total_length <= summary.original_total_length
    assert summary.attempts >= 1


def test_argument_validation() -> None:
    args = Namespace(
        nodes=1,
        area_size=100,
        radius_ratio=0.33,
        edge_probability=0.8,
        max_attempts=10,
    )

    try:
        wsn_mst.validate_args(args)
    except ValueError as exc:
        assert "--nodes" in str(exc)
    else:
        raise AssertionError("Expected validate_args to reject nodes < 2")


if __name__ == "__main__":
    test_connected_network_and_mst()
    test_argument_validation()
    print("WSN smoke tests passed.")
