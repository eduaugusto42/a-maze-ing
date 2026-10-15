#!/usr/bin/env python3

from .cell import Cell


class Visualizer:
    def __init__(
            self,
            grid_cells: list[list[Cell]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            path: list[tuple[int, int]],
            show_path: bool,
            wall_color: int
            ) -> None:
        self.grid = grid_cells
        self.entry = entry
        self.exit = exit
        self.path = path
        self.show = show_path
        self.color = wall_color

    def display(self) -> None:
        canvas: list[list[str]] = self.render_canvas()

        self.render_42(canvas)
        if self.show:
            self.mark_path(canvas)
        self.mark_canvas(canvas, self.entry, "E")
        self.mark_canvas(canvas, self.exit, "X")
        self.paint_walls(canvas)
        print("\n".join("".join(line) for line in canvas))

    def render_canvas(self) -> list[list[str]]:
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
        x: int = spot[0] * 4 + 2
        y: int = spot[1] * 2 + 1

        canvas[y][x] = mark

    def mark_path(self, canvas: list[list[str]]) -> None:
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
        colors: list[str] = ["\033[96m", "\033[93m", "\033[1;34m"]
        walls: set[str] = {"+", "-", "|", "#"}
        chosen: str = colors[self.color % len(colors)]
        reset: str = "\033[0m"

        for i, row in enumerate(canvas):
            for j, ch in enumerate(row):
                if ch in walls:
                    if ch == "#":
                        canvas[i][j] = f"\033[95m{ch}{reset}"
                    canvas[i][j] = f"{chosen}{ch}{reset}"
