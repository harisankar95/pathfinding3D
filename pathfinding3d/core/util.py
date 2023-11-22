import copy
import math
from typing import List, Tuple

from .grid import Grid
from .node import GridNode

# square root of 2 for diagonal distance
SQRT2 = math.sqrt(2)
# square root of 3 for octile distance
SQRT3 = math.sqrt(3)

Coords = Tuple[float, float, float]


def backtrace(node: GridNode) -> List[GridNode]:
    """
    Backtrace according to the parent records and return the path.
    (including both start and end nodes)

    Parameters
    ----------
    node : GridNode
        node to backtrace from

    Returns
    -------
    List[GridNode]
        path
    """
    path = [node]
    while node.parent:
        node = node.parent
        path.append(node)
    path.reverse()
    return path


def bi_backtrace(node_a: GridNode, node_b: GridNode) -> List[GridNode]:
    """
    Backtrace from start and end node, returns the path for bi-directional A*
    (including both start and end nodes)

    Parameters
    ----------
    node_a : GridNode
        start node
    node_b : GridNode
        end node

    Returns
    -------
    List[GridNode]
        path
    """
    path_a = backtrace(node_a)
    path_b = backtrace(node_b)
    path_b.reverse()
    return path_a + path_b


def raytrace(coords_a: Coords, coords_b: Coords) -> List[List[float]]:
    """
    Given the start and end coordinates, return all the coordinates lying
    on the line formed by these coordinates, based on ray tracing.

    Parameters
    ----------
    coords_a : Coords
        start coordinates
    coords_b : Coords
        end coordinates

    Returns
    -------
    List[List[float]]
        list of coordinates
    """
    line = []
    x0, y0, z0 = coords_a
    x1, y1, z1 = coords_b

    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0

    t = 0.0
    grid_pos = [x0, y0, z0]
    t_for_one = [abs(1.0 / d) if d != 0 else 1e10 for d in (dx, dy, dz)]

    frac_start = [
        (x0 + 0.5) - x0,
        (y0 + 0.5) - y0,
        (z0 + 0.5) - z0,
    ]

    t_for_next_border = [
        (1 - frac_start[0]) * t_for_one[0] if dx < 0 else frac_start[0] * t_for_one[0],
        (1 - frac_start[1]) * t_for_one[1] if dy < 0 else frac_start[1] * t_for_one[1],
        (1 - frac_start[2]) * t_for_one[2] if dz < 0 else frac_start[2] * t_for_one[2],
    ]

    step = [1 if d >= 0 else -1 for d in (dx, dy, dz)]

    while t <= 1.0:
        line.append(copy.copy(grid_pos))
        index = None
        if (
            t_for_next_border[0] <= t_for_next_border[1]
            and t_for_next_border[0] <= t_for_next_border[2]
        ):
            index = 0
        elif (
            t_for_next_border[1] <= t_for_next_border[2]
            and t_for_next_border[1] <= t_for_next_border[0]
        ):
            index = 1
        else:
            index = 2
        t = t_for_next_border[index]
        t_for_next_border[index] += t_for_one[index]
        grid_pos[index] += step[index]

    return line


def bresenham(coords_a: Coords, coords_b: Coords) -> List[List[float]]:
    """
    Given the start and end coordinates, return all the coordinates lying
    on the line formed by these coordinates, based on Bresenham's algorithm.

    Parameters
    ----------
    coords_a : Coords
        start coordinates
    coords_b : Coords
        end coordinates

    Returns
    -------
    List[List[float]]
        list of coordinates
    """
    line = []
    x0, y0, z0 = coords_a
    x1, y1, z1 = coords_b
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    sz = 1 if z0 < z1 else -1

    # Driving axis is X-axis
    if dx >= dy and dx >= dz:
        err_1 = 2 * dy - dx
        err_2 = 2 * dz - dx
        while x0 != x1:
            line.append([x0, y0, z0])
            if err_1 > 0:
                y0 += sy
                err_1 -= 2 * dx
            if err_2 > 0:
                z0 += sz
                err_2 -= 2 * dx
            err_1 += 2 * dy
            err_2 += 2 * dz
            x0 += sx
    # Driving axis is Y-axis
    elif dy >= dx and dy >= dz:
        err_1 = 2 * dx - dy
        err_2 = 2 * dz - dy
        while y0 != y1:
            line.append([x0, y0, z0])
            if err_1 > 0:
                x0 += sx
                err_1 -= 2 * dy
            if err_2 > 0:
                z0 += sz
                err_2 -= 2 * dy
            err_1 += 2 * dx
            err_2 += 2 * dz
            y0 += sy
    # Driving axis is Z-axis
    else:
        err_1 = 2 * dy - dz
        err_2 = 2 * dx - dz
        while z0 != z1:
            line.append([x0, y0, z0])
            if err_1 > 0:
                y0 += sy
                err_1 -= 2 * dz
            if err_2 > 0:
                x0 += sx
                err_2 -= 2 * dz
            err_1 += 2 * dy
            err_2 += 2 * dx
            z0 += sz

    line.append([x0, y0, z0])

    return line


def expand_path(path: List[Coords]) -> List[Coords]:
    """
    Given a compressed path, return a new path that has all the segments
    in it interpolated.

    Parameters
    ----------
    path : List[Coords]
        path to expand

    Returns
    -------
    List[Coords]
        expanded path
    """
    expanded: List[Coords] = []
    if len(path) < 2:
        return expanded
    for i in range(len(path) - 1):
        expanded += bresenham(path[i], path[i + 1])
    expanded += [path[:-1]]
    return expanded


def smoothen_path(
    grid: Grid, path: List[Coords], use_raytrace: bool = False
) -> List[List[float]]:
    """
    Given an uncompressed path, return a new path that has less
    turnings and looks more natural.

    Parameters
    ----------
    grid : Grid
        grid
    path : List[Coords]
        path to smoothen
    use_raytrace : bool, optional
        whether to use raytrace, by default False

    Returns
    -------
    List[List[float]]
        smoothened path
    """
    sx, sy, sz = path[0]
    new_path = [[sx, sy, sz]]

    interpolate = raytrace if use_raytrace else bresenham
    last_valid = path[1]
    for coord in path[2:-1]:
        line = interpolate((sx, sy, sz), coord)
        blocked = False
        for test_coord in line[1:]:
            if not grid.walkable(
                int(test_coord[0]), int(test_coord[1]), int(test_coord[2])
            ):
                blocked = True
                break
        if not blocked:
            new_path.append(last_valid)
            sx, sy, sz = last_valid
        last_valid = coord

    new_path.append(path[-1])
    return new_path
