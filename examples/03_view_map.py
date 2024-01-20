# import the necessary packages
import os

import numpy as np

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid, GridNode
from pathfinding3d.finder.a_star import AStarFinder

USE_OPEN3D = True
try:
    # for visualization
    # only py 3.8, 3.9 and 3.10
    import open3d as o3d
except ImportError:
    USE_OPEN3D = False
    print("Open3D is not installed. Please install it using 'pip install open3d'")

# load map
sample_map_path = os.path.join(os.path.dirname(__file__), "sample_map.npy")
matrix = np.load(sample_map_path)

# define start and end points
start_pt = [21, 21, 21]
end_pt = [5, 38, 33]

# create grid representation and start and end nodes
grid = Grid(matrix=matrix)
start = grid.node(*start_pt)
end = grid.node(*end_pt)

# initialize A* finder
finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
path_, runs = finder.find_path(start, end, grid)
path_cost = end.g
print(f"path cost: {path_cost:.4f}, path length: {len(path_)}, runs: {runs}")

path = []
for node in path_:
    if isinstance(node, GridNode):
        path.append([node.x, node.y, node.z])
    elif isinstance(node, tuple):
        path.append([node[0], node[1], node[2]])
print(f"path: {path}")


# visualize path in open3d
if USE_OPEN3D:
    # Find the obstacles and represent in blue
    obstacle_indices = np.where(matrix == 0)
    xyz_pt = np.stack(obstacle_indices, axis=-1).astype(float)
    colors = np.zeros((xyz_pt.shape[0], 3))
    colors[:, 2] = obstacle_indices[2] / np.max(obstacle_indices[2])

    # Prepare start and end colors
    start_color = np.array([[1.0, 0, 0]])  # Red
    end_color = np.array([[0, 1.0, 0]])  # Green
    path_colors = np.full((len(path) - 2, 3), [0.7, 0.7, 0.7])  # Grey for the path

    # Combine points and colors
    xyz_pt = np.concatenate((xyz_pt, [start_pt], [end_pt], path[1:-1]))
    colors = np.concatenate((colors, start_color, end_color, path_colors))

    # Create and visualize the point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz_pt)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=1.0)
    axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=15.0, origin=np.array([-3.0, -3.0, -3.0]))
    o3d.visualization.draw_geometries([axes, voxel_grid], window_name="Voxel Env", width=1024, height=768)
