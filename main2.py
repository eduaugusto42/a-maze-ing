from amazing.maze_generator import MazeGenerator
from amazing.solver import Solver
from config import parse_config
import sys


def print_maze(maze: MazeGenerator) -> None:
    for row in maze.grid_cells:
        for cell in row:
            print("+", end="")
            if cell.north:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        for cell in row:
            if cell.west:
                print("|", end="")
            else:
                print(" ", end="")

            print("   ", end="")

        if row[-1].east:
            print("|")
        else:
            print(" ")

    for cell in maze.grid_cells[-1]:
        print("+", end="")
        if cell.south:
            print("---", end="")
        else:
            print("   ", end="")
    print("+")


def print_solution(
    maze: MazeGenerator,
    path: list[tuple[int, int]],
) -> None:
    path_set = set(path)

    for y, row in enumerate(maze.grid_cells):
        for cell in row:
            print("+", end="")
            if cell.north:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        for x, cell in enumerate(row):
            if cell.west:
                print("|", end="")
            else:
                print(" ", end="")

            position = (x, y)

            if position == maze.entry:
                print(" S ", end="")
            elif position == maze.exit:
                print(" E ", end="")
            elif position in path_set:
                print(" * ", end="")
            else:
                print("   ", end="")

        if row[-1].east:
            print("|")
        else:
            print(" ")

    for cell in maze.grid_cells[-1]:
        print("+", end="")
        if cell.south:
            print("---", end="")
        else:
            print("   ", end="")
    print("+")


def main() -> None:
    config = parse_config(sys.argv[1])

    maze = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        perfect=config.perfect,
        seed=config.seed,
    )

    maze.generate()

    print("=== MAZE ===")
    print_maze(maze)

    solver = Solver(
        grid=maze.grid_cells,
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
    )

    path = solver.solve()

    print()
    print("=== SOLUTION ===")
    print_solution(maze, path)

    print()
    print("=== PATH ===")
    print(path)


if __name__ == "__main__":
    main()