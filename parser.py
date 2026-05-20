# ****************************************************************************
#
#    a_maze_ing.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Parses and validates the maze configuration file (KEY=VALUE),
#                 ensuring correct types and required parameters before
#                 execution.
#
#    Created: 2026/04/22
#
# ****************************************************************************

# TODO adicionar docstrings
from exceptions import ConfigError, MazeError


class Parser:
    def __init__(self, file_name: str = "config.txt"):
        self.file_name = file_name
        self.width: (int | None) = None
        self.height: (int | None) = None
        self.entry: (tuple[int, int] | None) = None
        self.exit: (tuple[int, int] | None) = None
        self.output_file: (str | None) = None
        self.perfect: (bool | None) = None
        self.seed: (int | None) = None
        self.algorithm = "BFS"

        self._read_file()

    def _read_file(self) -> None:
        errors: list[ConfigError] = []
        try:
            with open(self.file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        self._parse_line(line)
                    except ConfigError as e:
                        errors.append(e)

        except FileNotFoundError:
            raise ConfigError.missing_file(f"[FILE] `{self.file_name}`")

        try:
            self._validate_required_fields()
        except ConfigError as e:
            errors.insert(0, e)

        if errors:
            raise ConfigError.aggregate(errors)

    def _parse_line(self, line: str) -> None:
        key, _, value = line.partition("=")

        if key == "WIDTH":
            try:
                self.width = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int(f"[{key}]") from e

            if self.width <= 0:
                raise ConfigError.invalid_bound(f"[{key}]")

        elif key == "HEIGHT":
            try:
                self.height = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("[HEIGHT]") from e

            if self.height <= 0:
                raise ConfigError.invalid_bound("[HEIGHT]")

        elif key == "ENTRY":
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())

                self.entry = (x, y)

            except Exception as e:
                raise ConfigError.invalid_coordinates(f"[{key}]") from e

            if self.width is None or self.height is None:
                raise ConfigError(
                    (f"[{key}]"),
                    "WIDTH and HEIGHT must be defined before ENTRY"
                    )
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise ConfigError.invalid_bound_coordinates(
                    (f"[{key}]"), self.width, self.height
                    )

        elif key == "EXIT":
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                self.exit = (x, y)
            except Exception as e:
                raise ConfigError.invalid_coordinates(f"[{key}]") from e

            if self.width is None or self.height is None:
                raise ConfigError(
                    (f"[{key}]"),
                    "WIDTH and HEIGHT must be defined before EXIT"
                    )
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise ConfigError.invalid_bound_coordinates(
                    (f"[{key}]"), self.width, self.height
                    )
            if self.exit == self.entry:
                raise MazeError("Entry and exit must be different")

        elif key == "OUTPUT_FILE":
            if not value:
                raise ConfigError(f"[{key}]", "cannot be empty")
            self.output_file = value

        elif key == "PERFECT":
            if value == "True":
                self.perfect = True
            elif value == "False":
                self.perfect = False
            else:
                raise ConfigError(f"[{key}]", "must be True or False")

        elif key == "SEED":
            if value == "None":
                pass
            else:
                try:
                    self.seed = int(value)
                except ValueError as e:
                    raise ConfigError.invalid_int(f"[{key}]") from e

        else:
            raise ConfigError("[" + key + "]", "unknown parameter")

    def _validate_required_fields(self) -> None:
        if self.width is None:
            raise ConfigError.missing_field("[WIDTH]")

        if self.height is None:
            raise ConfigError.missing_field("[HEIGHT]")

        if self.entry is None:
            raise ConfigError.missing_field("[ENTRY]")

        if self.exit is None:
            raise ConfigError.missing_field("[EXIT]")

        if self.output_file is None:
            raise ConfigError.missing_field("[OUTPUT_FILE]")

        if self.perfect is None:
            raise ConfigError.missing_field("[PERFECT]")
