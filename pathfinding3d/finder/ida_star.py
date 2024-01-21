import time
from typing import Callable, List, Optional, Tuple, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.heuristic import manhattan, octile
from ..core.node import GridNode
from .finder import MAX_RUNS, TIME_LIMIT, Finder


class IDAStarFinder(Finder):
    """
    Iterative Deeping A Star (IDA*) path-finder.

    Recursion based on:
    http://www.apl.jhu.edu/~hall/AI-Programming/IDA-Star.html

    Path retracing based on:
    V. Nageshwara Rao, Vipin Kumar and K. Ramesh
    "A Parallel Implementation of Iterative-Deeping-A*", January 1987.
    ftp://ftp.cs.utexas.edu/.snapshot/hourly.1/pub/AI-Lab/tech-reports/
    UT-AI-TR-87-46.pdf

    based on the JavaScript implementation by Gerard Meier
    (www.gerardmeier.com)
    """

    def __init__(
        self,
        heuristic: Optional[Callable] = None,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.never,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
        track_recursion: bool = True,
    ):
        """
        Find shortest path using IDA* algorithm

        Parameters
        ----------
        heuristic : Callable
            heuristic used to calculate distance of 2 points
        weight : int
            weight for the edges
        diagonal_movement : int
            if diagonal movement is allowed
            (see enum in diagonal_movement)
        time_limit : float
            max. runtime in seconds
        max_runs : int
            max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        track_recursion : bool
            if we should track recursion
        """
        super().__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            weighted=False,
            time_limit=time_limit,
            max_runs=max_runs,
        )
        self.track_recursion = track_recursion
        if not heuristic:
            if diagonal_movement == DiagonalMovement.never:
                self.heuristic = manhattan
            else:
                # When diagonal movement is allowed the manhattan heuristic is
                # not admissible it should be octile instead
                self.heuristic = octile

        self.nodes_visited: int

    def search(
        self,
        node: GridNode,
        g: float,
        cutoff: float,
        path: List[GridNode],
        depth: int,
        end: GridNode,
        grid: Grid,
    ) -> Union[float, GridNode]:
        """
        Recursive IDA* search implementation

        Parameters
        ----------
        node : GridNode
            current node
        g : float
            cost from start to current node
        cutoff : float
            cutoff cost
        path : List[GridNode]
            path
        depth : int
            current depth
        end : GridNode
            end node
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list

        Returns
        -------
        Union[float, GridNode]
            cutoff cost or end node
        """
        self.runs += 1
        self.keep_running()

        self.nodes_visited += 1

        f = g + self.apply_heuristic(node, end) * self.weight

        # We've searched too deep for this iteration.
        if f > cutoff:
            return f

        if node == end:
            if len(path) < depth:
                path += [None] * (depth - len(path) + 1)
            path[depth] = node
            return node

        neighbors = self.find_neighbors(grid, node)

        # Sort the neighbors, gives nicer paths. But, this deviates
        # from the original algorithm - so I left it out
        # TODO: make this an optional parameter
        #    def sort_neighbors(a, b):
        #        return self.apply_heuristic(a, end) - \
        #            self.apply_heuristic(b, end)
        #    sorted(neighbors, sort_neighbors)
        min_t = float("inf")
        for neighbor in neighbors:
            if self.track_recursion:
                # Retain a copy for visualisation. Due to recursion, this
                # node may be part of other paths too.
                neighbor.retain_count += 1
                neighbor.tested = True

            t = self.search(
                neighbor,
                g + grid.calc_cost(node, neighbor),
                cutoff,
                path,
                depth + 1,
                end,
                grid,
            )

            if isinstance(t, GridNode):
                if len(path) < depth:
                    path += [None] * (depth - len(path) + 1)
                path[depth] = node
                return t

            # Decrement count, then determine whether it's actually closed.
            if self.track_recursion:
                neighbor.retain_count -= 1
                if neighbor.retain_count == 0:
                    neighbor.tested = False

            if t < min_t:
                min_t = t

        return min_t

    def find_path(self, start: GridNode, end: GridNode, grid: Grid) -> Tuple[List, int]:
        """
        Find a path from start to end node on grid using the IDA* algorithm

        Parameters
        ----------
        start : GridNode
            start node
        end : GridNode
            end node
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list

        Returns
        -------
        Tuple[List, int]
            path, number of iterations
        """
        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations

        self.nodes_visited = 0  # for statistics

        # initial search depth, given the typical heuristic contraints,
        # there should be no cheaper route possible.
        cutoff = self.apply_heuristic(start, end)

        while True:
            path = []

            # search till cut-off depth:
            t = self.search(start, 0, cutoff, path, 0, end, grid)

            if isinstance(t, bool) and not t:
                # only when an error occured we return "False"
                break

            # If t is a node, it's also the end node. Route is now
            # populated with a valid path to the end node.
            if isinstance(t, GridNode):
                return (
                    [(node.x, node.y, node.z, node.grid_id) for node in path],
                    self.runs,
                )

            # Try again, this time with a deeper cut-off. The t score
            # is the closest we got to the end node.
            cutoff = t

        return [], self.runs
