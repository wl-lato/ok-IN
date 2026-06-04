"""Infinity Nikki scene detection module.

Extends ok.BaseScene for state caching.
BaseScene only has reset() method; actual scene detection is done in tasks via find_one().

Scene states are tracked as instance attributes (not class constants)
because scene detection depends on runtime UI recognition.
"""

from ok import BaseScene


class INScene(BaseScene):
    """Scene state cache for Infinity Nikki.

    Scene states are detected by tasks and cached here for cross-task access.
    reset() is called by the task executor between tasks.
    """

    SCENE_UNKNOWN = 0
    SCENE_LOADING = 1
    SCENE_IN_GAME = 2       # HUD visible (main game screen)
    SCENE_DAILY_WISHES = 3  # 朝夕心愿 page open
    SCENE_REALM = 4         # 幻境 page open
    SCENE_JOURNEY = 5       # 奇迹之旅 page open

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_hud = None
        self._current_scene = self.SCENE_UNKNOWN

    def reset(self):
        """Reset cached scene state."""
        self._in_hud = None
        self._current_scene = self.SCENE_UNKNOWN

    @property
    def current_scene(self):
        return self._current_scene

    @current_scene.setter
    def current_scene(self, value):
        self._current_scene = value

    def in_hud(self):
        return self._in_hud

    def set_in_hud(self, value=True):
        self._in_hud = value
        if value:
            self._current_scene = self.SCENE_IN_GAME
