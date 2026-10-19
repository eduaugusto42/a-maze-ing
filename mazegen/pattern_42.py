"""Draw the mandatory "42" pattern on the maze grid.

The pattern is made of fully closed cells drawn in the middle of the maze.
It is centered whenever possible and moved to another position when the
entry or the exit would be covered by it, so that the maze always keeps a
usable entry, a usable exit and open corridors on the four corners and on
the centre of the board (Subject IV.4).
"""

from .cell import Cell

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5

# The pattern must stay strictly inside the maze, so that the four corners
# of the board remain open corridors.
MIN_WIDTH = PATTERN_WIDTH + 2
MIN_HEIGHT = PATTERN_HEIGHT + 2

# Possible results of stamp_42().
PLACED = "placed"
TOO_SMALL = "too small"
NO_FREE_POSITION = "no free position"


def centre_candidates(width: int, height: int) -> list[tuple[int, int]]:
    """List the cells that may hold the centre of the maze.

    With an odd number of rows or columns the centre is a single cell;
    with an even one there is no cell dead in the middle, so the cells
    around the middle are all accepted.

    Args:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.

    Returns:
        The candidate cells, as (row, column) couples.
    """
    rows = {height // 2} if height % 2 else {height // 2 - 1, height // 2}
    columns = {width // 2} if width % 2 else {width // 2 - 1, width // 2}
    return [(row, column) for row in rows for column in columns]


def corner_cells(width: int, height: int) -> list[tuple[int, int]]:
    """List the four corners of the maze.

    Args:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.

    Returns:
        The corner cells, as (row, column) couples.
    """
    return [
        (0, 0),
        (0, width - 1),
        (height - 1, 0),
        (height - 1, width - 1),
    ]


def pattern_cells(start_x: int, start_y: int) -> list[tuple[int, int]]:
    """List the cells covered by the pattern at the given position.

    Only the cells that draw the glyphs are covered: the holes of the "4"
    and of the "2" stay open and remain part of the maze.

    Args:
        start_x: Index of the column of the top-left cell of the pattern.
        start_y: Index of the row of the top-left cell of the pattern.

    Returns:
        The covered cells, as (row, column) couples.
    """
    cells: list[tuple[int, int]] = []
    for y in range(PATTERN_HEIGHT):
        for x in range(PATTERN_WIDTH):
            if PATTERN_42[y][x] == 1:
                cells.append((start_y + y, start_x + x))
    return cells


def candidate_positions(width: int, height: int) -> list[tuple[int, int]]:
    """List the positions where the pattern could be drawn, best first.

    Only the positions that keep the pattern strictly inside the maze are
    returned, so that the four corners of the board stay open corridors.
    The centered position comes first and the others are sorted by their
    distance to it.

    Args:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.

    Returns:
        The candidate positions, as (start_x, start_y) couples.
    """
    center_x = (width - PATTERN_WIDTH) // 2
    center_y = (height - PATTERN_HEIGHT) // 2
    positions = [
        (start_x, start_y)
        for start_y in range(1, height - PATTERN_HEIGHT)
        for start_x in range(1, width - PATTERN_WIDTH)
    ]
    positions.sort(
        key=lambda position: (
            abs(position[0] - center_x) + abs(position[1] - center_y),
            position[1],
            position[0],
        )
    )
    return positions


def is_free_position(
    width: int,
    height: int,
    start_x: int,
    start_y: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> bool:
    """Tell whether the pattern can be drawn at the given position.

    The position is refused when the pattern would cover the entry, the
    exit, one of the four corners of the board, or every cell that may
    hold the centre of the maze.

    Args:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        start_x: Index of the column of the top-left cell of the pattern.
        start_y: Index of the row of the top-left cell of the pattern.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.

    Returns:
        True if the pattern can be drawn at this position.
    """
    cells = pattern_cells(start_x, start_y)
    entry_cell = (entry[1], entry[0])
    exit_cell = (exit[1], exit[0])
    if entry_cell in cells or exit_cell in cells:
        return False
    for corner in corner_cells(width, height):
        if corner in cells:
            return False
    centre = centre_candidates(width, height)
    return any(cell not in cells for cell in centre)


def stamp_42(
    grid: list[list[Cell]],
    width: int,
    height: int,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> str:
    """Draw the mandatory "42" pattern on the grid.

    The pattern is made of fully closed cells, drawn in the middle of the
    maze. Those cells are marked as blocked, which prevents the
    generation algorithms from opening any of their walls and from using
    them as a passage.

    The pattern is only drawn when the maze is large enough and when a
    position is found where it covers neither the entry nor the exit nor
    the four corners nor the whole centre of the board. When it cannot be
    drawn the maze is left without it, and the reason is returned instead
    of raising, so that the generation can go on.

    Args:
        grid: The maze grid, as a list of rows of Cell objects.
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.

    Returns:
        PLACED when the pattern was drawn, TOO_SMALL when the maze is too
        small to hold it and NO_FREE_POSITION when every position was
        refused.
    """
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return TOO_SMALL
    for start_x, start_y in candidate_positions(width, height):
        if not is_free_position(width, height, start_x, start_y, entry, exit):
            continue
        for row, column in pattern_cells(start_x, start_y):
            grid[row][column].blocked = True
        return PLACED
    return NO_FREE_POSITION
