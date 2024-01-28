# Generate HTML documentation with Sphinx
docs-html:
	sphinx-apidoc -f -e -M -o docs/ pathfinding3d/
	sphinx-build -b html docs docs/_build
	cp -r docs/additional_resources/* docs/_build/