# ****************************************************************************
#
#    solver.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Breadth-First Search maze solver.
#    Created: 2026/05/19
#
# ****************************************************************************

from __future__ import annotations

from collections import deque

from maze_structure import Maze


class MazeSolver:

    DIRECTION_OFFSETS: dict[
        str,
        tuple[int, int],
    ] = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0),
    }

    def __init__(
        self,
        maze: Maze,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None:

        self.maze = maze

        self.start = start

        self.end = end

    def _is_valid_position(
        self,
        x: int,
        y: int,
    ) -> bool:
        """Check if position is inside maze."""

        return (
            0 <= x < self.maze.width
            and 0 <= y < self.maze.height
        )

    def _get_neighbors(
        self,
        x: int,
        y: int,
    ) -> list[tuple[int, int]]:
        """Return reachable neighbors."""

        neighbors = []

        cell = self.maze.grid[y][x]

        for direction, (
            dx,
            dy,
        ) in (
            self.DIRECTION_OFFSETS.items()
        ):

            if not cell.has_wall(direction):

                nx = x + dx

                ny = y + dy

                if self._is_valid_position(
                    nx,
                    ny,
                ):

                    neighbors.append(
                        (nx, ny)
                    )

        return neighbors

    def _reconstruct_path(
        self,
        parents: dict[
            tuple[int, int],
            tuple[int, int] | None,
        ],
    ) -> list[tuple[int, int]]:
        """Reconstruct shortest path."""

        path = []

        current = self.end

        while current is not None:

            path.append(current)

            current = parents[current]

        path.reverse()

        return path

    def solve(
        self,
    ) -> list[tuple[int, int]]:
        """Solve maze using BFS."""

        queue = deque()

        queue.append(self.start)

        visited = set()

        visited.add(self.start)

        parents: dict[
            tuple[int, int],
            tuple[int, int] | None,
        ] = {
            self.start: None
        }

        while queue:

            current = queue.popleft()

            if current == self.end:

                return self._reconstruct_path(
                    parents
                )

            x, y = current

            neighbors = (
                self._get_neighbors(
                    x,
                    y,
                )
            )

            for neighbor in neighbors:

                if neighbor not in visited:

                    visited.add(neighbor)

                    parents[neighbor] = current

                    queue.append(neighbor)

        return []