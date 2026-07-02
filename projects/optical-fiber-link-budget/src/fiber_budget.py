import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class LinkBudget:
    tx_power_dbm: float
    length_km: float
    fiber_loss_db_per_km: float
    connectors: int
    connector_loss_db: float
    splices: int
    splice_loss_db: float
    receiver_sensitivity_dbm: float
    system_margin_db: float = 0.0

    @property
    def total_loss_db(self) -> float:
        return (
            self.length_km * self.fiber_loss_db_per_km
            + self.connectors * self.connector_loss_db
            + self.splices * self.splice_loss_db
            + self.system_margin_db
        )

    @property
    def received_power_dbm(self) -> float:
        return self.tx_power_dbm - self.total_loss_db

    @property
    def margin_db(self) -> float:
        return self.received_power_dbm - self.receiver_sensitivity_dbm

    @property
    def passes(self) -> bool:
        return self.margin_db >= 0


def fbg_wavelength_shift_nm(
    center_wavelength_nm: float = 1550.0,
    strain_microstrain: float = 0.0,
    temperature_delta_c: float = 0.0,
    strain_sensitivity_pm_per_microstrain: float = 1.2,
    temperature_sensitivity_pm_per_c: float = 10.0,
) -> float:
    strain_shift_pm = strain_microstrain * strain_sensitivity_pm_per_microstrain
    temperature_shift_pm = temperature_delta_c * temperature_sensitivity_pm_per_c
    return center_wavelength_nm + (strain_shift_pm + temperature_shift_pm) / 1000.0


def validate_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def build_budget(args: argparse.Namespace) -> LinkBudget:
    validate_non_negative("length_km", args.length_km)
    validate_non_negative("fiber_loss_db_km", args.fiber_loss_db_km)
    validate_non_negative("connectors", args.connectors)
    validate_non_negative("connector_loss_db", args.connector_loss_db)
    validate_non_negative("splices", args.splices)
    validate_non_negative("splice_loss_db", args.splice_loss_db)
    validate_non_negative("system_margin_db", args.system_margin_db)

    return LinkBudget(
        tx_power_dbm=args.tx_dbm,
        length_km=args.length_km,
        fiber_loss_db_per_km=args.fiber_loss_db_km,
        connectors=args.connectors,
        connector_loss_db=args.connector_loss_db,
        splices=args.splices,
        splice_loss_db=args.splice_loss_db,
        receiver_sensitivity_dbm=args.rx_sensitivity_dbm,
        system_margin_db=args.system_margin_db,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Optical fiber link-budget and FBG sensor calculator.")
    parser.add_argument("--tx-dbm", type=float, default=0.0)
    parser.add_argument("--length-km", type=float, default=25.0)
    parser.add_argument("--fiber-loss-db-km", type=float, default=0.22)
    parser.add_argument("--connectors", type=int, default=2)
    parser.add_argument("--connector-loss-db", type=float, default=0.5)
    parser.add_argument("--splices", type=int, default=4)
    parser.add_argument("--splice-loss-db", type=float, default=0.05)
    parser.add_argument("--rx-sensitivity-dbm", type=float, default=-24.0)
    parser.add_argument("--system-margin-db", type=float, default=1.0)
    parser.add_argument("--strain-microstrain", type=float, default=1000.0)
    parser.add_argument("--temperature-delta-c", type=float, default=13.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    budget = build_budget(args)
    shifted_wavelength = fbg_wavelength_shift_nm(
        strain_microstrain=args.strain_microstrain,
        temperature_delta_c=args.temperature_delta_c,
    )

    print(f"Received power: {budget.received_power_dbm:.2f} dBm")
    print(f"System margin: {budget.margin_db:.2f} dB")
    print(f"Link status: {'PASS' if budget.passes else 'FAIL'}")
    print(f"FBG shift: {shifted_wavelength - 1550.0:.3f} nm")


if __name__ == "__main__":
    main()
