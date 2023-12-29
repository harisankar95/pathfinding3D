from pathfinding3d.core.grid import Grid
from pathfinding3d.core.world import World
from pathfinding3d.finder.a_star import AStarFinder

PATH = [
    (2, 0, 0, 0),
    (2, 0, 1, 0),
    (2, 0, 2, 0),
    (2, 1, 2, 0),
    (2, 2, 2, 0),
    # move to grid 1
    (2, 2, 2, 1),
    (2, 1, 2, 1),
    (2, 0, 2, 1),
    (2, 0, 1, 1),
    (2, 0, 0, 1),
]


def test_connect():
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

    finder = AStarFinder()
    path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)
    assert [tuple(p) for p in path] == PATH
