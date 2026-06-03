"""Infinity Nikki scene detection module.

Identifies the current game screen based on UI template matching.
Scene hierarchy:
  HUD (main game) ─┬─ 美鸭梨平板 ─┬─ 美鸭梨挖掘
                    │              └─ 邮件
                    ├─ 奇想日历 ─┬─ 朝夕心愿
                    │            └─ 幻境挑战
                    └─ 奇迹之旅
"""

from ok import Scene

from src.features import (
    HUD_PEARPAL,
    LOGIN_BUTTON,
    CALENDAR_DAILY,
    CALENDAR_REALM,
    PEARPAL_MINING,
    PEARPAL_MAIL,
    HUD_MIRACLE,
    JOURNEY_TASKS,
    JOURNEY_REWARDS,
    BACK_BUTTON,
)


class INScene(Scene):
    """Scene detection for Infinity Nikki."""

    # Scene constants
    UNKNOWN = "unknown"
    LOGIN = "login"
    HUD = "hud"
    PEAR_PAL = "pear_pal"           # 美鸭梨平板主界面
    PEAR_PAL_MINING = "pear_pal_mining"  # 美鸭梨挖掘
    PEAR_PAL_MAIL = "pear_pal_mail"  # 邮件界面
    CALENDAR = "calendar"           # 奇想日历
    DAILY_WISHES = "daily_wishes"   # 朝夕心愿
    REALM = "realm"                 # 幻境挑战
    MIRACLE_JOURNEY = "miracle_journey"  # 奇迹之旅
    JOURNEY_TASKS = "journey_tasks"  # 奇迹之旅-任务列表
    JOURNEY_REWARDS = "journey_rewards"  # 奇迹之旅-奖励页面

    # Detection priority: specific sub-screens first, general screens last
    SCENE_FEATURES = [
        # (scene_name, feature_name, threshold)
        (LOGIN, LOGIN_BUTTON, 0.8),
        (PEAR_PAL_MINING, PEARPAL_MINING, 0.8),
        (PEAR_PAL_MAIL, PEARPAL_MAIL, 0.8),
        (CALENDAR, CALENDAR_DAILY, 0.8),  # 朝夕心愿 tab visible = on calendar
        (CALENDAR, CALENDAR_REALM, 0.8),  # 每日幻境 tab visible = on calendar
        (JOURNEY_TASKS, JOURNEY_TASKS, 0.8),
        (JOURNEY_REWARDS, JOURNEY_REWARDS, 0.8),
        (HUD, HUD_PEARPAL, 0.8),
    ]

    def detect_scene(self):
        """Detect the current game scene by template matching.

        Returns:
            str: The detected scene type constant.
        """
        for scene_name, feature_name, threshold in self.SCENE_FEATURES:
            if self.find_one(feature_name, threshold=threshold):
                return scene_name
        return self.UNKNOWN
