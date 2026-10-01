from random import Random
from .cell import Cell


class PerfectMaze:
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
