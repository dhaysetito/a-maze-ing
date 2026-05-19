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
from renderer import MazeRenderer
from menu import MazeMenu

if __name__ == "__main__":
    try:
        config = Parser("config.txt")

        maze = Maze(config)

        gen = MazeGenerator(maze, config)

        gen.generate()
        gen.save_maze(maze, config)
  
        #mazerender = MazeRenderer(maze, config)
        
        #mazerender.render()

        menu = MazeMenu(
            maze,
            gen,
            config,
        )

        menu.run()

    except ConfigError as e:
        print(f"Config error: {e}")

    except MazeError as e:
        print(f"Maze error: {e}")

    except Exception as e:
        print(f"Error found: {e}")
        
    except KeyboardInterrupt as e:
        print(f"\nQue a força esteja sempre com você!")
