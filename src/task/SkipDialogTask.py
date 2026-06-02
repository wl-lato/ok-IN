"""Skip dialog task for Infinity Nikki.

Automatically skips story dialogues and cutscenes.
"""

from ok import TriggerTask


class SkipDialogTask(TriggerTask):
    """Auto-skip dialogues in Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {
            "_enabled": False,
            "Skip Speed": "Fast",
        }
        self.config_type = {
            "Skip Speed": {
                "options": ["Normal", "Fast"],
            },
        }
        self.trigger_interval = 0.5

    def run(self):
        """Skip any visible dialogue."""
        # Look for skip button
        skip_btn = self.find_one("dialog_skip_button", threshold=0.8)
        if skip_btn:
            self.click_box(skip_btn, after_sleep=0)
            self.log_debug("Skipped dialog")

        # Also try clicking through dialog by pressing Space/Enter
        dialog_next = self.find_one("dialog_next_indicator", threshold=0.7)
        if dialog_next:
            self.send_key("space", after_sleep=0)
