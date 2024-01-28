import logging
from typing import Callable, List, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.node import GridNode
from ..core.util import line_of_sight
from .a_star import AStarFinder
from .finder import MAX_RUNS, TIME_LIMIT


class ThetaStarFinder(AStarFinder):
    def __init__(
        self,
        heuristic: Callable = None,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.always,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
    ):
        """
        Find shortest path using Theta* algorithm
        Diagonal movement is forced to always. Not weighted.

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

        if diagonal_movement != DiagonalMovement.always:
            logging.warning("Diagonal movement is forced to always for Theta*")
        diagonal_movement = DiagonalMovement.always

        super().__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

        self.weighted = False

    def process_node(
        self,
        grid: Grid,
        node: GridNode,
        parent: GridNode,
        end: GridNode,
        open_list: List,
        open_value: int = 1,
    ):
        """
        Check if we can reach the grandparent node directly from the current node
        and if so, skip the parent.

        Parameters
        ----------
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list
        node : GridNode
            the node we like to test
        parent : GridNode
            the parent node (of the current node we like to test)
        end : GridNode
            the end point to calculate the cost of the path
        open_list : List
            the list that keeps track of our current path
        open_value : bool
            needed if we like to set the open list to something
            else than True (used for bi-directional algorithms)
        """
        # Check for line of sight to the grandparent
        if parent and parent.parent and parent.parent.grid_id == node.grid_id:
            grid_to_use = grid.grids[node.grid_id] if hasattr(grid, "grids") else grid
            if line_of_sight(grid_to_use, node, parent.parent):
                ng = parent.parent.g + grid.calc_cost(parent.parent, node, self.weighted)
                if not node.opened or ng < node.g:
                    old_f = node.f
                    node.g = ng
                    node.h = node.h or self.apply_heuristic(node, end)
                    node.f = node.g + node.h
                    node.parent = parent.parent
                    if not node.opened:
                        open_list.push_node(node)
                        node.opened = open_value
                    else:
                        open_list.remove_node(node, old_f)
                        open_list.push_node(node)
            else:
                super().process_node(grid, node, parent, end, open_list)
        else:
            super().process_node(grid, node, parent, end, open_list)
