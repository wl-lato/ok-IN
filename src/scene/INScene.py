"""Infinity Nikki scene detection module.

Extends ok.BaseScene for state caching.
BaseScene only has reset() method; actual scene detection is done in tasks via find_one().
"""

from ok import BaseScene


class INScene(BaseScene):
    """Scene state cache for Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_hud = None

    def reset(self):
        """Reset cached scene state."""
        self._in_hud = None

    def in_hud(self):
        return self._in_hud

    def set_in_hud(self, value=True):
        self._in_hud = value
