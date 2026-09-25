from config import Config
from .cell import Cell
from .perfect_maze import generate_perfect
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

    def create_grid(self) -> None:
        self.grid_cells = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                cell = Cell()
                row.append(cell)
            self.grid_cells.append(row)

    def generate(self) -> None:
        self.create_grid()
        stamp_42(
            self.grid_cells,
            self.width,
            self.height,
            self.entry,
            self.exit,
        )
        if self.perfect:
            generate_perfect(
                self.grid_cells,
                self.width,
                self.height,
                self.entry,
                self.random,
            )