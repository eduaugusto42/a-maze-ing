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
      predecessor: dict[tuple[int, int], tuple[int,int]] = {}
      while queue:
          cell_position: tuple[int, int] = queue[0]
          if cell_position == self.exit:
              break
          cell_current: Cell = self.grid[cell_position[1]][cell_position[0]]
          if cell_current.north == False:
              north = (cell_position[0], cell_position[1] - 1)
              if north not in visited:
                  visited.add(north)
                  predecessor[north] = cell_position
                  queue.append(north)
          if cell_current.south == False:
              south = (cell_position[0], cell_position[1] + 1)
              if south not in visited:
                  visited.add(south)
                  predecessor[south] = cell_position
                  queue.append(south)
          if cell_current.east == False:
              east = (cell_position[0] + 1, cell_position[1])
              if east not in visited:
                  visited.add(east)
                  predecessor[east] = cell_position
                  queue.append(east)
          if cell_current.west == False:
              west = (cell_position[0] - 1, cell_position[1])
              if west not in visited:
                  visited.add(west)
                  predecessor[west] = cell_position
                  queue.append(west)
          queue.pop(0)
      path: list[tuple[int, int]] = []
      current = self.exit
      while current != self.entry:
          path.append(current)
          current = predecessor[current]
      path.append(self.entry)
      path.reverse()
      return path


