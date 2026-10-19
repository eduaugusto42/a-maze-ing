#!/usr/bin/env python3
"""The terminal renderer.

Draws the maze as ASCII art: the walls, the entry, the exit, the
solution path and the "42" pattern.
"""


from .cell import Cell


class Visualizer:
    """Render a maze as ASCII art in the terminal.

    The maze is drawn on a character canvas: the walls are made of "+",
    "-" and "|", the cells of the "42" pattern are drawn as "#", the entry
    is marked with an "E", the exit with an "X" and the solution path with
    "*". The walls are finally painted with an ANSI colour.

    Attributes:
        grid: The maze grid, as a list of rows of Cell objects.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.
        path: The solution path, as the list of the cells to go through.
        show: True to draw the solution path, False to hide it.
        color: Index of the colour used to paint the walls.
    """

    def __init__(
            self,
            grid_cells: list[list[Cell]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            path: list[tuple[int, int]],
            show_path: bool,
            wall_color: int
            ) -> None:
        """Create a visualizer for the given maze.

        Args:
            grid_cells: The maze grid, as a list of rows of Cell objects.
            entry: Coordinates (x, y) of the entrance cell.
            exit: Coordinates (x, y) of the exit cell.
            path: The solution path, as the list of the cells to go through.
            show_path: True to draw the solution path, False to hide it.
            wall_color: Index of the colour used to paint the walls.
        """
        self.grid = grid_cells
        self.entry = entry
        self.exit = exit
        self.path = path
        self.show = show_path
        self.color = wall_color

    def display(self) -> None:
        """Draw the maze on the standard output."""
        canvas: list[list[str]] = self.render_canvas()

        self.render_42(canvas)
        if self.show:
            self.mark_path(canvas)
        self.mark_canvas(canvas, self.entry, "E")
        self.mark_canvas(canvas, self.exit, "X")
        self.paint_walls(canvas)
        print("\n".join("".join(line) for line in canvas))

    def render_canvas(self) -> list[list[str]]:
        """Draw the walls of the maze on a character canvas.

        Returns:
            The canvas, as a list of rows of characters.
        """
        canvas: list[list[str]] = []

        for row in self.grid:
            line = "+"
            for cell in row:
                if cell.north:
                    line += "---+"
                else:
                    line += "   +"
            canvas.append(list(line))
            line = "|"
            for cell in row:
                if cell.east:
                    line += "   |"
                else:
                    line += "    "
            canvas.append(list(line))
        line = "+" + ("---+" * len(self.grid[0]))
        canvas.append(list(line))
        return canvas

    def render_42(self, canvas: list[list[str]]) -> None:
        """Draw the cells of the "42" pattern on the canvas.

        Args:
            canvas: The canvas to draw on, modified in place.
        """
        for row in self.grid:
            for cell in row:
                if cell.blocked:
                    x: int = cell.column * 4 + 1
                    y: int = cell.row * 2 + 1
                    canvas[y][x] = "#"
                    canvas[y][x + 1] = "#"
                    canvas[y][x + 2] = "#"

    def mark_canvas(
            self, canvas: list[list[str]], spot: tuple[int, int], mark: str
            ) -> None:
        """Write a single character at the centre of a cell.

        Args:
            canvas: The canvas to draw on, modified in place.
            spot: Coordinates (x, y) of the cell to mark.
            mark: The character to write.
        """
        x: int = spot[0] * 4 + 2
        y: int = spot[1] * 2 + 1

        canvas[y][x] = mark

    def mark_path(self, canvas: list[list[str]]) -> None:
        """Draw the solution path on the canvas.

        Args:
            canvas: The canvas to draw on, modified in place.
        """
        for i in range(len(self.path) - 1):
            current = self.path[i]
            next = self.path[i + 1]

            current_x = current[0] * 4 + 2
            current_y = current[1] * 2 + 1
            next_x = next[0] * 4 + 2
            next_y = next[1] * 2 + 1

            if next[1] < current[1]:
                for y in range(next_y, current_y):
                    canvas[y + 1][current_x] = "*"

            elif next[0] > current[0]:
                for x in range(current_x, next_x):
                    canvas[current_y][x] = "*"

            elif next[1] > current[1]:
                for y in range(current_y, next_y + 1):
                    canvas[y][current_x] = "*"

            else:
                for x in range(next_x, current_x + 1):
                    canvas[current_y][x] = "*"

    def paint_walls(self, canvas: list[list[str]]) -> None:
        """Colour the walls of the canvas with ANSI escape codes.

        The walls get the colour chosen by the ``color`` attribute, while
        the cells of the "42" pattern always get their own colour.

        Args:
            canvas: The canvas to paint, modified in place.
        """
        colors: list[str] = ["\033[96m", "\033[93m", "\033[1;34m"]
        walls: set[str] = {"+", "-", "|", "#"}
        chosen: str = colors[self.color % len(colors)]
        reset: str = "\033[0m"

        for i, row in enumerate(canvas):
            for j, ch in enumerate(row):
                if ch in walls:
                    if ch == "#":
                        canvas[i][j] = f"\033[95m{ch}{reset}"
                    else:
                        canvas[i][j] = f"{chosen}{ch}{reset}"

    def update(
            self,
            grid_cells: list[list[Cell]],
            path: list[tuple[int, int]],
            ) -> None:
        """Replace the maze and its path, for a newly generated maze.

        The entry, the exit and the display options are left untouched, so
        that the choices made by the user survive a regeneration.

        Args:
            grid_cells: The new maze grid.
            path: The new solution path.
        """
        self.grid = grid_cells
        self.path = path
