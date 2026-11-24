#!/usr/bin/env python3
"""Extract acceleration times from a time/speed CSV (e.g. exported from a telemetry tool).

Every pass counts, including a 60-100 segment inside a longer 0-100 run; run separate tests
for clean numbers. The CSV needs a time column (seconds) and a speed column (km/h). Column names are
configurable. For each --window A B the tool finds every pass from A to B km/h
while accelerating and reports the time (linear interpolation between samples).

Example:
    python perf_from_telemetry.py run.csv --window 0 100 --window 60 100
    python perf_from_telemetry.py run.csv --time-col t --speed-col speed --window 80 120
"""
import argparse
import csv
import sys


def load(path, tcol, vcol):
    t, v = [], []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                t.append(float(row[tcol]))
                v.append(float(row[vcol]))
            except (KeyError, ValueError):
                continue
    if len(t) < 2:
        sys.exit(f"No usable rows with columns {tcol!r}/{vcol!r} in {path}")
    return t, v


def crossing_time(t, v, i, target):
    """Interpolated time between sample i and i+1 where v crosses target upwards."""
    v0, v1 = v[i], v[i + 1]
    if v1 == v0:
        return t[i]
    return t[i] + (target - v0) * (t[i + 1] - t[i]) / (v1 - v0)


def windows(t, v, lo, hi):
    """Yield durations of each continuous accelerating pass from lo to hi km/h."""
    standing = lo <= 0.5  # 0-X runs start at the last stationary sample
    results = []
    start = None
    for i in range(len(v) - 1):
        if start is None:
            if standing and v[i] <= 0.5 < v[i + 1]:
                start = t[i]
            elif not standing and v[i] <= lo < v[i + 1]:
                start = crossing_time(t, v, i, lo)
        if start is not None:
            if v[i + 1] < v[i] - 2.0:  # clear deceleration -> abort this pass
                start = None
                continue
            if v[i] < hi <= v[i + 1]:
                results.append(crossing_time(t, v, i, hi) - start)
                start = None
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--time-col", default="time_s")
    p.add_argument("--speed-col", default="speed_kmh")
    p.add_argument("--window", nargs=2, type=float, action="append", metavar=("FROM", "TO"), required=True)
    a = p.parse_args()

    t, v = load(a.csv, a.time_col, a.speed_col)
    for lo, hi in a.window:
        res = windows(t, v, lo, hi)
        if not res:
            print(f"{lo:g}-{hi:g} km/h: no complete pass found")
            continue
        times = ", ".join(f"{x:.2f}s" for x in res)
        print(f"{lo:g}-{hi:g} km/h: {len(res)} pass(es): {times}  | mean {sum(res)/len(res):.2f}s")


if __name__ == "__main__":
    main()
