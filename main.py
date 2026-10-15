from amazing.maze_generator import MazeGenerator
from config import parse_config
import sys
from file_output import OutputWriter
from amazing.solver import Solver
from amazing.visualizer import Visualizer


def main() -> None:
    config = parse_config(sys.argv[1])
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


if __name__ == "__main__":
    main()
