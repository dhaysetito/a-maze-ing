from __future__ import annotations

from maze_structure import Maze
from parser import Parser
from themes import DEFAULT_THEME


class MazeRenderer:

    BLOCK = "██"

    DIRECTION_OFFSETS: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0),
    }

    def __init__(
        self,
        maze: Maze,
        config: Parser,
        path: list[tuple[int, int]] | None = None,
        theme: dict[str, str] | None = None,
    ) -> None:

        self.maze = maze
        self.config = config
        self.path = path

        if theme is None:
            self.theme = DEFAULT_THEME

        else:
            self.theme = theme

        self.real_width = (
            self.maze.width * 2
        ) + 1

        self.real_height = (
            self.maze.height * 2
        ) + 1

        self._update_theme()

        self.canvas: list[list[str]] = []

    def _update_theme(self) -> None:
        """Update renderer theme colors."""

        self.wall_color = self.theme["wall"]

        self.bg_color = self.theme["bg"]

        self.path_color = self.theme["path"]

        self.entry_color = self.theme["entry"]

        self.exit_color = self.theme["exit"]

        self.reset = self.theme["reset"]

    def _create_canvas(self) -> None:
        """Create a fresh render canvas."""

        self.canvas = [
            [
                (
                    f"{self.wall_color}"
                    f"{self.BLOCK}"
                    f"{self.reset}"
                )
                for _ in range(
                    self.real_width
                )
            ]
            for _ in range(
                self.real_height
            )
        ]

    def _paint(
        self,
        x: int,
        y: int,
        color: str,
    ) -> None:
        """Paint a single block."""

        self.canvas[y][x] = (
            f"{color}"
            f"{self.BLOCK}"
            f"{self.reset}"
        )

    def _draw_cells(self) -> None:
        """Draw maze cells."""

        for y in range(self.maze.height):

            for x in range(self.maze.width):

                cx = (x * 2) + 1

                cy = (y * 2) + 1

                self._paint(
                    cx,
                    cy,
                    self.bg_color,
                )

                cell = self.maze.grid[y][x]

                for direction, (
                    dx,
                    dy,
                ) in (
                    self.DIRECTION_OFFSETS.items()
                ):

                    if not cell.has_wall(
                        direction
                    ):

                        nx = cx + dx

                        ny = cy + dy

                        if (
                            0 <= nx
                            < self.real_width
                            and 0 <= ny
                            < self.real_height
                        ):

                            self._paint(
                                nx,
                                ny,
                                self.bg_color,
                            )

    def _draw_path(self) -> None:
        """Draw solution path."""

        if not self.path:

            return

        for i, (
            px,
            py,
        ) in enumerate(self.path):

            vx = (px * 2) + 1

            vy = (py * 2) + 1

            self._paint(
                vx,
                vy,
                self.path_color,
            )

            if i < len(self.path) - 1:

                nx, ny = (
                    self.path[i + 1]
                )

                connector_x = (
                    vx + (nx - px)
                )

                connector_y = (
                    vy + (ny - py)
                )

                if (
                    0 <= connector_x
                    < self.real_width
                    and 0 <= connector_y
                    < self.real_height
                ):

                    self._paint(
                        connector_x,
                        connector_y,
                        self.path_color,
                    )

    def _draw_entry_exit(self) -> None:
        """Draw entry and exit."""

        entry_x, entry_y = (
            self.config.entry
        )

        exit_x, exit_y = (
            self.config.exit
        )

        self._paint(
            (entry_x * 2) + 1,
            (entry_y * 2) + 1,
            self.entry_color,
        )

        self._paint(
            (exit_x * 2) + 1,
            (exit_y * 2) + 1,
            self.exit_color,
        )

    def render(self) -> None:
        """Render complete maze."""

        self._update_theme()

        self._create_canvas()

        self._draw_cells()

        self._draw_path()

        self._draw_entry_exit()

        for line in self.canvas:

            print("".join(line))