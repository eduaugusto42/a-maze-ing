from random import Random

from .cell import Cell


def generate_perfect(
    grid: list[list[Cell]],
    width: int,
    height: int,
    entry: tuple[int, int],
    random: Random,
) -> None:
    initial_cell: tuple[int, int] = (
        entry[1],
        entry[0]
    )
    stack: list[tuple[int, int]] = [initial_cell]
    visited_count = 1
    grid[initial_cell[0]][initial_cell[1]].visited = True
    total_cells = 0
    for row in grid:
        for cell in row:
            if not cell.blocked:
                total_cells += 1
    while visited_count < total_cells:
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
                0 <= position[0] < height
                and 0 <= position[1] < width
            ):
                cell = grid[position[0]][position[1]]
                if not cell.visited and not cell.blocked:
                    candidates.append((direction, position))
        if candidates:
            chosen = random.choice(candidates)
            current = grid[cell_current[0]][cell_current[1]]
            chosen_cell = grid[chosen[1][0]][chosen[1][1]]
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