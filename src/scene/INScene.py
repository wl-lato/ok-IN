"""Infinity Nikki scene detection module.

Responsible for identifying the current game state/screen,
such as main menu, loading, combat, daily wishes, etc.
"""

from ok import Scene


class INScene(Scene):
    """Scene detection for Infinity Nikki."""

    # Scene type constants
    SCENE_UNKNOWN = "unknown"
    SCENE_LOADING = "loading"
    SCENE_MAIN_MENU = "main_menu"
    SCENE_IN_GAME = "in_game"
    SCENE_PAUSE_MENU = "pause_menu"
    SCENE_DAILY_WISHES = "daily_wishes"
    SCENE_REALM = "realm"
    SCENE_PEAR_PAL = "pear_pal"
    SCENE_MAIL = "mail"
    SCENE_DIALOG = "dialog"
    SCENE_LOGIN = "login"
    SCENE_MONTHLY_CARD = "monthly_card"

    def detect_scene(self):
        """Detect the current game scene.

        Returns:
            str: The detected scene type constant.
        """
        # Priority order: popup scenes first, then main scenes
        # Check for monthly card popup (can interrupt any flow)
        if self.find_one("monthly_card", threshold=0.8):
            return self.SCENE_MONTHLY_CARD

        # Check for dialog/popup
        if self.find_one("dialog_close", threshold=0.8):
            return self.SCENE_DIALOG

        # Check for loading screen
        if self.find_one("loading_icon", threshold=0.7):
            return self.SCENE_LOADING

        # Check for login screen
        if self.find_one("login_button", threshold=0.8):
            return self.SCENE_LOGIN

        # Check for pause menu
        if self.find_one("pause_menu_title", threshold=0.8):
            return self.SCENE_PAUSE_MENU

        # Check for daily wishes screen
        if self.find_one("daily_wishes_title", threshold=0.8):
            return self.SCENE_DAILY_WISHES

        # Check for realm entrance
        if self.find_one("realm_entrance", threshold=0.8):
            return self.SCENE_REALM

        # Check for Pear-Pal screen
        if self.find_one("pear_pal_icon", threshold=0.8):
            return self.SCENE_PEAR_PAL

        # Check for mail screen
        if self.find_one("mail_icon", threshold=0.8):
            return self.SCENE_MAIL

        # Check for in-game (main HUD visible)
        if self.find_one("hud_minimap", threshold=0.7):
            return self.SCENE_IN_GAME

        return self.SCENE_UNKNOWN
