"""Daily task for Infinity Nikki - one-click daily routine.

Complete daily workflow based on logic doc:
1. Navigate to HUD
2. 美鸭梨挖掘 (Pear-Pal Mining)
3. 邮件领取 (Claim Mail)
4. 奇迹之旅 (Miracle Journey)
5. 幻境挑战 (Realm Challenge) - requires manual config for realm type
6. 朝夕心愿 (Daily Wishes) - auto-select tasks to reach 500 points
"""

import re

from ok import OneTimeTask

from src.features import (
    # 通用
    CONFIRM_BUTTON,
    BACK_BUTTON,
    CLAIM_DONE,
    # HUD
    HUD_PEARPAL,
    HUD_CALENDAR,
    HUD_MIRACLE,
    # 美鸭梨
    PEARPAL_MINING,
    MINING_CLAIM,
    MINING_REDIG,
    PEARPAL_MAIL,
    MAIL_CLAIM,
    # 奇迹之旅
    JOURNEY_SKIP,
    JOURNEY_SKIP2,
    JOURNEY_TASKS,
    JOURNEY_CLAIM,
    JOURNEY_REWARDS,
    # 奇想日历
    CALENDAR_DAILY,
    CALENDAR_REALM,
    DAILY_PROGRESS,
    DAILY_CLAIM_REWARD,
    REALM_VITALITY,
    # 幻境 - 魔物试炼
    REALM_TRIAL,
    TRIAL_QUICK,
    TRIAL_MAX_Y,
    TRIAL_CLAIM,
    # 幻境 - 祝福闪光
    REALM_BLESSING,
    # 幻境 - 素材激化
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
    # 朝夕心愿子任务
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

# ── Constants ──────────────────────────────────────────────
REALM_TRIAL_TYPE = "魔物试炼"
REALM_BLESSING_TYPE = "祝福闪光"
REALM_ESCALATION_TYPE = "素材激化"

VITALITY_COST_TRIAL = 40
VITALITY_COST_BLESSING = 40
VITALITY_COST_ESCALATION = 10

INSPIRATION_GOAL = 500
INSPIRATION_LV1 = 100  # 1级任务灵感
INSPIRATION_LV2 = 200  # 2级任务灵感

# Task weights (higher = slower to complete)
WISH_WEIGHTS = {
    WISH_PHOTO: ("1级", 1, INSPIRATION_LV1),
    WISH_UPGRADE: ("1级", 2, INSPIRATION_LV1),
    WISH_ENERGY: ("2级", 3, INSPIRATION_LV2),
    WISH_COLLECT: ("2级", 2, INSPIRATION_LV2),
    WISH_ESCALATION: ("2级", 4, INSPIRATION_LV2),
}


class DailyTask(OneTimeTask):
    """One-click daily task for Infinity Nikki."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                "options": [REALM_TRIAL_TYPE, REALM_BLESSING_TYPE, REALM_ESCALATION_TYPE],
            },
        }
        self.config_description = {
            "美鸭梨挖掘": "美鸭梨挖掘并领取奖励",
            "邮件领取": "领取所有邮件奖励",
            "奇迹之旅": "完成奇迹之旅任务和奖励领取",
            "幻境挑战": "消耗活力完成幻境挑战",
            "幻境类型": "选择幻境类型（魔物试炼/祝福闪光/素材激化）",
            "朝夕心愿": "完成朝夕心愿获取500灵感",
        }

    # ── Main Entry ─────────────────────────────────────────

    def run(self):
        """Execute the daily task workflow."""
        self.log_info("Starting daily task...")
        self.info_set("Status", "Running")

        self._navigate_to_hud()

        if self.get_config("美鸭梨挖掘"):
            self._pear_pal_mining()
        if self.get_config("邮件领取"):
            self._claim_mail()
        if self.get_config("奇迹之旅"):
            self._miracle_journey()
        if self.get_config("幻境挑战"):
            self._realm_challenge()
        if self.get_config("朝夕心愿"):
            self._daily_wishes()

        self.info_set("Status", "Completed")
        self.log_info("Daily task completed!")
        self.notification("Daily task completed!", tray=True)

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
                self.send_key("escape", after_sleep=0.5)
            if self.find_one(HUD_PEARPAL, threshold=0.8):
                return
        raise RuntimeError("Failed to navigate to HUD after 10 attempts")

    def _go_back(self, times=1):
        """Press ESC or click back button to return to previous screen."""
        for _ in range(times):
            back = self.find_one(BACK_BUTTON, threshold=0.8)
            if back:
                self.click_box(back, after_sleep=0.5)
            else:
                self.send_key("escape", after_sleep=0.5)

    def _check_claim_done(self, timeout=1):
        """Check for 领完标志 in bottom-right corner after an action.

        If found, press F to confirm collection.
        """
        self.sleep(timeout)
        if self.find_one(CLAIM_DONE, threshold=0.8):
            self.send_key("f", after_sleep=0.5)

    # ── 1. 美鸭梨挖掘 ─────────────────────────────────────

    def _pear_pal_mining(self):
        """美鸭梨挖掘: open Pear-Pal → mine → claim → redig → back."""
        self.log_info("Starting Pear-Pal mining...")
        self.info_set("Step", "美鸭梨挖掘")

        # HUD → 美鸭梨平板
        self._navigate_to_hud()
        self.wait_click_feature(HUD_PEARPAL, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 美鸭梨平板 → 美鸭梨挖掘
        self.wait_click_feature(PEARPAL_MINING, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 领取奖励
        self.wait_click_feature(MINING_CLAIM, time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # 再次挖掘
        self.wait_click_feature(MINING_REDIG, time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # 返回美鸭梨平板
        self._go_back()
        self.log_info("Pear-Pal mining done.")

    # ── 2. 邮件领取 ────────────────────────────────────────

    def _claim_mail(self):
        """邮件领取: open Pear-Pal → mail → claim → check done → back."""
        self.log_info("Claiming mail rewards...")
        self.info_set("Step", "邮件领取")

        # Ensure we're on 美鸭梨平板
        if not self.find_one(PEARPAL_MAIL, threshold=0.8):
            self._navigate_to_hud()
            self.wait_click_feature(HUD_PEARPAL, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 进入邮件
        self.wait_click_feature(PEARPAL_MAIL, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 领取
        self.wait_click_feature(MAIL_CLAIM, time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # 检查领完标志
        self._check_claim_done()

        # 返回美鸭梨平板
        self._go_back()
        self.log_info("Mail claimed.")

    # ── 3. 奇迹之旅 ────────────────────────────────────────

    def _miracle_journey(self):
        """奇迹之旅: HUD → journey → skip → tasks → claim → rewards → claim → back."""
        self.log_info("Starting Miracle Journey...")
        self.info_set("Step", "奇迹之旅")

        self._navigate_to_hud()

        # 进入奇迹之旅 (HUD按钮 或 J键)
        hud_btn = self.find_one(HUD_MIRACLE, threshold=0.8)
        if hud_btn:
            self.click_box(hud_btn, after_sleep=1)
        else:
            self.send_key("j", after_sleep=1)

        # 检测右下角跳过按钮 (2.1)
        skip = self.find_one(JOURNEY_SKIP, threshold=0.8)
        if skip:
            self.send_key("f", after_sleep=0.5)
            # 点击再次跳过 (2.2)
            self.wait_click_feature(JOURNEY_SKIP2, time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # 进入任务列表 (2.3 或 E键)
        tasks_btn = self.find_one(JOURNEY_TASKS, threshold=0.8)
        if tasks_btn:
            self.click_box(tasks_btn, after_sleep=1)
        else:
            self.send_key("e", after_sleep=1)

        # 一键领取 (2.4)
        self.wait_click_feature(JOURNEY_CLAIM, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        self._check_claim_done()

        # 进入奖励页面 (2.5 或 Q键)
        rewards_btn = self.find_one(JOURNEY_REWARDS, threshold=0.8)
        if rewards_btn:
            self.click_box(rewards_btn, after_sleep=1)
        else:
            self.send_key("q", after_sleep=1)

        # 一键领取 (2.4)
        self.wait_click_feature(JOURNEY_CLAIM, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        self._check_claim_done()

        # 返回HUD
        self._go_back(2)
        self._navigate_to_hud()
        self.log_info("Miracle Journey done.")

    # ── 4. 幻境挑战 ────────────────────────────────────────

    def _realm_challenge(self):
        """幻境挑战: navigate to realm, read vitality, execute selected realm type."""
        realm_type = self.get_config("幻境类型")
        self.log_info(f"Starting Realm Challenge: {realm_type}")
        self.info_set("Step", f"幻境: {realm_type}")

        # 前往奇想日历 → 幻境挑战
        self._navigate_to_realm()

        # 读取活力值
        vitality = self._read_vitality()
        if vitality is None:
            self.log_info("Cannot read vitality, proceeding anyway.")
            vitality = 999

        # 检测是否已在幻境挑战页面
        if not self.find_one(REALM_TRIAL, threshold=0.7) and \
           not self.find_one(REALM_BLESSING, threshold=0.7) and \
           not self.find_one(REALM_ESCALATION, threshold=0.7):
            # 不在幻境页面，重新导航
            self._navigate_to_realm()

        # 执行对应幻境
        if realm_type == REALM_TRIAL_TYPE:
            self._realm_trial(vitality)
        elif realm_type == REALM_BLESSING_TYPE:
            self._realm_blessing(vitality)
        elif realm_type == REALM_ESCALATION_TYPE:
            self._realm_escalation(vitality)

        self._navigate_to_hud()
        self.log_info(f"Realm Challenge ({realm_type}) done.")

    def _navigate_to_realm(self):
        """Navigate to 幻境挑战 page."""
        self._navigate_to_hud()
        # 进入奇想日历 (3.0 或 L键)
        cal_btn = self.find_one(HUD_CALENDAR, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        # 点击每日幻境 (3.2.0)
        self.wait_click_feature(CALENDAR_REALM, time_out=5, raise_if_not_found=True, after_sleep=1)

    def _read_vitality(self):
        """Read current vitality value from 3.2.1 area via OCR.

        Returns:
            int or None: Current vitality points.
        """
        vitality_area = self.find_one(REALM_VITALITY, threshold=0.7)
        if not vitality_area:
            return None
        # OCR the area around vitality icon
        result = self.ocr(box=vitality_area, match=re.compile(r"(\d+)/(\d+)"))
        if result and len(result) > 0:
            match = re.search(r"(\d+)", result[0].name if hasattr(result[0], 'name') else str(result[0]))
            if match:
                return int(match.group(1))
        return None

    def _check_vitality(self, vitality, required):
        """Check if enough vitality. If not, go back and return False."""
        if vitality < required:
            self.log_info(f"Insufficient vitality: {vitality}/{required}")
            self._go_back()
            return False
        return True

    # ── 4a. 魔物试炼幻境 ───────────────────────────────────

    def _realm_trial(self, vitality):
        """魔物试炼: vitality ≥ 40 → enter → quick → max → claim → back."""
        if not self._check_vitality(vitality, VITALITY_COST_TRIAL):
            return

        # 点击魔物试炼 (3.2.2)
        self.wait_click_feature(REALM_TRIAL, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 快速挑战 (3.2.2.1)
        self.wait_click_feature(TRIAL_QUICK, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 次数max-Y (3.2.2.2)
        self.wait_click_feature(TRIAL_MAX_Y, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 领取 (3.2.2.3)
        self.wait_click_feature(TRIAL_CLAIM, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        self._check_claim_done()
        self._go_back()

    # ── 4b. 祝福闪光幻境 ───────────────────────────────────

    def _realm_blessing(self, vitality):
        """祝福闪光: vitality ≥ 40 → enter → quick → max → claim → back."""
        if not self._check_vitality(vitality, VITALITY_COST_BLESSING):
            return

        # 点击祝福闪光 (3.2.3)
        self.wait_click_feature(REALM_BLESSING, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 快速挑战 (3.2.2.1)
        self.wait_click_feature(TRIAL_QUICK, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 次数max-Y (3.2.2.2)
        self.wait_click_feature(TRIAL_MAX_Y, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 领取 (3.2.2.3)
        self.wait_click_feature(TRIAL_CLAIM, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        self._check_claim_done()
        self._go_back()

    # ── 4c. 素材激化幻境 ───────────────────────────────────

    def _realm_escalation(self, vitality):
        """素材激化: vitality ≥ 10 → enter → walk → platform → select → activate → back."""
        if not self._check_vitality(vitality, VITALITY_COST_ESCALATION):
            return

        # 点击素材激化 (3.2.4.0)
        self.wait_click_feature(REALM_ESCALATION, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 前往 (3.2.4.1)
        self.wait_click_feature(ESCALATION_GO, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 等待加载，检测幻境内 (3.2.4.2)
        self.wait_feature(ESCALATION_INSIDE, time_out=30, raise_if_not_found=True)

        # 走向激化台：按W键，间断性检测打开激化台 (3.2.4.3)
        for _ in range(20):
            self.send_key("w", after_sleep=0.3)
            if self.find_one(ESCALATION_PLATFORM, threshold=0.8):
                break
        else:
            self.log_info("Could not find escalation platform after walking.")
            return

        # 按F打开激化台
        self.send_key("f", after_sleep=1)

        # 选择闪亮泡泡 (3.2.4.4)
        self.wait_click_feature(ESCALATION_BUBBLE, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        # 品质切换 (3.2.4.5)
        self.wait_click_feature(ESCALATION_QUALITY, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        # 选择数量 (3.2.4.6)
        self.wait_click_feature(ESCALATION_QUANTITY, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        # 数量排序 (3.2.4.7)
        self.wait_click_feature(ESCALATION_SORT, time_out=3, raise_if_not_found=True, after_sleep=0.3)

        # 点击红框区域 (3.2.4.8 - 锚点+偏移法)
        redbox = self.find_one(ESCALATION_REDBOX, threshold=0.7)
        if redbox:
            self.click_box(redbox, after_sleep=0.3)
        else:
            self.log_info("Could not find red box area, trying direct click.")

        # 次数max-Y (3.2.4.9)
        self.wait_click_feature(ESCALATION_MAX_Y, time_out=3, raise_if_not_found=True, after_sleep=0.3)
        # 确认按钮
        self.wait_click_feature(CONFIRM_BUTTON, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 激化 (3.2.4.10)
        self.wait_click_feature(ESCALATION_ACTIVATE, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 按F
        self.send_key("f", after_sleep=0.5)

        # 检查领完标志
        self._check_claim_done()

        # 退出：ESC退出激化台，BACKSPACE退出幻境
        self.send_key("escape", after_sleep=0.5)
        self.send_key("backspace", after_sleep=0.5)

    # ── 5. 朝夕心愿 ────────────────────────────────────────

    def _daily_wishes(self):
        """朝夕心愿: reach 500 inspiration by auto-selecting optimal tasks.

        Logic:
        1. Read current inspiration from 3.1.1
        2. If 500, claim reward and return
        3. Detect available tasks (4.1~4.5)
        4. Select tasks by weight to reach 500 optimally
        5. Execute selected tasks
        6. Re-check and claim
        """
        self.log_info("Starting Daily Wishes...")
        self.info_set("Step", "朝夕心愿")

        # 前往朝夕心愿
        self._navigate_to_daily_wishes()

        # 读取灵感值
        inspiration = self._read_inspiration()
        self.log_info(f"Current inspiration: {inspiration}")

        if inspiration >= INSPIRATION_GOAL:
            self.log_info("Already at 500 inspiration, claiming reward.")
            self._claim_daily_reward()
            self._go_back()
            return

        # 检测可用任务
        available_tasks = self._detect_available_tasks()
        self.log_info(f"Available tasks: {[t[0] for t in available_tasks]}")

        # 选择最优任务组合
        needed = INSPIRATION_GOAL - inspiration
        selected = self._select_tasks(available_tasks, needed)
        self.log_info(f"Selected tasks: {[(t[0], t[3]) for t in selected]}")

        # 执行任务
        for task_feature, task_level, weight, task_name in selected:
            self._execute_wish_task(task_feature, task_name)
            # 每完成一个任务后回到朝夕心愿重新检测
            self._navigate_to_daily_wishes()

        # 最终检测灵感值
        inspiration = self._read_inspiration()
        self.log_info(f"Inspiration after tasks: {inspiration}")

        if inspiration >= INSPIRATION_GOAL:
            self._claim_daily_reward()
        else:
            self.log_info(f"Warning: inspiration is {inspiration}, expected 500.")

        self._go_back()
        self.log_info("Daily Wishes done.")

    def _navigate_to_daily_wishes(self):
        """Navigate to 朝夕心愿 page from any state."""
        self._navigate_to_hud()
        # 进入奇想日历
        cal_btn = self.find_one(HUD_CALENDAR, threshold=0.8)
        if cal_btn:
            self.click_box(cal_btn, after_sleep=1)
        else:
            self.send_key("l", after_sleep=1)
        # 点击朝夕心愿 (3.1.0)
        self.wait_click_feature(CALENDAR_DAILY, time_out=5, raise_if_not_found=True, after_sleep=1)

    def _read_inspiration(self):
        """Read current inspiration value from 3.1.1 area via OCR.

        Returns:
            int: Current inspiration (0 if unreadable).
        """
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
        """Click 领取奖励 (3.1.2)."""
        self.wait_click_feature(DAILY_CLAIM_REWARD, time_out=3, raise_if_not_found=False, after_sleep=0.5)

    def _detect_available_tasks(self):
        """Detect which wish tasks (4.1~4.5) are available.

        Returns:
            list of (feature_name, level, weight, name) tuples.
        """
        available = []
        for feature, (level, weight, points) in WISH_WEIGHTS.items():
            if self.find_one(feature, threshold=0.8):
                available.append((feature, level, weight, feature))
        return available

    def _select_tasks(self, available_tasks, needed):
        """Select optimal task combination to reach 500 inspiration.

        Greedy approach: prefer lower-weight (faster) tasks first.

        Args:
            available_tasks: list of (feature, level, weight, name) tuples.
            needed: inspiration points still needed.

        Returns:
            list of selected tasks, sorted by weight (fastest first).
        """
        # Sort by weight ascending (faster tasks first)
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
        """Execute a specific wish task by its feature name."""
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
        """4.1 - 1级任务 - 拍照 (权重1): HUD → camera → snap → delete → back."""
        self.log_info("Wish task: 拍照")
        # 返回HUD (按2次ESC)
        self._go_back(2)
        self._navigate_to_hud()

        # 按P进入相机
        self.send_key("p", after_sleep=1)
        # 按空格拍照
        self.send_key("space", after_sleep=0.5)
        # 点击删除按钮 (4.1.1)
        self.wait_click_feature(PHOTO_DELETE, time_out=3, raise_if_not_found=False, after_sleep=0.3)
        # 确认
        self.wait_click_feature(CONFIRM_BUTTON, time_out=3, raise_if_not_found=False, after_sleep=0.3)
        # 返回HUD
        self._go_back()

    def _wish_task_upgrade(self):
        """4.2 - 1级任务 - 升级祝福闪光 (权重2):
        click 4.2 → go → sort → upgrade → select mat → add → confirm → upgrade → claim → back×2.
        """
        self.log_info("Wish task: 升级祝福闪光")

        # 点击升级祝福闪光 (4.2)
        self.wait_click_feature(WISH_UPGRADE, time_out=3, raise_if_not_found=False, after_sleep=0.5)
        # 立即前往 (4.2.1)
        self.wait_click_feature(WISH_GO, time_out=3, raise_if_not_found=True, after_sleep=1)

        # 切换排序 (4.2.2)
        self.wait_click_feature(WISH_SORT, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 右下角升级按钮 (4.2.3)
        self.wait_click_feature(WISH_UPGRADE_BTN, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 选择素材 (4.2.4)
        self.wait_click_feature(WISH_SELECT_MAT, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 点击添加 (4.2.5)
        self.wait_click_feature(WISH_ADD, time_out=3, raise_if_not_found=True, after_sleep=0.3)

        # 点击4次数量加一 (4.2.6)
        for _ in range(4):
            self.wait_click_feature(WISH_ADD_ONE, time_out=2, raise_if_not_found=True, after_sleep=0.2)

        # 确认
        self.wait_click_feature(CONFIRM_BUTTON, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 点击升级按钮 (4.2.3)
        self.wait_click_feature(WISH_UPGRADE_BTN, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 检查领完标志
        self._check_claim_done()

        # 返回朝夕心愿 (ESC×2)
        self._go_back(2)

    def _wish_task_energy(self):
        """4.3 - 2级任务 - 消耗活跃能量 (权重3):
        Check 4.5 for completion → click 4.3 → go → realm → back.
        """
        self.log_info("Wish task: 消耗活跃能量")

        # 检测4.5是否已完成（如果4.5存在则视为任务已完成）
        if self.find_one(WISH_ESCALATION, threshold=0.8):
            self.log_info("素材激化 task exists, treating energy task as done.")
            return

        # 点击消耗活跃能量 (4.3)
        self.wait_click_feature(WISH_ENERGY, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 立即前往 (4.2.1)
        self.wait_click_feature(WISH_GO, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 执行幻境挑战任务
        realm_type = self.get_config("幻境类型")
        vitality = self._read_vitality()

        # 确保在幻境挑战页面
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
        """4.4 - 2级任务 - 采集植物 (权重2): skipped in v1.0."""
        self.log_info("Wish task: 采集植物 - SKIPPED (not automatable in v1.0)")

    def _wish_task_escalation(self):
        """4.5 - 2级任务 - 素材激化 (权重4):
        click 4.5 → go → realm escalation → back.
        """
        self.log_info("Wish task: 素材激化")

        # 点击素材激化 (4.5)
        self.wait_click_feature(WISH_ESCALATION, time_out=3, raise_if_not_found=True, after_sleep=0.5)
        # 立即前往 (4.2.1)
        self.wait_click_feature(WISH_GO, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # 执行素材激化幻境任务
        vitality = self._read_vitality() or 999

        if not self.find_one(REALM_TRIAL, threshold=0.7):
            self._navigate_to_realm()

        self._realm_escalation(vitality)

        self._navigate_to_daily_wishes()
