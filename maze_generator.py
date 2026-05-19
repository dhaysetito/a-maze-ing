# ****************************************************************************
#
#    maze_generator.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Created: 2026/04/28
#
# ****************************************************************************

import random
from maze_structure import Maze
from exceptions import MazeError
from parser import Parser


class MazeGenerator:
    def __init__(self, maze: Maze, config: Parser) -> None:
        self.maze = maze
        self.config = config
        self.random = random.Random(config.seed)
        self.has_42_pattern = False

    def _unvisited_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []

        for _, n_x, n_y in self.maze.neighbors(x, y):
            neighbor = self.maze.get_cell(n_x, n_y)

            if not neighbor.visited and not neighbor.blocked:
                result.append((n_x, n_y))
        return result

    def _reset_visited(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                cell.visited = False

    def _clear_42_pattern(self) -> None:
        """Remove 42 blocked cells."""
        for row in self.maze.grid:
            for cell in row:
                cell.blocked = False

    def _validate_entry_exit(self) -> None:
        # TODO: modificar logica se quiser funcionar para qualquer
        # entrada e saida
        assert self.config.entry is not None
        assert self.config.exit is not None
        entry = self.config.entry
        exit = self.config.exit

        if entry == exit:
            raise MazeError("Entry and exit must be different")

        if self.maze.get_cell(entry[0], entry[1]).blocked:
            raise MazeError("Entry cannot be inside the 42 pattern")

        if self.maze.get_cell(exit[0], exit[1]).blocked:
            raise MazeError("Exit cannot be inside the 42 pattern")

        self.entry = entry
        self.exit = exit

    # Algorithm DFS - deep first search
    def generate(self) -> None:
        stack: list[tuple[int, int]] = []

        try:
            self._create_42_pattern()
            self._validate_entry_exit()
        except MazeError:
            self._clear_42_pattern()
            self.has_42_pattern = False

        x, y = 0, 0
        self.maze.get_cell(x, y).visited = True

        while True:
            neighbors = self._unvisited_neighbors(x, y)

            if neighbors:
                nx, ny = self.random.choice(neighbors)

                # remove wall between (x,y) and (nx,ny)
                self.maze.remove_wall(x, y, nx, ny)

                stack.append((x, y))

                x, y = nx, ny
                self.maze.get_cell(x, y).visited = True

            elif stack:
                x, y = stack.pop()

            else:
                break

        self._reset_visited()

    def _create_42_pattern(self) -> None:
        """Create isolated 42 pattern."""

        if (self.maze.width < 12 or self.maze.height < 7):
            return

        cx = (self.maze.width // 2) - 4
        cy = (self.maze.height // 2) - 2

        pattern = [
            # 4
            (cx, cy),
            (cx, cy + 1),
            (cx, cy + 2),
            (cx + 1, cy + 2),
            (cx + 2, cy + 2),
            (cx + 2, cy + 3),
            (cx + 2, cy + 4),

            # 2
            (cx + 4, cy),
            (cx + 5, cy),
            (cx + 6, cy),
            (cx + 6, cy + 1),
            (cx + 4, cy + 2),
            (cx + 5, cy + 2),
            (cx + 6, cy + 2),
            (cx + 4, cy + 3),
            (cx + 4, cy + 4),
            (cx + 5, cy + 4),
            (cx + 6, cy + 4),
        ]

        for x, y in pattern:

            if (
                0 <= x < self.maze.width
                and 0 <= y < self.maze.height
            ):
                cell = self.maze.get_cell(x, y)
                cell.blocked = True
        self.has_42_pattern = True

    @staticmethod
    def save_maze(maze: Maze, config: Parser, solution: str) -> None:
        assert config.output_file is not None
        assert config.entry is not None
        assert config.exit is not None

        try:
            with open(config.output_file, "w") as file:
                for row in maze.grid:
                    line = "".join(maze.cell_to_hex(c) for c in row)
                    file.write(line + "\n")
                    # print("".join(maze.cell_to_hex(c) for c in row))

                file.write("\n")
                file.write(f"{str(config.entry[0])},{str(config.entry[1])}")
                file.write("\n")
                file.write(f"{str(config.exit[0])},{str(config.exit[1])}")
                file.write("\n")
                file.write(f"{solution}\n")

        except OSError as e:
            raise MazeError("Can't create file.") from e
