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


def save_maze(config: Parser, maze: Maze) -> None:
    try:
        with open(config.output_file, "w") as file:
            for row in maze.grid:
                line = "".join(maze.cell_to_hex(c) for c in row)
                file.write(line + "\n")
                print("".join(maze.cell_to_hex(c) for c in row))

            file.write("\n")
            file.write(str(config.entry[0]) + "," + str(config.entry[1]))
            file.write("\n")
            file.write(str(config.exit[0]) + "," + str(config.exit[1]))
            file.write("\n")

    except ValueError as e:
        raise MazeError("Can't create file.") from e


if __name__ == "__main__":
    try:
        config = Parser("config.txt")

        maze = Maze(config.width, config.height)
        gen = MazeGenerator(maze)
        gen.generate()

        save_maze(config, maze)

    except ConfigError as e:
        print(f"Config error: {e}")

    except MazeError as e:
        print(f"Maze error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
