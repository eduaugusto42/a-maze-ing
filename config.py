#!/usr/bin/env python3
"""Parser of the configuration file.

Reads the KEY=VALUE pairs of the configuration file, converts them
and checks that they describe a maze that can be built.
"""


import random


class Config:
    """The options of a maze generation.

    This object holds everything the configuration file can define. It is
    filled by :func:`parse_config` and then given to the generator, to
    the solver and to the output writer.

    Attributes:
        width: Number of cells on the horizontal axis.
        height: Number of cells on the vertical axis.
        entry: Coordinates (x, y) of the entrance cell.
        exit: Coordinates (x, y) of the exit cell.
        output_file: Name of the file the maze is written to.
        perfect: True for a maze with a single path, False for a playable
            board with several independent routes.
        seed: Seed of the random generator, for reproducible mazes.
        interactive: True to start the interactive viewer once the maze has
            been written, False to only display the maze and stop.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
    interactive: bool


def main() -> None:
    """Print the configuration file of the repository, for a quick check."""
    try:
        config = parse_config("config.txt")
        print(vars(config))
    except ValueError as error:
        print(error)


def parse_config(path: str) -> Config:
    """Read and validate a configuration file.

    The file holds one "KEY=VALUE" pair per line; the lines starting with
    a "#" are comments and are ignored. The mandatory keys are WIDTH,
    HEIGHT, ENTRY, EXIT, OUTPUT_FILE and PERFECT; the optional key SEED
    makes the maze reproducible.

    Args:
        path: Path of the configuration file to read.

    Returns:
        The configuration described by the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a line is malformed, if a mandatory key is missing
            or if a value is invalid.
    """
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    values = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "" or line[0] == '#':
                continue
            if '=' not in line:
                raise ValueError(
                    f"Error: invalid line '{line}' (expected KEY=VALUE)"
                )
            key, value = line.split('=', 1)
            values[key.strip()] = value.strip()

        for k in keys:
            if k not in values:
                raise ValueError(f"'{k}' not found")
    config = convert_config(values)
    validate_config(config)
    return config


def convert_config(values: dict[str, str]) -> Config:
    """Turn the raw key/value pairs of a file into a Config object.

    Args:
        values: The key/value pairs read from the configuration file.

    Returns:
        The configuration described by the pairs.

    Raises:
        ValueError: If a value cannot be converted to the expected type.
    """
    config = Config()

    config.width = parse_int(values["WIDTH"], "WIDTH")
    config.height = parse_int(values["HEIGHT"], "HEIGHT")
    config.entry = parse_coordinates(values["ENTRY"], "ENTRY")
    config.exit = parse_coordinates(values["EXIT"], "EXIT")

    config.output_file = values["OUTPUT_FILE"]
    config.perfect = parse_bool(values["PERFECT"], "PERFECT")
    config.interactive = parse_bool(
        values.get("INTERACTIVE", "True"), "INTERACTIVE"
    )
    if "SEED" in values:
        config.seed = parse_int(values["SEED"], "SEED")
    else:
        config.seed = random.randint(0, 2**32 - 1)

    return config


def parse_int(value: str, entry: str) -> int:
    """Convert a string into an integer.

    Args:
        value: The string to convert.
        entry: Name of the configuration key, used in the error message.

    Returns:
        The converted integer.

    Raises:
        ValueError: If the string is not a valid integer.
    """
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Error in {entry}: {e}") from e


def parse_bool(value: str, entry: str) -> bool:
    """Convert a string into a boolean.

    The value is read case-insensitively, so that "True", "true" and "1"
    all mean the same thing.

    Args:
        value: The string to convert.
        entry: Name of the configuration key, used in the error message.

    Returns:
        The converted boolean.

    Raises:
        ValueError: If the string is not a valid boolean.
    """
    normalized: str = value.strip().lower()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    raise ValueError(f"Error in {entry}: invalid boolean '{value}'")


def parse_coordinates(value: str, entry: str) -> tuple[int, int]:
    """Convert a "x,y" string into a pair of coordinates.

    Args:
        value: The string to convert, such as "0,0".
        entry: Name of the configuration key, used in the error message.

    Returns:
        The coordinates (x, y).

    Raises:
        ValueError: If the string does not hold exactly two coordinates.
    """
    values = value.split(',')
    if len(values) != 2:
        raise ValueError(
                f"Error in {entry}: "
                "expected two coordinates separated by a comma"
                )
    return (parse_int(values[0], entry), parse_int(values[1], entry))


def validate_config(config: Config) -> None:
    """Check that the configuration describes a maze that can be built.

    The size must be positive, the entry and the exit must be inside the
    maze and they must be two different cells.

    Args:
        config: The configuration to check.

    Raises:
        ValueError: If the configuration is not usable.
    """
    if config.width <= 0:
        raise ValueError("Error in WIDTH: must be greater than 0!")
    if config.height <= 0:
        raise ValueError("Error in HEIGHT: must be greater than 0!")

    if not (0 <= config.entry[0] < config.width):
        raise ValueError("Error in ENTRY: must be inside WIDTH")
    if not (0 <= config.entry[1] < config.height):
        raise ValueError("Error in ENTRY: must be inside HEIGHT")

    if not (0 <= config.exit[0] < config.width):
        raise ValueError("Error in EXIT: must be inside WIDTH")
    if not (0 <= config.exit[1] < config.height):
        raise ValueError("Error in EXIT: must be inside HEIGHT")

    if (
            config.entry[0] == config.exit[0]
            and config.entry[1] == config.exit[1]
            ):
        raise ValueError("Error in ENTRY: must be different from EXIT")


if __name__ == "__main__":
    main()
