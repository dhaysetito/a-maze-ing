from __future__ import annotations

from maze_structure import Maze
from themes import *

BLOCK = "██"

DIRECTION_OFFSETS: dict[str, tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


def _paint(
    canvas: list[list[str]],
    x: int,
    y: int,
    color: str,
    reset: str,
) -> None:
    """Paint a single block in the canvas."""
    canvas[y][x] = f"{color}{BLOCK}{reset}"


def render_ascii_maze(
    generator: MazeGenerator,
    config: dict[str, tuple[int, int]],
    path: list[tuple[int, int]] | None = None,
    theme: dict[str, str] | None = None,
) -> None:
    """Render the maze as colored ASCII art."""
    if theme is None:
        theme = DEFAULT_THEME

    wall_color = theme["wall"]
    bg_color = theme["bg"]
    path_color = theme["path"]
    entry_color = theme["entry"]
    exit_color = theme["exit"]
    reset = theme["reset"]

    real_width = (generator.width * 2) + 1
    real_height = (generator.height * 2) + 1

    canvas: list[list[str]] = [
        [
            f"{wall_color}{BLOCK}{reset}"
            for _ in range(real_width)
        ]
        for _ in range(real_height)
    ]

    for y in range(generator.height):
        for x in range(generator.width):
            cx = (x * 2) + 1
            cy = (y * 2) + 1

            _paint(canvas, cx, cy, bg_color, reset)

            cell = generator.grid[y][x]

            for direction, (dx, dy) in DIRECTION_OFFSETS.items():
                if not cell.has_wall(direction):
                    _paint(
                        canvas,
                        cx + dx,
                        cy + dy,
                        bg_color,
                        reset,
                    )

    if path:
        for i, (px, py) in enumerate(path):
            vx = (px * 2) + 1
            vy = (py * 2) + 1

            _paint(canvas, vx, vy, path_color, reset)

            if i < len(path) - 1:
                nx, ny = path[i + 1]

                connector_x = vx + (nx - px)
                connector_y = vy + (ny - py)

                _paint(
                    canvas,
                    connector_x,
                    connector_y,
                    path_color,
                    reset,
                )

    entry_x, entry_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    _paint(
        canvas,
        (entry_x * 2) + 1,
        (entry_y * 2) + 1,
        entry_color,
        reset,
    )

    _paint(
        canvas,
        (exit_x * 2) + 1,
        (exit_y * 2) + 1,
        exit_color,
        reset,
    )

    for line in canvas:
        print("".join(line))