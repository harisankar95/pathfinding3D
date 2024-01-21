# Steps/Portals/Bridges

With *pathfinding3d*, you can seamlessly connect multiple grids. This feature is invaluable for simulating multi-story structures connected by staircases, bridges between different buildings, or even magical portals linking disparate locations.

## Toy Example: Connecting Two Building Storeys with a Bridge

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
