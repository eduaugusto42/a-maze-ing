#!/usr/bin/env python3

from .cell import Cell


class Visualizer:
    def __init__(
            self,
            grid_cells: list[list[Cell]],
            entry: tuple[int, int],
            exit: tuple[int, int],
            path: list[tuple[int, int]]
            ) -> None:
        self.grid = grid_cells
        self.entry = entry
        self.exit = exit
        self.path = path

    def display(self) -> None:
        canvas: list[list[str]] = self.render_canvas()

        self.render_42(canvas)
        self.mark_path(canvas)
        self.mark_canvas(canvas, self.entry, "E")
        self.mark_canvas(canvas, self.exit, "X")
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
        pass

    def mark_canvas(
            self, canvas: list[list[str]], spot: tuple[int, int], mark: str
            ) -> None:
        x: int = spot[0] * 4 + 1
        y: int = spot[1] * 2 + 1

        canvas[y][x] = mark

def mark_path(self, canvas: list[list[str]]) -> None:
    for i in range(len(self.path) - 1):
        current = self.path[i]
        next = self.path[i + 1]

        current_x = current[0] * 4 + 1
        current_y = current[1] * 2 + 1
        next_x = next[0] * 4 + 1
        next_y = next[1] * 2 + 1

        if next[1] < current[1]:
            for y in range(next_y, current_y):
                canvas[y][current_x] = "*"

        elif next[0] > current[0]:
            for x in range(current_x, next_x):
                canvas[current_y][x] = "*"

        elif next[1] > current[1]:
            for y in range(current_y, next_y + 1):
                canvas[y][current_x] = "*"

        else:
            for x in range(next_x, current_x + 1):
                canvas[current_y][x] = "*"
