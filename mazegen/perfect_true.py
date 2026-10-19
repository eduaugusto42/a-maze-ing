"""The generator of the perfect mazes.

Carves the corridors with the recursive backtracker, so that there
is exactly one path between any two cells of the maze.
"""

from random import Random
from .cell import Cell


class PerfectMaze:
    """Carve a perfect maze with the recursive backtracker algorithm.

    The algorithm walks the grid with a depth-first search, always pushing
    a random unvisited neighbour on a stack and opening the wall between
    the two cells. Every cell is visited exactly once and every pair of
    cells is connected by exactly one path, which is what a perfect maze
    means.

    The blocked cells of the "42" pattern are skipped, so they keep all
    their walls closed and stay isolated from the rest of the maze. The
    holes of the glyphs are normal cells and stay part of the maze.

    Attributes:
        grid: The maze grid, as a list of rows of Cell objects.
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        entry: Coordinates (x, y) of the entrance cell.
        random: The random generator used to choose the next cell.
    """

    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry: tuple[int, int],
        random: Random,
    ) -> None:
        """Create the carver of a perfect maze.

        Args:
            grid: The maze grid, as a list of rows of Cell objects.
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            entry: Coordinates (x, y) of the entrance cell.
            random: The random generator used to choose the next cell.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.random = random

    def generate(self) -> None:
        """Carve the corridors of the maze in place.

        The grid is expected to be filled with closed cells; this method
        only opens the walls of the passages it creates.
        """
        initial_cell: Cell = self.grid[self.entry[1]][self.entry[0]]
        stack: list[Cell] = [initial_cell]
        initial_cell.visited = True
        visited_count = 1
        total_cells = 0
        for row in self.grid:
            for cell in row:
                if not cell.blocked:
                    total_cells += 1
        while visited_count < total_cells:
            current: Cell = stack[-1]
            north = (current.row - 1, current.column)
            south = (current.row + 1, current.column)
            east = (current.row, current.column + 1)
            west = (current.row, current.column - 1)
            directions: list[tuple[str, tuple[int, int]]] = [
                ("north", north),
                ("south", south),
                ("east", east),
                ("west", west)
            ]
            candidates: list[tuple[str, Cell]] = []
            for direction, position in directions:
                if (
                    0 <= position[0] < self.height
                    and 0 <= position[1] < self.width
                ):
                    cell = self.grid[position[0]][position[1]]
                    if not cell.visited and not cell.blocked:
                        candidates.append((direction, cell))
            if candidates:
                chosen = self.random.choice(candidates)
                direction = chosen[0]
                chosen_cell = chosen[1]
                if direction == "north":
                    current.north = False
                    chosen_cell.south = False
                elif direction == "south":
                    current.south = False
                    chosen_cell.north = False
                elif direction == "east":
                    current.east = False
                    chosen_cell.west = False
                elif direction == "west":
                    current.west = False
                    chosen_cell.east = False
                chosen_cell.visited = True
                visited_count += 1
                stack.append(chosen_cell)
            else:
                stack.pop()
