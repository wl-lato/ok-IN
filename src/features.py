"""Feature name constants for Infinity Nikki template matching.

Mapping between user-facing icon numbers (from logic doc) and code-friendly names.
Template images are stored in features/ directory as {name}.png.
"""

# ── 0 - 通用 ──────────────────────────────────────────────
LOGIN_BUTTON = "login_button"           # 0 - 登录界面 - 登录按钮
CONFIRM_BUTTON = "confirm_button"       # 0 - 通用 - 确认按钮
BACK_BUTTON = "back_button"             # 0 - 通用 - 返回按钮
CLAIM_DONE = "claim_done"               # 0 - 通用 - 领完标志
SKIP_BUTTON = "skip_button"             # 0 - 通用 - 跳过按钮

# ── 1 - 美鸭梨平板 ────────────────────────────────────────
HUD_PEARPAL = "hud_pearpal"             # 1.0 - HUD - 美鸭梨平板
PEARPAL_MINING = "pearpal_mining"       # 1.1.0 - 美鸭梨挖掘
MINING_CLAIM = "mining_claim"           # 1.1.1 - 领取按钮
MINING_REDIG = "mining_redig"           # 1.1.2 - 再次挖掘
PEARPAL_MAIL = "pearpal_mail"           # 1.2.0 - 邮件
MAIL_CLAIM = "mail_claim"               # 1.2.1 - 领取按钮

# ── 2 - 奇迹之旅 ──────────────────────────────────────────
HUD_MIRACLE = "hud_miracle"             # 2.0 - HUD - 奇迹之旅
JOURNEY_SKIP = "journey_skip"           # 2.1 - 跳过按钮
JOURNEY_SKIP2 = "journey_skip2"         # 2.2 - 再次跳过
JOURNEY_TASKS = "journey_tasks"         # 2.3 - 任务列表
JOURNEY_CLAIM = "journey_claim"         # 2.4 - 一键领取
JOURNEY_REWARDS = "journey_rewards"     # 2.5 - 奖励页面

# ── 3 - 奇想日历 ──────────────────────────────────────────
HUD_CALENDAR = "hud_calendar"           # 3.0 - HUD - 奇想日历
CALENDAR_DAILY = "calendar_daily"       # 3.1.0 - 朝夕心愿
DAILY_PROGRESS = "daily_progress"       # 3.1.1 - 进度检测
DAILY_CLAIM_REWARD = "daily_claim_reward"  # 3.1.2 - 领取奖励
CALENDAR_REALM = "calendar_realm"       # 3.2.0 - 每日幻境
REALM_VITALITY = "realm_vitality"       # 3.2.1 - 当前活力值

# ── 3.2.2 - 魔物试炼幻境 ──────────────────────────────────
REALM_TRIAL = "realm_trial"             # 3.2.2 - 魔物试炼
TRIAL_QUICK = "trial_quick"             # 3.2.2.1 - 快速挑战
TRIAL_MAX_Y = "trial_max_y"             # 3.2.2.2 - 次数max-Y
TRIAL_CLAIM = "trial_claim"             # 3.2.2.3 - 领取

# ── 3.2.3 - 祝福闪光幻境 ──────────────────────────────────
REALM_BLESSING = "realm_blessing"       # 3.2.3 - 祝福闪光

# ── 3.2.4 - 素材激化幻境 ──────────────────────────────────
REALM_ESCALATION = "realm_escalation"   # 3.2.4.0 - 素材激化
ESCALATION_GO = "escalation_go"         # 3.2.4.1 - 前往
ESCALATION_INSIDE = "escalation_inside" # 3.2.4.2 - 幻境内
ESCALATION_PLATFORM = "escalation_platform"  # 3.2.4.3 - 打开激化台
ESCALATION_BUBBLE = "escalation_bubble" # 3.2.4.4 - 闪亮泡泡
ESCALATION_QUALITY = "escalation_quality"  # 3.2.4.5 - 品质切换
ESCALATION_QUANTITY = "escalation_quantity"  # 3.2.4.6 - 选择数量
ESCALATION_SORT = "escalation_sort"     # 3.2.4.7 - 数量排序
ESCALATION_REDBOX = "escalation_redbox" # 3.2.4.8 - 点击红框区域
ESCALATION_MAX_Y = "escalation_max_y"  # 3.2.4.9 - 次数max-Y
ESCALATION_ACTIVATE = "escalation_activate"  # 3.2.4.10 - 激化

# ── 4 - 朝夕心愿子任务 ────────────────────────────────────
WISH_PHOTO = "wish_photo"               # 4.1 - 拍照
PHOTO_DELETE = "photo_delete"           # 4.1.1 - 删除按钮
WISH_UPGRADE = "wish_upgrade"           # 4.2 - 升级祝福闪光
WISH_GO = "wish_go"                     # 4.2.1 - 立即前往
WISH_SORT = "wish_sort"                 # 4.2.2 - 切换排序
WISH_UPGRADE_BTN = "wish_upgrade_btn"   # 4.2.3 - 升级按钮
WISH_SELECT_MAT = "wish_select_mat"     # 4.2.4 - 选择素材
WISH_ADD = "wish_add"                   # 4.2.5 - 点击添加
WISH_ADD_ONE = "wish_add_one"           # 4.2.6 - 数量加一
WISH_ENERGY = "wish_energy"             # 4.3 - 消耗活跃能量
WISH_COLLECT = "wish_collect"           # 4.4 - 采集植物
WISH_ESCALATION = "wish_escalation"     # 4.5 - 素材激化
