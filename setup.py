#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# read the version from version.txt
with open(os.path.join("pathfinding3d", "version.txt"), encoding="utf-8") as file_handler:
    __version__ = file_handler.read().strip()

setup(
    name="pathfinding3d",
    description="Pathfinding algorithms in 3D grids (based on python-pathfinding)",
    url="https://github.com/harisankar95/pathfinding3D",
    version=__version__,
    license="MIT",
    author="Harisankar Babu",
    keywords=["pathfinding", "pathplanning", "python", "3D", "A*", "Dijkstra", "Theta*"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    packages=[package for package in find_packages() if package.startswith("pathfinding3d")],
    package_data={"pathfinding3d": ["version.txt"]},
    install_requires=["numpy"],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "coverage",
            "sphinx<=7.2.6",
            "sphinx_rtd_theme",
            "recommonmark",
            "sphinx-autodoc-typehints",
            "sphinx-copybutton",
            "sphinx-prompt",
            "sphinx-notfound-page",
            "sphinx-autodoc-annotation",
        ]
    },
    tests_require=[
        "pytest",
        "coverage",
    ],
    python_requires=">=3.8",
    platforms=["any"],
)
