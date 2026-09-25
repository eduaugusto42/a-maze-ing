from amazing.maze_generator import MazeGenerator
from config import parse_config

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


def main() -> None:
    config = parse_config("config.txt")
    maze1 = MazeGenerator(
    width=config.width,
    height=config.height,
    entry=config.entry,
    exit=config.exit,
    perfect=config.perfect,
    seed=config.seed,
)
    maze1.generate()
    print_maze(maze1)
    print()
    for row in maze1.grid_cells:
        print("".join("#" if cell.blocked else "." for cell in row))

if __name__ == "__main__":
    main()

