import math
from typing import Union

from .util import SQRT2_MINUS_1, SQRT3_MINUS_SQRT2


def null(dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> float:
    """
    Special heuristic for Dijkstra
    return 0, so node.h will always be calculated as 0,
    distance cost (node.f) is calculated only from
    start to current point (node.g)

    Parameters
    ----------
    dx : Union[int, float]
        x distance
    dy : Union[int, float]
        y distance
    dz : Union[int, float]
        z distance

    Returns
    -------
    float
        0.0
    """
    return 0.0


def manhattan(dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> float:
    """Manhattan heuristics

    Parameters
    ----------
    dx : Union[int, float]
        x distance
    dy : Union[int, float]
        y distance
    dz : Union[int, float]
        z distance

    Returns
    -------
    float
        manhattan distance
    """
    return dx + dy + dz


def euclidean(dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> float:
    """Euclidean distance heuristics

    Parameters
    ----------
    dx : Union[int, float]
        x distance
    dy : Union[int, float]
        y distance
    dz : Union[int, float]
        z distance

    Returns
    -------
    float
        euclidean distance
    """
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def chebyshev(dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> float:
    """Chebyshev distance.

    Parameters
    ----------
    dx : Union[int, float]
        x distance
    dy : Union[int, float]
        y distance
    dz : Union[int, float]
        z distance

    Returns
    -------
    float
        chebyshev distance
    """
    return max(dx, dy, dz)


def octile(dx: Union[int, float], dy: Union[int, float], dz: Union[int, float]) -> float:
    """Octile distance.

    Parameters
    ----------
    dx : Union[int, float]
        x distance
    dy : Union[int, float]
        y distance
    dz : Union[int, float]
        z distance

    Returns
    -------
    float
        octile distance
    """
    dmax = max(dx, dy, dz)
    dmin = min(dx, dy, dz)
    dmid = dx + dy + dz - dmax - dmin

    return dmax + SQRT2_MINUS_1 * dmid + SQRT3_MINUS_SQRT2 * dmin
