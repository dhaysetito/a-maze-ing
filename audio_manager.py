# ****************************************************************************
#
#    audio_manager.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Background music manager.
#    Created: 2026/05/19
#
# ****************************************************************************

from __future__ import annotations
import os


class AudioManager:

    def __init__(self) -> None:
        self.current_music: str | None = None

    def stop(self) -> None:
        """Stop current music."""
        os.system("pkill mpg123 > /dev/null 2>&1")
        self.current_music = None

    def play(self, music_path: str) -> None:
        """Play music in background."""
        self.stop()
        self.current_music = music_path
        os.system(
            f"mpg123 --loop -1 "
            f"{music_path} > /dev/null 2>&1 &"
        )

    def is_playing(self) -> bool:
        """Check if music is playing."""
        return (
            self.current_music
            is not None
        )

    def toggle(self, music_path: str) -> None:
        """Toggle music playback."""
        if self.is_playing():
            self.stop()
        else:
            self.play(music_path)
