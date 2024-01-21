""" Test heuristics """

import math

from pathfinding3d.core.heuristic import chebyshev, euclidean, manhattan, null, octile

EPS = 1e-6


def test_null():
    assert null(1, -2, 3) == 0.0


def test_manhattan():
    assert manhattan(1, -2, 3) == 2.0


def test_euclidean():
    assert math.isclose(euclidean(1, -2, 3), math.sqrt(14), rel_tol=EPS)


def test_chebyshev():
    assert chebyshev(1, -2, 3) == 3.0


def test_octile():
    assert math.isclose(octile(1, 1, 1), math.sqrt(3), rel_tol=EPS)


def test_octile2():
    dx, dy, dz = 1, 2, 3
    dmax, dmid, dmin = 3, 2, 1
    expected_result = dmax + ((2**0.5 - 1) * dmid) + ((3**0.5 - 2**0.5) * dmin)
    assert math.isclose(octile(dx, dy, dz), expected_result, rel_tol=EPS)
