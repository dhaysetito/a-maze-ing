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

import os

import themes

from maze_generator import MazeGenerator
from maze_structure import Maze
from parser import Parser
from renderer import MazeRenderer
from solver import MazeSolver


class MazeMenu:

    THEMES: dict[str, dict[str, str]] = {
        "1": themes.DEFAULT_THEME,
        "2": themes.NORD_THEME,
        "3": themes.DRACULA_THEME,
        "4": themes.LUFFY_THEME,
        "5": themes.ZORO_THEME,
        "6": themes.BROOK_THEME,
        "7": themes.GAME_THEME
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

        self.path: (list[tuple[int, int]] | None) = None

        self.current_theme = themes.DEFAULT_THEME
        self.current_theme_name = "Default"

        self.renderer = MazeRenderer(
            self.maze,
            self.config,
            self.path,
            self.current_theme,
        )

        self.save = True

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
        if not self.show_path:
            print("[2] Toggle shortest path (Disabled)")
        else:
            print("[2] Toggle shortest path (Enabled)")
        print(f"[3] Change theme ({self.current_theme_name})")
        if self.save:
            print(f"[4] Save maze (saved to `{self.config.output_file}`)")
        else:
            print("[4] Save maze (not saved)")
        print("[0] Exit")
        print("================================")

        print()

    def _regenerate(self) -> None:
        """Generate a new maze."""

        self.maze = Maze(self.config)
        self.generator = MazeGenerator(self.maze, self.config)
        self.generator.generate()
        solver = MazeSolver(self.maze, self.config)
        self.path = solver.solve()
        self.save = False

    def _toggle_path(self) -> None:
        """Show or hide shortest path."""

        self.show_path = not self.show_path

        if self.show_path:
            solver = MazeSolver(self.maze, self.config)
            self.path = solver.solve()

        else:
            self.path = None

    def _change_theme(self) -> None:
        """Change renderer theme."""

        print("\nChoose a theme:")
        print("[1] Default")
        print("[2] Nord")
        print("[3] Dracula")
        print("[4] Luffy")
        print("[5] Zoro")
        print("[6] Brook")
        print("[7] Game")

        print()

        choice = input("Theme: ").strip()

        if choice in themes.THEMES:
            name, theme = (themes.THEMES[choice])
            self.current_theme = theme
            self.current_theme_name = name

    def _save_maze(self) -> None:
        """Save maze to output file."""

        try:
            new_file = input(
                f"Enter the name of the file to save"
                f" ({self.config.output_file}): "
                )
            if new_file:
                self.config.output_file = new_file
            solver = MazeSolver(self.maze, self.config)
            solver.solve()
            solution = solver.path_to_directions()
            self.generator.save_maze(self.maze, self.config, solution)
            self.save = True

        except Exception:
            print("\nFailed to save maze.\n")
            self.save = False
            self._pause()

    def _handle_choice(self, choice: str) -> bool:
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
            print("\nQue a força esteja sempre com você!\n")
            return False

        else:
            print("\nSelect a valid menu option (0-4).\n")
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

            choice = input("Option: ").strip()
            running = self._handle_choice(choice)
