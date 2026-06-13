"""Daily task for Infinity Nikki - one-click daily routine.

Aligned with ok-ww/src/task/DailyTask.py structure:
- Inherits from INOneTimeTask + BaseINTask (mirrors WWOneTimeTask + BaseWWTask)
- Feature masks are loaded via process_feature.py (registered in config.py),
  NOT via _setup_feature_masks() in run().

Complete daily workflow based on logic doc:
1. Navigate to HUD
2. 美鸭梨挖掘 (Pear-Pal Mining)
3. 邮件领取 (Claim Mail)
4. 奇迹之旅 (Miracle Journey)
5. 幻境挑战 (Realm Challenge)
6. 朝夕心愿 (Daily Wishes)
"""

import re

from qfluentwidgets import FluentIcon

from ok import Logger

from src.Labels import Labels
from src.task.BaseINTask import BaseINTask
from src.task.INOneTimeTask import INOneTimeTask

logger = Logger.get_logger(__name__)

# ── Constants ──────────────────────────────────────────────
REALM_TRIAL_TYPE = "魔物试炼"
REALM_BLESSING_TYPE = "祝福闪光"
REALM_ESCALATION_TYPE = "素材激化"

VITALITY_COST_TRIAL = 40
VITALITY_COST_BLESSING = 40
VITALITY_COST_ESCALATION = 10

INSPIRATION_GOAL = 500
INSPIRATION_LV1 = 100
INSPIRATION_LV2 = 200

WISH_WEIGHTS = {
    Labels.wish_photo: ("1级", 1, INSPIRATION_LV1),
    Labels.wish_upgrade: ("1级", 2, INSPIRATION_LV1),
    Labels.wish_energy: ("2级", 3, INSPIRATION_LV2),
    Labels.wish_collect: ("2级", 2, INSPIRATION_LV2),
    Labels.wish_escalation: ("2级", 4, INSPIRATION_LV2),
}


class DailyTask(INOneTimeTask, BaseINTask):
    """One-click daily task for Infinity Nikki.

    Aligned with ok-ww DailyTask.py:
    - Inherits INOneTimeTask (runs MouseResetTask + activates interaction before main logic)
    - Inherits BaseINTask (provides ensure_main, in_team_and_world, logged_in, etc.)
    - Feature masks are auto-loaded via feature_processor registered in config.py
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Daily Task"
        self.group_name = "Daily"
        self.group_icon = FluentIcon.CALENDAR
        self.icon = FluentIcon.CAR
        self.support_schedule_task = True
        self.description = "一键日常：美鸭梨挖掘、邮件领取、奇迹之旅、幻境挑战、朝夕心愿"
        self.default_config = {
            "美鸭梨挖掘": True,
            "邮件领取": True,
            "奇迹之旅": True,
            "幻境挑战": True,
            "幻境类型": REALM_TRIAL_TYPE,
            "朝夕心愿": True,
        }
        self.config_type = {
            "幻境类型": {
                "type": "drop_down",
                "options": [REALM_TRIAL_TYPE, REALM_BLESSING_TYPE, REALM_ESCALATION_TYPE],
            },
        }
        self.config_description = {
            "美鸭梨挖掘": "美鸭梨挖掘并领取奖励",
            "邮件领取": "领取所有邮件奖励",
            "奇迹之旅": "完成奇迹之旅任务和奖励领取",
            "幻境挑战": "消耗活力完成幻境挑战",
            "幻境类型": "选择幻境类型",
            "朝夕心愿": "完成朝夕心愿获取500灵感",
        }
        self.add_exit_after_config()

    # ── Main Entry (mirrors ok-ww DailyTask.run()) ─────────

    def run(self):
        """Main entry point aligned with ok-ww pattern."""
        # INOneTimeTask.run() activates MouseResetTask and PostMessageInteraction
        INOneTimeTask.run(self)

        self.logged_in = False

        # Wait for game to be at main screen (with extended timeout for first login)
        # NOTE: ensure_main is inherited from BaseINTask (mirrors BaseWWTask.ensure_main)
        self.ensure_main(time_out=180)

        self.info_set("Status", "Running")

        self._navigate_to_hud()

        if self.config.get("美鸭梨挖掘"):
            self._pear_pal_mining()
        if self.config.get("邮件领取"):
            self._claim_mail()
        if self.config.get("奇迹之旅"):
            self._miracle_journey()
        if self.config.get("幻境挑战"):
            self._realm_challenge()
        if self.config.get("朝夕心愿"):
            self._daily_wishes()

        self.info_set("Status", "Completed")
        self.log_info("Daily task completed!", notify=True)

    # ── Navigation Helpers ─────────────────────────────────

    def _navigate_to_hud(self):
        """Navigate to HUD (main game) from any state.

        Mirrors ok-ww pattern: keep pressing ESC / clicking back
        until hud_pearpal icon is visible.
        """
        if self.find_one(Labels.hud_pearpal, threshold=0.8):
            return
        for _ in range(10):
            back = self.find_one(Labels.back_button, threshold=0.8)
            if back:
                self.click_box(back, after_sleep=0.5)
            else:
                self.send_key("esc", after_sleep=0.5)
            if self.find_one(Labels.hud_pearpal, threshold=0.8):
                return
        raise RuntimeError("Failed to navigate to HUD after 10 attempts")

    def _go_back(self, times=1):
        """Press ESC or click back button (inherited from BaseINTask.back)."""
        self.back(times=times, after_sleep=0.5)

    def _check_claim_done(self, timeout=1):
        """Check if claim was successful (claim_done indicator visible)."""
        if self.find_one(Labels.claim_done, threshold=0.8):
            return True
        self.sleep(timeout)
        return self.find_one(Labels.claim_done, threshold=0.8) is not None

    # ── 1. 美鸭梨挖掘 ───────────────────────────────────────

    def _pear_pal_mining(self):
        self.log_info("Starting Pear-Pal Mining...")
        self.info_set("Step", "美鸭梨挖掘")

        self._navigate_to_hud()
        hud = self.find_one(Labels.hud_pearpal, threshold=0.8)
        if hud:
            self.click_box(hud, after_sleep=1)
        else:
            self.log_info("Cannot find hud_pearpal, skipping mining.")

        # Claim and re-dig loop
        for attempt in range(3):
            if self.find_one(Labels.mining_claim, threshold=0.8):
                self.click(self.find_one(Labels.mining_claim), after_sleep=0.5)
                self.log_info("Claimed mining reward.")
            if self.find_one(Labels.mining_redig, threshold=0.8):
                self.click(self.find_one(Labels.mining_redig), after_sleep=0.5)
                self.log_info(f"Re-dig attempt {attempt + 1}.")
                continue
            break

        self._go_back(2)
        self.log_info("Pear-Pal Mining done.")

    # ── 2. 邮件领取 ────────────────────────────────────────

    def _claim_mail(self):
        self.log_info("Starting Mail Claim...")
        self.info_set("Step", "邮件领取")

        self._navigate_to_hud()
        hud = self.find_one(Labels.hud_pearpal, threshold=0.8)
        if hud:
            self.click_box(hud, after_sleep=1)

        mail_btn = self.find_one(Labels.pearpal_mail, threshold=0.8)
        if mail_btn:
            self.click_box(mail_btn, after_sleep=1)
        else:
            self.log_info("Cannot find mail button, skipping mail claim.")
            return

        # Claim all mail items
        claimed = 0
        for _ in range(20):
            claim = self.find_one(Labels.mail_claim, threshold=0.8)
            if claim:
                self.click_box(claim, after_sleep=0.3)
                claimed += 1
            else:
                break
        self.log_info(f"Claimed {claimed} mail items.")

        self._go_back(2)
        self.log_info("Mail Claim done.")

    # ── 3. 奇迹之旅 ────────────────────────────────────────

    def _miracle_journey(self):
        self.log_info("Starting Miracle Journey...")
        self.info_set("Step", "奇迹之旅")

        self._navigate_to_hud()
        miracle = self.find_one(Labels.hud_miracle, threshold=0.8)
        if miracle:
            self.click_box(miracle, after_sleep=1)
        else:
            self.log_info("Cannot find miracle journey, skipping.")
            return

        # Skip dialogs
        for _ in range(5):
            skip1 = self.find_one(Labels.journey_skip, threshold=0.8)
            skip2 = self.find_one(Labels.journey_skip2, threshold=0.8)
            if skip1:
                self.click_box(skip1, after_sleep=0.3)
            elif skip2:
                self.click_box(skip2, after_sleep=0.3)
            else:
                break

        # Click tasks and claim rewards
        tasks = self.find_one(Labels.journey_tasks, threshold=0.8)
        if tasks:
            self.click_box(tasks, after_sleep=1)

        claim = self.find_one(Labels.journey_claim, threshold=0.8)
        if claim:
            self.click_box(claim, after_sleep=1)
            self.log_info("Claimed journey rewards.")

        rewards = self.find_one(Labels.journey_rewards, threshold=0.8)
        if rewards:
            self.click_box(rewards, after_sleep=1)

        self._go_back()
        self.log_info("Miracle Journey done.")

    # ── 4. 幻境挑战 ────────────────────────────────────────

    def _realm_challenge(self):
        self.log_info("Starting Realm Challenge...")
        self.info_set("Step", "幻境挑战")

        realm_type = self.config.get("幻境类型", REALM_TRIAL_TYPE)
        self._navigate_to_realm()

        vitality = self._read_vitality()
        if vitality is None:
            self.log_info("Cannot read vitality, proceeding anyway.")
            vitality = 999

        if realm_type == REALM_TRIAL_TYPE:
            self._realm_trial(vitality)
        elif realm_type == REALM_BLESSING_TYPE:
            self._realm_blessing(vitality)
        elif realm_type == REALM_ESCALATION_TYPE:
            self._realm_escalation(vitality)

        self._navigate_to_hud()
        self.log_info(f"Realm Challenge ({realm_type}) done.")

    def _navigate_to_realm(self):
        self._navigate_to_hud()
        cal_btn = self.find_one(Labels.hud_calendar, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        self.wait_click_feature(Labels.calendar_realm, time_out=5,
                               raise_if_not_found=True, after_sleep=1)

    def _read_vitality(self):
        vitality_area = self.find_one(Labels.realm_vitality, threshold=0.7)
        if not vitality_area:
            return None
        result = self.ocr(box=vitality_area, match=re.compile(r"(\d+)/(\d+)"))
        if result and len(result) > 0:
            text = result[0].name if hasattr(result[0], "name") else str(result[0])
            match = re.search(r"(\d+)", text)
            if match:
                return int(match.group(1))
        return None

    def _check_vitality(self, vitality, required):
        if vitality < required:
            self.log_info(f"Insufficient vitality: {vitality}/{required}")
            self._go_back()
            return False
        return True

    def _realm_trial(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_TRIAL):
            return
        self.wait_click_feature(Labels.realm_trial, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_quick, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_max_y, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_claim, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back()

    def _realm_blessing(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_BLESSING):
            return
        self.wait_click_feature(Labels.realm_blessing, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_quick, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_max_y, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.trial_claim, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back()

    def _realm_escalation(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_ESCALATION):
            return
        self.wait_click_feature(Labels.realm_escalation, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.escalation_go, time_out=3,
                               raise_if_not_found=True, after_sleep=1)
        # Wait for inside realm
        self.wait_feature(Labels.escalation_inside, time_out=30,
                         raise_if_not_found=True)
        # Walk to platform
        for _ in range(20):
            self.send_key("w", after_sleep=0.3)
            if self.find_one(Labels.escalation_platform, threshold=0.8):
                break
        else:
            self.log_info("Could not find escalation platform after walking.")
            return
        self.send_key("f", after_sleep=1)
        self.wait_click_feature(Labels.escalation_bubble, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(Labels.escalation_quality, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(Labels.escalation_quantity, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(Labels.escalation_sort, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        redbox = self.find_one(Labels.escalation_redbox, threshold=0.7)
        if redbox:
            self.click_box(redbox, after_sleep=0.3)
        else:
            self.log_info("Could not find red box area.")
        self.wait_click_feature(Labels.escalation_max_y, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(Labels.confirm_button, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.escalation_activate, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.send_key("f", after_sleep=0.5)
        self._check_claim_done()
        self.send_key("esc", after_sleep=0.5)
        self.send_key("backspace", after_sleep=0.5)

    # ── 5. 朝夕心愿 ────────────────────────────────────────

    def _daily_wishes(self):
        self.log_info("Starting Daily Wishes...")
        self.info_set("Step", "朝夕心愿")

        self._navigate_to_daily_wishes()

        inspiration = self._read_inspiration()
        self.log_info(f"Current inspiration: {inspiration}")

        if inspiration >= INSPIRATION_GOAL:
            self.log_info("Already at 500 inspiration, claiming reward.")
            self._claim_daily_reward()
            self._go_back()
            return

        available_tasks = self._detect_available_tasks()
        self.log_info(f"Available tasks: {[t[0].value for t in available_tasks]}")

        needed = INSPIRATION_GOAL - inspiration
        selected = self._select_tasks(available_tasks, needed)
        self.log_info(f"Selected tasks: {[(t[0].value, t[3]) for t in selected]}")

        for task_feature, task_level, weight, task_name in selected:
            self._execute_wish_task(task_feature, task_name)
            self._navigate_to_daily_wishes()

        inspiration = self._read_inspiration()
        self.log_info(f"Inspiration after tasks: {inspiration}")

        if inspiration >= INSPIRATION_GOAL:
            self._claim_daily_reward()
        else:
            self.log_info(f"Warning: inspiration is {inspiration}, expected 500.")

        self._go_back()
        self.log_info("Daily Wishes done.")

    def _navigate_to_daily_wishes(self):
        self._navigate_to_hud()
        cal_btn = self.find_one(Labels.hud_calendar, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        self.wait_click_feature(Labels.calendar_daily, time_out=5,
                               raise_if_not_found=True, after_sleep=1)

    def _read_inspiration(self):
        progress_area = self.find_one(Labels.daily_progress, threshold=0.7)
        if not progress_area:
            return 0
        result = self.ocr(box=progress_area, match=re.compile(r"\d+"))
        if result and len(result) > 0:
            text = result[0].name if hasattr(result[0], "name") else str(result[0])
            match = re.search(r"\d+", text)
            if match:
                return int(match.group())
        return 0

    def _claim_daily_reward(self):
        self.wait_click_feature(Labels.daily_claim_reward, time_out=3,
                               raise_if_not_found=False, after_sleep=0.5)

    def _detect_available_tasks(self):
        available = []
        for feature, (level, weight, points) in WISH_WEIGHTS.items():
            if self.find_one(feature, threshold=0.8):
                available.append((feature, level, weight, feature))
        return available

    def _select_tasks(self, available_tasks, needed):
        sorted_tasks = sorted(available_tasks, key=lambda t: t[2])
        selected = []
        remaining = needed
        for task in sorted_tasks:
            if remaining <= 0:
                break
            feature, level, weight, name = task
            points = WISH_WEIGHTS[feature][2]
            selected.append(task)
            remaining -= points
        return selected

    def _execute_wish_task(self, task_feature, task_name):
        if task_feature == Labels.wish_photo:
            self._wish_task_photo()
        elif task_feature == Labels.wish_upgrade:
            self._wish_task_upgrade()
        elif task_feature == Labels.wish_energy:
            self._wish_task_energy()
        elif task_feature == Labels.wish_collect:
            self._wish_task_collect()
        elif task_feature == Labels.wish_escalation:
            self._wish_task_escalation()

    def _wish_task_photo(self):
        """4.1 - 拍照"""
        self.log_info("Wish task: 拍照")
        self._go_back(2)
        self._navigate_to_hud()
        self.send_key("p", after_sleep=1)
        self.send_key("space", after_sleep=0.5)
        self.wait_click_feature(Labels.photo_delete, time_out=3,
                               raise_if_not_found=False, after_sleep=0.3)
        self.wait_click_feature(Labels.confirm_button, time_out=3,
                               raise_if_not_found=False, after_sleep=0.3)
        self._go_back()

    def _wish_task_upgrade(self):
        """4.2 - 升级祝福闪光"""
        self.log_info("Wish task: 升级祝福闪光")
        self.wait_click_feature(Labels.wish_upgrade, time_out=3,
                               raise_if_not_found=False, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_go, time_out=3,
                               raise_if_not_found=True, after_sleep=1)
        self.wait_click_feature(Labels.wish_sort, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_upgrade_btn, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_select_mat, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_add, time_out=3,
                               raise_if_not_found=True, after_sleep=0.3)
        for _ in range(4):
            self.wait_click_feature(Labels.wish_add_one, time_out=2,
                                  raise_if_not_found=True, after_sleep=0.2)
        self.wait_click_feature(Labels.confirm_button, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_upgrade_btn, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back(2)

    def _wish_task_energy(self):
        """4.3 - 消耗活跃能量"""
        self.log_info("Wish task: 消耗活跃能量")
        if self.find_one(Labels.wish_escalation, threshold=0.8):
            self.log_info("素材激化 task exists, treating energy task as done.")
            return
        self.wait_click_feature(Labels.wish_energy, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_go, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        realm_type = self.config.get("幻境类型")
        vitality = self._read_vitality()
        if not self.find_one(Labels.realm_trial, threshold=0.7):
            self._navigate_to_realm()
        if realm_type == REALM_TRIAL_TYPE:
            self._realm_trial(vitality or 999)
        elif realm_type == REALM_BLESSING_TYPE:
            self._realm_blessing(vitality or 999)
        elif realm_type == REALM_ESCALATION_TYPE:
            self._realm_escalation(vitality or 999)
        self._navigate_to_daily_wishes()

    def _wish_task_collect(self):
        """4.4 - 采集植物 (v1.0 跳过)"""
        self.log_info("Wish task: 采集植物 - SKIPPED (not automatable in v1.0)")

    def _wish_task_escalation(self):
        """4.5 - 素材激化"""
        self.log_info("Wish task: 素材激化")
        self.wait_click_feature(Labels.wish_escalation, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(Labels.wish_go, time_out=3,
                               raise_if_not_found=True, after_sleep=0.5)
        vitality = self._read_vitality() or 999
        if not self.find_one(Labels.realm_trial, threshold=0.7):
            self._navigate_to_realm()
        self._realm_escalation(vitality)
        self._navigate_to_daily_wishes()


if __name__ == "__main__":
    from ok import run_task
    from src.config import config
    run_task(config, task=DailyTask, debug=True)
