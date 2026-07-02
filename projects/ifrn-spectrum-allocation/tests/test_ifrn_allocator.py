from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ifrn_allocator import assign_channels, build_hex_grid, evaluate_allocation, sweep_reuse_factors


def test_hex_grid_cell_count_radius_two():
    cells = build_hex_grid(radius=2)
    assert len(cells) == 19
    assert len({cell.cell_id for cell in cells}) == 19


def test_reuse_reduces_cochannel_interference():
    cells = build_hex_grid(radius=2)
    reuse_1 = evaluate_allocation(cells, assign_channels(cells, reuse_factor=1, channel_count=7))
    reuse_7 = evaluate_allocation(cells, assign_channels(cells, reuse_factor=7, channel_count=7))

    assert reuse_7.total_interference < reuse_1.total_interference
    assert reuse_7.average_sinr > reuse_1.average_sinr


def test_sweep_keeps_fairness_in_valid_range():
    results = sweep_reuse_factors(radius=2)
    assert [row.reuse_factor for row in results] == [1, 3, 4, 7]
    for row in results:
        assert 0.0 < row.jain_fairness <= 1.0
        assert row.average_spectral_efficiency > 0.0


if __name__ == "__main__":
    test_hex_grid_cell_count_radius_two()
    test_reuse_reduces_cochannel_interference()
    test_sweep_keeps_fairness_in_valid_range()
    print("ifrn-spectrum-allocation checks passed")
