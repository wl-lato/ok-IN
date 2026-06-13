"""INOneTimeTask: mixin for one-time tasks in Infinity Nikki.

Mirrors src/task/WWOneTimeTask.py from ok-ww.
Runs mouse reset and activates interaction before executing the task.
"""

from ok import BrowserInteraction, PostMessageInteraction


class INOneTimeTask:
    """Mixin class for one-time tasks.

    Mirrors WWOneTimeTask from ok-ww.
    All one-time tasks should include this mixin in their inheritance.
    """

    def run(self):
        # Activate mouse reset if available
        try:
            from src.task.MouseResetTask import MouseResetTask
            mouse_reset_task = self.executor.get_task_by_class(MouseResetTask)
            mouse_reset_task.run()
        except Exception:
            pass

        # Activate interaction for PostMessageInteraction
        if isinstance(self.executor.interaction, PostMessageInteraction):
            self.executor.interaction.activate()
        self.sleep(0.5)
