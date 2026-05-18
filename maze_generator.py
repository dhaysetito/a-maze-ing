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


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        self.maze = maze
        self.random = random.Random(seed)

    def _unvisited_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for n_x, n_y in self.maze.neighbors(x, y):
            if not self.maze.get_cell(n_x, n_y).visited:
                result.append((n_x, n_y))
        return result

    def _reset_visited(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                cell.visited = False

    def open_entry_exit(self, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        ex, ey = entry
        tx, ty = exit

        if not self.maze.in_bounds(ex, ey):
            raise MazeError("Entry out of bounds")

        if not self.maze.in_bounds(tx, ty):
            raise MazeError("Exit out of bounds")

        if entry == exit:
            raise MazeError("Entry and exit must be different")

        self.entry = entry
        self.exit = exit

    # Algorithm DFS - deep first search
    def generate(self) -> None:
        stack: list[tuple[int, int]] = []

		# Deveria sempre começar em 0,0?
        # start in (0,0)
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


if __name__ == "__main__":
    maze = Maze(5, 5)
    gen = MazeGenerator(maze, seed=0)
    gen.generate()
    gen.open_entry_exit((1, 1), (4, 4))

    for row in maze.grid:
        print("".join(maze.cell_to_hex(c) for c in row))
