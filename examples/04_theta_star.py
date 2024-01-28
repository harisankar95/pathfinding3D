"""
This example shows how Theta* algorithm differs from A* algorithm
Requires plotly for visualization. Install it using `pip install plotly`
"""

import numpy as np
import plotly.graph_objects as go

from pathfinding3d.core.diagonal_movement import DiagonalMovement
from pathfinding3d.core.grid import Grid
from pathfinding3d.finder.a_star import AStarFinder
from pathfinding3d.finder.theta_star import ThetaStarFinder

# Create a 3D numpy array with 0s as obstacles and 1s as walkable paths
matrix = np.ones((10, 10, 10), dtype=np.int8)
# mark the center of the grid as an obstacle
matrix[5, 5, 5] = 0

# Create a grid object from the numpy array
grid = Grid(matrix=matrix)

# Mark the start and end points
start = grid.node(0, 0, 0)
end = grid.node(9, 9, 9)

# Create an instance of the Theta* finder with diagonal movement allowed
finder = ThetaStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

# Path will be a list with all the waypoints as nodes
# Convert it to a list of coordinate tuples
path = [p.identifier for p in path]

print("operations:", runs, "path length:", len(path))
print("path:", path)

# clean up the grid
grid.cleanup()

# Create an instance of the A* finder with diagonal movement allowed
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
astar_path, runs = finder.find_path(start, end, grid)

astar_path = [p.identifier for p in astar_path]

print("AStarFinder operations:", runs, "AStarFinder path length:", len(astar_path))
print("AStarFinder path:", astar_path)


def calculate_path_cost(path):
    cost = 0
    for pt, pt_next in zip(path[:-1], path[1:]):
        dx, dy, dz = pt_next[0] - pt[0], pt_next[1] - pt[1], pt_next[2] - pt[2]
        cost += (dx**2 + dy**2 + dz**2) ** 0.5
    return cost


theta_star_cost = calculate_path_cost(path)
astar_cost = calculate_path_cost(astar_path)

print("ThetaStarFinder path cost:", theta_star_cost, "\nAStarFinder path cost:", astar_cost)

# Create a plotly figure to visualize the path
fig = go.Figure(
    data=[
        go.Scatter3d(
            x=[pt[0] + 0.5 for pt in path],
            y=[pt[1] + 0.5 for pt in path],
            z=[pt[2] + 0.5 for pt in path],
            mode="lines + markers",
            line=dict(color="blue", width=4),
            marker=dict(size=4, color="blue"),
            name="Theta* path",
            hovertext=["Theta* path point"] * len(path),
        ),
        go.Scatter3d(
            x=[pt[0] + 0.5 for pt in astar_path],
            y=[pt[1] + 0.5 for pt in astar_path],
            z=[pt[2] + 0.5 for pt in astar_path],
            mode="lines + markers",
            line=dict(color="red", width=4),
            marker=dict(size=4, color="red"),
            name="A* path",
            hovertext=["A* path point"] * len(astar_path),
        ),
        go.Scatter3d(
            x=[5.5],
            y=[5.5],
            z=[5.5],
            mode="markers",
            marker=dict(color="black", size=7.5),
            name="Obstacle",
            hovertext=["Obstacle point"],
        ),
        go.Scatter3d(
            x=[0.5],
            y=[0.5],
            z=[0.5],
            mode="markers",
            marker=dict(color="green", size=7.5),
            name="Start",
            hovertext=["Start point"],
        ),
        go.Scatter3d(
            x=[9.5],
            y=[9.5],
            z=[9.5],
            mode="markers",
            marker=dict(color="orange", size=7.5),
            name="End",
            hovertext=["End point"],
        ),
    ]
)

# Define the camera position
camera = {
    "up": {"x": 0, "y": 0, "z": 1},
    "center": {"x": 0.1479269806756467, "y": 0.06501594452841505, "z": -0.0907033779622012},
    "eye": {"x": 1.3097359159706334, "y": 0.4710974884501846, "z": 2.095154166796815},
    "projection": {"type": "perspective"},
}

# Update the layout of the figure
fig.update_layout(
    scene=dict(
        xaxis=dict(
            title="x - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, 10],
            dtick=1,
        ),
        yaxis=dict(
            title="y - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, 10],
            dtick=1,
        ),
        zaxis=dict(
            title="z - axis",
            backgroundcolor="white",
            gridcolor="lightgrey",
            showbackground=True,
            zerolinecolor="white",
            range=[0, 10],
            dtick=1,
        ),
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255, 255, 255, 0.7)",
    ),
    title=dict(text="Theta* vs A*"),
    scene_camera=camera,
)

# Save the figure as a html file
# fig.write_html("theta_star.html", full_html=False, include_plotlyjs="cdn")
# Show the figure in a new tab
fig.show()
