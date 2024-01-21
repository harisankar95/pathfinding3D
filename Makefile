# Generate HTML documentation with Sphinx
docs-html:
	sphinx-apidoc -M -o docs/ pathfinding3d/
	sphinx-build -b html docs docs/_build
