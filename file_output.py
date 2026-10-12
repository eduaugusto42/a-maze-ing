from amazing.cell import Cell


class OutputWriter:
    def __init__(
        self,
        grid: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: list[tuple[int, int]],
        output_file: str,
    ) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.path = path
        self.output_file = "maze.txt"

    def grid_to_hex(self) -> list[str]:
        result: list[str] = []
        for row in self.grid:
            line: str = ""
            for cell in row:
                line += self.cell_to_hex(cell)
            result.append(line)
        return result

    def cell_to_hex(self, cell: Cell) -> str:
        binary = (
            str(int(cell.west))
            + str(int(cell.south))
            + str(int(cell.east))
            + str(int(cell.north))
        )
        decimal: int = int(binary, 2)
        return format(decimal, "x")

    def path_to_directions(self) -> str:
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
        with open(self.output_file, "w") as file:
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
