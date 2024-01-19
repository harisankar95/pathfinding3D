import dataclasses
from typing import List, Optional, Tuple


@dataclasses.dataclass
class Node:
    __slots__ = ["h", "g", "f", "opened", "closed", "parent", "retain_count", "tested"]

    def __init__(self):
        self.cleanup()

    def __lt__(self, other: "Node") -> bool:
        return self.f < other.f

    def cleanup(self):
        """
        Reset all calculated values, fresh start for pathfinding
        """
        # cost from this node to the goal (for A* including the heuristic)
        self.h = 0.0

        # cost from the start node to this node
        # (calculated by distance function, e.g. including diagonal movement)
        self.g = 0.0

        # overall cost for a path using this node (f = g + h )
        self.f = 0.0

        self.opened = 0
        self.closed = False

        # used for backtracking to the start point
        self.parent = None

        # used for recurion tracking of IDA*
        self.retain_count = 0
        # used for IDA* and Jump-Point-Search
        self.tested = False


@dataclasses.dataclass
class GridNode(Node):
    """
    basic node, saves X, Y and Z coordinates on some grid and determine if
    it is walkable.
    """

    # Coordinates
    x: int = 0
    y: int = 0
    z: int = 0

    # Wether this node can be walked through.
    walkable: bool = True

    # used for weighted algorithms
    weight: float = 1.0

    # grid_id is used if we have more than one grid,
    # normally we just count our grids by number
    # but you can also use a string here.
    # Set it to None if you only have one grid.
    grid_id: Optional[int] = None

    connections: Optional[List] = None

    identifier: Optional[Tuple] = None

    def __post_init__(self):
        super().__init__()
        # for heap
        self.identifier: Tuple = (
            (self.x, self.y, self.z) if self.grid_id is None else (self.x, self.y, self.z, self.grid_id)
        )

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        if self.grid_id is not None:
            yield self.grid_id

    def connect(self, other_node: "GridNode"):
        if not self.connections:
            self.connections = [other_node]
        else:
            self.connections.append(other_node)
