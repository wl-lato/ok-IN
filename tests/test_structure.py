"""Basic tests for ok-IN project structure and configuration."""

import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProjectStructure:
    """Test that the project structure is correct."""

    def test_main_py_exists(self):
        assert os.path.exists("main.py")

    def test_main_debug_py_exists(self):
        assert os.path.exists("main_debug.py")

    def test_config_exists(self):
        assert os.path.exists("src/config.py")

    def test_daily_task_exists(self):
        assert os.path.exists("src/task/DailyTask.py")

    def test_scene_exists(self):
        assert os.path.exists("src/scene/INScene.py")

    def test_readme_exists(self):
        assert os.path.exists("README.md")

    def test_requirements_exists(self):
        assert os.path.exists("requirements.txt")

    def test_features_dir_exists(self):
        assert os.path.exists("features")


class TestConfig:
    """Test configuration module."""

    def test_config_imports(self):
        from src.config import config

        assert config is not None

    def test_config_has_windows(self):
        from src.config import config

        assert "windows" in config

    def test_config_windows_exe(self):
        from src.config import config

        assert config["windows"]["exe"] == "X6Game-Win64-Shipping.exe"

    def test_config_windows_hwnd_class(self):
        from src.config import config

        assert config["windows"]["hwnd_class"] == "UnrealWindow"

    def test_config_windows_interaction(self):
        from src.config import config

        assert config["windows"]["interaction"] == "PostMessage"

    def test_config_has_ocr(self):
        from src.config import config

        assert "ocr" in config

    def test_config_has_onetime_tasks(self):
        from src.config import config

        assert "onetime_tasks" in config
        assert len(config["onetime_tasks"]) > 0

    def test_config_has_trigger_tasks(self):
        from src.config import config

        assert "trigger_tasks" in config

    def test_config_gui_title(self):
        from src.config import config

        assert config["gui_title"] == "OK-IN"

    def test_config_supported_resolution(self):
        from src.config import config

        assert config["supported_resolution"]["ratio"] == "16:9"


class TestSceneModule:
    """Test scene module structure."""

    def test_scene_imports(self):
        from src.scene.INScene import INScene

        assert INScene is not None

    def test_scene_inherits_base_scene(self):
        from ok import BaseScene
        from src.scene.INScene import INScene

        assert issubclass(INScene, BaseScene)

    def test_scene_has_reset(self):
        from src.scene.INScene import INScene

        assert hasattr(INScene, "reset")

    def test_scene_has_hud_tracking(self):
        from src.scene.INScene import INScene

        assert hasattr(INScene, "in_hud")
        assert hasattr(INScene, "set_in_hud")


class TestTaskModules:
    """Test task module structure."""

    def test_daily_task_imports(self):
        from src.task.DailyTask import DailyTask

        assert DailyTask is not None

    def test_skip_dialog_imports(self):
        from src.task.SkipDialogTask import SkipDialogTask

        assert SkipDialogTask is not None

    def test_auto_login_imports(self):
        from src.task.AutoLoginTask import AutoLoginTask

        assert AutoLoginTask is not None

    def test_daily_task_inherits_base_task(self):
        from ok import BaseTask
        from src.task.DailyTask import DailyTask

        assert issubclass(DailyTask, BaseTask)

    def test_trigger_tasks_inherit_correctly(self):
        from ok import BaseTask, TriggerTask
        from src.task.SkipDialogTask import SkipDialogTask
        from src.task.AutoLoginTask import AutoLoginTask

        assert issubclass(SkipDialogTask, BaseTask)
        assert issubclass(SkipDialogTask, TriggerTask)
        assert issubclass(AutoLoginTask, BaseTask)
        assert issubclass(AutoLoginTask, TriggerTask)
