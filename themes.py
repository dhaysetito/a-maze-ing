# ****************************************************************************
#
#    themes.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Terminal color themes used for maze rendering,
#                 including path, walls, entry, exit and background
#                 customization.
#    Created: 2026/05/19
#
# ****************************************************************************

DEFAULT_THEME: dict[str, str] = {
    "path": "\x1b[38;5;110m",
    "entry": "\x1b[38;5;108m",
    "exit": "\x1b[38;5;131m",
    "wall": "\x1b[38;5;240m",
    "bg": "\x1b[48;5;237m",
    "reset": "\x1b[0m",
}

NORD_THEME: dict[str, str] = {
    "path": "\033[33m",
    "entry": "\033[32m",
    "exit": "\033[31m",
    "wall": "\033[38;5;130m",
    "bg": "\033[30m",
    "reset": "\033[0m",
}

DRACULA_THEME: dict[str, str] = {
    "path": "\x1b[38;5;212m",
    "entry": "\x1b[38;5;84m",
    "exit": "\x1b[38;5;203m",
    "wall": "\x1b[38;5;61m",
    "bg": "\x1b[48;5;236m",
    "reset": "\x1b[0m",
}

LUFFY_THEME: dict[str, str] = {
    "path": "\x1b[38;5;220m",
    "entry": "\x1b[38;5;196m",
    "exit": "\x1b[38;5;27m",
    "wall": "\x1b[38;5;221m",
    "bg": "\x1b[48;5;234m",
    "reset": "\x1b[0m",
}

ZORO_THEME: dict[str, str] = {
    "path": "\x1b[38;5;118m",
    "entry": "\x1b[38;5;46m",
    "exit": "\x1b[38;5;161m",
    "wall": "\x1b[38;5;34m",
    "bg": "\x1b[48;5;232m",
    "reset": "\x1b[0m",
}

BROOK_THEME: dict[str, str] = {
    "path": "\x1b[38;5;39m",
    "entry": "\x1b[38;5;15m",
    "exit": "\x1b[38;5;214m",
    "wall": "\x1b[38;5;232m",
    "bg": "\x1b[48;5;17m",
    "reset": "\x1b[0m",
}

THEMES: dict[str, tuple[str, dict[str, str]]] = {
    "1": ("Default", DEFAULT_THEME),
    "2": ("Nord", NORD_THEME),
    "3": ("Dracula", DRACULA_THEME),
    "4": ("Luffy", LUFFY_THEME),
    "5": ("Zoro", ZORO_THEME),
    "6": ("Brook", BROOK_THEME),
}
