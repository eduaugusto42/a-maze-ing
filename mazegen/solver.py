"""The shortest path solver.

Walks the grid with a breadth-first search and returns the cells of
the shortest path between the entry and the exit.
"""

from .cell import Cell


class Solver:
    """Find the shortest path between the entry and the exit of a maze.

    The solver walks the grid with a breadth-first search, so the path it
    returns is always a shortest one, expressed as the list of the cells
    to go through, from the entry to the exit.

    Attributes:
        grid: The maze grid, as a list of rows of Cell objects.
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.

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

    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Create a solver for the given maze.

        Args:
            grid: The maze grid, as a list of rows of Cell objects.
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            entry: Coordinates (x, y) of the entrance cell.
            exit: Coordinates (x, y) of the exit cell.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

    def solve(self) -> list[tuple[int, int]]:
        """Compute the shortest path from the entry to the exit.

        Returns:
            The list of the cells of the path, from the entry to the exit,
            both included.

        Raises:
            ValueError: If the exit cannot be reached from the entry.
        """
        queue: list[tuple[int, int]] = [self.entry]
        visited: set[tuple[int, int]] = {self.entry}
        predecessor: dict[tuple[int, int], tuple[int, int]] = {}
        while queue:
            cell_position: tuple[int, int] = queue[0]
            if cell_position == self.exit:
                break
            cell_current: Cell = self.grid[cell_position[1]][cell_position[0]]
            for neighbor in self._open_neighbors(cell_current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    predecessor[neighbor] = cell_position
                    queue.append(neighbor)
            queue.pop(0)
        if self.exit not in visited:
            raise ValueError("Error: exit unreachable from entry.")
        path: list[tuple[int, int]] = []
        current = self.exit
        while current != self.entry:
            path.append(current)
            current = predecessor[current]
        path.append(self.entry)
        path.reverse()
        return path

    def _open_neighbors(self, cell: Cell) -> list[tuple[int, int]]:
        """List the neighbours of a cell that can be reached from it.

        Args:
            cell: The cell to inspect.

        Returns:
            The coordinates (x, y) of the neighbours sharing an open
            passage with the cell.
        """
        neighbors: list[tuple[int, int]] = []
        x, y = cell.column, cell.row
        if not cell.north and y - 1 >= 0:
            neighbors.append((x, y - 1))
        if not cell.south and y + 1 < self.height:
            neighbors.append((x, y + 1))
        if not cell.east and x + 1 < self.width:
            neighbors.append((x + 1, y))
        if not cell.west and x - 1 >= 0:
            neighbors.append((x - 1, y))
        return neighbors
