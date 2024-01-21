""" Test Grid class. """

import numpy as np
import pytest

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


DIRECTIONS = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 2, 0),
    (1, 0, 0),
    (1, 1, 0),
    (1, 2, 0),
    (2, 0, 0),
    (2, 1, 0),
    (2, 2, 0),
    (0, 0, 1),
    (0, 1, 1),
    (0, 2, 1),
    (1, 0, 1),
    (1, 2, 1),
    (2, 0, 1),
    (2, 1, 1),
    (2, 2, 1),
    (0, 0, 2),
    (0, 1, 2),
    (0, 2, 2),
    (1, 0, 2),
    (1, 1, 2),
    (1, 2, 2),
    (2, 0, 2),
    (2, 1, 2),
    (2, 2, 2),
]


@pytest.fixture
def gen_grid():
    grid = Grid(width=3, height=3, depth=3)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                grid.nodes[x][y][z].walkable = True
    node = grid.node(1, 1, 1)
    return grid, node


def test_diagonal_movement_always(gen_grid):
    test_grid, node = gen_grid
    neighbors = test_grid.neighbors(node, DiagonalMovement.always)
    assert len(neighbors) == 26  # All 26 possible neighbors


def test_diagonal_movement_never(gen_grid):
    test_grid, node = gen_grid
    neighbors = test_grid.neighbors(node, DiagonalMovement.never)
    assert len(neighbors) == 6  # Only 6 neighbors (no diagonals)
    # only the following nodes are considered neighbors:
    expected_neighbors = [
        (0, 1, 1),
        (1, 0, 1),
        (1, 2, 1),
        (2, 1, 1),
        (1, 1, 0),
        (1, 1, 2),
    ]
    actual_neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    # assert all neighbors are in the expected list
    for neighbor in actual_neighbors:
        assert neighbor in expected_neighbors


# current plane : cs (z = 1)
# upper plane : us (z = 2)
# lower plane : ls (z = 0)
def test_diagonal_movement_if_at_most_one_obstacle_cs(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][0][1].walkable = False  # Create an obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.if_at_most_one_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 25
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 0, 1))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors

    test_grid.nodes[0][1][1].walkable = False  # Create another obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.if_at_most_one_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 21
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors.remove((0, 1, 1))
    expected_neighbors.remove((0, 0, 1))
    expected_neighbors.remove((0, 0, 0))
    expected_neighbors.remove((0, 0, 2))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_if_at_most_one_obstacle_us(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][1][2].walkable = False  # Create an obstacle
    test_grid.nodes[1][2][1].walkable = False  # Create another obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.if_at_most_one_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 21
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 1, 2))
    expected_neighbors.remove((1, 2, 1))
    expected_neighbors.remove((1, 2, 2))
    expected_neighbors.remove((2, 2, 2))
    expected_neighbors.remove((0, 2, 2))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_if_at_most_one_obstacle_ls(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][1][0].walkable = False  # Create an obstacle
    test_grid.nodes[1][0][1].walkable = False  # Create another obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.if_at_most_one_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 21
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 1, 0))
    expected_neighbors.remove((1, 0, 1))
    expected_neighbors.remove((1, 0, 0))
    expected_neighbors.remove((2, 0, 0))
    expected_neighbors.remove((0, 0, 0))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_only_when_no_obstacle_cs(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][0][1].walkable = False  # Create an obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.only_when_no_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 17
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 0, 1))
    expected_neighbors.remove((0, 0, 1))
    expected_neighbors.remove((2, 0, 1))
    expected_neighbors.remove((1, 0, 0))
    expected_neighbors.remove((0, 0, 0))
    expected_neighbors.remove((2, 0, 0))
    expected_neighbors.remove((1, 0, 2))
    expected_neighbors.remove((0, 0, 2))
    expected_neighbors.remove((2, 0, 2))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_only_when_no_obstacle_cd(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[0][0][1].walkable = False  # Create an obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.only_when_no_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 23
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((0, 0, 1))
    expected_neighbors.remove((0, 0, 0))
    expected_neighbors.remove((0, 0, 2))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_only_when_no_obstacle_us(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][2][2].walkable = False  # Create an obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.only_when_no_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 23
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 2, 2))
    expected_neighbors.remove((0, 2, 2))
    expected_neighbors.remove((2, 2, 2))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors


def test_diagonal_movement_only_when_no_obstacle_ud(gen_grid):
    test_grid, node = gen_grid
    test_grid.nodes[1][1][0].walkable = False  # Create an obstacle
    neighbors = test_grid.neighbors(node, DiagonalMovement.only_when_no_obstacle)
    neighbors = [(neighbor.x, neighbor.y, neighbor.z) for neighbor in neighbors]
    expected_neighbors_count = 17
    assert len(neighbors) == expected_neighbors_count
    expected_neighbors = DIRECTIONS.copy()
    expected_neighbors.remove((1, 1, 0))
    expected_neighbors.remove((0, 1, 0))
    expected_neighbors.remove((2, 1, 0))
    expected_neighbors.remove((1, 0, 0))
    expected_neighbors.remove((0, 0, 0))
    expected_neighbors.remove((2, 0, 0))
    expected_neighbors.remove((1, 2, 0))
    expected_neighbors.remove((0, 2, 0))
    expected_neighbors.remove((2, 2, 0))
    # assert all neighbors are in the expected list
    for neighbor in neighbors:
        assert neighbor in expected_neighbors
