"""
Simple heap with ordering and removal.
Inspired from https://github.com/brean/python-pathfinding/pull/54
Original author: https://github.com/peterchenadded
"""
import heapq
from typing import Callable, Union

from .grid import Grid
from .node import GridNode
from .world import World


class SimpleHeap:
    """
    A simple implementation of a heap data structure optimized for pathfinding.
    It maintains an open list of nodes, a status for each node, and a function to retrieve nodes.
    """

    def __init__(self, node: GridNode, grid: Union[Grid, World]):
        """
        Initializes the SimpleHeap with a given node and grid.

        Parameters
        ----------
        node : GridNode
            The initial node to be added to the heap. This node should have an 'f' attribute representing its cost.
        grid : Union[Grid, World]
            The grid in which the nodes are located.
        """

        self.grid = grid
        self._get_node_tuple = self._determine_node_retrieval_function()
        self._get_node = self._determine_node_function()
        self.open_list = [self._get_node_tuple(node, 0)]
        self.removed_node_tuples = set()
        self.heap_order = {}
        self.number_pushed = 0

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
            return lambda node, heap_order: (node.f, heap_order, *node.identifier)

        if isinstance(self.grid, World):
            return lambda node, heap_order: (node.f, heap_order, *node.identifier)

        raise ValueError("Unsupported grid type")

    def _determine_node_function(self) -> Callable:
        """
        Determines the node function based on the type of grid.

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
            return lambda node_tuple: self.grid.node(*node_tuple[2:])

        if isinstance(self.grid, World):
            return lambda node_tuple: self.grid.grids[node_tuple[5]].node(*node_tuple[2:5])

        raise ValueError("Unsupported grid type")

    def pop_node(self) -> GridNode:
        """
        Pops the node with the lowest cost from the heap.

        Returns
        -------
        GridNode
            The node with the lowest cost.
        """
        node_tuple = heapq.heappop(self.open_list)
        while node_tuple in self.removed_node_tuples:
            node_tuple = heapq.heappop(self.open_list)

        return self._get_node(node_tuple)

    def push_node(self, node: GridNode):
        """
        Pushes a node to the heap.

        Parameters
        ----------
        node : GridNode
            The node to be pushed to the heap.
        """
        self.number_pushed = self.number_pushed + 1
        node_tuple = self._get_node_tuple(node, self.number_pushed)

        self.heap_order[node.identifier] = self.number_pushed

        heapq.heappush(self.open_list, node_tuple)

    def remove_node(self, node: GridNode, old_f: float):
        """
        Remove the node from the heap.

        This just stores it in a set and we just ignore the node if it does
        get popped from the heap.

        Parameters
        ----------
        node : GridNode
            The node to be removed from the heap.
        old_f: float
            The old cost of the node.
        """
        heap_order = self.heap_order[node.identifier]
        node_tuple = self._get_node_tuple(node, heap_order)
        self.removed_node_tuples.add(node_tuple)

    def __len__(self) -> int:
        """
        Returns the length of the heap.

        Returns
        -------
        int
            The length of the heap.
        """
        return len(self.open_list)
