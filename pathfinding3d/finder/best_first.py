from typing import Callable, Optional, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.node import GridNode
from .a_star import MAX_RUNS, TIME_LIMIT, AStarFinder


class BestFirst(AStarFinder):
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
        Find shortest path using BestFirst algorithm

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

        self.weighted = False

    def apply_heuristic(self, node_a: GridNode, node_b: GridNode, heuristic: Optional[Callable] = None) -> float:
        """
        Helper function to apply heuristic

        Parameters
        ----------
        node_a : GridNode
            first node
        node_b : GridNode
            second node
        heuristic : Callable
            heuristic used to calculate distance of 2 points

        Returns
        -------
        float
            heuristic value
        """
        return super().apply_heuristic(node_a, node_b, heuristic) * 1000000
