#!/usr/bin/env python3

class Config:
    pass

def main() -> None:
    config = parse_config("config.txt")


def parse_config(path: str) -> Config:
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    values = {}

    with open(path, "r") as file:
        for line in file:
            key, value = line.strip().split('=')
            values[key] = value

        for k in keys:
            if k not in values:
                raise ValueError(f"'{k}' not found")
    config = convert_config(values)
    validate_config(config)
    return config


def convert_config(values: dict) -> Config:
    config = Config()

    config.width = int(values["WIDTH"])
    config.height = int(values["HEIGHT"])

    entry = values["ENTRY"].split(',')
    config.entry = (int(entry[0]), int(entry[1]))

    ext = values["EXIT"].split(',')
    config.exit = (int(ext[0]), int(ext[1]))

    config.output_file = values["OUTPUT_FILE"]
    if values["PERFECT"] == "True":
        config.perfect = True
    elif values["PERFECT"] == "False":
        config.perfect = False
    else:
        raise ValueError("PERFECT invalid")

    return config


def validate_config(config: Config) -> None:
    if config.width <= 0:
        raise ValueError("WIDTH must be greater than 0!")
    if config.height <= 0:
        raise ValueError("HEIGHT must be greater than 0!")

    if not (0 <= config.entry[0] < config.width):
        raise ValueError("ENTRY must be inside WIDTH")
    if not (0 <= config.entry[1] < config.height):
        raise ValueError("ENTRY must be inside HEIGHT")

    if not (0 <= config.exit[0] < config.width):
        raise ValueError("EXIT must be inside WIDTH")
    if not (0 <= config.exit[1] < config.height):
        raise ValueError("EXIT must be inside HEIGHT")

    if (
            config.entry[0] == config.exit[0]
            and config.entry[1] == config.exit[1]
            ):
        raise ValueError("ENTRY must be different from EXIT")

if __name__ == "__main__":
    main()
