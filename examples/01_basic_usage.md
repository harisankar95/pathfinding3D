# Basic usage

A simple usage example to find a path using the A* algorithm in a 3D environment.

1. Import the required libraries:

    ```python
    import numpy as np

    from pathfinding3d.core.diagonal_movement import DiagonalMovement
    from pathfinding3d.core.grid import Grid
    from pathfinding3d.finder.a_star import AStarFinder
    ```

2. Create a Map:
   - Define a 3D grid using a numpy array. Any value smaller or equal to 0 represents an obstacle. Any positive value represents the weight of a field that can be walked on. The bigger the value higher the cost to walk that field. In this example, all walkable fields have the same cost of 1. Feel free to create a more complex map or use some sensor data as input for it.

    ```python
    # Define the 3D grid as 'x, y, z'
    matrix = np.ones((3, 3, 3))
    matrix[1, 1, 1] = 0  # Setting an obstacle at the center
    ```

    Note: You can use different positive values to represent varying costs of traversing different fields.

3. Create the Grid:
   - Instantiate a Grid object from the map. This will create Node instances for every element of the map and also sets the size of the map.

    ```python
    grid = Grid(matrix=matrix)
    ```

4. Define Start and End Nodes:
    - Determine the start and end nodes on the grid. Coordinates start at 0. The nodes can be accessed by their coordinates. The first parameter is the x coordinate, the second the y coordinate and the third the z coordinate. So the top left corner is (0, 0, 0) and the bottom right corner is (2, 2, 2).

    ```python
    start = grid.node(0, 0, 0)
    end = grid.node(2, 2, 2)
    ```

5. Instantiate the Pathfinding Finder:
   - Create a new instance of `AStarFinder` and find the path. Here we allow diagonal movement which is not allowed by default. The `find_path` method returns the path and the number of iterations needed.

    ```python
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    ```

6. Output the Result:
    - The path is a list with all the waypoints as nodes. Convert it to a list of coordinate tuples to pretty print it. Note that the start and end points are part of the path.

    ```python
    # Path will be a list with all the waypoints as nodes
    # Convert it to a list of coordinate tuples
    path = [p.identifier for p in path]

    # Output the results
    print("operations:", runs, "path length:", len(path))
    print("path:", path)
    ```

Here is the whole example which you can copy-and-paste to play with it:

  ```python
  import numpy as np

  from pathfinding3d.core.diagonal_movement import DiagonalMovement
  from pathfinding3d.core.grid import Grid
  from pathfinding3d.finder.a_star import AStarFinder

  # Define the 3D grid
  matrix = np.ones((3, 3, 3))
  matrix[1, 1, 1] = 0
  grid = Grid(matrix=matrix)

  # Define start and end nodes
  start = grid.node(0, 0, 0)
  end = grid.node(2, 2, 2)

  # Instantiate the finder and find the path
  finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
  path, runs = finder.find_path(start, end, grid)

  # Path will be a list with all the waypoints as nodes
  # Convert it to a list of coordinate tuples
  path = [p.identifier for p in path]

  # Output the results
  print("operations:", runs, "path length:", len(path))
  print("path:", path)

```
