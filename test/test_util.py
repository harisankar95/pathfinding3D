import pytest

from pathfinding3d.core.grid import Grid
from pathfinding3d.core.node import GridNode
from pathfinding3d.core.util import (
    bresenham,
    expand_path,
    line_of_sight,
    raytrace,
    smoothen_path,
)


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


def test_expand_path():
    """
    test expand_path function
    """
    # Test with empty path
    assert not expand_path([])

    # Test with one point path
    assert not expand_path([[0, 0, 0]])

    # Test with two points path
    assert expand_path([[0, 0, 0], [1, 1, 1]]) == [[0, 0, 0], [1, 1, 1]]

    # Test with multiple points path
    assert expand_path([[0, 0, 0], [2, 2, 2], [4, 2, 2]]) == [
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2],
        [3, 2, 2],
        [4, 2, 2],
    ]


@pytest.fixture
def grid():
    # Create a 5x5x5 grid with all nodes walkable
    grid = Grid(5, 5, 5)
    for x in range(5):
        for y in range(5):
            for z in range(5):
                grid.nodes[x][y][z].walkable = True
    return grid


def test_line_of_sight_self(grid):
    """
    test line_of_sight function with self
    """
    # Test with self
    node = GridNode(0, 0, 0)
    assert line_of_sight(grid, node, node)


def test_line_of_sight_clear(grid):
    """
    test line_of_sight function with clear line of sight
    """
    # Test with clear line of sight
    node1 = GridNode(0, 0, 0)
    node2 = GridNode(4, 4, 4)
    assert line_of_sight(grid, node1, node2)


def test_line_of_sight_obstacle(grid):
    """
    test line_of_sight function with obstacle
    """
    # Test with obstacle
    node1 = GridNode(0, 0, 0)
    node2 = GridNode(4, 4, 4)
    grid.nodes[2][2][2].walkable = False
    assert not line_of_sight(grid, node1, node2)
