# Pathfinding3D

[![MIT License](https://img.shields.io/github/license/harisankar95/pathfinding3d)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pathfinding3d)](https://pypi.org/project/pathfinding3d/)
[![Pipeline](https://github.com/harisankar95/pathfinding3D/actions/workflows/test-main.yml/badge.svg?branch=main)](https://github.com/harisankar95/pathfinding3D/actions/workflows/test-main.yml)
[![codecov](https://codecov.io/gh/harisankar95/pathfinding3D/branch/main/graph/badge.svg?token=ZQZQZQZQZQ)](https://codecov.io/gh/harisankar95/pathfinding3D)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Pathfinding algorithms for python3 froked from [python-pathfinding](https://github.com/brean/python-pathfinding) by [@brean](https://github.com/brean).

Pathfinding3D is a comprehensive library designed for 3D pathfinding applications.

Currently there are 7 path-finders bundled in this library, namely:

- A\*: Versatile and most widely used algorithm.
- Dijkstra: A\* without heuristic.
- Best-First
- Bi-directional A\*: Efficient for large graphs with a known goal.
- Breadth First Search (BFS)
- Iterative Deeping A\* (IDA\*): Memory efficient algorithm for large graphs.
- Minimum Spanning Tree (MSP)
- Theta\*: Almost A\* with path smoothing.

Dijkstra, A\* and Bi-directional A\* take the weight of the fields on the map into account.
Theta\* is a variant of A\* but with any angle of movement allowed.

## Installation

### Requirements

- python >= 3.8
- numpy

To install Pathfinding3D, use pip:

```bash
pip install pathfinding3d
```

For more details, see [pathfinding3d on pypi](https://pypi.org/project/pathfinding3d/)

## Usage examples

For a quick start, here's a basic example:
  
  ```python
  import numpy as np

  from pathfinding3d.core.diagonal_movement import DiagonalMovement
  from pathfinding3d.core.grid import Grid
  from pathfinding3d.finder.a_star import AStarFinder

  # Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
  matrix = np.ones((10, 10, 10), dtype=np.int8)
  # mark the center of the grid as an obstacle
  matrix[5, 5, 5] = 0

  # Create a grid object from the numpy array
  grid = Grid(matrix=matrix)

  # Mark the start and end points
  start = grid.node(0, 0, 0)
  end = grid.node(9, 9, 9)

  # Create an instance of the A* finder with diagonal movement allowed
  finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
  path, runs = finder.find_path(start, end, grid)

  # Path will be a list with all the waypoints as nodes
  # Convert it to a list of coordinate tuples
  path = [p.identifier for p in path]

  print("operations:", runs, "path length:", len(path))
  print("path:", path)
  ```

For usage examples with detailed descriptions take a look at the [examples](examples/) folder.

## Rerun the Algorithm

When rerunning the algorithm, remember to clean the grid first using `Grid.cleanup`. This will reset the grid to its original state.

  ```python
  grid.cleanup()
  ```

Please note that this operation can be time-consuming but is usally faster than creating a new grid object.

## Implementation details

All pathfinding algorithms in this library inherit from the `Finder` class. This class provides common functionality that can be overridden by specific pathfinding algorithm implementations.

General Process:

1. You call `find_path` on one of your finder implementations.
2. `init_find` instantiates the `open_list` and resets all values and counters. The `open_list` is a priority queue that keeps track of nodes to be explored.
3. The main loop starts on the `open_list` which contains all nodes to be processed next (e.g. all current neighbors that are walkable). You need to implement `check_neighbors`  in your finder implementation to fill this list.
4. For example in A\* implementation (`AStarFinder`), `check_neighbors`  pops the node with the minimum 'f' value from the open list and marks it as closed. It then either returns the path (if the end node is reached) or continues processing neighbors.
5. If the end node is not reached, `check_neighbors` calls `find_neighbors` to get all adjacent walkable nodes. For most algorithms, this calls `grid.neighbors`.
6. If none of the neighbors are walkable, the algorithm terminates. Otherwise, `check_neighbors` calls `process_node` on each neighbor. It calculates the cost `f` for each neighbor node. This involves computing `g` (the cost from the start node to the current node) and `h` (the estimated cost from the current node to the end node, calculated by `apply_heuristic`).
7. Finally `process_node` updates the open list so `find_path` with new or updated nodes. This allows `find_path` to continue the process with the next node in the subsequent iteration.

flow:

```pseudo
  find_path
    init_find  # (re)set global values and open list
    while open_list not empty:
      check_neighbors  # for the node with min 'f' value in open list
        pop_node  # node with min 'f' value
        find_neighbors  # get neighbors
        process_node  # calculate new cost for each neighbor
```

## Testing

Run the tests locally using pytest. For detailed instructions, see the `test` folder:

```bash
pytest test
```

## Contributing

We welcome contributions of all sizes and levels! For bug reports and feature requests, please use the [issue tracker](https://github.com/harisankar95/pathfinding3D/issues) to submit bug reports and feature requests. Please Follow the guidelines in [CONTRIBUTING.md](/CONTRIBUTING.md) for submitting merge requests.

## License

Pathfinding3D is distributed under the [MIT license](https://opensource.org/licenses/MIT).

## Authors / Contributers

Find a list of contributors [here](https://github.com/harisankar95/pathfinding3D/graphs/contributors).
