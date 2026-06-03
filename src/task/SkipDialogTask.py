"""Skip dialog task for Infinity Nikki.

Automatically skips story dialogues and cutscenes.
"""

from ok import TriggerTask

from src.features import SKIP_BUTTON


class SkipDialogTask(TriggerTask):
    """Auto-skip dialogues in Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {
            "_enabled": False,
        }
        self.trigger_interval = 0.5

    def run(self):
        """Skip any visible dialogue."""
        skip_btn = self.find_one(SKIP_BUTTON, threshold=0.8)
        if skip_btn:
            self.click_box(skip_btn, after_sleep=0.2)
            self.log_debug("Skipped dialog")
