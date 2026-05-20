# ****************************************************************************
#
#    exceptions.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Custom exception hierarchy used for maze generation,
#                 parsing validation, configuration handling and runtime
#                 error management across the A-Maze-ing project.
#
#    Created: 2026/04/22
#
# ****************************************************************************

class MazeError(Exception):
    def __init__(self, message: str = "Unknown error") -> None:
        super().__init__(message)


class ConfigError(MazeError):
    def __init__(
            self, field: str, message: str = "Unknown config error"
            ) -> None:
        super().__init__(f"{field} {message}")

    @staticmethod
    def missing_file(field: str) -> "ConfigError":
        return ConfigError(field, "is missing")

    @staticmethod
    def missing_field(field: str) -> "ConfigError":
        return ConfigError(field, "is missing")

    @staticmethod
    def invalid_int(field: str) -> "ConfigError":
        return ConfigError(field, "must be an integer")

    @staticmethod
    def invalid_bound(field: str) -> "ConfigError":
        return ConfigError(
            field,
            "out of bounds: expected greater than 0"
        )

    @staticmethod
    def invalid_coordinates(field: str) -> "ConfigError":
        return ConfigError(
            field,
            "must be in format x,y where x and y are integers"
        )

    @staticmethod
    def invalid_bound_coordinates(field: str, width: int, height: int
                                  ) -> "ConfigError":
        return ConfigError(
            field,
            f"coordinates out of bounds: "
            f"expected 0 <= x < {width} and 0 <= y < {height}"
        )

    @staticmethod
    def aggregate(errors: list["ConfigError"]) -> "ConfigError":
        messages = "\n".join(str(e) for e in errors)
        return ConfigError(f"\n{messages}", "")
