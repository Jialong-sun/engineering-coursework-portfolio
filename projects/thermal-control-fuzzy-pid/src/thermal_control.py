"""TEC thermal-control simulation with fuzzy-style PID gain scheduling."""

from __future__ import annotations

from dataclasses import dataclass


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


@dataclass(frozen=True)
class ThermalPlant:
    ambient_c: float = 25.0
    thermal_mass_j_per_c: float = 260.0
    heat_loss_w_per_c: float = 1.15
    tec_w_per_amp: float = 18.0
    max_current_a: float = 4.0

    def step(self, temp_c: float, current_a: float, dt_s: float) -> float:
        current = clamp(current_a, -self.max_current_a, self.max_current_a)
        passive_w = self.heat_loss_w_per_c * (self.ambient_c - temp_c)
        tec_w = self.tec_w_per_amp * current
        return temp_c + (passive_w + tec_w) / self.thermal_mass_j_per_c * dt_s


@dataclass
class FuzzyPidController:
    kp: float = 0.55
    ki: float = 0.012
    kd: float = 0.18
    max_current_a: float = 4.0
    integral_limit: float = 80.0
    integral: float = 0.0
    previous_error: float = 0.0

    def gain_scale(self, error: float, derivative: float) -> tuple[float, float, float]:
        magnitude = abs(error)
        if magnitude > 8.0:
            return 1.45, 0.45, 1.10
        if magnitude > 3.0:
            return 1.10, 0.75, 1.00
        if abs(derivative) > 0.08:
            return 0.85, 0.90, 1.35
        return 0.72, 1.10, 0.90

    def update(self, setpoint_c: float, measured_c: float, dt_s: float) -> float:
        error = setpoint_c - measured_c
        derivative = (error - self.previous_error) / dt_s
        kp_scale, ki_scale, kd_scale = self.gain_scale(error, derivative)

        self.integral = clamp(
            self.integral + error * dt_s,
            -self.integral_limit,
            self.integral_limit,
        )

        command = (
            self.kp * kp_scale * error
            + self.ki * ki_scale * self.integral
            + self.kd * kd_scale * derivative
        )
        current = clamp(command, -self.max_current_a, self.max_current_a)

        if abs(command) > self.max_current_a:
            self.integral *= 0.96

        self.previous_error = error
        return current


def simulate(
    setpoint_c: float = 35.0,
    initial_c: float = 20.0,
    duration_s: float = 480.0,
    dt_s: float = 1.0,
    plant: ThermalPlant | None = None,
    controller: FuzzyPidController | None = None,
) -> list[dict[str, float]]:
    plant = plant or ThermalPlant()
    controller = controller or FuzzyPidController(max_current_a=plant.max_current_a)

    temp = initial_c
    records: list[dict[str, float]] = []
    steps = int(duration_s / dt_s)
    for index in range(steps + 1):
        time_s = index * dt_s
        current = controller.update(setpoint_c, temp, dt_s)
        records.append(
            {
                "time_s": time_s,
                "temp_c": temp,
                "current_a": current,
                "error_c": setpoint_c - temp,
            }
        )
        temp = plant.step(temp, current, dt_s)
    return records


def settling_time(records: list[dict[str, float]], setpoint_c: float, tolerance_c: float) -> float | None:
    for index, record in enumerate(records):
        remaining = records[index:]
        if all(abs(row["temp_c"] - setpoint_c) <= tolerance_c for row in remaining):
            return record["time_s"]
    return None


def ripple(records: list[dict[str, float]], window_s: float = 120.0) -> float:
    if not records:
        return 0.0
    end_time = records[-1]["time_s"]
    window = [row["temp_c"] for row in records if row["time_s"] >= end_time - window_s]
    return max(window) - min(window)


def main() -> None:
    records = simulate()
    settle = settling_time(records, setpoint_c=35.0, tolerance_c=0.05)
    print(f"final_temp_c={records[-1]['temp_c']:.3f}")
    print(f"settling_time_s={settle}")
    print(f"last_120s_ripple_c={ripple(records):.4f}")


if __name__ == "__main__":
    main()
