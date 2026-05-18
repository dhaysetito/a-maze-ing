# ****************************************************************************
#
#    a_maze_ing.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Parses and validates the maze configuration file (KEY=VALUE),
#                 ensuring correct types and required parameters before
#                 execution.
#
#    Created: 2026/04/22
#
# ****************************************************************************

#TODO adicionar docstrings
from exceptions import ConfigError


class Parser:
    #TODO fazer validação para os atributos obritgatórios
    def __init__(self, file_name: str = "config.txt"):
        self.file_name = file_name
        self.width = 0
        self.height = 0
        self.entry = (0, 0)
        self.exit = (0, 0)
        self.output_file = "maze.txt"
        self.perfect = False
        self.seed = 0
        self.algorithm = "BFS"
        self.display_mode = "ASCII"

        self._read_file()

    def _read_file(self) -> None:
        errors: list[ConfigError] = []
		#TODO open sem tratamento para arquivo inexistente
        with open(self.file_name, "r") as file:
            for line in file:
                # TODO tratar indexError
                if (line[0] == "#"):
                    pass
                else:
                    try:
                        self._parse_line(line.strip())
                    except ConfigError as e:
                        errors.append(e)
            if errors:
                raise ConfigError.aggregate(errors)

    def _parse_line(self, line: str) -> None:
        key, _, value = line.partition("=")

        if key == "WIDTH":
            try:
                self.width = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("[WIDTH]") from e

        elif key == "HEIGHT":
            try:
                self.height = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("[HEIGHT]") from e

        elif key == "ENTRY":
        # TODO tratamento para as coordenadas que estiverem fora do labirinto
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                self.entry = (x, y)
            except Exception as e:
                raise ConfigError.invalid_coordinates("[ENTRY]") from e

        elif key == "EXIT":
        # TODO tratamento para as coordenadas que estiverem fora do labirinto
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                self.exit = (x, y)
            except Exception as e:
                raise ConfigError.invalid_coordinates("[EXIT]") from e

        elif key == "OUTPUT_FILE":
            if not value:
                raise ConfigError("[OUTPUT_FILE]", "cannot be empty")
            self.output_file = value

        elif key == "PERFECT":
            if value == "True":
                self.perfect = True
            elif value == "False":
                self.perfect = False
            else:
                raise ConfigError("[PERFECT]", "must be True or False")
        # opcional!
        elif key == "SEED":
            try:
                self.seed = int(value)
            except ValueError as e:
                raise ConfigError.invalid_int("[SEED]") from e
        # opcional!
        elif key == "ALGORITHM":
            #TODO tratar algoritmo inválido
            if not value:
                pass
            valid_algorithms = {"BFS", "A*"}
            if value.upper() not in valid_algorithms:
                pass
        # opcional!
        elif key == "DISPLAY_MODE":
            #TODO tratar modos inválidos
            if not value:
                pass
            valid_modes = {"ASCII", "MLX"}
            if value.upper() not in valid_modes:
                pass
            self.display_mode = value.upper()
        else:
            raise ConfigError("[" + key + "]", "unknown parameter")


if __name__ == "__main__":
    config = Parser("config.txt")
    print(config.width)
    print(config.output_file)
