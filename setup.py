#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# read the version from version.txt
with open(os.path.join("pathfinding3d", "version.txt"), encoding="utf-8") as file_handler:
    __version__ = file_handler.read().strip()

setup(
    name="pathfinding3d",
    description="Pathfinding algorithms in 3D (based on python-pathfinding)",
    url="https://github.com/harisankar95/python-pathfinding-3D",
    version=__version__,
    license="MIT",
    author="Harisankar Babu",
    keywords=["pathfinding", "python"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=[package for package in find_packages() if package.startswith("pathfinding3d")],
    package_data={"pathfinding3d": ["version.txt"]},
    install_requires=["numpy"],
    tests_require=[
        "numpy",
        "pytest",
        "coverage",
        "sphinx<=6.2.1",
        "sphinx_rtd_theme",
        "sphinx-autodoc-typehints",
        "sphinx-copybutton",
        "sphinx-prompt",
        "sphinx-notfound-page",
        "sphinx-version-warning",
    ],
    min_python_version="3.8",
)
