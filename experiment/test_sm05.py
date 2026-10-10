from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("dolfinx")
from sm05 import simulate

# Output of the original notebook SM05_bistable_bit.ipynb (results/bistable_bit_data_v2.csv):
# rows t_s, separation_mm, disp_um, 0.5 * fx_mN * 1e3; column 0 is the initial state
REF = np.loadtxt(Path(__file__).parent / "sm05_reference.csv", delimiter=",")


def test_first_half_second_matches_notebook():
    r = simulate(t_end_s=0.5)
    t, sep, disp, force = REF[:, 1:len(r["t_s"]) + 1]
    assert r["completed"]
    assert np.allclose(r["t_s"], t)
    assert np.allclose(r["separation_mm"], sep, rtol=1e-6)
    assert np.allclose(r["disp_um"], disp, rtol=1e-6, atol=1e-9)
    assert np.allclose(0.5 * r["fx_mN"] * 1e3, force, rtol=1e-6, atol=1e-12)
