from amazing.maze_generator import MazeGenerator
from config import parse_config
import sys
from file_output import OutputWriter
from amazing.solver import Solver
from amazing.visualizer import Visualizer


def main(argv: list[str]) -> int:
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
        solver = Solver(
            grid=maze1.grid_cells,
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
        )
        path = solver.solve()
        writer = OutputWriter(
            grid=maze1.grid_cells,
            entry=config.entry,
            exit=config.exit,
            path=path,
            output_file=config.output_file,
        )
        writer.write_file()
        visualizer = Visualizer(
            grid_cells=maze1.grid_cells,
            entry=config.entry,
            exit=config.exit,
            path=path,
            show_path=True,
            wall_color=0,
        )
        visualizer.display()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
