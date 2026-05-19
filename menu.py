# ****************************************************************************
#
#    menu.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Interactive terminal menu for maze visualization and
#                 user interactions.
#    Created: 2026/05/19
#
# ****************************************************************************

from __future__ import annotations

from maze_generator import MazeGenerator
from maze_structure import Maze
from parser import Parser
from solver import MazeSolver
import os
from renderer import MazeRenderer
import themes


class MazeMenu:

    THEMES: dict[str, dict[str, str]] = {
        "1": themes.DEFAULT_THEME,
        "2": themes.NORD_THEME,
        "3": themes.DRACULA_THEME,
        "4": themes.LUFFY_THEME,
        "5": themes.ZORO_THEME,
        "6": themes.BROOK_THEME
    }

    def __init__(
        self,
        maze: Maze,
        generator: MazeGenerator,
        config: Parser,
    ) -> None:

        self.maze = maze
        self.generator = generator
        self.config = config

        self.show_path = False

        self.path: list[tuple[int, int]] | None = None

        self.current_theme = themes.DEFAULT_THEME

        self.renderer = MazeRenderer(
            self.maze,
            self.config,
            self.path,
            self.current_theme,
        )

    def _clear_screen(self) -> None:
        """Clear terminal screen."""

        os.system("clear")

    def _render(self) -> None:
        """Render maze using current state."""

        self.renderer.maze = self.maze

        if self.show_path:
            self.renderer.path = self.path

        else:
            self.renderer.path = None

        self.renderer.theme = self.current_theme

        self.renderer.render()

    def _show_menu(self) -> None:
        """Display menu options."""

        print()

        print("========== A-Maze-ing ==========")
        print("[1] Regenerate maze")
        print("[2] Toggle shortest path")
        print("[3] Change theme")
        print("[4] Save maze")
        print("[0] Exit")
        print("================================")

        print()

    def _regenerate(self) -> None:
        """Generate a new maze."""

        self.maze = Maze(self.config)

        self.generator = MazeGenerator(
            self.maze,self.config
        )

        self.generator.generate()

        self.path = None

    def _toggle_path(self) -> None:
        """Show or hide shortest path."""

        self.show_path = not self.show_path

        if self.show_path:

            solver = MazeSolver(
                self.maze,
                self.config.entry,
                self.config.exit,
            )

            self.path = solver.solve()

            print()
            print("Path visualization enabled.")
            print()
            self._pause()

        else:

            self.path = None

            print()
            print("Path visualization disabled.")
            print()
            self._pause()

    def _change_theme(self) -> None:
        """Change renderer theme."""

        print()

        print("Choose a theme:")
        print("[1] Default")
        print("[2] Nord")
        print("[3] Dracula")
        print("[4] Luffy")
        print("[5] Zoro")
        print("[6] Brook")
        

        print()

        choice = input("Theme: ").strip()

        if choice in self.THEMES:

            self.current_theme = (
                self.THEMES[choice]
            )

            print()
            print("Theme updated.")
            print()
            self._pause()

        else:

            print()
            print("Invalid theme.")
            print()
            self._pause()

    def _save_maze(self) -> None:
        """Save maze to output file."""

        try:

            MazeGenerator.save_maze(
                self.maze,
                self.config,
            )

            print()

            print(
                f"Maze saved to "
                f"{self.config.output_file}"
            )

            print()

            self._pause()

        except Exception:

            print()
            print("Failed to save maze.")
            print()

            self._pause()

    def _handle_choice(
        self,
        choice: str,
    ) -> bool:
        """Handle user menu selection."""

        if choice == "1":

            self._regenerate()

        elif choice == "2":

            self._toggle_path()

        elif choice == "3":

            self._change_theme()

        elif choice == "4":

            self._save_maze()

        elif choice == "0":

            print()
            print("Exiting A-Maze-ing.")
            print()

            return False

        else:

            print()
            print("Invalid option.")
            print()
            self._pause()

        return True

    def _pause(self) -> None:
        """Wait for user before continuing."""

        input("Press ENTER to continue...")

    def run(self) -> None:
        """Start interactive menu loop."""

        running = True

        while running:

            self._clear_screen()

            self._render()

            self._show_menu()

            choice = input(
                "Option: "
            ).strip()

            running = self._handle_choice(
                choice
            )