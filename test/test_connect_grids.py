import pytest

from pathfinding3d.core.grid import Grid
from pathfinding3d.core.util import expand_path
from pathfinding3d.core.world import World
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.theta_star import ThetaStarFinder

PATH = [
    (2, 0, 0, 0),
    (2, 1, 0, 0),
    (2, 2, 0, 0),
    (2, 2, 1, 0),
    (2, 2, 2, 0),
    # move to grid 1
    (2, 2, 2, 1),
    (2, 1, 2, 1),
    (2, 0, 2, 1),
    (2, 0, 1, 1),
    (2, 0, 0, 1),
]

PATH_DIAGONAL = [
    (2, 0, 0, 0),
    (2, 1, 0, 0),
    (2, 1, 1, 0),
    (2, 2, 2, 0),
    # move to grid 1
    (2, 2, 2, 1),
    (2, 1, 2, 1),
    (2, 1, 1, 1),
    (2, 0, 0, 1),
]


@pytest.fixture
def gen_world():
    world0 = [
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    ]
    world1 = [
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
    ]
    # create Grid instances for both level
    grid0 = Grid(matrix=world0, grid_id=0)
    grid1 = Grid(matrix=world1, grid_id=1)

    grid0.node(2, 2, 2).connect(grid1.node(2, 2, 2))
    grid1.node(2, 2, 2).connect(grid0.node(2, 2, 2))

    # create world with both grids
    world = World({0: grid0, 1: grid1})
    return world, grid0, grid1


def test_connect(gen_world):
    world, grid0, grid1 = gen_world
    # clean up the grids
    world.cleanup()

    finder = AStarFinder()
    path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)
    assert [tuple(p) for p in path] == PATH


def test_connect_theta_star(gen_world):
    world, grid0, grid1 = gen_world
    # clean up the grids
    world.cleanup()

    finder = ThetaStarFinder()
    path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)
    path = [p.identifier for p in path]
    # path through grid 0 and grid 1
    paths = {0: [], 1: []}
    for p in path:
        paths[p[3]].append(p[:3])

    # expand the paths and combine them with the grid ids
    path = [(*p, grid_id) for grid_id, path_list in paths.items() for p in expand_path(path_list)]
    assert path == PATH_DIAGONAL
