"""The maze generator.

Builds the grid, stamps the mandatory "42" pattern and carves the
corridors, either as a perfect maze or as a playable board.
"""

from .cell import Cell
from .perfect_true import PerfectMaze
from .perfect_false import NonPerfectMaze
from .pattern_42 import PLACED, stamp_42
import random


class MazeGenerator:
    """Generate a maze and expose its cells and its solution.

    This is the reusable entry point of the project. It creates the grid,
    stamps the mandatory "42" pattern and carves the corridors according to
    the requested mode: a perfect maze with a single path between the entry
    and the exit, or a playable board with several independent routes and
    almost no dead-end.

    The "42" pattern is drawn whenever the maze is large enough to hold
    it and whenever a position is found where it covers neither the entry
    nor the exit. When it is omitted, the maze is still generated and
    ``pattern_42_status`` tells the reason.

    The generator is deterministic: the same seed always produces the same
    maze, which makes the mazes reproducible.

    Attributes:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.
        perfect: True for a maze with a single path, False for a playable
            board with several independent routes.
        seed: Seed of the random generator.
        random: The random generator used to carve the maze.
        grid_cells: The generated grid, as a list of rows of Cell objects.
        pattern_42_status: Result of the last generation: PLACED when the
            "42" pattern could be drawn, otherwise the reason why it was
            omitted (TOO_SMALL or NO_FREE_POSITION).

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
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """Create a generator, without generating anything yet.

        Args:
            width: Number of cells on the horizontal axis.
            height: Number of cells on the vertical axis.
            entry: Coordinates (x, y) of the entrance cell.
            exit: Coordinates (x, y) of the exit cell.
            perfect: True for a maze with a single path, False for a
                playable board with several independent routes.
            seed: Seed of the random generator; a random one is drawn
                when it is None.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        if seed is None:
            self.seed = random.randint(0, 2**32 - 1)
        else:
            self.seed = seed
        self.random = random.Random(self.seed)
        self.grid_cells: list[list[Cell]] = []
        self.pattern_42_status: str = PLACED

    def _create_grid(self) -> None:
        """Fill the grid with a fresh set of closed cells.

        Every cell starts with its four walls closed, so the borders of the
        maze are never opened and the generation only has to carve the
        passages between the cells.
        """
        self.grid_cells = []
        for row_index in range(self.height):
            row = []
            for column_index in range(self.width):
                cell = Cell(row_index, column_index)
                row.append(cell)
            self.grid_cells.append(row)

    def generate(self) -> None:
        """Build the maze and store it in ``grid_cells``.

        The grid is created, the "42" pattern is stamped on it and the
        corridors are carved, either as a perfect maze or as a playable
        board. Calling this method twice regenerates the maze from
        scratch, using the same seed.

        The "42" pattern is drawn whenever the maze is large enough and
        whenever a free position is found for it. When it is omitted the
        maze is still generated, and ``pattern_42_status`` tells why.
        """
        self._create_grid()
        self.pattern_42_status = stamp_42(
            self.grid_cells,
            self.width,
            self.height,
            self.entry,
            self.exit,
        )
        if self.perfect:
            perfect_maze = PerfectMaze(
                self.grid_cells,
                self.width,
                self.height,
                self.entry,
                self.random,
            )
            perfect_maze.generate()
        else:
            non_perfect_maze = NonPerfectMaze(
                self.grid_cells,
                self.width,
                self.height,
                self.entry,
                self.random,
            )
            non_perfect_maze.generate()
