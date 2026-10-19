"""Entry point of the A-Maze-ing program.

Reads the configuration file, generates the maze, writes it to the
output file and displays it, either once or in an interactive
viewer.
"""

from mazegen.maze_generator import MazeGenerator
from mazegen.pattern_42 import PLACED
from config import parse_config
import sys
from file_output import OutputWriter
from mazegen.solver import Solver
from mazegen.visualizer import Visualizer


def solve_maze(generator: MazeGenerator) -> list[tuple[int, int]]:
    """Return the shortest path of the maze currently held by the generator.

    A new solver is built for every call, because the generator replaces
    the whole grid when it generates a new maze: a solver that was built
    before would still hold the previous grid and would solve it again.

    Args:
        generator: The generator holding the maze to solve.

    Returns:
        The list of the cells of the path, from the entry to the exit.
    """
    solver = Solver(
        grid=generator.grid_cells,
        width=generator.width,
        height=generator.height,
        entry=generator.entry,
        exit=generator.exit,
    )
    return solver.solve()


def write_maze(
    generator: MazeGenerator,
    path: list[tuple[int, int]],
    output_file: str,
) -> None:
    """Write a maze and its solution path to the output file.

    Args:
        generator: The generator holding the maze to write.
        path: The solution path of the maze.
        output_file: Name of the file the maze is written to.
    """
    writer = OutputWriter(
        grid=generator.grid_cells,
        entry=generator.entry,
        exit=generator.exit,
        path=path,
        output_file=output_file,
    )
    writer.write_file()


def run_interactive(
        generator: MazeGenerator,
        visualizer: Visualizer,
        output_file: str,
        ) -> None:
    """Run the interactive maze viewer until the user quits.

    The viewer offers the three interactions required by the subject: it
    generates a new maze, it shows or hides the shortest path and it
    changes the colour of the walls. Every new maze is also written to
    the output file, so that the file always describes what is on screen.

    Args:
        generator: The maze generator, re-run to produce a new maze.
        visualizer: The visualizer, updated and redrawn on every action.
        output_file: Name of the file the maze is written to; it is
            rewritten every time a new maze is generated.
    """
    while True:
        print("\033[2J\033[H", end="")
        visualizer.display()
        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            return

        if choice == "1":
            generator.generate()
            path = solve_maze(generator)
            visualizer.update(generator.grid_cells, path)
            write_maze(generator, path, output_file)
        elif choice == "2":
            visualizer.show = not visualizer.show
        elif choice == "3":
            visualizer.color = (visualizer.color + 1) % 3
        elif choice == "4":
            return


def main(argv: list[str]) -> int:
    """Run the program: read the configuration and generate the maze.

    The maze is generated, the shortest path is computed, the result is
    written to the output file and the maze is drawn in the terminal.
    When the configuration asks for it, the interactive viewer is then
    started, so that the user can generate new mazes and change the way
    they are displayed.

    Args:
        argv: The arguments of the program, the first one being the name
            of the script and the second one the configuration file.

    Returns:
        0 if everything went well, 1 if the configuration is invalid or
        if the maze cannot be generated.
    """

    if len(argv) != 2:
        print(f"Usage: {argv[0]} <config_file>", file=sys.stderr)
        return 1
    try:
        config = parse_config(argv[1])
    except FileNotFoundError:
        print(f"Error: file not found: {argv[1]}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    try:
        maze1 = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
            seed=config.seed,
        )
        maze1.generate()
        if maze1.pattern_42_status != PLACED:
            print(
                f"Error: the \"42\" pattern could not be drawn "
                f"({maze1.pattern_42_status}); it has been omitted from "
                f"the maze.",
                file=sys.stderr,
            )
        path = solve_maze(maze1)
        write_maze(maze1, path, config.output_file)
        visualizer = Visualizer(
            grid_cells=maze1.grid_cells,
            entry=config.entry,
            exit=config.exit,
            path=path,
            show_path=True,
            wall_color=0,
        )
        if config.interactive:
            run_interactive(maze1, visualizer, config.output_file)
        else:
            visualizer.display()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
