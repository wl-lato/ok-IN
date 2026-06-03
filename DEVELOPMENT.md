# ok-IN 开发计划

## 项目概述
基于 ok-script 框架开发《无限暖暖》自动化程序 ok-IN，支持后台运行。
1.0 目标：一键日常。

## 技术栈
- Python 3.12
- ok-script >= 1.0.148
- OpenCV (模板匹配)
- OnnxOCR (文字识别)
- PySide6 (GUI)

## 游戏技术信息
- 主进程: X6Game-Win64-Shipping.exe
- 窗口类: UnrealWindow
- 交互模式: PostMessage (支持后台)
- 反作弊: Anti-Cheat Expert (ACE)
- 推荐分辨率: 1920x1080 (16:9)

---

## 模板命名映射

图标文件位于 `features/` 目录，命名规则为英文短名。完整映射见 `src/features.py`。

| 编号 | 英文名 | 说明 |
|------|--------|------|
| 0-登录按钮 | login_button | 登录界面 |
| 0-确认按钮 | confirm_button | 通用 |
| 0-返回按钮 | back_button | 通用 |
| 0-领完标志 | claim_done | 通用 |
| 0-跳过按钮 | skip_button | 通用 |
| 1.0 | hud_pearpal | HUD-美鸭梨平板 |
| 1.1.0 | pearpal_mining | 美鸭梨挖掘 |
| 1.1.1 | mining_claim | 领取按钮 |
| 1.1.2 | mining_redig | 再次挖掘 |
| 1.2.0 | pearpal_mail | 邮件 |
| 1.2.1 | mail_claim | 领取按钮 |
| 2.0 | hud_miracle | HUD-奇迹之旅 |
| 2.1 | journey_skip | 跳过 |
| 2.2 | journey_skip2 | 再次跳过 |
| 2.3 | journey_tasks | 任务列表 |
| 2.4 | journey_claim | 一键领取 |
| 2.5 | journey_rewards | 奖励页面 |
| 3.0 | hud_calendar | HUD-奇想日历 |
| 3.1.0 | calendar_daily | 朝夕心愿 |
| 3.1.1 | daily_progress | 进度检测(OCR) |
| 3.1.2 | daily_claim_reward | 领取奖励 |
| 3.2.0 | calendar_realm | 每日幻境 |
| 3.2.1 | realm_vitality | 活力值(OCR) |
| 3.2.2 | realm_trial | 魔物试炼 |
| 3.2.2.1 | trial_quick | 快速挑战 |
| 3.2.2.2 | trial_max_y | 次数max-Y |
| 3.2.2.3 | trial_claim | 领取 |
| 3.2.3 | realm_blessing | 祝福闪光 |
| 3.2.4.0 | realm_escalation | 素材激化 |
| 3.2.4.1 | escalation_go | 前往 |
| 3.2.4.2 | escalation_inside | 幻境内 |
| 3.2.4.3 | escalation_platform | 打开激化台 |
| 3.2.4.4 | escalation_bubble | 闪亮泡泡 |
| 3.2.4.5 | escalation_quality | 品质切换 |
| 3.2.4.6 | escalation_quantity | 选择数量 |
| 3.2.4.7 | escalation_sort | 数量排序 |
| 3.2.4.8 | escalation_redbox | 点击红框区域 |
| 3.2.4.9 | escalation_max_y | 次数max-Y |
| 3.2.4.10 | escalation_activate | 激化按钮 |
| 4.1 | wish_photo | 拍照 |
| 4.1.1 | photo_delete | 删除按钮 |
| 4.2 | wish_upgrade | 升级祝福闪光 |
| 4.2.1 | wish_go | 立即前往 |
| 4.2.2 | wish_sort | 切换排序 |
| 4.2.3 | wish_upgrade_btn | 升级按钮 |
| 4.2.4 | wish_select_mat | 选择素材 |
| 4.2.5 | wish_add | 点击添加 |
| 4.2.6 | wish_add_one | 数量加一 |
| 4.3 | wish_energy | 消耗活跃能量 |
| 4.4 | wish_collect | 采集植物 |
| 4.5 | wish_escalation | 素材激化 |

---

## 已知限制与待确认项

1. **3.2.4.8 红框区域**: 当前实现为直接模板匹配点击。如果匹配不稳定，需改为锚点+偏移法。
2. **4.2.5 点击添加 / 4.2.6 数量加一**: 切换排序后的列表第一项，动态图标依赖模板匹配，可能需要锚点+偏移。
3. **4.4 采集植物**: v1.0 暂时跳过，需后续手动完成。
4. **OCR 区域**: 3.2.1(活力值)和3.1.1(灵感值)的OCR实现依赖实际截图测试，可能需要调整ROI。
5. **快捷键**: ESC=美鸭梨平板/返回, L=奇想日历, J=奇迹之旅, E=任务列表, Q=奖励页面, P=相机, F=交互, BACKSPACE=退出幻境。

---

## 开发档期 (v1.0 一键日常)

### Phase 1: 项目骨架与基础设施 ✅
- [x] 创建项目结构
- [x] 配置游戏窗口参数
- [x] 编写 README、LICENSE、CI 配置
- [x] 推送 GitHub 仓库

### Phase 2: 场景识别与核心逻辑 ✅
- [x] 收集用户截图 (51个模板图标)
- [x] 建立模板命名映射 (features.py)
- [x] 重写 INScene 场景检测
- [x] 重写 AutoLoginTask
- [x] 重写 DailyTask 完整日常流程
- [ ] 实际运行测试与模板匹配调参

### Phase 3-5: 已合并到 Phase 2 ✅
所有子任务逻辑已写入 DailyTask，包括：
- [x] 美鸭梨挖掘
- [x] 邮件领取
- [x] 奇迹之旅
- [x] 幻境挑战（3种类型）
- [x] 朝夕心愿（5种子任务 + 贪心选择）

### Phase 6: 测试与优化 (待进行)
- [ ] 模板匹配阈值调优
- [ ] OCR 区域验证
- [ ] 后台运行稳定性测试
- [ ] 多分辨率测试
- [ ] 边界情况处理
- [ ] 文档完善
- [ ] 打包发布 v1.0
