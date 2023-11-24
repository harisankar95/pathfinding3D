import time
from typing import Callable, List, Optional, Tuple, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.node import GridNode
from .a_star import AStarFinder
from .finder import BY_END, BY_START, MAX_RUNS, TIME_LIMIT


class BiAStarFinder(AStarFinder):
    """
    Similar to the default A* algorithm from a_star.
    """

    def __init__(
        self,
        heuristic: Optional[Callable] = None,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.never,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
    ):
        """
        Find shortest path using Bi-A* algorithm

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
            (can be a list of grids)

        Returns
        -------
        Tuple[List, int]
            path, number of iterations
        """
        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations

        start_open_list = [start]
        start.g = 0
        start.f = 0
        start.opened = BY_START

        end_open_list = [end]
        end.g = 0
        end.f = 0
        end.opened = BY_END

        while len(start_open_list) > 0 and len(end_open_list) > 0:
            self.runs += 1
            self.keep_running()
            path = self.check_neighbors(
                start,
                end,
                grid,
                start_open_list,
                open_value=BY_START,
                backtrace_by=BY_END,
            )
            if path:
                return path, self.runs

            self.runs += 1
            self.keep_running()
            path = self.check_neighbors(
                end,
                start,
                grid,
                end_open_list,
                open_value=BY_END,
                backtrace_by=BY_START,
            )
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs
