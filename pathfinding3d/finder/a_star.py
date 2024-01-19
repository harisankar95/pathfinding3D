from typing import Callable, List, Optional, Tuple, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.heuristic import manhattan, octile
from ..core.node import GridNode
from ..core.util import backtrace, bi_backtrace
from .finder import BY_END, MAX_RUNS, TIME_LIMIT, Finder


class AStarFinder(Finder):
    def __init__(
        self,
        heuristic: Optional[Callable] = None,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.never,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
    ):
        """
        Find shortest path using A* algorithm

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
        """

        super().__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

        if not heuristic:
            if diagonal_movement == DiagonalMovement.never:
                self.heuristic = manhattan
            else:
                # When diagonal movement is allowed the manhattan heuristic is
                # not admissible it should be octile instead
                self.heuristic = octile

    def check_neighbors(
        self,
        start: GridNode,
        end: GridNode,
        grid: Grid,
        open_list: List,
        open_value: int = 1,
        backtrace_by=None,
    ) -> Optional[List[GridNode]]:
        """
        Find next path segment based on given node
        (or return path if we found the end)

        Parameters
        ----------
        start : GridNode
            start node
        end : GridNode
            end node
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list
        open_list : List
            stores nodes that will be processed next

        Returns
        -------
        Optional[List[GridNode]]
            path
        """

        # pop node with minimum 'f' value
        node = open_list.pop_node()
        node.closed = True

        # if reached the end position, construct the path and return it
        # (ignored for bi-directional a*, there we look for a neighbor that is
        #  part of the oncoming path)
        if not backtrace_by and node == end:
            return backtrace(end)

        # get neighbors of the current node
        neighbors = self.find_neighbors(grid, node)
        for neighbor in neighbors:
            if neighbor.closed:
                # already visited last minimum f value
                continue
            if backtrace_by and neighbor.opened == backtrace_by:
                # found the oncoming path
                if backtrace_by == BY_END:
                    return bi_backtrace(node, neighbor)

                return bi_backtrace(neighbor, node)

            # check if the neighbor has not been inspected yet, or
            # can be reached with smaller cost from the current node
            self.process_node(grid, neighbor, node, end, open_list, open_value)

        # the end has not been reached (yet) keep the find_path loop running
        return None

    def find_path(self, start: GridNode, end: GridNode, grid: Grid) -> Tuple[List, int]:
        """
        Find a path from start to end node on grid using the A* algorithm

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

        start.g = 0
        start.f = 0
        return super().find_path(start, end, grid)
