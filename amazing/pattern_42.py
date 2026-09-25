from .cell import Cell
import sys

PATTERN_42 = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5


def stamp_42(
    grid: list[list[Cell]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> bool:
    if width < 9 or height < 7:
        print("Error: maze too small for 42.", file=sys.stderr)
        return False
    start_x = (width - PATTERN_WIDTH) // 2
    start_y = (height - PATTERN_HEIGHT) // 2
    for y in range(PATTERN_HEIGHT):
        for x in range(PATTERN_WIDTH):
            if PATTERN_42[y][x] == 1:
                cell_x = start_x + x
                cell_y = start_y + y

                if (cell_x, cell_y) == entry or (cell_x, cell_y) == exit:
                    print(
                        "Error: 42 overlaps entry or exit.",
                        file=sys.stderr,
                    )
                    return False
    for y in range(PATTERN_HEIGHT):
        for x in range(PATTERN_WIDTH):
            if PATTERN_42[y][x] == 1:
                grid[start_y + y][start_x + x].blocked = True
    return True
