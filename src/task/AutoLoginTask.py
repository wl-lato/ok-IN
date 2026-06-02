"""Auto login task for Infinity Nikki.

Handles automatic login and server selection.
"""

import re

from ok import TriggerTask


class AutoLoginTask(TriggerTask):
    """Automatically login to Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {
            "_enabled": True,
        }
        self.trigger_interval = 2

    def run(self):
        """Handle login screen."""
        # Check if we're on the login screen
        login_btn = self.find_one("login_button", threshold=0.8)
        if login_btn:
            self.log_info("Found login button, clicking...")
            self.click_box(login_btn, after_sleep=3)

        # Handle server selection if needed
        server_confirm = self.find_one("server_confirm_button", threshold=0.8)
        if server_confirm:
            self.log_info("Confirming server selection...")
            self.click_box(server_confirm, after_sleep=3)

        # Handle "Start Game" button
        start_btn = self.find_one("start_game_button", threshold=0.8)
        if start_btn:
            self.log_info("Clicking Start Game...")
            self.click_box(start_btn, after_sleep=5)

        # Dismiss any announcements/news popups
        announcement_close = self.find_one("announcement_close", threshold=0.8)
        if announcement_close:
            self.click_box(announcement_close, after_sleep=0.5)

        # Dismiss event popups
        event_close = self.find_one("event_popup_close", threshold=0.8)
        if event_close:
            self.click_box(event_close, after_sleep=0.5)
