import math
import warnings
from functools import lru_cache
from typing import List, Optional, Tuple, Union

import numpy as np

from .diagonal_movement import DiagonalMovement
from .node import GridNode

try:
    import plotly.graph_objects as go

    USE_PLOTLY = True
except ImportError:
    USE_PLOTLY = False


MatrixType = Optional[Union[List[List[List[int]]], np.ndarray]]


def build_nodes(
    width: int,
    height: int,
    depth: int,
    matrix: MatrixType = None,
    inverse: bool = False,
    grid_id: Optional[int] = None,
) -> List[List[List[GridNode]]]:
    """
    Create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.

    Parameters
    ----------
    width : int
        The width of the grid.
    height : int
        The height of the grid.
    depth : int
        The depth of the grid.
    matrix : MatrixType
        A 3D array of values (numbers or objects specifying weight)
        that determine how nodes are connected and if they are walkable.
        If no matrix is given, all nodes will be walkable.
    inverse : bool, optional
        If true, all values in the matrix that are not 0 will be considered
        walkable. Otherwise all values that are 0 will be considered walkable.
    grid_id : int, optional
        The id of the grid.

    Returns
    -------
    List[List[List[GridNode]]]
        A list of list of lists containing the nodes in the grid.
    """
    nodes: List = []
    use_matrix = matrix is not None

    for x in range(width):
        nodes.append([])
        for y in range(height):
            nodes[x].append([])
            for z in range(depth):
                # 0, '0', False will be obstacles
                # all other values mark walkable cells.
                # you can use values bigger then 1 to assign a weight.
                # If inverse is False it changes
                # (1 and up becomes obstacle and 0 or everything negative marks a
                #  free cells)
                weight = int(matrix[x][y][z]) if use_matrix else 1
                walkable = weight <= 0 if inverse else weight >= 1

                nodes[x][y].append(GridNode(x=x, y=y, z=z, walkable=walkable, weight=weight, grid_id=grid_id))
    return nodes


class Grid:
    """
    A grid represents the map (as 3d-list of nodes).
    """

    def __init__(
        self,
        width: int = 0,
        height: int = 0,
        depth: int = 0,
        matrix: MatrixType = None,
        grid_id: Optional[int] = None,
        inverse: bool = False,
    ):
        """
        Create a new grid.

        Parameters
        ----------
        width : int, optional
            The width of the grid.
        height : int, optional
            The height of the grid.
        depth : int, optional
            The depth of the grid.
        matrix : MatrixType
            A 3D array of values (numbers or objects specifying weight)
            that determine how nodes are connected and if they are walkable.
            If no matrix is given, all nodes will be walkable.
        inverse : bool, optional
            If true, all values in the matrix that are not 0 will be considered
            walkable. Otherwise all values that are 0 will be considered walkable.
        """
        self.width, self.height, self.depth = self._validate_dimensions(width, height, depth, matrix)
        self.nodes = (
            build_nodes(self.width, self.height, self.depth, matrix, inverse, grid_id)
            if self.is_valid_grid()
            else [[[]]]
        )

    def _validate_dimensions(self, width: int, height: int, depth: int, matrix: MatrixType) -> tuple:
        if matrix is not None:
            if not (
                isinstance(matrix, (list, np.ndarray))
                and len(matrix) > 0
                and len(matrix[0]) > 0
                and len(matrix[0][0]) > 0
            ):
                raise ValueError("Provided matrix is not a 3D structure or is empty.")
            return len(matrix), len(matrix[0]), len(matrix[0][0])
        return width, height, depth

    def is_valid_grid(self) -> bool:
        """
        Check if grid is valid

        Returns
        -------
        bool
            True, if grid is valid
        """
        return self.width > 0 and self.height > 0 and self.depth > 0

    def node(self, x: int, y: int, z: int) -> Optional[GridNode]:
        """
        Get node at position

        Parameters
        ----------
        x : int
            x position
        y : int
            y position
        z : int
            z position

        Returns
        -------
        GridNode
            node at position
        """
        return self.nodes[x][y][z] if self.inside(x, y, z) else None

    def inside(self, x: int, y: int, z: int) -> bool:
        """
        Check, if field position is inside map

        Parameters
        ----------
        x : int
            x position
        y : int
            y position
        z : int
            z position

        Returns
        -------
        bool
            True, if position is inside map
        """
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth

    def walkable(self, x: int, y: int, z: int) -> bool:
        """
        Check, if the tile is inside grid and if it is set as walkable

        Parameters
        ----------
        x : int
            x position
        y : int
            y position
        z : int
            z position

        Returns
        -------
        bool
            True, if position is inside map and walkable
        """
        return self.inside(x, y, z) and self.nodes[x][y][z].walkable

    @lru_cache(maxsize=128)
    def _calc_cost(self, dx: int, dy: int, dz: int) -> float:
        """
        Get the distance between current node and the neighbor (cost)

        Parameters
        ----------
        dx : int
            x distance
        dy : int
            y distance
        dz : int
            z distance

        Returns
        -------
        float
            distance between current node and the neighbor (cost)
        """
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def calc_cost(self, node_a: GridNode, node_b: GridNode, weighted: bool = False) -> float:
        """
        Get the distance between current node and the neighbor (cost)

        Parameters
        ----------
        node_a : GridNode
            current node
        node_b : GridNode
            neighbor node
        weighted : bool, optional
            True, if weighted algorithm is used, by default False

        Returns
        -------
        float
            distance between current node and the neighbor (cost)
        """
        # Check if we have a straight, diagonal in plane or diagonal in space
        dx = node_b.x - node_a.x
        dy = node_b.y - node_a.y
        dz = node_b.z - node_a.z

        ng = self._calc_cost(dx, dy, dz)

        # weight for weighted algorithms
        if weighted:
            ng *= node_b.weight

        return ng

    def neighbors(
        self,
        node: GridNode,
        diagonal_movement: int = DiagonalMovement.never,
    ) -> List[GridNode]:
        """
        Get all neighbors of one node

        Parameters
        ----------
        node : GridNode
            node to get neighbors from
        diagonal_movement : int, optional
            if diagonal movement is allowed
            (see enum in diagonal_movement), by default DiagonalMovement.never

        Returns
        -------
        List[GridNode]
            list of all neighbors
        """
        x, y, z = node.x, node.y, node.z

        neighbors = []
        # current plane
        cs0 = cd0 = cs1 = cd1 = cs2 = cd2 = cs3 = cd3 = False
        # upper plane
        us0 = ud0 = us1 = ud1 = us2 = ud2 = us3 = ud3 = ut = False  # ut = upper top
        # lower plane
        ls0 = ld0 = ls1 = ld1 = ls2 = ld2 = ls3 = ld3 = lb = False  # lb = lower bottom

        # -y
        if self.walkable(x, y - 1, z):
            neighbors.append(self.nodes[x][y - 1][z])
            cs0 = True

        # +x
        if self.walkable(x + 1, y, z):
            neighbors.append(self.nodes[x + 1][y][z])
            cs1 = True

        # +y
        if self.walkable(x, y + 1, z):
            neighbors.append(self.nodes[x][y + 1][z])
            cs2 = True

        # -x
        if self.walkable(x - 1, y, z):
            neighbors.append(self.nodes[x - 1][y][z])
            cs3 = True

        # +z
        if self.walkable(x, y, z + 1):
            neighbors.append(self.nodes[x][y][z + 1])
            ut = True

        # -z
        if self.walkable(x, y, z - 1):
            neighbors.append(self.nodes[x][y][z - 1])
            lb = True

        # check for connections to other grids
        if node.connections:
            neighbors.extend(node.connections)

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            cd0 = cs0 and cs1
            cd1 = cs1 and cs2
            cd2 = cs2 and cs3
            cd3 = cs3 and cs0

            us0 = cs0 and ut
            us1 = cs1 and ut
            us2 = cs2 and ut
            us3 = cs3 and ut

            ls0 = cs0 and lb
            ls1 = cs1 and lb
            ls2 = cs2 and lb
            ls3 = cs3 and lb

        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            cd0 = cs0 or cs1
            cd1 = cs1 or cs2
            cd2 = cs2 or cs3
            cd3 = cs3 or cs0

            us0 = cs0 or ut
            us1 = cs1 or ut
            us2 = cs2 or ut
            us3 = cs3 or ut

            ls0 = cs0 or lb
            ls1 = cs1 or lb
            ls2 = cs2 or lb
            ls3 = cs3 or lb

        elif diagonal_movement == DiagonalMovement.always:
            cd0 = cd1 = cd2 = cd3 = True
            us0 = us1 = us2 = us3 = True
            ls0 = ls1 = ls2 = ls3 = True

        # +x -y
        if cd0 and self.walkable(x + 1, y - 1, z):
            neighbors.append(self.nodes[x + 1][y - 1][z])
        else:
            cd0 = False

        # +x +y
        if cd1 and self.walkable(x + 1, y + 1, z):
            neighbors.append(self.nodes[x + 1][y + 1][z])
        else:
            cd1 = False

        # -x +y
        if cd2 and self.walkable(x - 1, y + 1, z):
            neighbors.append(self.nodes[x - 1][y + 1][z])
        else:
            cd2 = False

        # -x -y
        if cd3 and self.walkable(x - 1, y - 1, z):
            neighbors.append(self.nodes[x - 1][y - 1][z])
        else:
            cd3 = False

        # -y +z
        if us0 and self.walkable(x, y - 1, z + 1):
            neighbors.append(self.nodes[x][y - 1][z + 1])
        else:
            us0 = False

        # +x +z
        if us1 and self.walkable(x + 1, y, z + 1):
            neighbors.append(self.nodes[x + 1][y][z + 1])
        else:
            us1 = False

        # +y +z
        if us2 and self.walkable(x, y + 1, z + 1):
            neighbors.append(self.nodes[x][y + 1][z + 1])
        else:
            us2 = False

        # -x +z
        if us3 and self.walkable(x - 1, y, z + 1):
            neighbors.append(self.nodes[x - 1][y][z + 1])
        else:
            us3 = False

        # -y -z
        if ls0 and self.walkable(x, y - 1, z - 1):
            neighbors.append(self.nodes[x][y - 1][z - 1])
        else:
            ls0 = False

        # +x -z
        if ls1 and self.walkable(x + 1, y, z - 1):
            neighbors.append(self.nodes[x + 1][y][z - 1])
        else:
            ls1 = False

        # +y -z
        if ls2 and self.walkable(x, y + 1, z - 1):
            neighbors.append(self.nodes[x][y + 1][z - 1])
        else:
            ls2 = False

        # -x -z
        if ls3 and self.walkable(x - 1, y, z - 1):
            neighbors.append(self.nodes[x - 1][y][z - 1])
        else:
            ls3 = False

        # remaining daigonal neighbors
        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            ud0 = cs0 and cd0 and cs1 and us0 and us1 and ut
            ud1 = cs1 and cd1 and cs2 and us1 and us2 and ut
            ud2 = cs2 and cd2 and cs3 and us2 and us3 and ut
            ud3 = cs3 and cd3 and cs0 and us3 and us0 and ut

            ld0 = cs0 and cd0 and cs1 and ls0 and ls1 and lb
            ld1 = cs1 and cd1 and cs2 and ls1 and ls2 and lb
            ld2 = cs2 and cd2 and cs3 and ls2 and ls3 and lb
            ld3 = cs3 and cd3 and cs0 and ls3 and ls0 and lb

        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            ud0 = sum([cs0, cd0, cs1, us0, us1, ut]) >= 5
            ud1 = sum([cs1, cd1, cs2, us1, us2, ut]) >= 5
            ud2 = sum([cs2, cd2, cs3, us2, us3, ut]) >= 5
            ud3 = sum([cs3, cd3, cs0, us3, us0, ut]) >= 5

            ld0 = sum([cs0, cd0, cs1, ls0, ls1, lb]) >= 5
            ld1 = sum([cs1, cd1, cs2, ls1, ls2, lb]) >= 5
            ld2 = sum([cs2, cd2, cs3, ls2, ls3, lb]) >= 5
            ld3 = sum([cs3, cd3, cs0, ls3, ls0, lb]) >= 5

        elif diagonal_movement == DiagonalMovement.always:
            ud0 = ud1 = ud2 = ud3 = True
            ld0 = ld1 = ld2 = ld3 = True

        # +x -y +z
        if ud0 and self.walkable(x + 1, y - 1, z + 1):
            neighbors.append(self.nodes[x + 1][y - 1][z + 1])

        # +x +y +z
        if ud1 and self.walkable(x + 1, y + 1, z + 1):
            neighbors.append(self.nodes[x + 1][y + 1][z + 1])

        # -x +y +z
        if ud2 and self.walkable(x - 1, y + 1, z + 1):
            neighbors.append(self.nodes[x - 1][y + 1][z + 1])

        # -x -y +z
        if ud3 and self.walkable(x - 1, y - 1, z + 1):
            neighbors.append(self.nodes[x - 1][y - 1][z + 1])

        # +x -y -z
        if ld0 and self.walkable(x + 1, y - 1, z - 1):
            neighbors.append(self.nodes[x + 1][y - 1][z - 1])

        # +x +y -z
        if ld1 and self.walkable(x + 1, y + 1, z - 1):
            neighbors.append(self.nodes[x + 1][y + 1][z - 1])

        # -x +y -z
        if ld2 and self.walkable(x - 1, y + 1, z - 1):
            neighbors.append(self.nodes[x - 1][y + 1][z - 1])

        # -x -y -z
        if ld3 and self.walkable(x - 1, y - 1, z - 1):
            neighbors.append(self.nodes[x - 1][y - 1][z - 1])

        return neighbors

    def cleanup(self):
        """
        Cleanup grid
        """
        for x_nodes in self.nodes:
            for y_nodes in x_nodes:
                for z_node in y_nodes:
                    z_node.cleanup()

    def visualize(
        self,
        path: Optional[List[Union[GridNode, Tuple]]] = None,
        start: Optional[Union[GridNode, Tuple]] = None,
        end: Optional[Union[GridNode, Tuple]] = None,
        visualize_weight: bool = True,
        save_html: bool = False,
        save_to: str = "./pathfinding3d_visualization.html",
        always_show: bool = False,
    ):
        """
        Creates a 3D visualization of the grid, including optional path, start/end points,
        and node weights using plotly. This method is designed to help visualize the
        spatial layout, obstacles, and pathfinding results in three dimensions.

        Parameters
        ----------
        path : Optional[List[Union[GridNode, Tuple]]], optional
            The path to visualize, specified as a list of GridNode instances or coordinate tuples (x, y, z).
            If omitted, the grid is visualized without a path. Defaults to None.
        start : Optional[Union[GridNode, Tuple]], optional
            The start node for the path, as either a GridNode or a tuple of coordinates.
            If not provided and a path is given, the first node of the path is used. Defaults to None.
        end : Optional[Union[GridNode, Tuple]], optional
            The end node for the path, as either a GridNode or a tuple of coordinates.
            If not provided and a path is given, the last node of the path is used. Defaults to None.
        visualize_weight : bool, optional
            Whether to visualize the weights of the nodes, enhancing the representation of node costs.
            Defaults to True.
        save_html : bool, optional
            If True, the visualization is saved to an HTML file specified by `save_to` instead of being displayed.
            Defaults to False.
        save_to : str, optional
            File path where the HTML visualization is saved if `save_html` is True.
            Defaults to "./pathfinding3d_visualization.html".
        always_show : bool, optional
            If True, displays the visualization in the browser even when `save_html` is True.
            Useful for immediate feedback while also saving the result. Defaults to False.

        Raises
        ------
        Warning
            If plotly is not installed, a warning is logged and the visualization is skipped.

        Notes
        -----
        - Requires plotly for visualization. Install with `pip install plotly` if not already installed.
        """
        if not USE_PLOTLY:
            warnings.warn("Plotly is not installed. Please install it to use this feature.")
            return

        # Extract obstacle and weight information directly from the grid
        X, Y, Z, obstacle_values, weight_values = [], [], [], [], []
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    node = self.node(x, y, z)
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                    obstacle_values.append(0 if node.walkable else 1)
                    weight_values.append(node.weight if node.walkable else 0)

        # Create obstacle volume visualization
        obstacle_vol = go.Volume(
            x=np.array(X),
            y=np.array(Y),
            z=np.array(Z),
            value=np.array(obstacle_values),
            isomin=0.1,
            isomax=1.0,
            opacity=0.1,
            surface_count=25,  # Increase for better visibility
            colorscale="Greys",
            showscale=False,
            name="Obstacles",
        )

        # List of items to visualize
        visualizations = [obstacle_vol]

        # Create weight volume visualization
        if visualize_weight:
            weight_vol = go.Volume(
                x=np.array(X),
                y=np.array(Y),
                z=np.array(Z),
                value=np.array(weight_values),
                isomin=1.01,  # Assuming default weight is 1, adjust as needed
                isomax=max(weight_values) * 1.01,
                opacity=0.5,  # Adjust for better visibility
                surface_count=25,
                colorscale="Viridis",  # A different colorscale for distinction
                showscale=True,
                colorbar=dict(title="Weight", ticks="outside"),
            )
            visualizations.append(weight_vol)

        # Add path visualization if path is provided
        if path:
            # Convert path to coordinate tuples
            path = [p.identifier if isinstance(p, GridNode) else p for p in path]

            # Create path visualization
            path_x, path_y, path_z = zip(*path)
            path_trace = go.Scatter3d(
                x=path_x,
                y=path_y,
                z=path_z,
                mode="markers+lines",
                marker=dict(size=6, color="red", opacity=0.9),
                line=dict(color="red", width=3),
                name="Path",
                hovertext=[f"Step {i}: ({x}, {y}, {z})" for i, (x, y, z) in enumerate(path)],
                hoverinfo="text",
            )
            visualizations.append(path_trace)

            # Set start and end nodes if not provided
            start = start or path[0]
            end = end or path[-1]

        # Add start and end node visualizations if available
        if start:
            start = start.identifier if isinstance(start, GridNode) else start
            start_trace = go.Scatter3d(
                x=[start[0]],
                y=[start[1]],
                z=[start[2]],
                mode="markers",
                marker=dict(size=8, color="green", symbol="diamond"),
                name="Start",
                hovertext=f"Start: {start}",
                hoverinfo="text",
            )
            visualizations.append(start_trace)

        if end:
            end = end.identifier if isinstance(end, GridNode) else end
            end_trace = go.Scatter3d(
                x=[end[0]],
                y=[end[1]],
                z=[end[2]],
                mode="markers",
                marker=dict(size=8, color="blue", symbol="diamond"),
                name="End",
                hovertext=f"End: {end}",
                hoverinfo="text",
            )
            visualizations.append(end_trace)

        # Camera settings
        # Set camera perpendicular to the z-axis
        camera = dict(eye=dict(x=0.0, y=0.0, z=self.depth / 4))

        # Specify layout
        layout = go.Layout(
            title="3D Pathfinding Visualization",
            scene=dict(
                xaxis=dict(title="X-axis", showbackground=True),
                yaxis=dict(title="Y-axis", showbackground=True),
                zaxis=dict(title="Z-axis", showbackground=True),
                aspectmode="auto",
            ),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            autosize=True,
            scene_camera=camera,
        )

        # Create figure
        fig = go.Figure(data=visualizations, layout=layout)

        # Save visualization to HTML file if specified
        if save_html:
            fig.write_html(save_to, auto_open=False)
            print(f"Visualization saved to: {save_to}")

        if always_show or not save_html:
            fig.show()
