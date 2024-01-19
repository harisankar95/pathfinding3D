"""
Simple heap with ordering and removal.
Inspired from https://github.com/brean/python-pathfinding/pull/54
"""
import heapq
from typing import Callable, Tuple

from .grid import Grid
from .world import World


class SimpleHeap:
    """
    A simple implementation of a heap data structure.
    It maintains an open list of nodes, a status for each node, and a function to retrieve nodes.
    """

    def __init__(self, node, grid):
        """
        Initializes the SimpleHeap with a given node and grid.

        Parameters
        ----------
        node : Node
            The initial node to be added to the heap. This node should have an 'f' attribute representing its cost.
        grid : list of list of Node
            The grid in which the nodes are located. This is used for pathfinding purposes.
        """

        self.grid = grid
        self.open_list = [(node.f, node)]
        self.node_status = {self._generate_node_identifier(node): True}
        self.node_retrieval_function = self._determine_node_retrieval_function()

    def _determine_node_retrieval_function(self) -> Callable:
        """
        Determines the node retrieval function based on the type of grid.

        Returns
        -------
        function
            A function that takes a node tuple and returns the corresponding node.

        Raises
        ------
        ValueError
            If the grid is not of type Grid or World.
        """
        if isinstance(self.grid, Grid):
            return lambda node_tuple: self.grid.node(node_tuple[1].x, node_tuple[1].y, node_tuple[1].z)

        if isinstance(self.grid, World):
            return lambda node_tuple: self.grid.grids[node_tuple[1].grid_id].node(
                node_tuple[1].x, node_tuple[1].y, node_tuple[1].z
            )

        raise ValueError("Unsupported grid type")

    def _generate_node_identifier(self, node) -> Tuple:
        """
        Generates the node identifier based on the type of grid.

        Parameters
        ----------
        node : Node
            The node for which to generate the identifier.

        Returns
        -------
        Tuple
            The node identifier.
        """

        if isinstance(self.grid, World):
            return (node.x, node.y, node.z, node.grid_id)

        return (node.x, node.y, node.z)

    def pop_node(self) -> Tuple:
        """
        Pops the node with the lowest cost from the heap.

        Returns
        -------
        Tuple
            The node with the lowest cost.
        """

        while True:
            _, node = heapq.heappop(self.open_list)
            if self.node_status.get(self._generate_node_identifier(node), False):
                return self.node_retrieval_function((None, node))

    def push_node(self, node):
        """
        Pushes a node to the heap.

        Parameters
        ----------
        node : Node
            The node to be pushed to the heap.
        """
        heapq.heappush(self.open_list, (node.f, node))
        self.node_status[self._generate_node_identifier(node)] = True

    def remove_node(self, node):
        """
        Removes a node from the heap.

        Parameters
        ----------
        node : Node
            The node to be removed from the heap.
        """
        self.node_status[self._generate_node_identifier(node)] = False

    def __len__(self) -> int:
        """
        Returns the length of the heap.

        Returns
        -------
        int
            The length of the heap.
        """
        return len(self.open_list)
