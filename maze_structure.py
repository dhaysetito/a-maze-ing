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


class Cell:
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False

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


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        directions = [
            (x, y - 1),  # North
            (x + 1, y),  # East
            (x, y + 1),  # South
            (x - 1, y),  # West
        ]

        return [
            (nx, ny)
            for nx, ny in directions
            if self.in_bounds(nx, ny)
        ]

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


if __name__ == "__main__":

    import random

    maze = Maze(5, 4)

    random.seed(0)

    for y in range(maze.height):
        for x in range(maze.width):

            neighbors = maze.neighbors(x, y)

            if neighbors:
                nx, ny = random.choice(neighbors)

                maze.remove_wall(x, y, nx, ny)

    for row in maze.to_hex_grid():
        print("".join(row))