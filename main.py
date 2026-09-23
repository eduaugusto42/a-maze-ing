from amazing.maze_generator import MazeGenerator


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
    maze1 = MazeGenerator(5, 5, 42)
    maze1.generate()
    print_maze(maze1)
    print()
    maze2 = MazeGenerator(5, 5, 42)
    maze2.generate()
    print_maze(maze2)
    print()
    maze3 = MazeGenerator(5, 5, 42)
    maze3.generate()
    print_maze(maze3)
    print()
    maze4 = MazeGenerator(5, 5, 123)
    maze4.generate()
    print_maze(maze4)


if __name__ == "__main__":
    main()

