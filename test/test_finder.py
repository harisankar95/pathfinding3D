import numpy as np
import pytest

from pathfinding3d.core.grid import Grid, GridNode
from pathfinding3d.finder.finder import Finder
from pathfinding3d.finder.msp import MinimumSpanningTree


class DummyFinder(Finder):
    def __init__(self):
        super().__init__()


def test_check_neighbors_raises_exception():
    finder = DummyFinder()
    start = GridNode(0, 0, 0)
    end = GridNode(1, 1, 1)
    grid = Grid(matrix=[[[1]]])
    open_list = []

    with pytest.raises(NotImplementedError):
        finder.check_neighbors(start, end, grid, open_list)


def test_msp():
    """
    Test that the minimum spanning tree finder returns all nodes.
    """
    matrix = np.array(np.ones((3, 3, 3)))
    grid = Grid(matrix=matrix)

    start = grid.node(0, 0, 0)

    finder = MinimumSpanningTree()
    assert finder.tree(grid, start).sort() == [node for row in grid.nodes for col in row for node in col].sort()
