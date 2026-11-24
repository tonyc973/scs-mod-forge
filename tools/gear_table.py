#!/usr/bin/env python3
"""Speed / RPM table from gear ratios, final drive and tyre size.

Example:
    python gear_table.py --ratios 3.643 2.080 1.361 1.024 0.830 0.686 \
        --final 4.105 --tyre 215/50R17 --redline 6500 --speeds 100 130 160
"""
import argparse
import math
import re


def tyre_diameter_m(code: str) -> float:
    """Outer diameter in metres from a metric tyre code like 215/50R17."""
    m = re.fullmatch(r"\s*(\d{3})\s*/\s*(\d{2})\s*Z?R\s*(\d{2}(?:\.\d)?)\s*", code.upper())
    if not m:
        raise ValueError(f"Unrecognised tyre code: {code!r} (expected e.g. 215/50R17)")
    width_mm, aspect, rim_in = int(m.group(1)), int(m.group(2)), float(m.group(3))
    sidewall_mm = width_mm * aspect / 100.0
    return (rim_in * 25.4 + 2 * sidewall_mm) / 1000.0


def rpm_at(speed_kmh: float, ratio: float, final: float, diameter_m: float) -> float:
    wheel_rpm = (speed_kmh * 1000 / 60) / (math.pi * diameter_m)
    return wheel_rpm * ratio * final


def speed_at(rpm: float, ratio: float, final: float, diameter_m: float) -> float:
    wheel_rpm = rpm / (ratio * final)
    return wheel_rpm * math.pi * diameter_m * 60 / 1000


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ratios", type=float, nargs="+", required=True, help="forward gear ratios, 1st first")
    p.add_argument("--final", type=float, required=True, help="final drive ratio")
    p.add_argument("--tyre", required=True, help="tyre code, e.g. 215/50R17")
    p.add_argument("--redline", type=float, default=6500)
    p.add_argument("--speeds", type=float, nargs="*", default=[100, 130], help="speeds (km/h) to tabulate rpm for")
    a = p.parse_args()

    d = tyre_diameter_m(a.tyre)
    print(f"Tyre {a.tyre}: outer diameter {d*1000:.0f} mm, circumference {math.pi*d:.3f} m")
    print(f"Final drive {a.final}\n")

    header = f"{'gear':>4} {'ratio':>7} {'v@redline km/h':>15}" + "".join(f" {'rpm@'+str(int(s)):>9}" for s in a.speeds)
    print(header)
    print("-" * len(header))
    for i, r in enumerate(a.ratios, 1):
        vmax = speed_at(a.redline, r, a.final, d)
        cells = "".join(f" {rpm_at(s, r, a.final, d):9.0f}" for s in a.speeds)
        print(f"{i:>4} {r:7.3f} {vmax:15.1f}{cells}")


if __name__ == "__main__":
    main()
