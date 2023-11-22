from typing import Callable, List, Optional

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.node import Node
from ..core.util import backtrace
from .finder import MAX_RUNS, TIME_LIMIT, Finder


class BreadthFirstFinder(Finder):
    def __init__(
        self,
        heuristic: Optional[Callable] = None,
        weight: int = 1,
        diagonal_movement: DiagonalMovement = DiagonalMovement.never,
        time_limit: float = TIME_LIMIT,
        max_runs: int = MAX_RUNS,
    ):
        """
        Find shortest path using Breadth First algorithm

        Parameters
        ----------
        heuristic : Callable
            heuristic used to calculate distance of 2 points
        weight : int
            weight for the edges
        diagonal_movement : DiagonalMovement
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
            weighted=False,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )
        if not diagonal_movement:
            self.diagonalMovement = DiagonalMovement.never

    def check_neighbors(
        self,
        start: Node,
        end: Node,
        grid: Grid,
        open_list: List,
    ) -> Optional[List[Node]]:
        """
        Find next path segment based on given node
        (or return path if we found the end)

        Parameters
        ----------
        start : Node
            start node
        end : Node
            end node
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list
        open_list : List
            stores nodes that will be processed next

        Returns
        -------
        Optional[List[Node]]
            path
        """
        node = open_list.pop(0)
        node.closed = True

        if node == end:
            return backtrace(end)

        neighbors = self.find_neighbors(grid, node)
        for neighbor in neighbors:
            if neighbor.closed or neighbor.opened:
                continue

            open_list.append(neighbor)
            neighbor.opened = True
            neighbor.parent = node
