#!/usr/bin/env python3

class Config:
    pass

def main() -> None:
    parse_config("config.txt")

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

        return convert_config(values)

def convert_config(values: dict) -> Config:
    config = Config()

    config.width = int(values["WIDTH"])
    config.height = int(values["HEIGHT"])

    entry = tuple(values["ENTRY"].split(','))
    config.entry = (int(entry[0]), int(entry[1]))

    ext = tuple(values["EXIT"].split(','))
    config.exit = (int(ext[0]), int(ext[1]))

    config.output_file = values["OUTPUT_FILE"]
    if values["PERFECT"] == "True":
        config.perfect = True
    elif values["PERFECT"] == "False":
        config.perfect = False
    else:
        raise ValueError("PERFECT invalid")

    return config

if __name__ == "__main__":
    main()
