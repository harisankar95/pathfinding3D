import pytest

from pathfinding3d.core.grid import Grid
from pathfinding3d.core.heap import SimpleHeap


def test_determine_node_retrieval_function():
    grid = Grid(width=10, height=10, depth=10)
    start = grid.node(0, 0, 0)
    heap = SimpleHeap(start, grid)

    assert callable(heap._determine_node_retrieval_function())

    with pytest.raises(ValueError):
        heap.grid = "UnsupportedType"
        heap._determine_node_retrieval_function()


def test_determine_node_function():
    grid = Grid(width=10, height=10, depth=10)
    start = grid.node(0, 0, 0)
    heap = SimpleHeap(start, grid)

    assert callable(heap._determine_node_function())

    with pytest.raises(ValueError):
        heap.grid = "UnsupportedType"
        heap._determine_node_function()


def test_push_node():
    grid = Grid(width=10, height=10, depth=10)
    start = grid.node(0, 0, 0)
    heap = SimpleHeap(start, grid)

    heap.push_node(grid.node(1, 1, 1))
    assert len(heap) == 2
    assert heap.number_pushed == 1


def test_remove_node():
    grid = Grid(width=10, height=10, depth=10)
    start = grid.node(0, 0, 0)
    heap = SimpleHeap(start, grid)

    heap.push_node(grid.node(1, 1, 1))
    heap.remove_node(grid.node(1, 1, 1), 0)
    assert len(heap) == 2
    assert (0.0, 1, 1, 1, 1) in heap.removed_node_tuples


def test_heap():
    grid = Grid(width=10, height=10, depth=10)
    start = grid.node(0, 0, 0)
    open_list = SimpleHeap(start, grid)

    # Test pop
    assert open_list.pop_node() == start
    assert len(open_list) == 0

    # Test push
    open_list.push_node(grid.node(1, 1, 1))
    open_list.push_node(grid.node(1, 1, 2))
    open_list.push_node(grid.node(1, 1, 3))

    # Test removal and pop
    assert len(open_list) == 3
    open_list.remove_node(grid.node(1, 1, 2), 0)
    assert len(open_list) == 3

    assert open_list.pop_node() == grid.node(1, 1, 1)
    assert open_list.pop_node() == grid.node(1, 1, 3)
    assert len(open_list) == 0
