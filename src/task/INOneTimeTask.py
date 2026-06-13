"""INOneTimeTask: mixin for one-time tasks in Infinity Nikki.

Mirrors src/task/WWOneTimeTask.py from ok-ww.
Activates PostMessageInteraction before executing the task.

Note: ok-ww also runs MouseResetTask here, but ok-IN does not have
a MouseResetTask (no mouse displacement issue in Infinity Nikki).
"""
from ok import PostMessageInteraction


class INOneTimeTask:
    """Mixin class for one-time tasks.

    Mirrors WWOneTimeTask from ok-ww.
    All one-time tasks should include this mixin in their inheritance.
    """

    def run(self):
        # Activate interaction for PostMessageInteraction
        if isinstance(self.executor.interaction, PostMessageInteraction):
            self.executor.interaction.activate()
        self.sleep(0.5)
