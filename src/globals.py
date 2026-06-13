import os.path
from os import path

from PySide6.QtCore import Signal, QObject

from ok import Logger, get_path_relative_to_exe, og

logger = Logger.get_logger(__name__)


class Globals(QObject):
    """Global state holder for Infinity Nikki.

    Mirrors ok-ww/src/globals.py pattern.
    """

    def __init__(self, exit_event):
        super().__init__()
        self._in_hud = False

    @property
    def in_hud(self):
        return self._in_hud

    @in_hud.setter
    def in_hud(self, value):
        self._in_hud = value
        logger.debug(f"in_hud set to {value}")


if __name__ == "__main__":
    glbs = Globals(exit_event=None)
