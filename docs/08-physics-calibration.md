# 08 · Physics calibration

Goal: the car must **feel** right, and "feel" means in-gear acceleration, not the brochure's 0–100.

## 1. Collect targets (measured, not claimed)

Priority:
1. **Your own car**: rpm at a known speed in top gear, tyre size from the sidewall, GPS-measured in-gear runs *done safely and legally*.
2. **Independent road tests with measurements** (e.g. ADAC Autotest PDFs list mass, rpm at 130 km/h, 60–100 km/h in several gears).
3. Manufacturer data (power, torque band, 0–100, top speed, gear ratios).

### Worked example: Civic Sedan 1.5 VTEC Turbo 6MT (EU)
ADAC's test of the Civic Limousine 1.5 Turbo Elegance (manual, 215/50 R17) reports:

| Test | Measured |
|---|---|
| 60–100 km/h, 4th / 5th / 6th gear | 6.0 s / 8.2 s / 11.2 s |
| 60–100 km/h overtaking (2nd + 3rd) | 4.2 s |
| Measured kerb mass | 1 290 kg |
| Engine speed at 130 km/h | ~3 100 rpm |

Source: [ADAC Autotest PDF](https://assets.adac.de/image/upload/Autodatenbank/Autotest/AT5835_Honda_Civic_Limousine_1_5_Turbo_Elegance/Honda_Civic_Limousine_1_5_Turbo_Elegance.pdf). Published engine data: 134 kW at 5 500 rpm, 240 Nm from 1 900 to 5 000 rpm (manual).

Gear ratios published for the 10th-gen 1.5T 6MT (US spec, confirm for your market): 3.643 / 2.080 / 1.361 / 1.024 / 0.830 / 0.686, final drive 4.105.

## 2. Check the drivetrain math first

```bash
python tools/gear_table.py --ratios 3.643 2.080 1.361 1.024 0.830 0.686 \
    --final 4.105 --tyre 215/50R17 --redline 6500 --speeds 100 130 160
```

If the computed rpm at 130 km/h in 6th (≈3 000) disagrees with the measured value (≈3 100), the final drive, the tyre or the tachometer differs. **Ask the owner** to read rpm at 100 and 130 km/h on the real car and fix the final drive to match. Speed-to-rpm must be right before you touch torque.

## 3. Torque curve

Start from the published shape, normalized to peak:

| rpm | fraction of peak |
|---|---|
| 1 000 | ~0.55 |
| 1 500 | ~0.80 |
| 1 900 – 5 000 | 1.00 |
| 5 500 | ~0.97 (matches peak power) |
| 6 000 | ~0.85 |
| 6 500 | ~0.72 |

Refine with a trustworthy stock dyno chart if you find one.

## 4. Calibrate against measured times

1. List which parameters are **per-vehicle** in your game version (engine torque and curve, rpm limits, ratios, final drive, wheel radius, anything mass-related) and which are global.
2. Run each target test in game **three times** on a flat, straight road without traffic, logging time and speed (telemetry → CSV).
3. Extract times:
   ```bash
   python tools/perf_from_telemetry.py run.csv --window 60 100 --window 0 100
   ```
4. Adjust per-vehicle parameters until **every** test is within **±5 %**. In-gear tests have priority: they define "pulls like the real one".
5. If targets conflict (e.g. global aero limits top speed), document the trade-off.

## 5. Deliverable
A table *real vs game* per test, plus speed–time plots for the in-gear runs overlaid on the targets.
