"""BaseINTask: base task class for Infinity Nikki.

Mirrors src/task/BaseWWTask.py structure from ok-ww.
Provides common navigation, feature lookup, and game-state methods.
Does NOT include combat logic (no battle system in Infinity Nikki).
"""

import re
import time
from datetime import datetime, timedelta

import cv2
import numpy as np

from ok import BaseTask, Logger, og, CannotFindException

from src.Labels import Labels
from src.scene.INScene import INScene

logger = Logger.get_logger(__name__)

# Login-related OCR patterns
LOGIN_TEXTS = ["登录", re.compile(r"Log", re.IGNORECASE), "登入"]

# Color range for white F-key highlight detection
f_white_color = {
    "r": (235, 255),
    "g": (235, 255),
    "b": (235, 255),
}


class BaseINTask(BaseTask):
    """Base task for Infinity Nikki.

    Mirrors BaseWWTask from ok-ww.
    All IN tasks should inherit from this class.
    """

    map_zoomed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monthly_card_config = self.get_global_config("Monthly Card Config")
        self.next_monthly_card_start = 0
        self.scene: INScene | None = None

    # ── logged_in property (mirrors BaseWWTask) ─────────────

    @property
    def logged_in(self):
        """Check if user is logged in.

        Stored in og.my_app.logged_in (set by Globals class in src/globals.py).
        This mirrors ok-ww's pattern where logged_in is stored in Globals.
        """
        return getattr(og.my_app, "logged_in", False)

    @logged_in.setter
    def logged_in(self, value):
        og.my_app.logged_in = value

    # ── Monthly card helpers ────────────────────────────────

    def set_check_monthly_card(self, next_day=False):
        if self.monthly_card_config.get("Check Monthly Card"):
            now = datetime.now()
            hour = self.monthly_card_config.get("Monthly Card Time")
            next_target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if now >= next_target or next_day:
                next_target += timedelta(days=1)
            self.next_monthly_card_start = (next_target - timedelta(seconds=30)).timestamp()
            logger.info(f"set next monthly card start time to {next_target - timedelta(seconds=30)}")
        else:
            self.next_monthly_card_start = 0

    def find_monthly_card(self):
        return self.find_one(Labels.monthly_card, threshold=0.65,
                             horizontal_variance=0.05, vertical_variance=0.05)

    def handle_monthly_card(self):
        monthly_card = self.find_monthly_card()
        if monthly_card is not None:
            self.log_info("monthly_card found, clicking")
            self.click_relative(0.50, 0.89)
            self.sleep(2)
            self.click_relative(0.50, 0.89)
            self.sleep(2)
            self.wait_until(self.in_team_and_world, time_out=10,
                           post_action=lambda: self.click_relative(0.50, 0.89, after_sleep=1))
            self.set_check_monthly_card(next_day=True)
        return monthly_card is not None

    # ── Navigation / main-state helpers ────────────────────

    def ensure_main(self, esc=True, time_out=30):
        """Wait until the game is at the main HUD screen.

        Mirrors ok-ww BaseWWTask.ensure_main().
        If not logged in, extends timeout to 600s.
        """
        self.info_set("current task", f"wait main esc={esc}")
        if not self.logged_in:
            time_out = 600
        if not self.wait_until(lambda: self.is_main(esc=esc), time_out=time_out,
                              raise_if_not_found=False):
            raise Exception("Please start in game world!")
        self.sleep(0.5)
        self.info_set("current task", f"in main esc={esc}")

    def is_main(self, esc=True):
        """Check if game is at main HUD, handling login dialogs."""
        if self.in_team_and_world():
            self.logged_in = True
            return True
        if self.wait_login():
            return False
        if self.handle_monthly_card():
            return False
        if esc:
            self.log_debug("main esc")
            self.back(after_sleep=2)
            return False
        return False

    def wait_login(self):
        """Handle login screen: click login button, close announcements, etc.

        Mirrors ok-ww BaseWWTask.wait_login().
        """
        if self.logged_in:
            return True
        if self.in_team_and_world():
            self.logged_in = True
            return True

        self.handle_monthly_card()

        # Close announcement dialog if present
        if login_close := self.find_one(Labels.login_button, horizontal_variance=0.15,
                                       vertical_variance=0.1):
            self.click(login_close, after_sleep=1)
            self.log_info("closed announcement!")
            return False

        texts = self.ocr(log=self.debug)

        # Check for login button text
        if login_boxes := self.find_boxes(texts,
                                          boundary=self.box_of_screen(0.3, 0.3, 0.7, 0.7),
                                          match=LOGIN_TEXTS):
            if not self.find_boxes(texts,
                                  boundary=self.box_of_screen(0.3, 0.3, 0.7, 0.7),
                                  match="+86"):
                self.click(login_boxes, after_sleep=1)
                self.log_info("clicked login button!")
            return False

        # Check for "agree" button (privacy policy)
        if agree := self.find_boxes(texts,
                                   boundary=self.box_of_screen(0.3, 0.3, 0.7, 0.7),
                                   match="同意"):
            self.log_debug(f"found agree {agree}")
            if self.find_boxes(texts,
                              boundary=self.box_of_screen(0.3, 0.3, 0.7, 0.7),
                              match=re.compile("隐私")):
                self.click(agree, after_sleep=1)
                self.log_info("clicked agree button!")
            return False

        # Check for "start game" button
        if start := self.find_boxes(texts, boundary="bottom_right",
                                   match=["开始游戏", re.compile(r"进入游戏")]):
            if not self.find_boxes(texts, boundary="bottom_right", match=LOGIN_TEXTS):
                self.click(start)
                self.log_info(f"clicked start game! {start}")
            return False

        return False

    def in_team_and_world(self):
        """Check if the game is at the main HUD (team visible in world).

        For Infinity Nikki, this is detected by finding hud_pearpal icon.
        Mirrors ok-ww's in_team_and_world() which calls in_team().
        """
        return self.find_one(Labels.hud_pearpal, threshold=0.8) is not None

    def in_team(self):
        """Alias for in_team_and_world for compatibility.

        Mirrors ok-ww BaseWWTask.in_team() which returns a tuple.
        For IN, we simplify to returning a tuple consistent with ok-script API.
        """
        result = self.in_team_and_world()
        return (result, -1, 1 if result else 0)

    def check_main(self):
        """Verify we are at main screen, raise if not."""
        if not self.in_team_and_world():
            self.click_relative(0, 0)
            self.send_key("esc")
            self.sleep(1)
            if not self.in_team_and_world():
                raise Exception("must be in game world!")
        return True

    # ── Game language detection ─────────────────────────────

    @property
    def game_lang(self):
        if "无限暖暖" in self.hwnd_title or "Infinity Nikki" in self.hwnd_title:
            return "zh_CN"
        return "unknown_lang"

    # ── Back / ESC helpers ─────────────────────────────────

    def back(self, times=1, after_sleep=0):
        """Press ESC or click back button to navigate back.

        Mirrors ok-ww BaseWWTask.back().
        """
        for _ in range(times):
            back_btn = self.find_one(Labels.back_button, threshold=0.8)
            if back_btn:
                self.click_box(back_btn, after_sleep=after_sleep)
            else:
                self.send_key("esc", after_sleep=after_sleep)

    # ── Feature lookup helpers ──────────────────────────────

    def get_feature_by_lang(self, feature):
        """Get feature name with language suffix if available."""
        lang_feature = feature + "_" + self.game_lang
        if self.feature_exists(lang_feature):
            return lang_feature
        return None

    # ── F-key / interact helpers ────────────────────────────

    def f_search_box(self):
        """Get a search box around the F-key pickup indicator."""
        f_box = self.find_one("pick_up_f_hcenter_vcenter", threshold=0.8)
        if f_box is None:
            return None
        return f_box.copy(
            x_offset=-f_box.width * 0.3,
            width_offset=f_box.width * 0.65,
            height_offset=f_box.height * 6.5,
            y_offset=-f_box.height * 5,
            name="search_dialog",
        )

    def find_f_with_text(self, target_text=None):
        """Find F-key pickup indicator with specific nearby text."""
        f = self.find_one("pick_up_f_hcenter_vcenter", box=self.f_search_box(),
                         threshold=0.8)
        if not f:
            return None
        if not target_text:
            return f

        start = time.time()
        percent = 0.0
        while time.time() - start < 1:
            percent = self.calculate_color_percentage(f_white_color, f)
            if percent > 0.5:
                break
            self.next_frame()
            self.log_debug(f"f white color percent: {percent} wait")
        if percent < 0.5:
            return None

        if target_text:
            search_text_box = f.copy(
                x_offset=f.width * 5.2, width_offset=f.width * 6,
                height_offset=4.5 * f.height, y_offset=-0.8 * f.height,
                name="search_text_box",
            )
            text = self.ocr(box=search_text_box, match=target_text)
            logger.debug(f"found f with text {text}, target_text {target_text}")
            if text:
                if text[0].y > search_text_box.y + f.height * 1:
                    logger.debug(f"found f with text {text} below, target_text {target_text}")
                    self.scroll_relative(0.5, 0.5, 1)
                return f
        else:
            return f

    # ── Image processing helpers ────────────────────────────

    def find_skip_button(self):
        """Find skip dialog button."""
        return self.find_one(Labels.skip_button, threshold=0.8)


# ── Color / image processing functions (mirrors BaseWWTask) ──

lower_white = np.array([244, 244, 244], dtype=np.uint8)
lower_white_none_inclusive = np.array([240, 240, 240], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
black = np.array([0, 0, 0], dtype=np.uint8)
lower_icon_white = np.array([210, 210, 210], dtype=np.uint8)
upper_icon_white = np.array([244, 244, 244], dtype=np.uint8)


def isolate_white_text_to_black(cv_image):
    """Convert near-white pixels (244-255) to black, others to white."""
    match_mask = cv2.inRange(cv_image, black, lower_white_none_inclusive)
    return cv2.cvtColor(match_mask, cv2.COLOR_GRAY2BGR)


def convert_bw(cv_image):
    """Binarize image: white pixels become white, all others become black."""
    match_mask = cv2.inRange(cv_image, lower_white, upper_white)
    return cv2.cvtColor(match_mask, cv2.COLOR_GRAY2BGR)


def convert_dialog_icon(cv_image):
    """Extract dialog icon by keeping icon-white range."""
    match_mask = cv2.inRange(cv_image, lower_icon_white, upper_icon_white)
    return cv2.cvtColor(match_mask, cv2.COLOR_GRAY2BGR)


def binarize_for_matching(cv_image):
    """Binarize for template matching: pixels > 244 become white."""
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 244, 255, cv2.THRESH_BINARY)
    return binary
