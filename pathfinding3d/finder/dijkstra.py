from typing import Callable, Optional, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.heuristic import null
from ..core.node import Node
from .a_star import MAX_RUNS, TIME_LIMIT, AStarFinder


class DijkstraFinder(AStarFinder):
    def __init__(
        self,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.never,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
    ):
        """
        Find shortest path using Dijkstra algorithm

        Parameters
        ----------
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
            heuristic=null,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

    def apply_heuristic(
        self, node_a: Node, node_b: Node, heuristic: Optional[Callable] = None
    ) -> float:
        """
        Helper function to apply heuristic

        Parameters
        ----------
        node_a : Node
            first node
        node_b : Node
            second node
        heuristic : Callable
            heuristic used to calculate distance of 2 points

        Returns
        -------
        float
            1.0
        """
        return 1.0
