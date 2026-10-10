import numpy as np

from magnet import potential


def on_axis_B(d, Br, L=25.4, W=6.35, T=6.35):
    """Textbook on-axis field of a block magnet at distance d from its pole face."""
    a, b = W / 2, L / 2
    f = lambda z: np.arctan(a * b / (z * np.sqrt(a * a + b * b + z * z)))
    return Br / np.pi * (f(d) - f(d + T))


def test_on_axis_field_matches_textbook():
    Br, cx, h = 1480.0, 20.0, 1e-5
    for d in (0.5, 2.0, 10.0):
        x = cx - 6.35 / 2 - d                        # on the axis, in front of the -x face
        Bx = -(potential(x + h, 0, cx, 0, Br) - potential(x - h, 0, cx, 0, Br)) / (2 * h)
        assert np.isclose(Bx, on_axis_B(d, Br), rtol=1e-6)
