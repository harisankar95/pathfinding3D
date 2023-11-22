from pathfinding3d.core.grid import Grid
from pathfinding3d.core.util import bresenham, raytrace, smoothen_path


def test_bresenham():
    """
    test bresenham path interpolation
    """
    assert bresenham([0, 0, 0], [2, 5, 1]) == [
        [0, 0, 0],
        [0, 1, 0],
        [1, 2, 0],
        [1, 3, 1],
        [2, 4, 1],
        [2, 5, 1],
    ]
    assert bresenham([0, 1, 4], [0, 4, 1]) == [
        [0, 1, 4],
        [0, 2, 3],
        [0, 3, 2],
        [0, 4, 1],
    ]


def test_raytrace():
    """
    test raytrace path interpolation
    """
    assert raytrace([0, 0, 0], [2, 5, 1]) == [
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [1, 2, 0],
        [1, 3, 0],
        [1, 3, 1],
        [1, 4, 1],
        [2, 4, 1],
        [2, 5, 1],
    ]
    assert raytrace([0, 1, 4], [0, 4, 1]) == [
        [0, 1, 4],
        [0, 2, 4],
        [0, 2, 3],
        [0, 3, 3],
        [0, 3, 2],
        [0, 4, 2],
        [0, 4, 1],
    ]


def test_smoothen_path():
    matrix = [[[1 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    grid = Grid(matrix=matrix)
    path = [
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 1, 0],
        [2, 2, 0],
        [3, 2, 0],
        [3, 3, 1],
        [3, 3, 2],
        [4, 4, 2],
    ]
    smooth_path = [
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 1, 0],
        [2, 2, 0],
        [3, 2, 0],
        [3, 3, 1],
        [4, 4, 2],
    ]
    assert smoothen_path(grid, path) == smooth_path
