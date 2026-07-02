"""Interference-aware frequency reuse simulator for M-cell networks."""

from __future__ import annotations

from dataclasses import dataclass
from math import log2, sqrt


@dataclass(frozen=True)
class Cell:
    cell_id: int
    q: int
    r: int
    x: float
    y: float


@dataclass(frozen=True)
class AllocationResult:
    reuse_factor: int
    channel_count: int
    total_interference: float
    average_sinr: float
    average_spectral_efficiency: float
    jain_fairness: float


def build_hex_grid(radius: int = 2, spacing: float = 1.0) -> list[Cell]:
    cells: list[Cell] = []
    cell_id = 0
    for q in range(-radius, radius + 1):
        r_min = max(-radius, -q - radius)
        r_max = min(radius, -q + radius)
        for r in range(r_min, r_max + 1):
            x = spacing * (sqrt(3.0) * q + sqrt(3.0) / 2.0 * r)
            y = spacing * (1.5 * r)
            cells.append(Cell(cell_id=cell_id, q=q, r=r, x=x, y=y))
            cell_id += 1
    return cells


def assign_channels(cells: list[Cell], reuse_factor: int, channel_count: int) -> dict[int, int]:
    if reuse_factor <= 0:
        raise ValueError("reuse_factor must be positive")
    if channel_count <= 0:
        raise ValueError("channel_count must be positive")

    allocation: dict[int, int] = {}
    for cell in cells:
        reuse_group = (cell.q + 2 * cell.r) % reuse_factor
        allocation[cell.cell_id] = reuse_group % channel_count
    return allocation


def distance(a: Cell, b: Cell) -> float:
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def evaluate_allocation(
    cells: list[Cell],
    allocation: dict[int, int],
    tx_power: float = 1.0,
    noise_power: float = 0.01,
    path_loss_exponent: float = 3.5,
) -> AllocationResult:
    if not cells:
        raise ValueError("cells must not be empty")

    sinrs: list[float] = []
    total_interference = 0.0
    channels = set(allocation.values())

    for serving in cells:
        interference = 0.0
        for neighbor in cells:
            if neighbor.cell_id == serving.cell_id:
                continue
            if allocation[neighbor.cell_id] != allocation[serving.cell_id]:
                continue
            d = max(distance(serving, neighbor), 1e-6)
            interference += tx_power / (d ** path_loss_exponent)

        total_interference += interference
        signal = tx_power
        sinrs.append(signal / (noise_power + interference))

    spectral_efficiencies = [log2(1.0 + value) for value in sinrs]
    fairness_den = len(spectral_efficiencies) * sum(v * v for v in spectral_efficiencies)
    fairness = (sum(spectral_efficiencies) ** 2 / fairness_den) if fairness_den else 1.0

    return AllocationResult(
        reuse_factor=max(len(channels), 1),
        channel_count=len(channels),
        total_interference=total_interference,
        average_sinr=sum(sinrs) / len(sinrs),
        average_spectral_efficiency=sum(spectral_efficiencies) / len(spectral_efficiencies),
        jain_fairness=fairness,
    )


def sweep_reuse_factors(
    radius: int = 2,
    channel_count: int = 7,
    reuse_factors: tuple[int, ...] = (1, 3, 4, 7),
) -> list[AllocationResult]:
    cells = build_hex_grid(radius=radius)
    results: list[AllocationResult] = []
    for reuse in reuse_factors:
        allocation = assign_channels(cells, reuse_factor=reuse, channel_count=channel_count)
        result = evaluate_allocation(cells, allocation)
        results.append(
            AllocationResult(
                reuse_factor=reuse,
                channel_count=result.channel_count,
                total_interference=result.total_interference,
                average_sinr=result.average_sinr,
                average_spectral_efficiency=result.average_spectral_efficiency,
                jain_fairness=result.jain_fairness,
            )
        )
    return results


def main() -> None:
    for result in sweep_reuse_factors():
        print(
            f"reuse={result.reuse_factor:>2} "
            f"interference={result.total_interference:.4f} "
            f"avg_sinr={result.average_sinr:.3f} "
            f"avg_eff={result.average_spectral_efficiency:.3f} "
            f"fairness={result.jain_fairness:.3f}"
        )


if __name__ == "__main__":
    main()
