"""INScene: scene state cache for Infinity Nikki.

Mirrors src/scene/WWScene.py from ok-ww.
Lazy-loading cache pattern: scene states are computed once and cached
until reset() is called by the task executor.
"""

from ok import BaseScene, Logger

logger = Logger.get_logger(__name__)


class INScene(BaseScene):
    """Scene state cache for Infinity Nikki.

    Mirrors WWScene from ok-ww.
    All cached scene checks use lazy-loading: computed once on first access,
    then cached until reset() is called.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_team = None
        self._in_hud = None

    def reset(self):
        """Reset all cached scene states.

        Called by the task executor between tasks.
        """
        self._in_team = None
        self._in_hud = None

    def in_team(self, fun):
        """Lazy-load cached in_team state.

        Mirrors WWScene.in_team() pattern.

        Args:
            fun: Callable that performs the actual detection.

        Returns:
            Cached or freshly computed team state.
        """
        if self._in_team is None:
            self._in_team = fun()
        return self._in_team

    def in_hud(self, fun=None):
        """Lazy-load cached in_hud state.

        If fun is None, return the cached value directly.
        Otherwise compute via fun and cache.
        """
        if fun is None:
            return self._in_hud
        if self._in_hud is None:
            self._in_hud = fun()
        return self._in_hud

    def set_in_hud(self, value=True):
        """Manually set the in_hud cached state."""
        self._in_hud = value
        return value
