"""Writer of the maze output file.

Writes the maze with the hexadecimal wall encoding of the subject,
followed by the entry, the exit and the shortest path.
"""

from mazegen.cell import Cell


class OutputWriter:
    """Write a maze to the output file described by the subject.

    The file holds one hexadecimal digit per cell, row by row, where a set
    bit means a closed wall: bit 0 is North, bit 1 East, bit 2 South and
    bit 3 West. After an empty line come the entry coordinates, the exit
    coordinates and the shortest path, written with the letters N, E, S
    and W.

    Attributes:
        grid: The maze grid, as a list of rows of Cell objects.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.
        path: The solution path, as the list of the cells to go through.
        output_file: Name of the file the maze is written to.
    """

    def __init__(
        self,
        grid: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: list[tuple[int, int]],
        output_file: str,
    ) -> None:
        """Create a writer for the given maze.

        Args:
            grid: The maze grid, as a list of rows of Cell objects.
            entry: Coordinates (x, y) of the entrance cell.
            exit: Coordinates (x, y) of the exit cell.
            path: The solution path, as the list of the cells to go through.
            output_file: Name of the file the maze is written to.
        """
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.path = path
        self.output_file = output_file

    def grid_to_hex(self) -> list[str]:
        """Convert the whole grid into its hexadecimal representation.

        Returns:
            One string of hexadecimal digits per row of the maze.
        """
        result: list[str] = []
        for row in self.grid:
            line: str = ""
            for cell in row:
                line += self.cell_to_hex(cell)
            result.append(line)
        return result

    def cell_to_hex(self, cell: Cell) -> str:
        """Convert a single cell into a hexadecimal digit.

        The four walls of the cell are packed into a nibble, North being
        the least significant bit and West the most significant one.

        Args:
            cell: The cell to convert.

        Returns:
            The hexadecimal digit describing the walls of the cell.
        """
        binary = (
            str(int(cell.west))
            + str(int(cell.south))
            + str(int(cell.east))
            + str(int(cell.north))
        )
        decimal: int = int(binary, 2)
        return format(decimal, "x")

    def path_to_directions(self) -> str:
        """Convert the solution path into a string of directions.

        Returns:
            The path written with the letters N, E, S and W, one letter per
            step from the entry to the exit.
        """
        directions: str = ""
        for i in range(len(self.path) - 1):
            current = self.path[i]
            next_cell = self.path[i + 1]
            x1, y1 = current
            x2, y2 = next_cell
            if x2 == x1 + 1 and y2 == y1:
                directions += "E"
            elif x2 == x1 - 1 and y2 == y1:
                directions += "W"
            elif y2 == y1 + 1 and x2 == x1:
                directions += "S"
            elif y2 == y1 - 1 and x2 == x1:
                directions += "N"
        return directions

    def write_file(self) -> None:
        """Write the maze, the entry, the exit and the path to the file.

        Raises:
            OSError: If the file cannot be written.
        """
        with open(
            self.output_file, "w", encoding="utf-8", newline="\n"
        ) as file:
            list_lines: list[str] = self.grid_to_hex()
            for line in list_lines:
                file.write(f"{line}\n")
            file.write("\n")
            x, y = self.entry
            file.write(f"{x},{y}\n")
            x, y = self.exit
            file.write(f"{x},{y}\n")
            path: str = self.path_to_directions()
            file.write(f"{path}\n")
