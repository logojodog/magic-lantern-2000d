T7 film OS optimizations are applied at build time by `.github/workflows/build-2000d.yml` after cloning upstream M-Film.

Changes:
- Fewer canisters drawn while the shelf is moving or quality is low
- Contact shadows skipped while moving / at quality 0
- Reflections dropped on side canisters under load
- Quality throttle more aggressive (avg>42 drops quality)
- FRAME_PERIOD 32 (was 28)
