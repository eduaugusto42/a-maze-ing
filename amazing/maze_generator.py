from .cell import Cell
from .perfect_true import PerfectMaze
from .perfect_false import NonPerfectMaze
from .pattern_42 import stamp_42
import random


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
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

    def _create_grid(self) -> None:
        self.grid_cells = []
        for row_index in range(self.height):
            row = []
            for column_index in range(self.width):
                cell = Cell(row_index, column_index)
                row.append(cell)
            self.grid_cells.append(row)

    def generate(self) -> None:
        self._create_grid()
        stamp_42(
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
