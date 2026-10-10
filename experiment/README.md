# experiment/

SM05 bistable bit as a function, so it can run unattended (night sweeps → surrogate).

```python
from sm05 import simulate, MATERIALS

r = simulate(**MATERIALS[18])          # E_MPa, ms_MA_per_m of the 18 % dynamic range
r["separation_mm"], r["disp_um"]       # deflection vs magnet separation, one row per step
```

- `magnet.py`: potential of the block magnet (pure numpy, same formula as the notebook)
- `sm05.py`: `simulate(...)`, same physics, mesh, solver and time stepping as `SM05_bistable_bit.ipynb`;
  plots and VTX field output removed. Serial only
- `sm05_reference.csv`: output of the original notebook, used by the test
- Validated on the full ramp: same 275 steps as the notebook, max difference 2e-6 µm on 606 µm.
  Run time 37 min on one core (notebook 42 min on the same machine)
- Returns: `t_s`, `travel_mm`, `separation_mm`, `disp_um`, `fx_mN`, `completed`

## Environment
FEniCSx 0.8 (Docker as in the main README, or `conda env create -f environment.yml`).

## Tests
```
cd experiment && pytest -q
```
- `test_magnet.py`: on-axis field vs the textbook block-magnet formula (no FEniCSx needed)
- `test_sm05.py`: first 0.5 s of `simulate()` vs the notebook output (skipped without dolfinx)

## Open questions
- The notebook saves `0.5 * Fx * 1e3` as force: meaning of the 0.5 to confirm with Eric
- `BIT_EDGE = 0.5 + 2.016` turns magnet travel into separation: taken from the notebook as is
