"""Daily task for Infinity Nikki - one-click daily routine.

Inherits BaseTask directly (no OneTimeTask class in ok-script).
"onetime_tasks" is just a config registration concept.

Complete daily workflow based on logic doc:
1. Navigate to HUD
2. 美鸭梨挖掘 (Pear-Pal Mining)
3. 邮件领取 (Claim Mail)
4. 奇迹之旅 (Miracle Journey)
5. 幻境挑战 (Realm Challenge)
6. 朝夕心愿 (Daily Wishes)
"""

import re

from ok import BaseTask, Logger

from src.features import (
    CONFIRM_BUTTON,
    BACK_BUTTON,
    CLAIM_DONE,
    HUD_PEARPAL,
    HUD_CALENDAR,
    HUD_MIRACLE,
    PEARPAL_MINING,
    MINING_CLAIM,
    MINING_REDIG,
    PEARPAL_MAIL,
    MAIL_CLAIM,
    JOURNEY_SKIP,
    JOURNEY_SKIP2,
    JOURNEY_TASKS,
    JOURNEY_CLAIM,
    JOURNEY_REWARDS,
    CALENDAR_DAILY,
    CALENDAR_REALM,
    DAILY_PROGRESS,
    DAILY_CLAIM_REWARD,
    REALM_VITALITY,
    REALM_TRIAL,
    TRIAL_QUICK,
    TRIAL_MAX_Y,
    TRIAL_CLAIM,
    REALM_BLESSING,
    REALM_ESCALATION,
    ESCALATION_GO,
    ESCALATION_INSIDE,
    ESCALATION_PLATFORM,
    ESCALATION_BUBBLE,
    ESCALATION_QUALITY,
    ESCALATION_QUANTITY,
    ESCALATION_SORT,
    ESCALATION_REDBOX,
    ESCALATION_MAX_Y,
    ESCALATION_ACTIVATE,
    WISH_PHOTO,
    PHOTO_DELETE,
    WISH_UPGRADE,
    WISH_GO,
    WISH_SORT,
    WISH_UPGRADE_BTN,
    WISH_SELECT_MAT,
    WISH_ADD,
    WISH_ADD_ONE,
    WISH_ENERGY,
    WISH_COLLECT,
    WISH_ESCALATION,
)

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
    WISH_PHOTO: ("1级", 1, INSPIRATION_LV1),
    WISH_UPGRADE: ("1级", 2, INSPIRATION_LV1),
    WISH_ENERGY: ("2级", 3, INSPIRATION_LV2),
    WISH_COLLECT: ("2级", 2, INSPIRATION_LV2),
    WISH_ESCALATION: ("2级", 4, INSPIRATION_LV2),
}


class DailyTask(BaseTask):
    """One-click daily task for Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Daily Task"
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

    # ── Main Entry ─────────────────────────────────────────

    def run(self):
        self.log_info("Starting daily task...")
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

        Keep pressing ESC / clicking back until 美鸭梨平板 icon is visible.
        """
        if self.find_one(HUD_PEARPAL, threshold=0.8):
            return
        for _ in range(10):
            back = self.find_one(BACK_BUTTON, threshold=0.8)
            if back:
                self.click_box(back, after_sleep=0.5)
            else:
                self.send_key("esc", after_sleep=0.5)
            if self.find_one(HUD_PEARPAL, threshold=0.8):
                return
        raise RuntimeError("Failed to navigate to HUD after 10 attempts")

    def _go_back(self, times=1):
        """Press ESC or click back button."""
        for _ in range(times):
            back = self.find_one(BACK_BUTTON, threshold=0.8)
            if back:
                self.click_box(back, after_sleep=0.5)
            else:
                self.send_key("esc", after_sleep=0.5)

    def _check_claim_done(self, timeout=1):
        """Check for 领完标志 in bottom-right corner. If found, press F."""
        self.sleep(timeout)
        if self.find_one(CLAIM_DONE, threshold=0.8):
            self.send_key("f", after_sleep=0.5)

    # ── 1. 美鸭梨挖掘 ─────────────────────────────────────

    def _pear_pal_mining(self):
        self.log_info("Starting Pear-Pal mining...")
        self.info_set("Step", "美鸭梨挖掘")

        self._navigate_to_hud()
        # 点击美鸭梨平板 (1.0)
        pearpal = self.find_one(HUD_PEARPAL, threshold=0.8)
        if pearpal:
            self.click_box(pearpal, after_sleep=1)
        else:
            self.send_key("esc", after_sleep=1)

        # 美鸭梨挖掘 (1.1.0)
        self.wait_click_feature(PEARPAL_MINING, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=1)
        # 领取 (1.1.1)
        self.wait_click_feature(MINING_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        # 再次挖掘 (1.1.2)
        self.wait_click_feature(MINING_REDIG, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        # 返回
        self._go_back()
        self.log_info("Pear-Pal mining done.")

    # ── 2. 邮件领取 ────────────────────────────────────────

    def _claim_mail(self):
        self.log_info("Claiming mail rewards...")
        self.info_set("Step", "邮件领取")

        if not self.find_one(PEARPAL_MAIL, threshold=0.8):
            self._navigate_to_hud()
            pearpal = self.find_one(HUD_PEARPAL, threshold=0.8)
            if pearpal:
                self.click_box(pearpal, after_sleep=1)
            else:
                self.send_key("esc", after_sleep=1)

        # 邮件 (1.2.0)
        self.wait_click_feature(PEARPAL_MAIL, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=1)
        # 领取 (1.2.1)
        self.wait_click_feature(MAIL_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        # 领完标志
        self._check_claim_done()
        # 返回
        self._go_back()
        self.log_info("Mail claimed.")

    # ── 3. 奇迹之旅 ────────────────────────────────────────

    def _miracle_journey(self):
        self.log_info("Starting Miracle Journey...")
        self.info_set("Step", "奇迹之旅")

        self._navigate_to_hud()

        # 进入奇迹之旅 (2.0 或 J键)
        hud_btn = self.find_one(HUD_MIRACLE, threshold=0.8)
        if hud_btn:
            self.click_box(hud_btn, after_sleep=1)
        else:
            self.send_key("j", after_sleep=1)

        # 检测跳过 (2.1)
        skip = self.find_one(JOURNEY_SKIP, threshold=0.8)
        if skip:
            self.send_key("f", after_sleep=0.5)
            self.wait_click_feature(JOURNEY_SKIP2, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # 任务列表 (2.3 或 E键)
        tasks_btn = self.find_one(JOURNEY_TASKS, threshold=0.8)
        if tasks_btn:
            self.click_box(tasks_btn, after_sleep=1)
        else:
            self.send_key("e", after_sleep=1)

        # 一键领取 (2.4)
        self.wait_click_feature(JOURNEY_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        self._check_claim_done()

        # 奖励页面 (2.5 或 Q键)
        rewards_btn = self.find_one(JOURNEY_REWARDS, threshold=0.8)
        if rewards_btn:
            self.click_box(rewards_btn, after_sleep=1)
        else:
            self.send_key("q", after_sleep=1)

        # 一键领取 (2.4)
        self.wait_click_feature(JOURNEY_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        self._check_claim_done()

        # 返回HUD
        self._go_back(2)
        self._navigate_to_hud()
        self.log_info("Miracle Journey done.")

    # ── 4. 幻境挑战 ────────────────────────────────────────

    def _realm_challenge(self):
        realm_type = self.config.get("幻境类型")
        self.log_info(f"Starting Realm Challenge: {realm_type}")
        self.info_set("Step", f"幻境: {realm_type}")

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
        cal_btn = self.find_one(HUD_CALENDAR, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        self.wait_click_feature(CALENDAR_REALM, threshold=0.8, time_out=5, raise_if_not_found=True, after_sleep=1)

    def _read_vitality(self):
        """Read current vitality via OCR around 3.2.1 area."""
        vitality_area = self.find_one(REALM_VITALITY, threshold=0.7)
        if not vitality_area:
            return None
        result = self.ocr(box=vitality_area, match=re.compile(r"(\d+)/(\d+)"))
        if result and len(result) > 0:
            text = result[0].name if hasattr(result[0], 'name') else str(result[0])
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

    # ── 4a. 魔物试炼幻境 ───────────────────────────────────

    def _realm_trial(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_TRIAL):
            return
        self.wait_click_feature(REALM_TRIAL, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_QUICK, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_MAX_Y, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back()

    # ── 4b. 祝福闪光幻境 ───────────────────────────────────

    def _realm_blessing(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_BLESSING):
            return
        self.wait_click_feature(REALM_BLESSING, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_QUICK, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_MAX_Y, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(TRIAL_CLAIM, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back()

    # ── 4c. 素材激化幻境 ───────────────────────────────────

    def _realm_escalation(self, vitality):
        if not self._check_vitality(vitality, VITALITY_COST_ESCALATION):
            return
        self.wait_click_feature(REALM_ESCALATION, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(ESCALATION_GO, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=1)
        # 等待幻境内 (3.2.4.2)
        self.wait_feature(ESCALATION_INSIDE, threshold=0.8, time_out=30, raise_if_not_found=True)
        # 走向激化台
        for _ in range(20):
            self.send_key("w", after_sleep=0.3)
            if self.find_one(ESCALATION_PLATFORM, threshold=0.8):
                break
        else:
            self.log_info("Could not find escalation platform after walking.")
            return
        self.send_key("f", after_sleep=1)
        # 选择
        self.wait_click_feature(ESCALATION_BUBBLE, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(ESCALATION_QUALITY, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(ESCALATION_QUANTITY, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(ESCALATION_SORT, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        # 红框区域
        redbox = self.find_one(ESCALATION_REDBOX, threshold=0.7)
        if redbox:
            self.click_box(redbox, after_sleep=0.3)
        else:
            self.log_info("Could not find red box area.")
        self.wait_click_feature(ESCALATION_MAX_Y, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        self.wait_click_feature(CONFIRM_BUTTON, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(ESCALATION_ACTIVATE, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.send_key("f", after_sleep=0.5)
        self._check_claim_done()
        # 退出
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
        self.log_info(f"Available tasks: {[t[0] for t in available_tasks]}")

        needed = INSPIRATION_GOAL - inspiration
        selected = self._select_tasks(available_tasks, needed)
        self.log_info(f"Selected tasks: {[(t[0], t[3]) for t in selected]}")

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
        cal_btn = self.find_one(HUD_CALENDAR, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        self.wait_click_feature(CALENDAR_DAILY, threshold=0.8, time_out=5, raise_if_not_found=True, after_sleep=1)

    def _read_inspiration(self):
        progress_area = self.find_one(DAILY_PROGRESS, threshold=0.7)
        if not progress_area:
            return 0
        result = self.ocr(box=progress_area, match=re.compile(r"\d+"))
        if result and len(result) > 0:
            text = result[0].name if hasattr(result[0], 'name') else str(result[0])
            match = re.search(r"\d+", text)
            if match:
                return int(match.group())
        return 0

    def _claim_daily_reward(self):
        self.wait_click_feature(DAILY_CLAIM_REWARD, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)

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

    # ── 朝夕心愿子任务 ─────────────────────────────────────

    def _execute_wish_task(self, task_feature, task_name):
        if task_feature == WISH_PHOTO:
            self._wish_task_photo()
        elif task_feature == WISH_UPGRADE:
            self._wish_task_upgrade()
        elif task_feature == WISH_ENERGY:
            self._wish_task_energy()
        elif task_feature == WISH_COLLECT:
            self._wish_task_collect()
        elif task_feature == WISH_ESCALATION:
            self._wish_task_escalation()

    def _wish_task_photo(self):
        """4.1 - 拍照"""
        self.log_info("Wish task: 拍照")
        self._go_back(2)
        self._navigate_to_hud()
        self.send_key("p", after_sleep=1)
        self.send_key("space", after_sleep=0.5)
        self.wait_click_feature(PHOTO_DELETE, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.3)
        self.wait_click_feature(CONFIRM_BUTTON, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.3)
        self._go_back()

    def _wish_task_upgrade(self):
        """4.2 - 升级祝福闪光"""
        self.log_info("Wish task: 升级祝福闪光")
        self.wait_click_feature(WISH_UPGRADE, threshold=0.8, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        self.wait_click_feature(WISH_GO, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=1)
        self.wait_click_feature(WISH_SORT, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_UPGRADE_BTN, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_SELECT_MAT, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_ADD, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        for _ in range(4):
            self.wait_click_feature(WISH_ADD_ONE, threshold=0.8, time_out=2, raise_if_not_found=True, after_sleep=0.2)
        self.wait_click_feature(CONFIRM_BUTTON, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_UPGRADE_BTN, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self._check_claim_done()
        self._go_back(2)

    def _wish_task_energy(self):
        """4.3 - 消耗活跃能量"""
        self.log_info("Wish task: 消耗活跃能量")
        if self.find_one(WISH_ESCALATION, threshold=0.8):
            self.log_info("素材激化 task exists, treating energy task as done.")
            return
        self.wait_click_feature(WISH_ENERGY, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_GO, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        realm_type = self.config.get("幻境类型")
        vitality = self._read_vitality()
        if not self.find_one(REALM_TRIAL, threshold=0.7):
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
        self.wait_click_feature(WISH_ESCALATION, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        self.wait_click_feature(WISH_GO, threshold=0.8, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        vitality = self._read_vitality() or 999
        if not self.find_one(REALM_TRIAL, threshold=0.7):
            self._navigate_to_realm()
        self._realm_escalation(vitality)
        self._navigate_to_daily_wishes()


if __name__ == "__main__":
    from ok import run_task
    from src.config import config
    run_task(config, task=DailyTask, debug=True)
