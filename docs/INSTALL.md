# Installation

## Requirements

- python - 3.8 or higher
- numpy
- plotly (optional, for visualization)

## PyPI

The package is available on pypi, so you can install it with pip:

```bash
pip install pathfinding3d
```

If you want to use the visualization feature, you can install the package with the `vis` extra which includes the `plotly` library:

```bash
pip install pathfinding3d[vis]
```

## For development purposes please use editable mode

```bash
git clone https://github.com/harisankar95/pathfinding3D
cd pathfinding3D
pip install -e .[dev]
git checkout -b <branch_name>
```
