from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "sim"))

from digital_models import Adc0809ReaderModel, edge_pulses, seven_segment_pattern


def test_edge_pulses_are_one_cycle():
    rising, falling = edge_pulses([0, 0, 1, 1, 0, 1, 0])
    assert rising == [0, 0, 1, 0, 0, 1, 0]
    assert falling == [0, 0, 0, 0, 1, 0, 1]


def test_seven_segment_known_digits():
    assert seven_segment_pattern(0) == "1000000"
    assert seven_segment_pattern(8) == "0000000"
    assert seven_segment_pattern(0xF) == "0001110"


def test_adc0809_model_handshake_to_done():
    adc = Adc0809ReaderModel(setup_cycles=2)
    trace = []
    trace.append(adc.tick(start=True, eoc=True, adc_data=0x00))
    trace.append(adc.tick(start=False, eoc=True, adc_data=0x00))
    trace.append(adc.tick(start=False, eoc=True, adc_data=0x00))
    trace.append(adc.tick(start=False, eoc=False, adc_data=0x00))
    trace.append(adc.tick(start=False, eoc=False, adc_data=0x00))
    trace.append(adc.tick(start=False, eoc=True, adc_data=0xA5))
    trace.append(adc.tick(start=False, eoc=True, adc_data=0xA5))
    trace.append(adc.tick(start=False, eoc=True, adc_data=0xA5))

    done_steps = [step for step in trace if step["done"] == 1]
    assert any(step["start_conv"] == 1 for step in trace)
    assert len(done_steps) == 1
    assert done_steps[0]["oe"] == 1
    assert done_steps[0]["sample"] == 0xA5


def test_rtl_module_files_are_present():
    expected_modules = {
        "clock_divider.v": "module clock_divider",
        "edge_detector.v": "module edge_detector",
        "seven_segment_scan.v": "module seven_segment_scan",
        "adc0809_reader.v": "module adc0809_reader",
    }
    rtl_dir = PROJECT_ROOT / "rtl"
    for filename, needle in expected_modules.items():
        text = (rtl_dir / filename).read_text(encoding="utf-8")
        assert needle in text
        assert "endmodule" in text


if __name__ == "__main__":
    test_edge_pulses_are_one_cycle()
    test_seven_segment_known_digits()
    test_adc0809_model_handshake_to_done()
    test_rtl_module_files_are_present()
    print("fpga-digital-interface-lab checks passed")
