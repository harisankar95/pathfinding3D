# steps/portals/bridges

*python-pathfinding-3d* allows you to connect grids. This could be useful to create buildings with multiple storeys that are connected by bridges or different areas you want to connect with portals.

Lets say we want to connect 2nd storey of two buildings with a bridge:

```python
world0 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
world1 = [[[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 1], [1, 1, 1]]]
# create Grid instances for both worlds
grid0 = Grid(matrix=level0, grid_id=0)
grid1 = Grid(matrix=level1, grid_id=1)
```

We can connect a node from one grid to another by defining a connection between the two grids like this:

```python
grid0.node(2, 2, 2).connect(grid1.node(2, 2, 2))
grid1.node(2, 2, 2).connect(grid0.node(2, 2, 2))
```

Note that we need to do this in both directions if we want to allow the connection to go both ways (otherwise the portal can only go in one direction, which might be a desired feature).

Because the `find_neighbors`-function in the finder needs to look up both grids we need to provide both grids to the finder. We can create a "world" that looks up both grids:

```python
  # create world with both grids
world = World({
    0: grid0,
    1: grid1
})

finder = AStarFinder()
path, _ = finder.find_path(grid0.node(2, 0, 0), grid1.node(2, 0, 0), world)
```

and that gives you the path from the start node in the first grid to the end node in the second grid.

For the whole code take a look at the `test_connect_grids.py` file in the `test`-folder
