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
