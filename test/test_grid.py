""" Test Grid class. """

import numpy as np

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.core.node import GridNode
from pathfinding3d.finder.a_star import AStarFinder

SIMPLE_MATRIX = np.ones((3, 3, 3))
SIMPLE_MATRIX[1, 1, 1] = 0


def test_numpy():
    """
    test grid from numpy array
    """
    matrix = np.array(SIMPLE_MATRIX)
    grid = Grid(matrix=matrix)

    start = grid.node(0, 0, 0)
    end = grid.node(2, 2, 2)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path_, runs = finder.find_path(start, end, grid)

    assert isinstance(path_, list)
    assert len(path_) > 0
    assert isinstance(runs, int)

    path = []
    for node in path_:
        assert isinstance(node, GridNode)
        path.append([node.x, node.y, node.z])

    assert path == [[0, 0, 0], [1, 1, 0], [2, 2, 1], [2, 2, 2]]
