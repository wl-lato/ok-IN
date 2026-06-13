import os.path
from os import path

from PySide6.QtCore import Signal, QObject

from ok import Logger, get_path_relative_to_exe, og

logger = Logger.get_logger(__name__)


class Globals(QObject):
    """Global state holder for Infinity Nikki.

    Mirrors ok-ww/src/globals.py pattern.
    Uses logged_in attribute (same name as ok-ww) for cross-task state sharing.
    """

    def __init__(self, exit_event):
        super().__init__()
        self.logged_in = False


if __name__ == "__main__":
    glbs = Globals(exit_event=None)
