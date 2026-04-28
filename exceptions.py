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

class MazeError(Exception):
    def __init__(self, message: str = "Unknown error") -> None:
        super().__init__(message)


class ConfigError(MazeError):
    def __init__(
            self, field: str, message: str = "Unknown config error"
            ) -> None:
        super().__init__(f"[{field}] {message}")

    @staticmethod
    def invalid_int(field: str) -> "ConfigError":
        return ConfigError(field, "must be an integer")

    @staticmethod
    def invalid_coordinates(field: str) -> "ConfigError":
        return ConfigError(
            field,
            "must be in format (x,y) where x and y are integers"
            )
