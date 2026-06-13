from enum import Enum


class Labels(str, Enum):
    # ── 0 - 通用 ──────────────────────────────────────────
    back_button = "back_button"
    confirm_button = "confirm_button"
    claim_done = "claim_done"
    skip_button = "skip_button"
    login_button = "login_button"

    # ── 1 - 美鸭梨平板 ────────────────────────────────────
    hud_pearpal = "hud_pearpal"
    pearpal_mining = "pearpal_mining"
    mining_claim = "mining_claim"
    mining_redig = "mining_redig"
    pearpal_mail = "pearpal_mail"
    mail_claim = "mail_claim"

    # ── 2 - 奇迹之旅 ──────────────────────────────────────
    hud_miracle = "hud_miracle"
    journey_skip = "journey_skip"
    journey_skip2 = "journey_skip2"
    journey_tasks = "journey_tasks"
    journey_claim = "journey_claim"
    journey_rewards = "journey_rewards"

    # ── 3 - 奇想日历 ──────────────────────────────────────
    hud_calendar = "hud_calendar"
    calendar_daily = "calendar_daily"
    calendar_realm = "calendar_realm"
    daily_progress = "daily_progress"
    daily_claim_reward = "daily_claim_reward"
    realm_vitality = "realm_vitality"

    # ── 3.2.2 - 魔物试炼幻境 ──────────────────────────────
    realm_trial = "realm_trial"
    trial_quick = "trial_quick"
    trial_max_y = "trial_max_y"
    trial_claim = "trial_claim"

    # ── 3.2.3 - 祝福闪光幻境 ──────────────────────────────
    realm_blessing = "realm_blessing"

    # ── 3.2.4 - 素材激化幻境 ──────────────────────────────
    realm_escalation = "realm_escalation"
    escalation_go = "escalation_go"
    escalation_inside = "escalation_inside"
    escalation_platform = "escalation_platform"
    escalation_bubble = "escalation_bubble"
    escalation_quality = "escalation_quality"
    escalation_quantity = "escalation_quantity"
    escalation_sort = "escalation_sort"
    escalation_redbox = "escalation_redbox"
    escalation_max_y = "escalation_max_y"
    escalation_activate = "escalation_activate"

    # ── 4 - 朝夕心愿子任务 ────────────────────────────────
    wish_photo = "wish_photo"
    photo_delete = "photo_delete"
    wish_upgrade = "wish_upgrade"
    wish_go = "wish_go"
    wish_sort = "wish_sort"
    wish_upgrade_btn = "wish_upgrade_btn"
    wish_select_mat = "wish_select_mat"
    wish_add = "wish_add"
    wish_add_one = "wish_add_one"
    wish_energy = "wish_energy"
    wish_collect = "wish_collect"
    wish_escalation = "wish_escalation"
