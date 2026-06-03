"""Auto login task for Infinity Nikki.

Detects the login button on the login screen and clicks it.
"""

from ok import TriggerTask

from src.features import LOGIN_BUTTON


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
        login_btn = self.find_one(LOGIN_BUTTON, threshold=0.8)
        if login_btn:
            self.log_info("Found login button, clicking...")
            self.click_box(login_btn, after_sleep=3)
