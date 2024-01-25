"""
Visualize the 3D map and the path found by the A* algorithm
Requires open3d for visualization. Install it using `pip install open3d`
"""

# import the necessary packages
import os

import numpy as np

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder

# attempt to import Open3D for visualization
USE_OPEN3D = True
try:
    # for visualization
    # only py 3.8, 3.9 and 3.10
    import open3d as o3d
except ImportError:
    USE_OPEN3D = False
    print("Open3D is not installed. Please install it using 'pip install open3d'")

# load map as a 3D numpy array
# each element in the matrix represents a point in the space:
# 0 indicates an obstacle, 1 indicates free space
sample_map_path = os.path.join(os.path.dirname(__file__), "sample_map.npy")
matrix = np.load(sample_map_path)

# define start and end points as [x, y, z] coordinates
start_pt = [21, 21, 21]
end_pt = [5, 38, 33]

# create grid representation and start and end nodes
grid = Grid(matrix=matrix)
start = grid.node(*start_pt)
end = grid.node(*end_pt)

# initialize A* finder with specified diagonal movement setting
finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

# use the finder to get the path
path, runs = finder.find_path(start, end, grid)

# print results
path_cost = end.g
print(f"path cost: {path_cost:.4f}, path length: {len(path)}, runs: {runs}")

# convert the path to a list of coordinate tuples
path = [p.identifier for p in path]
print(f"path: {path}")


# visualize path in open3d
if USE_OPEN3D:
    # Identifying obstacles and representing them in blue
    obstacle_indices = np.where(matrix == 0)
    xyz_pt = np.stack(obstacle_indices, axis=-1).astype(float)
    colors = np.zeros((xyz_pt.shape[0], 3))
    colors[:, 2] = obstacle_indices[2] / np.max(obstacle_indices[2])

    # Prepare start and end colors
    start_color = np.array([[1.0, 0, 0]])  # Red
    end_color = np.array([[0, 1.0, 0]])  # Green
    path_colors = np.full((len(path) - 2, 3), [0.7, 0.7, 0.7])  # Grey for the path

    # Combine points and colors for visualization
    xyz_pt = np.concatenate((xyz_pt, [start_pt], [end_pt], path[1:-1]))
    colors = np.concatenate((colors, start_color, end_color, path_colors))

    # Create the point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz_pt)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Create the voxel grid from the point cloud
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=1.0)
    axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=15.0, origin=np.array([-3.0, -3.0, -3.0]))

    # Visualize the voxel grid
    o3d.visualization.draw_geometries([axes, voxel_grid], window_name="Voxel Env", width=1024, height=768)
