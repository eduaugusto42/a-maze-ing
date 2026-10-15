from .cell import Cell


class Solver:
    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

    def solve(self) -> list[tuple[int, int]]:
        queue: list[tuple[int, int]] = [self.entry]
        visited: set[tuple[int, int]] = {self.entry}
        predecessor: dict[tuple[int, int], tuple[int, int]] = {}
        while queue:
            cell_position: tuple[int, int] = queue[0]
            if cell_position == self.exit:
                break
            cell_current: Cell = self.grid[cell_position[1]][cell_position[0]]
            for neighbor in self._open_neighbors(cell_current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    predecessor[neighbor] = cell_position
                    queue.append(neighbor)
            queue.pop(0)
        if self.exit not in visited:
            raise ValueError("Error: exit unreachable from entry.")
        path: list[tuple[int, int]] = []
        current = self.exit
        while current != self.entry:
            path.append(current)
            current = predecessor[current]
        path.append(self.entry)
        path.reverse()
        return path

    def _open_neighbors(self, cell: Cell) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        x, y = cell.column, cell.row
        if not cell.north and y - 1 >= 0:
            neighbors.append((x, y - 1))
        if not cell.south and y + 1 < self.height:
            neighbors.append((x, y + 1))
        if not cell.east and x + 1 < self.width:
            neighbors.append((x + 1, y))
        if not cell.west and x - 1 >= 0:
            neighbors.append((x - 1, y))
        return neighbors
