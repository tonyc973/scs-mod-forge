# 09 · Sound

## 1. Legal sources only

| Source | OK in a published mod? |
|---|---|
| Your own recordings of your own vehicle | ✅ best fidelity |
| Purchased sound library with a licence that allows games/mods | ✅ keep the licence file |
| CC0 / CC-BY recordings | ✅ with attribution (CC-BY) |
| Audio ripped from YouTube, forums or other mods | ❌ reference listening only |

## 2. Recording your car (safety first)

- High rpm only on closed or empty roads, with a passenger operating the gear; follow traffic law.
- Nothing mounted near hot or moving parts. Engine-bay recordings only while stationary.

Suggested takes:
- cold and warm idle;
- steady rpm in neutral (1 000–6 000 in 500 rpm steps, briefly);
- full and part throttle ramps in 3rd;
- engine braking ramps;
- steady cruise in 4th, 5th and 6th;
- turbo spool/release;
- extras: shifts, indicator relay, doors, horn.

Log rpm with an OBD dongle and clap once at the start of each session for sync.

## 3. Input spec (validated by [`tools/check_wav.py`](../tools/check_wav.py))

- WAV PCM, **48 kHz, 24-bit, mono per microphone**, peaks ≤ −1 dBFS, no processing.
- File name: `<source>_<test>_<gear>_<note>.wav`, with source `int` / `exh` / `bay` (e.g. `exh_noload_n_3000rpm.wav`).
- Folder: `sound/raw/<session-date>/{int,exh,bay,obd}/`, plus a `session.json` with date, temperature, mic positions, recorder and clap offset.
- OBD CSV: `time_s, rpm[, speed_kmh, throttle_pct, load_pct]`, ≥ 5 Hz.

## 4. Pipeline

1. Sync audio ↔ OBD by the clap (cross-correlation).
2. Validate: the firing frequency of a 4-cylinder 4-stroke is **rpm / 30 Hz**. The spectrogram must follow the logged rpm.
3. Cut zero-crossing loops per rpm step, separately for on-load and off-load, interior and exterior. Normalize loudness consistently.
4. Build the FMOD project **from the SCS template for your game version**, using the documented engine events (`engine`, `exhaust`, `turbo`, `start_bad`) and parameters (`engine/rpm`, `engine/load`…). Check the SCS example project for the real units of `engine/rpm`.
5. Build bank → export GUIDs → `.guids`; `.soundref` files; `sounds[]` entries in the engine accessory, following vanilla.
6. Remove truck-only sounds (air brakes, compressor, retarder) where possible; calibrate cabin loudness against a vanilla truck.
7. Pack `/sound` with **store** compression.
8. Verify: in-game recordings of the same manoeuvres, spectrograms side by side with the real ones.
