from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from thermal_control import ThermalPlant, FuzzyPidController, ripple, settling_time, simulate


def test_heating_case_converges_within_project_window():
    plant = ThermalPlant()
    controller = FuzzyPidController(max_current_a=plant.max_current_a)
    records = simulate(plant=plant, controller=controller)
    settle = settling_time(records, setpoint_c=35.0, tolerance_c=0.08)

    assert settle is not None
    assert settle <= 420.0
    assert abs(records[-1]["temp_c"] - 35.0) < 0.04


def test_cooling_case_uses_negative_current():
    plant = ThermalPlant()
    records = simulate(setpoint_c=18.0, initial_c=32.0, plant=plant)

    assert min(row["current_a"] for row in records[:30]) < -1.0
    assert abs(records[-1]["temp_c"] - 18.0) < 0.08


def test_steady_state_ripple_is_small():
    records = simulate()
    assert ripple(records, window_s=120.0) < 0.12


if __name__ == "__main__":
    test_heating_case_converges_within_project_window()
    test_cooling_case_uses_negative_current()
    test_steady_state_ripple_is_small()
    print("thermal-control-fuzzy-pid checks passed")
