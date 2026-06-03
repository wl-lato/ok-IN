"""Auto login task for Infinity Nikki.

Detects the login button on the login screen and clicks it.
Pattern: inherits BaseTask + TriggerTask (like ok-ww AutoLoginTask).
"""

from ok import BaseTask, TriggerTask, Logger

from src.features import LOGIN_BUTTON

logger = Logger.get_logger(__name__)


class AutoLoginTask(BaseTask, TriggerTask):
    """Automatically login to Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {'_enabled': True}
        self.trigger_interval = 5
        self.name = "Auto Login"
        self.description = "Auto Login After Game Starts"

    def run(self):
        login_btn = self.find_one(LOGIN_BUTTON, threshold=0.8)
        if login_btn:
            self.log_info("Found login button, clicking...")
            self.click_box(login_btn, after_sleep=3)
