"""Magnetic scalar potential of a uniformly magnetized rectangular magnet (pure numpy)."""
import numpy as np


def potential(x, y, center_x, center_y, M, L=25.4, W=6.35, T=6.35):
    """phi at (x, y) in the magnet mid-plane z = 0.

    Magnetization M along +x. T along x, W along y, L along z (out of plane).
    Defaults: K&J BX042 (1 x 1/4 x 1/4 in). Units: mm, M in kA/mm.
    Same expression as phi_rect_prism_Mx_denhoj in SM05_bistable_bit.ipynb.
    """
    xp = x - center_x
    yp = y - center_y
    a, b, c = T / 2, W / 2, L / 2

    def F(i, j, k):
        r = np.sqrt(i * i + j * j + k * k)
        return -i * np.arctan2(j * k, i * r) + j * np.log(k + r) + k * np.log(j + r)

    def corner_sum(i):
        return F(i, yp - b, -c) - F(i, yp - b, c) - F(i, yp + b, -c) + F(i, yp + b, c)

    return M / (4 * np.pi) * (corner_sum(xp - a) - corner_sum(xp + a))
