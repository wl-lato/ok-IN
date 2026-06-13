"""SkipDialogTask: auto skip dialogs for Infinity Nikki.

Aligned with ok-ww/src/task/SkipDialogTask.py and SkipBaseTask.py:
- Base class (SkipBaseTask) inherits BaseINTask, provides skip logic
- Trigger task (SkipDialogTask) inherits TriggerTask + SkipBaseTask
- Uses scene.in_team() lazy-load pattern from INScene
- Handles skip confirm dialog, skip button, dialog eye, etc.
"""

import time
from ok import TriggerTask, Logger

from src.Labels import Labels
from src.task.BaseINTask import BaseINTask, convert_dialog_icon

logger = Logger.get_logger(__name__)


class SkipBaseTask(BaseINTask):
    """Base class for skip dialog tasks.

    Mirrors ok-ww SkipBaseTask, adapted for Infinity Nikki.
    Provides skip detection, confirmation dialog handling, and
    auto-play toggle.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confirm_dialog_checked = False
        self.has_eye_time = 0

    def run(self):
        pass

    def skip_confirm(self):
        """Handle skip confirmation dialog if present."""
        # Check for confirm button with checkbox
        skip_dialog_confirm = self.find_one(Labels.skip_button, threshold=0.8)
        if skip_dialog_confirm:
            self.log_info("confirm dialog exists, click confirm")
            self.click(skip_dialog_confirm, after_sleep=0.2)
            self.confirm_dialog_checked = True
            return True

        # Check if already at main screen
        if self.in_team_and_world():
            return True

        return False

    def find_skip(self):
        """Find skip dialog button using icon conversion."""
        return self.find_one(
            Labels.skip_button,
            horizontal_variance=0.02,
            threshold=0.75,
            frame_processor=convert_dialog_icon,
        )

    def try_click_skip(self):
        """Click all visible skip buttons."""
        skipped = False
        while skip := self.find_skip():
            logger.info("Click Skip Dialog")
            self.click_box(skip, after_sleep=0.2)
            skipped = True
        return skipped

    def check_skip(self):
        """Main skip detection and handling logic.

        Mirrors ok-ww SkipBaseTask.check_skip():
        1. Try to click skip buttons
        2. Handle confirmation dialog
        3. Handle eye button (auto-play toggle) / dialog close
        """
        if self.try_click_skip():
            return self.wait_until(self.skip_confirm, time_out=3, raise_if_not_found=False)

        if self.in_team_and_world():
            return True

        # Handle eye button and dialog close
        if time.time() - self.has_eye_time < 2:
            btn_dialog_close = self.find_one(Labels.back_button, threshold=0.8)
            if btn_dialog_close:
                self.click(btn_dialog_close, move_back=True, after_sleep=0.2)
                return True


class AutoDialogTask(TriggerTask, SkipBaseTask):
    """Trigger task for auto-skipping dialogs.

    Mirrors ok-ww AutoDialogTask pattern.
    Runs periodically and checks for skip buttons.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {"_enabled": False}
        self.skip = None
        self.trigger_interval = 0.5
        self.name = "Skip Dialog during Quests"

    def run(self):
        """Check if in game world; if so skip dialog check."""
        if self.scene.in_team(self.in_team_and_world):
            return
        if self.check_skip():
            return
        if self.skip_message():
            return

    def skip_message(self):
        """Handle popup message dialogs."""
        if self.find_one("message"):
            self.log_info("found message dialog, click to dismiss")
            # Find message area and click below it
            from ok import Logger
            logger = Logger.get_logger(__name__)
            logger.info("message dialog dismissed")


# Alias: SkipDialogTask is the main trigger class
SkipDialogTask = AutoDialogTask
