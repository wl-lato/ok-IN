"""AutoLoginTask: auto login trigger task for Infinity Nikki.

Aligned with ok-ww/src/task/AutoLoginTask.py:
- Inherits BaseINTask (provides logged_in property via og.my_app)
- Inherits TriggerTask (periodic trigger)
- Uses scene.in_team() lazy-load cache pattern from INScene
- Confirms login by waiting for in_team_and_world() state
"""

from qfluentwidgets import FluentIcon

from ok import TriggerTask, Logger

from src.Labels import Labels
from src.task.BaseINTask import BaseINTask

logger = Logger.get_logger(__name__)


class AutoLoginTask(BaseINTask, TriggerTask):
    """Automatically login to Infinity Nikki after game starts.

    Aligned with ok-ww AutoLoginTask:
    - Uses logged_in property (via og.my_app.logged_in)
    - Uses scene.in_team() for lazy-load caching
    - Waits for in_team_and_world() confirmation after clicking login
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {"_enabled": True}
        self.trigger_interval = 5
        self.name = "Auto Login"
        self.description = "Auto Login After Game Starts"
        self.icon = FluentIcon.ACCEPT

    def run(self):
        if self.logged_in:
            # Already logged in, nothing to do
            pass
        elif self.scene.in_team(self.in_team_and_world):
            # in_team_and_world returned True, confirm login
            self.logged_in = True
        else:
            # Try to click login button
            return self._wait_login()

    def _wait_login(self):
        """Find and click the login button, then wait for confirmation."""
        login_btn = self.find_one(Labels.login_button, threshold=0.8)
        if not login_btn:
            return

        self.log_info("Found login button, clicking...")
        self.click_box(login_btn, after_sleep=3)

        # Wait for login to complete: hud_pearpal should appear
        if self.wait_until(self.in_team_and_world, time_out=60, raise_if_not_found=False):
            self.logged_in = True
            self.log_info("Login confirmed: in game world.")
        else:
            self.log_info("Login button clicked but game not ready yet.")
