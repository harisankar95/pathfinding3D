# Examples

For usage examples with detailed descriptions take a look at the [examples](https://github.com/harisankar95/pathfinding3D/tree/main/examples/) folder.

## Basic usage

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

## Steps/Portals/Bridges

With *pathfinding3d*, you can seamlessly connect multiple grids. This feature is invaluable for simulating multi-story structures connected by staircases, bridges between different buildings, or even magical portals linking disparate locations.

### Toy Example: Connecting Two Building Storeys with a Bridge

Let's consider an example where we want to connect the second storey of two adjacent buildings with a bridge.

1. Define the Grids for Each Building:

   - Create two 3D grid arrays representing each building ('world0' and 'world1').

    ```python
    from pathfinding3d.core.grid import Grid
    from pathfinding3d.core.world import World
    from pathfinding3d.finder.a_star import AStarFinder

    world0 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], 
              [[1, 1, 1], [1, 0, 1], [1, 1, 1]], 
              [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
    world1 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], 
              [[1, 1, 1], [1, 0, 1], [1, 1, 1]], 
              [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
    # create Grid instances for both worlds
    grid0 = Grid(matrix=world0, grid_id=0)
    grid1 = Grid(matrix=world1, grid_id=1)
    ```

2. Connect Nodes Between Grids:
   - Establish a two-way connection between nodes in different grids to simulate a bridge.

    ```python
    # connect the two worlds
    grid0.node(2, 2, 2).connect(grid1.node(2, 2, 2))
    grid1.node(2, 2, 2).connect(grid0.node(2, 2, 2))
    ```

    Note: Establish connections in both directions for bi-directional travel. For unidirectional connections, define only one link.

3. Using the `World` to Manage Multiple Grids:
   - Create a `World` object to manage both grids, allowing `find_neighbors` to access them during pathfinding.

    ```python
    # create a world instance
    world = World({0: grid0, 1: grid1})
    ```

4. Pathfinding Across Connected Grids:
   - Utilize `AStarFinder` to find a path from a start node in the first grid to an end node in the second grid. This time we need to pass the `world` object to the `find_path` method.

   ```python
    # create a finder instance
    finder = AStarFinder()
    # find the path
    path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)
   ```

    This will output a path traversing from one building to another, demonstrating the unique capability of connecting different 3D spaces.

5. Visualizing the Path:
    - The path is a list of `Node` objects. We can convert the path to a list of tuples (x, y, z, grid_id) and separate the path into two lists of tuples (x, y, z) for each grid.

   ```python
    # convert the path to a list of tuples (x, y, z, grid_id)
    path = [p.identifier for p in path]
    # separate the path into two lists of tuples (x, y, z)
    path0 = [p[:3] for p in path if p[3] == 0]
    path1 = [p[:3] for p in path if p[3] == 1]
    # print the paths
    print("path through world 0:", path0)
    print("path through world 1:", path1)
   ```

6. The output should look like this:

    ```python
    path through world 0: [(2, 0, 0), (2, 1, 0), (2, 2, 0), (2, 2, 1), (2, 2, 2)]
    path through world 1: [(2, 2, 2), (2, 1, 2), (2, 0, 2), (2, 0, 1), (2, 0, 0)]
    ```

    The path through world 0 starts at (2, 0, 0) and ends at (2, 2, 2). The path through world 1 starts at (2, 2, 2) and ends at (2, 0, 0). The two paths are connected by the bridge at (2, 2, 2).

7. Putting it all together:

    ```python
    from pathfinding3d.core.grid import Grid
    from pathfinding3d.core.world import World
    from pathfinding3d.finder.a_star import AStarFinder

    world0 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
    world1 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
    # create Grid instances for both worlds
    grid0 = Grid(matrix=world0, grid_id=0)
    grid1 = Grid(matrix=world1, grid_id=1)

    # connect the two worlds
    grid0.node(2, 2, 2).connect(grid1.node(2, 2, 2))
    grid1.node(2, 2, 2).connect(grid0.node(2, 2, 2))

    # create a world instance
    world = World({0: grid0, 1: grid1})

    # create a finder instance
    finder = AStarFinder()
    # find the path
    path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)

    # convert the path to a list of tuples (x, y, z, grid_id)
    path = [p.identifier for p in path]
    # separate the path into two lists of tuples (x, y, z)
    path0 = [p[:3] for p in path if p[3] == 0]
    path1 = [p[:3] for p in path if p[3] == 1]
    # print the paths
    print("path through world 0:", path0)
    print("path through world 1:", path1)
    ```

## Visualizing the Path

Sometimes it is helpful to visualize the path to better understand the algorithm. Here is a simple example using the `open3d` library for this purpose.

### Prerequisites

- Install the `open3d` library:

    ```bash
    pip install open3d
    ```

### Example with Open3D

1. Import the required libraries:

    ```python
    import os

    import numpy as np
    import open3d as o3d

    from pathfinding3d.core.diagonal_movement import DiagonalMovement
    from pathfinding3d.core.grid import Grid
    from pathfinding3d.finder.a_star import AStarFinder
    ```

2. Load the sample map:

    ```python
    # Load the map
    matrix = np.load("sample_map.npy")
    ```
    `sample_map.npy` is a numpy array of shape (42, 42, 42), where each element indicates an obstacle or free space. This file can be downloaded from the provided [GitHub link](https://github.com/harisankar95/pathfinding3D/blob/main/examples/sample_map.npy).

3. Create the Grid and define the start and end nodes:

    ```python
    # define start and end points as [x, y, z] coordinates
    start_pt = [21, 21, 21]
    end_pt = [5, 38, 33]

    # create grid representation and start and end nodes
    grid = Grid(matrix=matrix)
    start = grid.node(*start_pt)
    end = grid.node(*end_pt)
    ```
    Note: The `*` operator unpacks the list into individual arguments.
    Here, we define the start and end points of our path and create a grid representation of our 3D space.

4. Find the path:

    ```python
    # initialize A* finder with specified diagonal movement setting
    finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

    # use the finder to get the path
    path, runs = finder.find_path(start, end, grid)

    # print results
    path_cost = end.g
    print(f"path cost: {path_cost:.4f}, path length: {len(path)}, runs: {runs}")
    ```
    
    This will output:

    ```bash
    path cost: 28.6130, path length: 20, runs: 458
    ```

    The path cost can be accessed from the `end` node's `g` attribute for A\*.

5. Visualize the path:
    - Find the obstacles and represent them in blue. The `colors` array is a numpy array of shape (n, 3) where n is the number of obstacles. The first column represents the red channel, the second column represents the green channel, and the third column represents the blue channel. The `xyz_pt` array is a numpy array of shape (n, 3) where n is the number of obstacles. The first column represents the x coordinate, the second column represents the y coordinate, and the third column represents the z coordinate. The `xyz_pt` array is used to create a `PointCloud` object which is then visualized using `draw_geometries`.

        ```python
        # Identifying obstacles and representing them in blue
        obstacle_indices = np.where(matrix == 0)
        xyz_pt = np.stack(obstacle_indices, axis=-1).astype(float)
        colors = np.zeros((xyz_pt.shape[0], 3))
        colors[:, 2] = obstacle_indices[2] / np.max(obstacle_indices[2])
        ```

    - The start point is represented in red and the end point is represented in green. The path is represented in grey. `path_colors` is a numpy array of shape (len(path) - 2, 3) where len(path) is the number of waypoints in the path. Since we already have the start and end points which are also part of the path, we subtract 2 from the length of the path to get the number of remaining waypoints.

        ```python
        # Prepare start and end colors
        start_color = np.array([[1.0, 0, 0]])  # Red
        end_color = np.array([[0, 1.0, 0]])  # Green
        path_colors = np.full((len(path) - 2, 3), [0.7, 0.7, 0.7])  # Grey for the path
        ```

    - Now we can add the start and end points to the `xyz_pt` array along with the remaining waypoints in the path. Similarly the colors can be added to the `colors` array. For every point in the `xyz_pt` array, there is a corresponding color in the `colors` array.

        ```python
        # Combine points and colors for visualization
        xyz_pt = np.concatenate((xyz_pt, [start_pt], [end_pt], path[1:-1]))
        colors = np.concatenate((colors, start_color, end_color, path_colors))
        ```

    - Create a `PointCloud` object with the `xyz_pt` and `colors` arrays.

        ```python
        # Create the point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz_pt)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        ```

    - Create a `VoxelGrid` object from the `PointCloud` object. This will generate a voxel grid from the point cloud. The `voxel_size` parameter determines the size of the voxels.

        ```python
        # Create the voxel grid from the point cloud
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=1.0)
        axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=15.0, origin=np.array([-3.0, -3.0, -3.0]))
        ```

        The axes is for reference and can be removed if not needed.

    - Visualize the voxel grid. The `width` and `height` parameters determine the size of the window.

        ```python
        # Visualize the voxel grid
        o3d.visualization.draw_geometries([axes, voxel_grid], window_name="Voxel Env", width=1024, height=768)
        ```

        You can rotate the voxel grid by clicking and dragging the mouse. You can also zoom in and out using the mouse wheel.

    - The output should look like this:

        ![voxel_grid](https://github.com/harisankar95/pathfinding3D/blob/main/examples/resources/open3d.png)


The full code is available [here](https://github.com/harisankar95/pathfinding3D/blob/main/examples/03_view_map.py)