"""The Cell class.

A single cell of the maze grid, with its four walls and the state
used by the generation algorithms.
"""


class Cell:
    """A single cell of the maze grid.

    A cell holds the four walls that surround it. A wall is ``True`` when it
    is closed and ``False`` when it is open, which is the opposite of the
    usual maze convention but matches the hexadecimal output format of the
    subject, where a set bit means "this wall is closed".

    Attributes:
        row: Index of the row the cell belongs to.
        column: Index of the column the cell belongs to.
        north: True when the northern wall is closed.
        east: True when the eastern wall is closed.
        south: True when the southern wall is closed.
        west: True when the western wall is closed.
        visited: True once the generation algorithm has reached the cell.
        blocked: True for the cells that draw the "42" pattern; they are
            never visited and keep all their walls closed.
    """

    def __init__(self, row: int, column: int) -> None:
        """Create a cell whose four walls are all closed.

        Args:
            row: Index of the row the cell belongs to.
            column: Index of the column the cell belongs to.
        """
        self.row: int = row
        self.column: int = column
        self.north: bool = True
        self.south: bool = True
        self.east: bool = True
        self.west: bool = True
        self.visited: bool = False
        self.blocked: bool = False
