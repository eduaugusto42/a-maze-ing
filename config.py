#!/usr/bin/env python3

import random


class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int


def main() -> None:
    try:
        config = parse_config("config.txt")
        print(vars(config))
    except ValueError as error:
        print(error)


def parse_config(path: str) -> Config:
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    values = {}

    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if line == "" or line[0] == '#':
                continue
            key, value = line.split('=')
            values[key] = value

        for k in keys:
            if k not in values:
                raise ValueError(f"'{k}' not found")
    config = convert_config(values)
    validate_config(config)
    return config


def convert_config(values: dict[str, str]) -> Config:
    config = Config()

    config.width = parse_int(values["WIDTH"], "WIDTH")
    config.height = parse_int(values["HEIGHT"], "HEIGHT")
    config.entry = parse_coordinates(values["ENTRY"], "ENTRY")
    config.exit = parse_coordinates(values["EXIT"], "EXIT")

    config.output_file = values["OUTPUT_FILE"]
    if values["PERFECT"] == "True":
        config.perfect = True
    elif values["PERFECT"] == "False":
        config.perfect = False
    else:
        raise ValueError("Error in PERFECT: invalid boolean")
    if "SEED" in values:
        config.seed = parse_int(values["SEED"], "SEED")
    else:
        config.seed = random.randint(0, 2**32 - 1)

    return config

def parse_int(value: str, entry: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Error in {entry}: {e}") from e

def parse_coordinates(value: str, entry: str) -> tuple[int, int]:
    values = value.split(',')
    if len(values) != 2:
        raise ValueError(
                f"Error in {entry}: expected two coordinates separated by a comma"
                )
    return (parse_int(values[0], entry), parse_int(values[1], entry))

def validate_config(config: Config) -> None:
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
