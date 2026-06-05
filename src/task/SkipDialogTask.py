"""Skip dialog task for Infinity Nikki.

Automatically skips story dialogues and cutscenes.
Pattern: inherits TriggerTask (which extends BaseTask, like ok-ww AutoDialogTask).
"""

from ok import TriggerTask, Logger

from src.features import SKIP_BUTTON

logger = Logger.get_logger(__name__)


class SkipDialogTask(TriggerTask):
    """Auto-skip dialogues in Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {'_enabled': False}
        self.trigger_interval = 0.5
        self.name = "Skip Dialog"

    def run(self):
        skip_btn = self.find_one(SKIP_BUTTON, threshold=0.8)
        if skip_btn:
            self.click_box(skip_btn, after_sleep=0.2)
            self.log_debug("Skipped dialog")
