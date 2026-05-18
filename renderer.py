# ****************************************************************************
#
#    renderer.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: ASCII renderer for maze visualization.
#                 Displays walls, entry, exit and optional solution path.
#
#    Created: 2026/05/18
#
# ****************************************************************************

from maze_structure import Maze


class MazeRenderer:
    """Render a maze structure using ASCII visualization."""

    WALL_HORIZONTAL = "███"
    WALL_VERTICAL = "█"
    EMPTY_SPACE = "   "

    START_SYMBOL = " S "
    EXIT_SYMBOL = " E "
    PATH_SYMBOL = " . "

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def render_ascii(
        self,
        entry: tuple[int, int] | None = None,
        exit: tuple[int, int] | None = None,
        path: list[tuple[int, int]] | None = None,
        show_path: bool = True,
    ) -> str:
        """
        Generate an ASCII representation of the maze.

        Args:
            entry: Entry coordinates.
            exit: Exit coordinates.
            path: Optional solution path.
            show_path: Controls path visibility.

        Returns:
            Full ASCII maze as a string.
        """

        rendered_lines: list[str] = []

        path_set = set(path) if path is not None else set()

        rendered_lines.append(self._top_border())

        for y in range(self.maze.height):
            rendered_lines.append(
                self._cell_line(
                    y,
                    entry,
                    exit,
                    path_set,
                    show_path,
                )
            )

            rendered_lines.append(self._bottom_line(y))

        return "\n".join(rendered_lines)

    def display_ascii(
        self,
        entry: tuple[int, int] | None = None,
        exit: tuple[int, int] | None = None,
        path: list[tuple[int, int]] | None = None,
        show_path: bool = True,
    ) -> None:
        """Print the ASCII maze to the terminal."""

        print(
            self.render_ascii(
                entry=entry,
                exit=exit,
                path=path,
                show_path=show_path,
            )
        )

    def _top_border(self) -> str:
        """Render the top border of the maze."""

        line = "█"

        for _ in range(self.maze.width):
            line += self.WALL_HORIZONTAL + "█"

        return line

    def _bottom_line(self, y: int) -> str:
        """Render horizontal walls for a row."""

        line = "█"

        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)

            if cell.south:
                line += self.WALL_HORIZONTAL
            else:
                line += self.EMPTY_SPACE

            line += "█"

        return line

    def _cell_line(
        self,
        y: int,
        entry: tuple[int, int] | None,
        exit: tuple[int, int] | None,
        path: set[tuple[int, int]],
        show_path: bool,
    ) -> str:
        """Render maze cells for a row."""

        line = ""

        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)

            if cell.west:
                line += self.WALL_VERTICAL
            else:
                line += " "

            line += self._cell_content(
                x,
                y,
                entry,
                exit,
                path,
                show_path,
            )

        last_cell = self.maze.get_cell(self.maze.width - 1, y)

        if last_cell.east:
            line += self.WALL_VERTICAL
        else:
            line += " "

        return line

    def _cell_content(
        self,
        x: int,
        y: int,
        entry: tuple[int, int] | None,
        exit: tuple[int, int] | None,
        path: set[tuple[int, int]],
        show_path: bool,
    ) -> str:
        """Return visual content for a cell."""

        position = (x, y)

        if entry is not None and position == entry:
            return self.START_SYMBOL

        if exit is not None and position == exit:
            return self.EXIT_SYMBOL

        if show_path and position in path:
            return self.PATH_SYMBOL

        return self.EMPTY_SPACE


if __name__ == "__main__":
    from maze_generator import MazeGenerator

    maze = Maze(10, 10)

    generator = MazeGenerator(maze)
    generator.generate()

    renderer = MazeRenderer(maze)

    renderer.display_ascii(
        entry=(0, 0),
        exit=(9, 5),
        path=[
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 2),
            (3, 2),
        ],
        show_path=True,
    )