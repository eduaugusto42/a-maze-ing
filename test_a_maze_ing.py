"""Unit tests for A-Maze-ing.

These tests are not part of the delivery: the subject only asks for them
to verify the project during the development (Chapter III.3), which is why
they are listed in the .gitignore.

Run them with::

    make test
"""

import subprocess
import sys
from pathlib import Path
from collections import deque

import pytest

from config import parse_config
from file_output import OutputWriter
from mazegen.maze_generator import MazeGenerator
from mazegen.pattern_42 import (
    NO_FREE_POSITION,
    PLACED,
    TOO_SMALL,
    stamp_42,
)
from mazegen.solver import Solver
from mazegen.visualizer import Visualizer

N, E, S, W = 1, 2, 4, 8
STEP = {N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def write_config(tmp_path: Path, **overrides: str) -> str:
    """Write a configuration file and return its path."""
    values = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": str(tmp_path / "maze.txt"),
        "PERFECT": "False",
    }
    values.update(overrides)
    path = tmp_path / "config.txt"
    path.write_text(
        "\n".join(f"{key}={value}" for key, value in values.items()) + "\n"
    )
    return str(path)


def neighbours(
    grid: list[list[int]], cell: tuple[int, int]
) -> list[tuple[int, int]]:
    """List the cells reachable from a cell."""
    rows = len(grid)
    cols = len(grid[0])
    row, column = cell
    result = []
    for side in (N, E, S, W):
        next_row = row + STEP[side][0]
        next_column = column + STEP[side][1]
        if not (0 <= next_row < rows and 0 <= next_column < cols):
            continue
        if not grid[row][column] & side:
            result.append((next_row, next_column))
    return result


def is_open(
    grid: list[list[int]], first: tuple[int, int], second: tuple[int, int]
) -> bool:
    """Tell whether two neighbouring cells share an open passage."""
    delta = (second[0] - first[0], second[1] - first[1])
    side = {(0, 1): E, (0, -1): W, (1, 0): S, (-1, 0): N}[delta]
    return not grid[first[0]][first[1]] & side


def region(
    grid: list[list[int]], start: tuple[int, int]
) -> set[tuple[int, int]]:
    """Return every cell reachable from a start cell."""
    seen = {start}
    queue = deque([start])
    while queue:
        for neighbour in neighbours(grid, queue.popleft()):
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return seen


# --------------------------------------------------------------------------- #
# Configuration parser
# --------------------------------------------------------------------------- #
class TestConfig:
    def test_valid_config(self, tmp_path: Path) -> None:
        config = parse_config(write_config(tmp_path))
        assert config.width == 20
        assert config.height == 15
        assert config.entry == (0, 0)
        assert config.exit == (19, 14)
        assert config.perfect is False
        assert config.interactive is True

    def test_comments_and_blank_lines_are_ignored(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "config.txt"
        path.write_text(
            "# a comment\n"
            "\n"
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=out.txt\n"
            "PERFECT=True\n"
            "\n"
            "# another comment\n"
        )
        config = parse_config(str(path))
        assert config.perfect is True

    def test_spaces_around_keys_and_values(self, tmp_path: Path) -> None:
        path = tmp_path / "config.txt"
        path.write_text(
            "  WIDTH = 20 \nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
            "OUTPUT_FILE=out.txt\nPERFECT=False\n"
        )
        assert parse_config(str(path)).width == 20

    @pytest.mark.parametrize("missing", [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT",
    ])
    def test_missing_mandatory_key(self, tmp_path: Path, missing: str) -> None:
        path = tmp_path / "config.txt"
        path.write_text(
            "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
            "OUTPUT_FILE=out.txt\nPERFECT=False\n"
        )
        content = path.read_text().replace(f"{missing}=", "XXX=")
        path.write_text(content)
        with pytest.raises(ValueError):
            parse_config(str(path))

    def test_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            parse_config(str(tmp_path / "nope.txt"))

    def test_line_without_equal_sign(self, tmp_path: Path) -> None:
        path = tmp_path / "config.txt"
        path.write_text("WIDTH 20\n")
        with pytest.raises(ValueError):
            parse_config(str(path))

    def test_non_integer_width(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, WIDTH="abc"))

    def test_invalid_boolean(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, PERFECT="maybe"))

    @pytest.mark.parametrize("value", ["True", "true", "1", "yes"])
    def test_truthy_booleans(self, tmp_path: Path, value: str) -> None:
        config = parse_config(write_config(tmp_path, PERFECT=value))
        assert config.perfect is True

    @pytest.mark.parametrize("value", ["False", "false", "0", "no"])
    def test_falsy_booleans(self, tmp_path: Path, value: str) -> None:
        config = parse_config(write_config(tmp_path, PERFECT=value))
        assert config.perfect is False

    def test_malformed_coordinates(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, ENTRY="0"))

    def test_entry_outside_the_maze(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, ENTRY="20,0"))

    def test_exit_outside_the_maze(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, EXIT="0,15"))

    def test_entry_and_exit_must_differ(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, EXIT="0,0"))

    def test_negative_size(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError):
            parse_config(write_config(tmp_path, WIDTH="0"))

    def test_seed_is_random_when_absent(self, tmp_path: Path) -> None:
        first = parse_config(write_config(tmp_path)).seed
        second = parse_config(write_config(tmp_path)).seed
        assert isinstance(first, int)
        assert first != second

    def test_seed_is_read_when_present(self, tmp_path: Path) -> None:
        assert parse_config(write_config(tmp_path, SEED="42")).seed == 42


# --------------------------------------------------------------------------- #
# Generator
# --------------------------------------------------------------------------- #
class TestGenerator:
    def test_perfect_maze_has_no_loop(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), perfect=True,
            seed=42,
        )
        generator.generate()
        grid = [[
            (int(cell.north) | int(cell.east) * 2
             | int(cell.south) * 4 | int(cell.west) * 8)
            for cell in row
        ] for row in generator.grid_cells]
        reached = region(grid, (0, 0))
        edges = sum(
            1 for cell in reached for n in neighbours(grid, cell)
            if n in reached and n > cell
        )
        assert edges - len(reached) + 1 == 0

    def test_playable_maze_has_several_routes(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), perfect=False,
            seed=42,
        )
        generator.generate()
        grid = [[
            (int(cell.north) | int(cell.east) * 2
             | int(cell.south) * 4 | int(cell.west) * 8)
            for cell in row
        ] for row in generator.grid_cells]
        reached = region(grid, (0, 0))
        edges = sum(
            1 for cell in reached for n in neighbours(grid, cell)
            if n in reached and n > cell
        )
        assert edges - len(reached) + 1 >= 2

    def test_playable_maze_has_no_dead_end(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), perfect=False,
            seed=42,
        )
        generator.generate()
        grid = [[
            (int(cell.north) | int(cell.east) * 2
             | int(cell.south) * 4 | int(cell.west) * 8)
            for cell in row
        ] for row in generator.grid_cells]
        reached = region(grid, (0, 0))
        for cell in reached:
            if len(neighbours(grid, cell)) != 1:
                continue
            row, column = cell
            for side in (N, E, S, W):
                next_row = row + STEP[side][0]
                next_column = column + STEP[side][1]
                if not (0 <= next_row < 15 and 0 <= next_column < 20):
                    continue
                if grid[row][column] & side:
                    other = grid[next_row][next_column]
                    if other != 15:
                        pytest.fail(f"dead-end found in {cell}")

    def test_same_seed_gives_the_same_maze(self) -> None:
        def build() -> list[list[bool]]:
            generator = MazeGenerator(
                width=20, height=15, entry=(0, 0), exit=(19, 14), seed=7,
            )
            generator.generate()
            return [
                [cell.north, cell.east, cell.south, cell.west]
                for row in generator.grid_cells for cell in row
            ]
        assert build() == build()

    def test_different_seed_gives_a_different_maze(self) -> None:
        def build(seed: int) -> list[list[bool]]:
            generator = MazeGenerator(
                width=20, height=15, entry=(0, 0), exit=(19, 14), seed=seed,
            )
            generator.generate()
            return [
                [cell.north, cell.east, cell.south, cell.west]
                for row in generator.grid_cells for cell in row
            ]
        assert build(1) != build(2)

    def test_borders_are_always_closed(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        for column, cell in enumerate(generator.grid_cells[0]):
            assert cell.north
        for column, cell in enumerate(generator.grid_cells[-1]):
            assert cell.south
        for row in generator.grid_cells:
            assert row[0].west
            assert row[-1].east

    def test_shared_walls_are_coherent(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        for row in generator.grid_cells:
            for column, cell in enumerate(row):
                if column + 1 < len(row):
                    assert cell.east == row[column + 1].west
        for index, row in enumerate(generator.grid_cells):
            if index + 1 < len(generator.grid_cells):
                below = generator.grid_cells[index + 1]
                for column, cell in enumerate(row):
                    assert cell.south == below[column].north

    def test_no_open_3x3_area(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        grid = [[
            (int(cell.north) | int(cell.east) * 2
             | int(cell.south) * 4 | int(cell.west) * 8)
            for cell in row
        ] for row in generator.grid_cells]
        for row in range(13):
            for column in range(18):
                cells = [
                    (row + i, column + j) for i in range(3) for j in range(3)
                ]
                all_open = all(
                    is_open(grid, first, second)
                    for first in cells for second in cells
                    if abs(first[0] - second[0])
                    + abs(first[1] - second[1]) == 1
                )
                assert not all_open, f"open 3x3 area at ({row}, {column})"


# --------------------------------------------------------------------------- #
# The "42" pattern
# --------------------------------------------------------------------------- #
class TestPattern42:
    def test_pattern_is_drawn_on_a_big_enough_maze(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        assert generator.pattern_42_status == PLACED

    def test_pattern_is_omitted_on_a_small_maze(self) -> None:
        generator = MazeGenerator(
            width=5, height=4, entry=(0, 0), exit=(4, 3), seed=42,
        )
        generator.generate()
        assert generator.pattern_42_status == TOO_SMALL
        assert not any(
            cell.blocked for row in generator.grid_cells for cell in row
        )

    def test_pattern_moves_away_from_the_entry(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(10, 7), exit=(19, 14), seed=42,
        )
        generator.generate()
        assert generator.pattern_42_status == PLACED
        blocked = [
            (cell.row, cell.column)
            for row in generator.grid_cells for cell in row if cell.blocked
        ]
        assert (7, 10) not in blocked

    def test_pattern_cells_are_fully_closed(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        for row in generator.grid_cells:
            for cell in row:
                if cell.blocked:
                    assert cell.north and cell.east
                    assert cell.south and cell.west

    def test_stamp_42_reports_the_absence_of_a_position(self) -> None:
        grid = [
            [type("C", (), {
                "row": r, "column": c, "north": True, "east": True,
                "south": True, "west": True, "visited": False,
                "blocked": False,
            })() for c in range(9)]
            for r in range(7)
        ]
        status = stamp_42(grid, 9, 7, (1, 1), (8, 6))
        assert status == NO_FREE_POSITION


# --------------------------------------------------------------------------- #
# Solver
# --------------------------------------------------------------------------- #
class TestSolver:
    def test_path_links_the_entry_to_the_exit(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        assert path[0] == (0, 0)
        assert path[-1] == (19, 14)

    def test_path_only_moves_between_neighbours(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        for first, second in zip(path, path[1:]):
            distance = abs(first[0] - second[0]) + abs(first[1] - second[1])
            assert distance == 1

    def test_path_does_not_cross_a_wall(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        for first, second in zip(path, path[1:]):
            cell = generator.grid_cells[first[1]][first[0]]
            if second[0] > first[0]:
                assert not cell.east
            elif second[0] < first[0]:
                assert not cell.west
            elif second[1] > first[1]:
                assert not cell.south
            else:
                assert not cell.north

    def test_unreachable_exit_raises(self) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        generator.grid_cells[0][0].north = True
        generator.grid_cells[0][0].east = True
        generator.grid_cells[0][0].south = True
        generator.grid_cells[0][0].west = True
        with pytest.raises(ValueError):
            Solver(generator.grid_cells, 9, 7, (0, 0), (8, 6)).solve()


# --------------------------------------------------------------------------- #
# Output writer
# --------------------------------------------------------------------------- #
class TestOutputWriter:
    def test_hexadecimal_encoding(self, tmp_path: Path) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 9, 7, (0, 0), (8, 6)
        ).solve()
        output = tmp_path / "maze.txt"
        OutputWriter(
            grid=generator.grid_cells, entry=(0, 0), exit=(8, 6), path=path,
            output_file=str(output),
        ).write_file()
        lines = output.read_text().split("\n")
        assert len(lines[0]) == 9
        assert all(character in "0123456789abcdef" for character in lines[0])

    def test_footer_holds_entry_exit_and_path(self, tmp_path: Path) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 9, 7, (0, 0), (8, 6)
        ).solve()
        output = tmp_path / "maze.txt"
        OutputWriter(
            grid=generator.grid_cells, entry=(0, 0), exit=(8, 6), path=path,
            output_file=str(output),
        ).write_file()
        lines = output.read_text().split("\n")
        assert lines[7] == ""
        assert lines[8] == "0,0"
        assert lines[9] == "8,6"
        assert all(character in "NESW" for character in lines[10])
        assert len(lines[10]) == len(path) - 1

    def test_every_line_ends_with_a_newline(self, tmp_path: Path) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 9, 7, (0, 0), (8, 6)
        ).solve()
        output = tmp_path / "maze.txt"
        OutputWriter(
            grid=generator.grid_cells, entry=(0, 0), exit=(8, 6), path=path,
            output_file=str(output),
        ).write_file()
        raw = output.read_bytes()
        assert b"\r" not in raw
        assert raw.endswith(b"\n")

    def test_path_directions(self, tmp_path: Path) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 9, 7, (0, 0), (8, 6)
        ).solve()
        output = tmp_path / "maze.txt"
        writer = OutputWriter(
            grid=generator.grid_cells, entry=(0, 0), exit=(8, 6), path=path,
            output_file=str(output),
        )
        assert len(writer.path_to_directions()) == len(path) - 1


# --------------------------------------------------------------------------- #
# Visualizer
# --------------------------------------------------------------------------- #
class TestVisualizer:
    def test_display_draws_the_entry_and_the_exit(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        generator = MazeGenerator(
            width=9, height=7, entry=(0, 0), exit=(8, 6), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 9, 7, (0, 0), (8, 6)
        ).solve()
        Visualizer(
            grid_cells=generator.grid_cells, entry=(0, 0), exit=(8, 6),
            path=path, show_path=True, wall_color=0,
        ).display()
        output = capsys.readouterr().out
        assert "E" in output
        assert "X" in output

    def test_update_replaces_the_maze_and_the_path(self) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        visualizer = Visualizer(
            grid_cells=generator.grid_cells, entry=(0, 0), exit=(19, 14),
            path=path, show_path=True, wall_color=0,
        )
        generator.generate()
        new_path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        visualizer.update(generator.grid_cells, new_path)
        assert visualizer.grid is generator.grid_cells
        assert visualizer.path == new_path

    def test_the_hidden_path_is_not_drawn(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        generator = MazeGenerator(
            width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42,
        )
        generator.generate()
        path = Solver(
            generator.grid_cells, 20, 15, (0, 0), (19, 14)
        ).solve()
        Visualizer(
            grid_cells=generator.grid_cells, entry=(0, 0), exit=(19, 14),
            path=path, show_path=False, wall_color=0,
        ).display()
        assert "*" not in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# End to end
# --------------------------------------------------------------------------- #
class TestProgram:
    def run(
        self, tmp_path: Path, **overrides: str
    ) -> subprocess.CompletedProcess[str]:
        config = write_config(tmp_path, **overrides)
        return subprocess.run(
            [sys.executable, "a_maze_ing.py", config],
            capture_output=True, text=True, timeout=60,
        )

    def test_the_program_generates_a_maze(self, tmp_path: Path) -> None:
        result = self.run(tmp_path)
        assert result.returncode == 0
        assert (tmp_path / "maze.txt").exists()

    def test_the_program_reports_a_missing_file(self, tmp_path: Path) -> None:
        result = subprocess.run(
            [sys.executable, "a_maze_ing.py", str(tmp_path / "nope.txt")],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 1
        assert "not found" in result.stderr

    def test_the_program_reports_a_bad_config(self, tmp_path: Path) -> None:
        result = self.run(tmp_path, WIDTH="abc")
        assert result.returncode == 1
        assert result.stderr

    def test_the_program_needs_one_argument(self) -> None:
        result = subprocess.run(
            [sys.executable, "a_maze_ing.py"],
            capture_output=True, text=True, timeout=60,
        )
        assert result.returncode == 1
        assert "Usage" in result.stderr

    def test_a_small_maze_still_produces_a_file(self, tmp_path: Path) -> None:
        result = self.run(tmp_path, WIDTH="5", HEIGHT="4", EXIT="4,3")
        assert result.returncode == 0
        assert (tmp_path / "maze.txt").exists()
        assert "42" in result.stderr

    def test_the_non_interactive_mode_exits_by_itself(
        self, tmp_path: Path
    ) -> None:
        result = self.run(tmp_path, INTERACTIVE="False")
        assert result.returncode == 0
        assert (tmp_path / "maze.txt").exists()

    def test_the_interactive_mode_exits_when_stdin_is_closed(
        self, tmp_path: Path
    ) -> None:
        config = write_config(tmp_path, INTERACTIVE="True")
        result = subprocess.run(
            [sys.executable, "a_maze_ing.py", config],
            capture_output=True, text=True, timeout=60,
            stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0
        assert (tmp_path / "maze.txt").exists()

    def test_the_same_seed_gives_the_same_file(self, tmp_path: Path) -> None:
        self.run(tmp_path, SEED="42")
        first = (tmp_path / "maze.txt").read_text()
        self.run(tmp_path, SEED="42")
        assert (tmp_path / "maze.txt").read_text() == first
