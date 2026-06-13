"""config.py for Infinity Nikki - aligned with ok-ww structure.

Key alignment points vs ok-ww:
- 'feature_processor': registered as imported function (not string)
- 'my_app': registered to provide Globals with shared state
- vcenter_features / hcenter_features for centered features
- vcenter/hcenter variance is set to 1 because COCO annotations come from
  a composite image (not real game screenshots); once real screenshots are
  available, change to ok-ww's 0.002 values.
"""

import os
import re
from pathlib import Path

from ok import Box, ConfigOption

version = "dev"

# Import feature processor directly (required by ok-script FeatureSet)
from src.task.process_feature import process_feature


def calculate_pc_exe_path(running_path):
    """Calculate the game executable path from the running process path."""
    game_exe_folder = Path(running_path).parents[3]
    return str(game_exe_folder / "X6Game-Win64-Shipping.exe")


def blur_area(width, height):
    """Blur area to hide UID info in screenshots."""
    blur_width = int(0.12 * width)
    blur_height = int(0.024 * height)
    return Box(width * 0.879, height * 0.976, blur_width * 0.973, blur_height * 0.994)


monthly_card_config_option = ConfigOption(
    "Monthly Card Config",
    {
        "Check Monthly Card": True,
        "Monthly Card Time": 4,
    },
    description="Turn on to avoid interruption by monthly card when executing tasks",
    config_description={
        "Check Monthly Card": "Check for monthly card to avoid interruption of tasks",
        "Monthly Card Time": "Your computer's local time when the monthly card will popup, hour in (1-24)",
    },
)

config = {
    "debug": False,
    "use_gui": True,
    "config_folder": "configs",
    "blur_area": blur_area,
    "gui_icon": "icons/icon.png",
    "global_configs": [monthly_card_config_option],
    "ocr": {
        "lib": "onnxocr",
        "auto_simplify": True,
        "params": {
            "use_openvino": True,
            "use_npu": True,
        },
    },
    # Aligned with ok-ww: 'my_app' provides shared state (logged_in, etc.)
    "my_app": ["src.globals", "Globals"],
    "start_timeout": 120,
    "wait_until_settle_time": 0,
    # Aligned with ok-ww: feature_processor registered as imported callable
    "template_matching": {
        "coco_feature_json": os.path.join("assets", "coco_annotations.json"),
        # NOTE: variance=1 because COCO annotations are from composite images,
        # not real game screenshots. This makes FeatureSet search the full screen.
        # When real screenshots are available, change to ok-ww values: 0.002
        "default_horizontal_variance": 1,
        "default_vertical_variance": 1,
        "default_threshold": 0.8,
        "feature_processor": process_feature,
        "vcenter_features": [],
        "hcenter_features": [],
    },
    "windows": {
        "top_hwnd_class": [
            re.compile("CAgreementDlg"),
            re.compile("CLoginDlg_P_"),
            "CefBrowserWindow",
            "Chrome_RenderWidgetHostHWND",
            "#32770",
            re.compile("CNativeLoginDlg"),
            "Static",
            "ComboBox",
            "ComboLBox",
            "Button",
        ],
        "calculate_pc_exe_path": calculate_pc_exe_path,
        "exe": "X6Game-Win64-Shipping.exe",
        "hwnd_class": "UnrealWindow",
        "interaction": "PostMessage",
        "capture_method": ["WGC", "BitBlt_RenderFull"],
        "check_hdr": False,
        "force_no_hdr": False,
        "check_night_light": True,
        "force_no_night_light": False,
    },
    "window_size": {
        "width": 1200,
        "height": 800,
        "min_width": 1200,
        "min_height": 800,
    },
    "supported_resolution": {
        "ratio": "16:9",
        "resize_to": [(2560, 1440), (1920, 1080), (1600, 900), (1280, 720)],
        "min_size": (1280, 720),
    },
    "links": {
        "default": {
            "github": "https://github.com/wl-lato/ok-IN",
            "faq": "https://github.com/wl-lato/ok-IN/blob/main/README_en.md",
        },
        "zh_CN": {
            "github": "https://github.com/wl-lato/ok-IN",
            "faq": "https://github.com/wl-lato/ok-IN/blob/main/README.md",
        },
    },
    "about": """
    <p style="color:red;">
        <strong>本软件是免费开源的。</strong> 如果你被收费，请立即退款。
    </p>
    <p style="color:red;">
        <strong>本软件仅供个人使用，用于学习Python编程、计算机视觉、UI自动化等。</strong> 请勿将其用于任何营利性或商业用途。
    </p>
    <p style="color:red;">
        <strong>使用本软件可能会导致账号被封。</strong> 请在了解风险后再使用。
    </p>
    """,
    "screenshots_folder": "screenshots",
    "gui_title": "OK-IN",
    "log_file": "logs/ok-in.log",
    "error_log_file": "logs/ok-in_error.log",
    "version": version,
    "onetime_tasks": [
        ["src.task.DailyTask", "DailyTask"],
    ],
    "trigger_tasks": [
        ["src.task.SkipDialogTask", "SkipDialogTask"],
        ["src.task.AutoLoginTask", "AutoLoginTask"],
    ],
    "scene": ["src.scene.INScene", "INScene"],
}
