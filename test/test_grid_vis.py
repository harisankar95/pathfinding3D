import warnings

import plotly
import pytest

from pathfinding3d.core.grid import Grid


def test_visualize_without_plotly(mocker):
    """
    Test visualize method when plotly is not installed
    """
    mocker.patch("pathfinding3d.core.grid.USE_PLOTLY", False)
    mocker.patch("warnings.warn")

    grid = Grid(width=3, height=3, depth=3)
    grid.visualize()

    warnings.warn.assert_called_once_with("Plotly is not installed. Please install it to use this feature.")


def test_visualize_with_plotly(mocker):
    """
    Test visualize method when plotly is installed
    """
    mocker.patch("pathfinding3d.core.grid.USE_PLOTLY", True)
    mocker.patch("plotly.graph_objects.Volume")
    mocker.patch("plotly.graph_objects.Scatter3d")
    mocker.patch("plotly.graph_objects.Layout")
    mocker.patch("plotly.graph_objects.Figure")
    mocker.patch("plotly.offline.plot")

    grid = Grid(width=3, height=3, depth=3)
    grid.visualize()

    plotly.graph_objects.Volume.assert_called()
    plotly.graph_objects.Figure.assert_called()


def test_visualize_with_path(mocker):
    """
    Test visualize method with a path
    """
    mocker.patch("pathfinding3d.core.grid.USE_PLOTLY", True)
    mocker.patch("plotly.graph_objects.Volume")
    mocker.patch("plotly.graph_objects.Scatter3d")
    mocker.patch("plotly.graph_objects.Layout")
    mocker.patch("plotly.graph_objects.Figure")
    mocker.patch("plotly.offline.plot")

    grid = Grid(width=3, height=3, depth=3)
    path = [grid.node(0, 0, 0), grid.node(1, 1, 1), grid.node(2, 2, 2)]
    grid.visualize(path=path)

    plotly.graph_objects.Scatter3d.assert_called()
    plotly.graph_objects.Figure.assert_called()
