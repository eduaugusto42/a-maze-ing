from .cell import Cell
import random


class MazeGenerator:
    def __init__(self, height: int, width: int, seed: int | None):
        self.height = height
        self.width = width
        self.random = random.Random(seed)
        self.grid_cells: list[list[Cell]] = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                cell = Cell()
                row.append(cell)
            self.grid_cells.append(row)

    def generate(self) -> None:
        initial_cell: tuple[int, int] = (
            self.random.randint(0, self.height - 1),
            self.random.randint(0, self.width - 1)
        )
        stack: list[tuple[int, int]] = [initial_cell]
        visited_count = 1
        self.grid_cells[initial_cell[0]][initial_cell[1]].visited = True
        while (visited_count < (self.height * self.width)):
            candidates: list[tuple[str, tuple[int, int]]] = []
            cell_current: tuple[int, int] = stack[-1]
            north = (cell_current[0] - 1, cell_current[1])
            south = (cell_current[0] + 1, cell_current[1])
            east = (cell_current[0], cell_current[1] + 1)
            west = (cell_current[0], cell_current[1] - 1)
            directions: list[tuple[str, tuple[int, int]]] = [
                ("north", north),
                ("south", south),
                ("east", east),
                ("west", west)
            ]
            for direction, position in directions:
                if (
                    0 <= position[0] < self.height
                    and 0 <= position[1] < self.width
                ):
                    cell = self.grid_cells[position[0]][position[1]]
                    if not cell.visited:
                        candidates.append((direction, position))
            if candidates:
                chosen = self.random.choice(candidates)
                current = self.grid_cells[cell_current[0]][cell_current[1]]
                chosen_cell = self.grid_cells[chosen[1][0]][chosen[1][1]]
                if chosen[0] == "north":
                    current.north = False
                    chosen_cell.south = False
                elif chosen[0] == "south":
                    current.south = False
                    chosen_cell.north = False
                elif chosen[0] == "east":
                    current.east = False
                    chosen_cell.west = False
                elif chosen[0] == "west":
                    current.west = False
                    chosen_cell.east = False
                chosen_cell.visited = True
                visited_count += 1
                stack.append(chosen[1])
            else:
                stack.pop()
