# ****************************************************************************
#
#    a_maze_ing.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Created: 2026/04/22
#
# ****************************************************************************

from maze_generator import MazeGenerator
from maze_structure import Maze
from parser import Parser
from exceptions import MazeError, ConfigError
from renderer import render_ascii_maze


if __name__ == "__main__":
    try:
        config = Parser("config.txt")

        maze = Maze(config)

        gen = MazeGenerator(maze, config)

        gen.generate()
        gen.save_maze(maze, config)
  
        render_ascii_maze(
            maze,
            {
                "ENTRY": config.entry,
                "EXIT": config.exit,
            }
        )


    except ConfigError as e:
        print(f"Config error: {e}")

    except MazeError as e:
        print(f"Maze error: {e}")

    except Exception as e:
        print(f"Error found: {e}")
