import heapq  # used for the so colled "open list" that stores known nodes
import time  # for time limitation
from typing import Callable, List, Optional, Tuple, Union

from ..core.diagonal_movement import DiagonalMovement
from ..core.grid import Grid
from ..core.node import GridNode

# max. amount of tries we iterate until we abort the search
MAX_RUNS = float("inf")
# max. time after we until we abort the search (in seconds)
TIME_LIMIT = float("inf")

# used for backtrace of bi-directional A*
BY_START = 1
BY_END = 2


class ExecutionTimeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ExecutionRunsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Finder:
    def __init__(
        self,
        heuristic: Optional[Callable] = None,
        weight: int = 1,
        diagonal_movement: int = DiagonalMovement.never,
        weighted: bool = True,
        time_limit: float = TIME_LIMIT,
        max_runs: Union[int, float] = MAX_RUNS,
    ):
        """
        Find shortest path

        Parameters
        ----------
        heuristic : Callable
            heuristic used to calculate distance of 2 points
        weight : int
            weight for the edges
        diagonal_movement : int
            if diagonal movement is allowed
            (see enum in diagonal_movement)
        weighted: the algorithm supports weighted nodes
            (should be True for A* and Dijkstra)
        time_limit : float
            max. runtime in seconds
        max_runs : int
            max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        self.time_limit = time_limit
        self.max_runs = max_runs
        self.weighted = weighted

        self.diagonal_movement = diagonal_movement
        self.weight = weight
        self.heuristic = heuristic

        self.start_time: float
        self.runs: int

    def apply_heuristic(
        self, node_a: GridNode, node_b: GridNode, heuristic: Optional[Callable] = None
    ) -> float:
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
        if not heuristic:
            heuristic = self.heuristic
        return heuristic(
            abs(node_a.x - node_b.x),
            abs(node_a.y - node_b.y),
            abs(node_a.z - node_b.z),
        )

    def find_neighbors(
        self,
        grid: Grid,
        node: GridNode,
        diagonal_movement: Optional[int] = None,
    ) -> List[GridNode]:
        """
        Find neighbor, same for Djikstra, A*, Bi-A*, IDA*

        Parameters
        ----------
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list
        node : GridNode
            node to find neighbors for
        diagonal_movement : int
            if diagonal movement is allowed
            (see enum in diagonal_movement)

        Returns
        -------
        List[GridNode]
            list of neighbors
        """
        if not diagonal_movement:
            diagonal_movement = self.diagonal_movement
        return grid.neighbors(node, diagonal_movement=diagonal_movement)

    def keep_running(self):
        """
        Check, if we run into time or iteration constrains.

        Raises
        ------
        ExecutionTimeException
            if we run into a time constrain
        ExecutionRunsException
            if we run into a iteration constrain
        """
        if self.runs >= self.max_runs:
            raise ExecutionRunsException(
                f"{self.__class__.__name__} run into barrier of {self.max_runs} iterations without "
                "finding the destination"
            )

        if time.time() - self.start_time >= self.time_limit:
            raise ExecutionTimeException(
                f"{self.__class__.__name__} took longer than {self.time_limit} seconds, aborting!"
            )

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
        We check if the given node is part of the path by calculating its
        cost and add or remove it from our path

        Parameters
        ----------
        grid : Grid
            grid that stores all possible steps/tiles as 3D-list
        node : GridNode
            the node we like to test
            (the neighbor in A* or jump-node in JumpPointSearch)
        parent : GridNode
            the parent node (the current node we like to test)
        end : GridNode
            the end point to calculate the cost of the path
        open_list : List
            the list that keeps track of our current path
        open_value : bool
            needed if we like to set the open list to something
            else than True (used for bi-directional algorithms)
        """

        # calculate cost from current node (parent) to the next node (neighbor)
        ng = grid.calc_cost(parent, node, self.weighted)

        if not node.opened or ng < node.g:
            node.g = ng
            node.h = node.h or self.apply_heuristic(node, end) * self.weight
            # f is the estimated total cost from start to goal
            node.f = node.g + node.h
            node.parent = parent

            if not node.opened:
                heapq.heappush(open_list, node)
                node.opened = open_value
            else:
                # the node can be reached with smaller cost.
                # Since its f value has been updated, we have to
                # update its position in the open list
                open_list.remove(node)
                heapq.heappush(open_list, node)

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
        find next path segment based on given node
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
        raise NotImplementedError("Please implement check_neighbors in your finder")

    def find_path(self, start: GridNode, end: GridNode, grid: Grid) -> Tuple[List, int]:
        """
        Find a path from start to end node on grid by iterating over
        all neighbors of a node (see check_neighbors)

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
        start.opened = True

        open_list = [start]

        while len(open_list) > 0:
            self.runs += 1
            self.keep_running()

            path = self.check_neighbors(start, end, grid, open_list)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs

    def __repr__(self):
        """
        Return a human readable representation
        """
        return (
            f"<{self.__class__.__name__}"
            f"diagonal_movement={self.diagonal_movement} >"
        )
