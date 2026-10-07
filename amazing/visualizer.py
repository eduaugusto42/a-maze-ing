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
        self.mark_canvas(canvas, self.entry, "E")
        self.mark_canvas(canvas, self.exit, "X")
        self.mark_path(canvas)
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
        pass

    def mark_path(self, canvas: list[list[str]]) -> None:
        pass
