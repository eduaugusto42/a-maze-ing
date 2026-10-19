"""A reusable maze generator.

This package is the reusable module of the A-Maze-ing project (Chapter VI
of the subject). It generates a maze, exposes its structure and finds the
shortest path between its entry and its exit, so that it can be reused
by another project without depending on the command line interface.

The package is installed with pip::

    pip install mazegen

Example:
    >>> from mazegen import MazeGenerator, Solver
    >>> generator = MazeGenerator(width=20, height=15,
    ...                          entry=(0, 0), exit=(19, 14), seed=42)
    >>> generator.generate()
    >>> solver = Solver(generator.grid_cells, 20, 15, (0, 0), (19, 14))
    >>> path = solver.solve()
    >>> path[0], path[-1]
    ((0, 0), (19, 14))
"""

from .cell import Cell
from .maze_generator import MazeGenerator
from .solver import Solver
from .visualizer import Visualizer

__all__ = ["Cell", "MazeGenerator", "Solver", "Visualizer"]
