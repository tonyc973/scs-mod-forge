#!/usr/bin/env python3
"""Validate raw recordings against the sound input spec (docs/09-sound.md).

Checks: WAV PCM, 48 kHz, 24-bit, mono, peak <= -1 dBFS, file-name pattern.

Example:
    python check_wav.py sound/raw/2026-12-01/
"""
import argparse
import pathlib
import re
import sys

import numpy as np
import soundfile as sf

NAME = re.compile(r"^(int|exh|bay)_[a-z0-9]+_[a-z0-9]+(_[a-z0-9]+)*\.wav$")


def check(path: pathlib.Path):
    problems = []
    if not NAME.match(path.name):
        problems.append("name must look like <int|exh|bay>_<test>_<gear>_<note>.wav (lowercase)")
    try:
        info = sf.info(str(path))
    except Exception as e:  # noqa: BLE001
        return [f"unreadable: {e}"]
    if info.format != "WAV":
        problems.append(f"format {info.format}, expected WAV")
    if info.subtype != "PCM_24":
        problems.append(f"subtype {info.subtype}, expected PCM_24")
    if info.samplerate != 48000:
        problems.append(f"sample rate {info.samplerate}, expected 48000")
    if info.channels != 1:
        problems.append(f"{info.channels} channels, expected mono (one file per microphone)")
    data, _ = sf.read(str(path), dtype="float32", always_2d=True)
    peak = float(np.max(np.abs(data))) if data.size else 0.0
    peak_db = 20 * np.log10(peak) if peak > 0 else -np.inf
    if peak_db > -1.0:
        problems.append(f"peak {peak_db:.1f} dBFS, must be <= -1 dBFS (possible clipping)")
    return problems


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paths", nargs="+")
    a = p.parse_args()
    files = []
    for x in a.paths:
        q = pathlib.Path(x)
        files += sorted(q.rglob("*.wav")) if q.is_dir() else [q]
    if not files:
        sys.exit("no .wav files found")
    bad = 0
    for f in files:
        pr = check(f)
        status = "OK " if not pr else "BAD"
        bad += bool(pr)
        print(f"[{status}] {f}")
        for msg in pr:
            print(f"       - {msg}")
    print(f"\n{len(files) - bad}/{len(files)} files pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
