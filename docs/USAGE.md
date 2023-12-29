# Examples

For usage examples with detailed descriptions take a look at the [examples](https://github.com/harisankar95/pathfinding3D/tree/main/examples/) folder, also take a look at the [test/](https://github.com/harisankar95/pathfinding3D/tree/main/test/) folder for more examples.

## Basic usage

A simple usage example to find a path using A*.

1. import the required libraries:

    ```python
    import numpy as np

    from pathfinding3d.core.diagonal_movement import DiagonalMovement
    from pathfinding3d.core.grid import Grid
    from pathfinding3d.core.node import GridNode
    from pathfinding3d.finder.a_star import AStarFinder
    ```

1. Create a map using a 2D-list. Any value smaller or equal to 0 describes an obstacle. Any number bigger than 0 describes the weight of a field that can be walked on. The bigger the number the higher the cost to walk that field. We ignore the weight for now, all fields have the same cost of 1. Feel free to create a more complex map or use some sensor data as input for it.

    ```python
    # is of style 'x, y, z'
    matrix = np.ones((3, 3, 3))
    matrix[1, 1, 1] = 0
    ```

  Note: you can use negative values to describe different types of obstacles. It does not make a difference for the path finding algorithm but it might be useful for your later map evaluation.

1. we create a new grid from this map representation. This will create Node instances for every element of our map. It will also set the size of the map. We assume that your map is a square, so the size width is defined by the length of the outer list, the height by the length of the inner lists, and the depth by the length of the innermost lists.

    ```python
    grid = Grid(matrix=matrix)
    ```

1. we get the start and end node from the grid. We assume that the start is at the top left corner and the end at the bottom right corner. You can access the nodes by their coordinates. The first parameter is the x coordinate, the second the y coordinate and the third the z coordinate. The coordinates start at 0. So the top left corner is (0, 0, 0) and the bottom right corner is (2, 2, 2).

    ```python
    start = grid.node(0, 0, 0)
    end = grid.node(2, 2, 2)
    ```

1. create a new instance of our finder and let it do its work. We allow diagonal movement. The `find_path` function does not only return you the path from the start to the end point it also returns the number of times the algorithm needed to be called until a way was found.

    ```python
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    ```

1. thats it. We found a way. Now we can print the result (or do something else with it). Note that the start and end points are part of the path.

    ```python
    print('operations:', runs, 'path length:', len(path))
    print('path:', path)
    ```

Here is the whole example if you just want to copy-and-paste the code and play with it:

```python
  import numpy as np

  from pathfinding3d.core.diagonal_movement import DiagonalMovement
  from pathfinding3d.core.grid import Grid
  from pathfinding3d.core.node import GridNode
  from pathfinding3d.finder.a_star import AStarFinder


  matrix = np.ones((3, 3, 3))
  matrix[1, 1, 1] = 0
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
      if isinstance(node, GridNode):
        path.append([node.x, node.y, node.z])
      elif isinstance(node, tuple):
        path.append([node[0], node[1], node[2]])
  
  print('operations:', runs, 'path length:', len(path))
  print('path:', path)
```
