from .perfect_true import PerfectMaze
from .cell import Cell
from random import Random


class NonPerfectMaze:
    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry: tuple[int, int],
        random: Random,
    ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.random = random

    def generate(self) -> None:
        perfect_maze = PerfectMaze(
            self.grid,
            self.width,
            self.height,
            self.entry,
            self.random,
        )
        perfect_maze.generate()
        dead_ends: int = self.count_dead_ends()
        while dead_ends > 0:
            walls: list[tuple[str, Cell, Cell]] = self.find_closed_walls()
            self.random.shuffle(walls)
            opened_wall = False
            for direction, cell_a, cell_b in walls:
                if not self.can_open_wall(direction, cell_a, cell_b):
                    continue
                new_dead_ends = self.count_dead_ends()
                if new_dead_ends < dead_ends:
                    dead_ends = new_dead_ends
                    opened_wall = True
                    break
                if direction == "east":
                    cell_a.east = True
                    cell_b.west = True
                else:
                    cell_a.south = True
                    cell_b.north = True
            if not opened_wall:
                break

    def count_dead_ends(self) -> int:
        dead_ends = 0
        for row in range(self.height):
            for column in range(self.width):
                if self.is_real_dead_end(row, column):
                    dead_ends += 1
        return dead_ends

    def is_real_dead_end(self, row: int, column: int) -> bool:
        current = self.grid[row][column]
        if current.blocked:
            return False
        open_passages = sum(
            not wall
            for wall in (
                current.north,
                current.east,
                current.south,
                current.west,
            )
        )
        if open_passages != 1:
            return False
        directions = [
            ("north", -1, 0, "south"),
            ("east", 0, 1, "west"),
            ("south", 1, 0, "north"),
            ("west", 0, -1, "east"),
        ]
        for wall, row_offset, col_offset, opposite_wall in directions:
            if not getattr(current, wall):
                continue
            neighbor_row = row + row_offset
            neighbor_col = column + col_offset
            if not (
                0 <= neighbor_row < self.height
                and 0 <= neighbor_col < self.width
            ):
                continue
            neighbor = self.grid[neighbor_row][neighbor_col]
            if not neighbor.blocked:
                return True
        return False

    def find_closed_walls(
        self,
    ) -> list[tuple[str, Cell, Cell]]:
        walls: list[tuple[str, Cell, Cell]] = []
        for row in range(self.height):
            for column in range(self.width):
                current = self.grid[row][column]
                if column < self.width - 1:
                    right = self.grid[row][column + 1]
                    if (
                        current.east
                        and not current.blocked
                        and not right.blocked
                    ):
                        walls.append(("east", current, right))
                if row < self.height - 1:
                    below = self.grid[row + 1][column]
                    if (
                        current.south
                        and not current.blocked
                        and not below.blocked
                    ):
                        walls.append(("south", current, below))
        return walls

    def can_open_wall(
        self,
        direction: str,
        cell_a: Cell,
        cell_b: Cell,
    ) -> bool:
        if direction == "east":
            cell_a.east = False
            cell_b.west = False

            start_row = max(0, cell_a.row - 2)
            end_row = min(self.height - 3, cell_a.row)
            start_column = max(0, cell_a.column - 1)
            end_column = min(self.width - 3, cell_a.column)

        else:
            cell_a.south = False
            cell_b.north = False

            start_row = max(0, cell_a.row - 1)
            end_row = min(self.height - 3, cell_a.row)
            start_column = max(0, cell_a.column - 2)
            end_column = min(self.width - 3, cell_a.column)

        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                if self.is_open_3x3(row, column):
                    if direction == "east":
                        cell_a.east = True
                        cell_b.west = True
                    else:
                        cell_a.south = True
                        cell_b.north = True
                    return False
        return True

    def is_open_3x3(self, row: int, column: int) -> bool:
        top_left = self.grid[row][column]
        top_middle = self.grid[row][column + 1]
        top_right = self.grid[row][column + 2]
        middle_left = self.grid[row + 1][column]
        center = self.grid[row + 1][column + 1]
        middle_right = self.grid[row + 1][column + 2]
        bottom_left = self.grid[row + 2][column]
        bottom_middle = self.grid[row + 2][column + 1]
        bottom_right = self.grid[row + 2][column + 2]
        top_open = (
            self.is_open(top_left, top_middle)
            and self.is_open(top_middle, top_right)
        )
        middle_open = (
            self.is_open(middle_left, center)
            and self.is_open(center, middle_right)
        )
        bottom_open = (
            self.is_open(bottom_left, bottom_middle)
            and self.is_open(bottom_middle, bottom_right)
        )
        left_open = (
            self.is_open(top_left, middle_left)
            and self.is_open(middle_left, bottom_left)
        )
        middle_vertical_open = (
            self.is_open(top_middle, center)
            and self.is_open(center, bottom_middle)
        )
        right_open = (
            self.is_open(top_right, middle_right)
            and self.is_open(middle_right, bottom_right)
        )
        return (
            top_open
            and middle_open
            and bottom_open
            and left_open
            and middle_vertical_open
            and right_open
        )

    def is_open(self, cell_a: Cell, cell_b: Cell) -> bool:
        if (
            cell_b.row == cell_a.row
            and cell_b.column == cell_a.column + 1
        ):
            return not cell_a.east
        elif (
            cell_b.row == cell_a.row
            and cell_b.column == cell_a.column - 1
        ):
            return not cell_a.west
        elif (
            cell_b.column == cell_a.column
            and cell_b.row == cell_a.row - 1
        ):
            return not cell_a.north
        elif (
            cell_b.column == cell_a.column
            and cell_b.row == cell_a.row + 1
        ):
            return not cell_a.south
        return False
