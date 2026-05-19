# ****************************************************************************
#
#    renderer.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Terminal maze renderer responsible for drawing walls,
#                 paths, entry and exit points using ANSI color themes
#                 and block-based visualization.
#
#    Created: 2026/04/22
#
# ****************************************************************************

import sys
from maze_generator import MazeGenerator
from maze_structure import Maze
from parser import Parser
from exceptions import MazeError, ConfigError
from menu import MazeMenu
from solver import MazeSolver


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config_path = sys.argv[1]
        config = Parser(config_path)

        maze = Maze(config)

        gen = MazeGenerator(maze, config)
        gen.generate()

        solver = MazeSolver(maze, config)
        solver.solve()
        solution = solver.path_to_directions()
        gen.save_maze(maze, config, solution)

        MazeMenu(maze, gen, config).run()

    except ConfigError as e:
        print(f"Config error: {e}")

    except MazeError as e:
        print(f"Maze error: {e}")

    except KeyboardInterrupt:
        print("\nQue a força esteja sempre com você!")

    except Exception as e:
        print(f"Error found: {e}")


if __name__ == "__main__":
    main()
