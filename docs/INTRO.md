# Pathfinding3D

[![MIT License](https://img.shields.io/github/license/harisankar95/pathfinding3d)](https://github.com/harisankar95/pathfinding3D/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pathfinding3d)](https://pypi.org/project/pathfinding3d/)

## Introduction

Pathfinding algorithms for python3 froked from [python-pathfinding](https://github.com/brean/python-pathfinding) by [@brean](https://github.com/brean).

Pathfinding3D is a comprehensive library designed for 3D pathfinding applications.

Currently there are 7 path-finders bundled in this library, namely:

- A\*: Versatile and most widely used algorithm.
- Dijkstra: A\* without heuristic.
- Best-First
- Bi-directional A\*: Efficient for large graphs with a known goal.
- Breadth First Search (BFS)
- Iterative Deeping A\* (IDA\*): Memory efficient algorithm for large graphs.
- Minimum Spanning Tree (MSP)
- Theta\*: Almost A\* with path smoothing.

Dijkstra, A\* and Bi-directional A\* take the weight of the fields on the map into account.
Theta\* is a variant of A\* but with any angle of movement allowed.
