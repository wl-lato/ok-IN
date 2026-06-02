# ok-IN

一款基于图像识别的《无限暖暖》自动化工具，支持后台运行。

基于 [ok-script](https://github.com/ok-oldking/ok-script) 框架开发。

## ⚠️ 免责声明

本软件为开源、免费的外部工具，仅供学习和交流使用，旨在通过模拟操作简化《无限暖暖》的游戏玩法。

- **工作原理**：程序仅通过识别现有用户界面与游戏进行交互，不修改任何游戏文件或代码。
- **使用目的**：旨在为用户提供便利，无意破坏游戏平衡或提供任何不公平优势。
- **法律责任**：使用本软件产生的所有问题及后果，均与本项目及开发者团队无关。开发者团队拥有对本项目的最终解释权。
- **商业行为**：若您遇到商家使用本软件进行代练并收费，此行为可能涉及设备与时间成本，与本软件本身无关。

**使用本软件即表示您已阅读、理解并同意以上声明，并自愿承担一切潜在风险。**

## ✨ 主要功能

- **后台运行**：支持 PC 游戏在后台运行时进行自动化操作。
- **一键日常**：自动完成日常流程（朝夕心愿、幻境、美鸭梨派遣、邮件领取）。
- **自动登录**：自动处理登录流程。
- **跳过对话**：跳过冗长的剧情对话。

## 🖥️ 运行环境与兼容性

- **操作系统**：Windows
- **游戏分辨率**：1920x1080 或更高（推荐 16:9 宽高比）
- **游戏语言**：简体中文 / English
- **Python**：3.12+

## 🚀 安装指南

### 方式一：使用安装包 (推荐)

请从 [GitHub Releases](https://github.com/ok-oldking/ok-IN/releases) 下载最新的安装包。

### 方式二：从源码运行

1. **环境要求**：确保已安装 **Python 3.12** 或更高版本。

2. **克隆仓库**：
```bash
git clone https://github.com/ok-oldking/ok-IN.git
cd ok-IN
```

3. **安装依赖**：
```bash
pip install -r requirements.txt
```

4. **运行程序**：
```bash
# 运行正式版
python main.py

# 运行调试版（会输出更详细的日志）
python main_debug.py
```

## 📖 使用指南

### 使用前配置 (必读)

- **图形设置**：
  - **禁用**所有会导致 UI 与默认不同的设置。
  - **关闭**所有显卡滤镜和锐化效果（如 NVIDIA Freestyle）。
  - 使用游戏**默认亮度**。

- **分辨率**：推荐使用 **1920x1080** 或以上。

- **按键设置**：请使用游戏**默认**按键绑定。

- **窗口状态**：游戏窗口可以置于后台，但**不可最小化**。请勿让电脑**熄屏**或**锁屏**。

## 💬 社区与交流

- **开发者群** : `938132715` (ok-script 通用开发者群)

## 🔗 使用 [ok-script](https://github.com/ok-oldking/ok-script) 开发的项目

- 鸣潮 [ok-wuthering-waves](https://github.com/ok-oldking/ok-wuthering-waves)
- 异环 [ok-nte](https://github.com/BnanZ0/ok-nte)
- 原神 [ok-genshin-impact](https://github.com/ok-oldking/ok-genshin-impact)
- 星铁 [ok-starrailassistant](https://github.com/Shasnow/ok-starrailassistant)
