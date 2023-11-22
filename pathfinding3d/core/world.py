from typing import Dict, List

from .grid import Grid
from .node import GridNode


# a world connects grids but can have multiple grids.
class World:
    def __init__(self, grids: Dict[int, Grid]):
        self.grids = grids

    def neighbors(self, node: GridNode, diagonal_movement: int) -> List[GridNode]:
        """
        Get neighbors of the given node.

        Parameters
        ----------
        node : GridNode
            node to get neighbors from
        diagonal_movement : int
            if diagonal movement is allowed
            (see enum in diagonal_movement)

        Returns
        -------
        List[GridNode]
            neighbors of the given node
        """

        return self.grids[node.grid_id].neighbors(
            node, diagonal_movement=diagonal_movement
        )

    def calc_cost(
        self, node_a: GridNode, node_b: GridNode, weighted: bool = False
    ) -> float:
        """
        Calculate the cost between two nodes.

        Parameters
        ----------
        node_a : GridNode
            first node
        node_b : GridNode
            second node
        weighted : bool
            wether to use weights or not

        Returns
        -------
        float
            cost between the two nodes
        """
        # TODO: if node_a.grid_id != node_b.grid_id calculate distance between
        # grids as well, for now we ignore switching grids
        return self.grids[node_a.grid_id].calc_cost(node_a, node_b, weighted=weighted)
