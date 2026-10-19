*This project has been created as part of the 42 curriculum by jcesar-o, eduaugu.*

# A-Maze-ing

## Description

**A-Maze-ing** is a maze generator written in Python. It reads a
configuration file, generates a maze, writes it to a file using the
hexadecimal wall encoding required by the subject, and displays it in the
terminal — interactively, so that new mazes can be generated and the
display can be changed while the program runs.

The goal of the project is to produce two kinds of maze from the same
engine:

- a **perfect maze**, in which there is exactly one path between the entry
  and the exit;
- a **playable board**, directly usable by a Pac-Man-like game, where every
  corridor is reachable, the four corners and the centre are open, and a
  chased player always has an alternative route.

Every maze also contains the mandatory **"42" pattern**, drawn with fully
closed cells, and every maze is **reproducible**: the same seed always
produces the same maze.

The generation logic is not tied to the command line interface. It lives
in a standalone package, **`mazegen`**, that is published as a Python
package and can be installed with `pip` and reused by another project.

Here is what the terminal display looks like (the `*` characters are the
shortest path, `E` the entry, `X` the exit and `#` the "42" pattern):

```text
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |                       |                               |           |
+   +---+---+---+---+---+---+   +---+---+---+   +---+---+   +---+---+---+   +   +
|                       |       |           |   |       |   |           |   |   |
+   +---+---+   +---+---+   +---+   +   +---+   +   +   +---+   +   +---+---+   +
|       |       |               |   |           |   |       |   |       |   |   |
+   +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Instructions

### Requirements

- **Python 3.10** or later (the project uses the `X | Y` type syntax and
  the `list[...]` / `tuple[...]` built-in generics)
- **GNU Make**, to use the shortcuts described below
- A POSIX-like terminal, for the coloured ASCII rendering

The maze generator itself only uses the standard library: it has **no
runtime dependency**. The development tools (linting, type checking,
testing and packaging) are listed in the `install` target of the
Makefile.

### Installation

```bash
git clone https://github.com/eduaugusto42/a-maze-ing.git
cd a-maze-ing
make install
```

`make install` installs `flake8`, `mypy`, `pytest` and the tooling needed
to build the `mazegen` package.

### Usage

The program takes exactly one argument, the configuration file:

```bash
python3 a_maze_ing.py config.txt
```

or, through the Makefile:

```bash
make run                                  # uses config.txt
make run CONFIG=my_own_config.txt         # uses another configuration file
```

It generates the maze, writes it to the output file, and displays it. If
`INTERACTIVE` is enabled in the configuration file — the default — the
interactive viewer is then started:

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

Pressing `1` generates a new maze, `2` shows or hides the shortest path,
`3` rotates the colour of the walls and `4` quits. The program also exits
cleanly when the standard input is closed, so it can be used in a
non-interactive pipeline.

### Makefile targets

| Target | What it does |
|---|---|
| `make help` | Lists every available target |
| `make install` | Installs the development dependencies |
| `make run` | Generates the maze and starts the viewer |
| `make debug` | Runs the program under `pdb` |
| `make clean` | Removes the caches and the build artifacts |
| `make lint` | Runs `flake8 .` and `mypy .` with the flags of the subject |
| `make lint-strict` | Same, with `mypy --strict` |
| `make test` | Runs the test suite |
| `make build` | Builds the `mazegen` package and copies the artifacts to the root |

### Output file format

The maze is written to the file given by `OUTPUT_FILE`, with **one
hexadecimal digit per cell**, one row per line. Each digit encodes the
walls of the cell:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A set bit means the wall is **closed**, an unset bit means it is open.
For example `3` (binary `0011`) means the walls are open to the south and
to the west, and `A` (binary `1010`) means the east and west walls are
closed.

After an empty line, the file holds the entry coordinates, the exit
coordinates and the shortest path between them, written with the letters
`N`, `E`, `S` and `W`:

```text
93955515553955511393
82c513c553845396ac6a
...

0,0
19,14
EEESENEEEEEEEESSSSESESWSSSSSSSSEENESEEE
```

The `maze_analyzer.py` script provided with the subject can be used to
check that the generated file is valid:

```bash
python3 maze_analyzer.py maze.txt
```

## Configuration file

The configuration file is a plain text file holding one `KEY=VALUE` pair
per line. Lines starting with a `#` are comments and are ignored, as are
the empty lines. The spaces around the keys and the values are trimmed.

```ini
# Default configuration of A-Maze-ing
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
INTERACTIVE=True
```

| Key | Mandatory | Type | Description | Default |
|---|---|---|---|---|
| `WIDTH` | yes | integer | Number of cells on the horizontal axis | — |
| `HEIGHT` | yes | integer | Number of cells on the vertical axis | — |
| `ENTRY` | yes | `x,y` | Coordinates of the entrance cell | — |
| `EXIT` | yes | `x,y` | Coordinates of the exit cell | — |
| `OUTPUT_FILE` | yes | string | Name of the file the maze is written to | — |
| `PERFECT` | yes | boolean | `True` for a maze with a single path, `False` for a playable board | — |
| `SEED` | no | integer | Seed of the random generator, for reproducible mazes | a random value |
| `INTERACTIVE` | no | boolean | `True` to start the interactive viewer after the maze is written | `True` |

The booleans are read case-insensitively: `True`, `true`, `1` and `yes`
mean the same thing, and so do `False`, `false`, `0` and `no`.

The entry and the exit must be two **different** cells, inside the
boundaries of the maze. A configuration that does not respect those rules
is rejected with a clear error message, and the program exits with a
non-zero status instead of crashing.

## Maze generation

### The algorithm

The generation relies on the **recursive backtracker**, also known as the
depth-first search maze generation.

A stack is initialised with the entry cell. The algorithm repeatedly
looks at the cell on top of the stack and picks, at random, one of its
unvisited neighbours. The wall between the two cells is opened, the
neighbour is pushed on the stack and the process repeats. When the current
cell has no unvisited neighbour left, it is popped from the stack and the
algorithm backtracks to the previous one. The maze is finished when the
stack is empty.

Because every cell is visited exactly once and exactly one wall is opened
per visit, the corridors form a **spanning tree** of the grid: there is
exactly one path between any two cells, and no loop at all. This is what
a perfect maze is.

The **playable mode** (`PERFECT=False`) starts from that perfect maze and
**braids** it: closed walls between two normal cells are opened, one at a
time, as long as doing so removes a dead-end and does not create a 3×3
open area. The result keeps every corridor reachable, opens the four
corners and the centre of the board, and offers several independent
routes so that a chased player always has a way out — with, ideally, no
dead-end at all.

The "42" pattern is stamped on the grid **before** the corridors are
carved, so that its cells are never visited and keep all their walls
closed. It is centred on the maze; when the entry or the exit would be
covered by it, the pattern is moved to another position. If the maze is
too small to hold it — under 9×7 cells — the pattern is omitted and an
error message is printed on the console, while the maze is still
generated.

### Why this algorithm

- It **guarantees a perfect maze by construction**. Other approaches, such
  as randomly opening walls, have to detect and repair the loops they
  create. The backtracker cannot produce one, because the corridors are a
  spanning tree by definition.
- It is **simple and efficient**: every cell is visited once, so the
  generation runs in linear time and uses linear memory, whatever the size
  of the maze.
- It **produces long winding corridors** rather than a grid of rooms,
  which is what makes a maze interesting to solve.
- It is **easy to seed**: the whole generation only depends on a
  `random.Random` instance, so passing a seed makes the maze perfectly
  reproducible, as the subject requires.
- For the playable mode, **braiding a perfect maze** is the standard way
  to obtain a Pac-Man board: the loops are added exactly where they are
  needed, at the dead-ends, and the "no 3×3 open area" rule is checked
  at every opening so that the corridors never become too wide.

## Reusable module

The generation logic lives in the **`mazegen`** package, which is
independent from the command line interface. The package is built as a
standard Python distribution and published at the root of the repository:

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```

### Installing it

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

The sources needed to rebuild it are also in the repository: run
`make build` (or `python3 -m build`) in a virtual environment to
reproduce the two artifacts.

### Using it

The package exports four objects:

| Object | Role |
|---|---|
| `MazeGenerator` | Generates the maze and exposes its cells |
| `Solver` | Finds the shortest path between the entry and the exit |
| `Cell` | A single cell, with its four walls |
| `Visualizer` | Draws the maze as ASCII art in the terminal |

A basic example:

```python
from mazegen import MazeGenerator, Solver

# Instantiate the generator and pass the custom parameters
generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=False,
    seed=42,
)

# Generate the maze
generator.generate()

# Access the generated structure
rows = generator.grid_cells
print(rows[0][0].north, rows[0][0].east)   # the walls of the first cell

# Access a solution
solver = Solver(generator.grid_cells, 20, 15, (0, 0), (19, 14))
path = solver.solve()
print(path[0], path[-1])                   # ((0, 0), (19, 14))
```

The generator is deterministic: the same seed always produces the same
maze. The `pattern_42_status` attribute tells whether the "42" pattern
could be drawn, and why not when it could not.

Note that the structure exposed by the module is **not** the format of
the output file: the module gives access to the maze itself, as a grid of
`Cell` objects, while the output file uses the hexadecimal encoding of
the subject.

## Resources

### References

- Jamis Buck, *Maze Generation on a Grid* — the reference survey of the
  maze generation algorithms, and the source of the vocabulary used here
  (recursive backtracker, braiding, dead-ends, loops)
  <https://www.jamisbuck.com/maze-generation/>
- Jamis Buck, *Mazes for Programmers* — the same material, in book form
- Michael McCann, *Maze Generation Algorithms* — a detailed comparison of
  the algorithms, with the properties of each one
  <https://www.mazeproblem.com>
- Wikipedia, *Maze generation algorithm* — the overview of the family of
  algorithms
  <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Wikipedia, *Spanning tree* — the graph theory behind the perfect maze
  <https://en.wikipedia.org/wiki/Spanning_tree>
- The `maze_analyzer.py` script provided with the subject, used to check
  the coherence and the properties of the generated mazes
- Python documentation, `typing` and `collections.abc` — for the type
  hints used throughout the project
  <https://docs.python.org/3/library/typing.html>
- PEP 8 and PEP 257 — the coding standard and the docstring conventions
  followed by the project
  <https://peps.python.org/pep-0008/> · <https://peps.python.org/pep-0257/>

### How AI was used

AI assistants were used throughout the project, as a pair of eyes and as
a source of explanations — never as a replacement for the design, which
was made by the team.

| Task | Where it was used |
|---|---|
| **Code review** | Reading the diffs and the whole codebase, checking the implementation against every requirement of the subject, and spotting problems such as variables used outside their scope, an entry point with the wrong name, or a `Makefile` target that silently did nothing |
| **Explanations of the algorithms** | Understanding how the recursive backtracker guarantees a perfect maze, how braiding turns it into a playable board, and the geometry of the "42" pattern — in particular why the centre of the board always stays a free corridor when the pattern is centred |
| **Debugging** | Tracking down a generator that would abort on a small maze, a solver that kept a reference to an outdated grid after a regeneration, and an output file that was never written when the program was interrupted |
| **Docstrings** | Writing the PEP 257 / Google style docstrings of the whole codebase, and checking that the examples they contain actually run |

## Team and project management

### Roles

| Member | Responsibility |
|---|---|
| **jcesar-o** (Julio) | The maze generator and the solver: the recursive backtracker, the braiding of the playable mode, the "42" pattern and the path finding |
| **eduaugu** (Eduardo) | The visualizer, the configuration parser and this README |

### Planning

At the beginning, the work was split by layers: one person took the
algorithm and the other one the parser, each on their own. As the
project progressed, the tasks were distributed more organically: whenever
one of us was free, we took the next piece of the puzzle, and the parts
met in the branches of the repository.

The project went through 31 commits, from the first parser to the
packaging of the `mazegen` module.

### What worked well

Our partnership was good, and we each managed to complete one part of the
project. Splitting the work between the generation and the display let us
work in parallel without stepping on each other, and the fact that the
two parts talk through a small, well-defined interface — the grid of cells
— made them easy to assemble.

### What could be improved

The parts were mostly validated against each other only at the end of the
project, so a few interfaces had to be adjusted late: the name of the
entry point, the behaviour of the "42" pattern on a small maze, and the
interactive viewer. Integrating the two parts more often, with the
interface written down first, would have avoided most of that rework.

### Tools

The project relies on the standard 42 toolchain: **Python 3.10+**,
**GNU Make** for the common tasks, **git** for the versioning, and
**flake8** and **mypy** for the linting and the static type checking,
which the subject requires. **pytest** is used for the unit tests, and
the `maze_analyzer.py` script of the subject to check the generated
mazes. No other specific tooling was needed.

## Advanced features

Beyond the mandatory part, the project implements:

- **An interactive terminal viewer**, with the three interactions required
  by the subject: generating a new maze, showing or hiding the shortest
  path, and changing the colour of the walls. The "42" pattern gets its
  own colour.
- **An `INTERACTIVE` option** in the configuration file, so that the
  program can also run without any interaction — useful in a pipeline or
  in an automated test.
- **A "42" that adapts to the maze**: it is moved when it would cover the
  entry or the exit, and omitted with an error message when the maze is
  too small to hold it — the maze is always generated.
- **A perfectly braided board**, with no dead-end at all, in the
  non-perfect mode. The `maze_analyzer.py` script confirms it with
  `--max-dead-ends 0`.
- **Reproducible mazes**, through the `SEED` option.
- **A pip-installable package**, `mazegen`, built from the sources of the
  repository.

## License

This project is licensed under the [MIT License](LICENSE.md), which
explicitly allows the reuse and the distribution of the maze generator by
the projects that build on it.
