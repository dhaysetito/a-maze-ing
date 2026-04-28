#!/usr/bin/env python3

# ****************************************************************************
#
#    a_maze_ing.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Created: 2026/04/22
#
# ****************************************************************************

from exceptions import ConfigError


class Parser():
    def __init__(self, file_name: str = "config.txt"):
        self.file_name = file_name
        self.widht = 0
        self.height = 0
        self.entry = (0, 0)
        self.exit = (0, 0)
        self.output_file = "maze.txt"
        self.perfect = False
        self.seed = 0
        self.algorithm = "DST"
        self.display_mode = "MLX"

    def read_file(self) -> None:
        errors: list[ConfigError] = []

        with open(self.file_name, "r") as file:
            for line in file:
                if (line[0] == "#"):
                    pass
                else:
                    try:
                        self.parse_line(line.strip())
                    except ConfigError as e:
                        print(f"Caught ConfigError: {e}")
                        errors.append(e)
            if errors:
                return

    def after_substring(self, s: str, sub: str) -> str:
        _, sep, tail = s.partition(sub)
        return tail if sep else ""

    def parse_line(self, line: str) -> None:
        key, _, value = line.partition("=")

        if key == "WIDHT":
            try:
                self.widht = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("WIDTH") from e
        elif key == "HEIGHT":
            try:
                self.height = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("HEIGHT") from e
        elif key == "ENTRY":
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                self.entry = (x, y)
            except Exception as e:
                raise ConfigError.invalid_coordinates("ENTRY") from e
        elif key == "EXIT":
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                self.exit = (x, y)
            except Exception as e:
                raise ConfigError.invalid_coordinates("EXIT") from e
        elif key == "OUTPUT_FILE":
            if not value:
                raise ConfigError("OUTPUT_FILE", "cannot be empty")
            self.output_file = value
        elif key == "PERFECT":
            if value == "True":
                self.perfect = True
            elif value == "False":
                self.perfect = False
            else:
                raise ConfigError("PERFECT", "must be True or False")
        else:
            raise ConfigError(key, "unknown parameter")


if __name__ == "__main__":
    Parser("test.txt").read_file()
