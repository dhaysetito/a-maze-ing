# ****************************************************************************
#
#    maze_structure.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Defines the internal representation of the maze, including
#                 cell structure, wall encoding, and grid organization used
#                 during generation, solving, and export.
#    Created: 2026/04/28
#
# ****************************************************************************

from parser import Parser


class Cell:
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
        self.blocked = False

    def has_wall(self, direction: str) -> bool:
        """Return whether a wall exists in the given direction."""

        mapping = {
            "N": self.north,
            "E": self.east,
            "S": self.south,
            "W": self.west,
        }

        if direction not in mapping:
            raise ValueError(
                f"Invalid direction: {direction}"
            )

        return mapping[direction]

    def close_all_walls(self) -> None:
        """Close all cell walls."""

        self.north = True
        self.east = True
        self.south = True
        self.west = True


class Maze:
    def __init__(self, config: Parser) -> None:
        assert config.width is not None
        assert config.height is not None

        self.width = config.width
        self.height = config.height

        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        directions = [
            ("N", x, y - 1),
            ("E", x + 1, y),
            ("S", x, y + 1),
            ("W", x - 1, y)
        ]

        return [
            (direction, nx, ny)
            for direction, nx, ny in directions
            if self.in_bounds(nx, ny)
        ]

    def reachable_neighbors(self, x: int, y: int
                            ) -> list[tuple[int, int]]:
        neighbors = []

        cell = self.get_cell(x, y)

        for direction, nx, ny in self.neighbors(x, y):

            if not cell.has_wall(direction):

                neighbors.append((nx, ny))

        return neighbors

    def remove_wall(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:
        """Remove walls between orthogonal neighboring cells."""

        c1 = self.get_cell(x1, y1)
        c2 = self.get_cell(x2, y2)

        if x1 == x2:

            if y1 > y2:
                c1.north = False
                c2.south = False

            else:
                c1.south = False
                c2.north = False

        elif y1 == y2:

            if x1 < x2:
                c1.east = False
                c2.west = False

            else:
                c1.west = False
                c2.east = False

        else:
            raise ValueError(
                f"Cells ({x1}, {y1}) and ({x2}, {y2}) "
                "are not orthogonal neighbors."
            )

    def cell_to_hex(self, cell: Cell) -> str:
        """Convert a cell wall structure into hexadecimal encoding."""

        value = 0

        if cell.north:
            value |= 1

        if cell.east:
            value |= 2

        if cell.south:
            value |= 4

        if cell.west:
            value |= 8

        return format(value, "X")

    def to_hex_grid(self) -> list[list[str]]:
        """Return the maze encoded as hexadecimal."""

        return [
            [self.cell_to_hex(cell) for cell in row]
            for row in self.grid
        ]
