"""Daily task for Infinity Nikki - one-click daily routine.

Handles the complete daily workflow:
1. Handle popups (monthly card, login rewards, etc.)
2. Complete Daily Wishes (朝夕心愿) - earn 500 points
3. Spend Vital Energy in Realms (幻境)
4. Dispatch Pear-Pal expedition
5. Claim mail rewards
6. Collect rare materials (optional)
"""

import re

from ok import OneTimeTask


class DailyTask(OneTimeTask):
    """One-click daily task for Infinity Nikki.

    Automatically completes the daily routine including
    daily wishes, vital energy spending, pear-pal dispatch, etc.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config = {
            "Complete Daily Wishes": True,
            "Spend Vital Energy": True,
            "Realm Type": "Escalation",
            "Dispatch Pear-Pal": True,
            "Pear-Pal Duration": "20h",
            "Claim Mail": True,
            "Check Monthly Card": True,
        }
        self.config_type = {
            "Realm Type": {
                "options": ["Escalation", "Nourishment", "Dark", "Eureka", "Breakthrough"],
            },
            "Pear-Pal Duration": {
                "options": ["4h", "8h", "12h", "20h"],
            },
        }
        self.config_description = {
            "Complete Daily Wishes": "Complete daily wishes to earn 500 points",
            "Spend Vital Energy": "Spend all vital energy in the selected realm",
            "Realm Type": "Which realm to spend vital energy in",
            "Dispatch Pear-Pal": "Send Pear-Pal on expedition",
            "Pear-Pal Duration": "Expedition duration for Pear-Pal",
            "Claim Mail": "Claim all mail rewards",
            "Check Monthly Card": "Handle monthly card popup to avoid interruption",
        }

    def run(self):
        """Execute the daily task workflow."""
        self.log_info("Starting daily task...")
        self.info_set("Status", "Running")

        # Step 1: Handle any popups first
        self._handle_popups()

        # Step 2: Complete Daily Wishes
        if self.get_config("Complete Daily Wishes"):
            self._complete_daily_wishes()

        # Step 3: Spend Vital Energy
        if self.get_config("Spend Vital Energy"):
            self._spend_vital_energy()

        # Step 4: Dispatch Pear-Pal
        if self.get_config("Dispatch Pear-Pal"):
            self._dispatch_pear_pal()

        # Step 5: Claim mail
        if self.get_config("Claim Mail"):
            self._claim_mail()

        # Step 6: Handle any remaining popups
        self._handle_popups()

        self.info_set("Status", "Completed")
        self.log_info("Daily task completed!")
        self.notification("Daily task completed!", tray=True)

    def _handle_popups(self):
        """Handle interrupting popups like monthly card, login rewards, etc."""
        # Check and close monthly card popup
        if self.get_config("Check Monthly Card"):
            monthly_card = self.wait_feature("monthly_card", time_out=2, raise_if_not_found=False)
            if monthly_card:
                self.log_info("Found monthly card popup, closing...")
                self.click_box(monthly_card, after_sleep=1)

        # Check and close any dialog popups
        dialog_close = self.wait_feature("dialog_close", time_out=1, raise_if_not_found=False)
        if dialog_close:
            self.log_info("Found dialog popup, closing...")
            self.click_box(dialog_close, after_sleep=0.5)

        # Check for login reward claim
        claim_btn = self.wait_feature("login_claim_button", time_out=1, raise_if_not_found=False)
        if claim_btn:
            self.log_info("Found login reward, claiming...")
            self.click_box(claim_btn, after_sleep=1)

    def _complete_daily_wishes(self):
        """Complete Daily Wishes (朝夕心愿) to earn 500 points.

        Daily wishes include tasks like:
        - Taking photos
        - Collecting items
        - Completing mini-games
        - Spending vital energy
        - Crafting items
        """
        self.log_info("Starting Daily Wishes...")
        self.info_set("Step", "Daily Wishes")

        # Navigate to Daily Wishes via menu
        # Press L key to open daily wishes (default hotkey)
        self.send_key("l", after_sleep=1)

        # Wait for daily wishes screen
        daily_title = self.wait_feature("daily_wishes_title", time_out=5, raise_if_not_found=False)
        if not daily_title:
            self.log_info("Could not open Daily Wishes screen, trying alternate method...")
            # Try clicking the daily wishes button on HUD
            self.wait_click_feature("daily_wishes_button", time_out=5, raise_if_not_found=False)

        # Process each wish task
        # Each wish appears as a bottle icon that can be clicked to complete/claim
        for i in range(6):  # Max 6 daily wishes
            self.sleep(0.5)
            wish_bottle = self.find_one("wish_bottle", threshold=0.7)
            if wish_bottle:
                self.log_info(f"Processing wish bottle {i + 1}...")
                self.click_box(wish_bottle, after_sleep=1)

                # Check if there's a "Go" or "Claim" button
                go_btn = self.wait_feature("wish_go_button", time_out=2, raise_if_not_found=False)
                if go_btn:
                    self.click_box(go_btn, after_sleep=1)

                claim_btn = self.wait_feature("wish_claim_button", time_out=2, raise_if_not_found=False)
                if claim_btn:
                    self.click_box(claim_btn, after_sleep=0.5)

        # Check if we've reached 500 points
        daily_points = self.ocr(
            box="daily_points_area",
            match=re.compile(r"\d+"),
            threshold=0.5,
        )
        if daily_points:
            self.log_info(f"Daily Wishes points: {daily_points[0].name}")

        # Claim overall daily reward if available
        self.wait_click_feature("daily_claim_all", time_out=2, raise_if_not_found=False, after_sleep=1)

        # Close daily wishes screen
        self.wait_click_feature("daily_close_button", time_out=3, raise_if_not_found=False, after_sleep=0.5)

        self.log_info("Daily Wishes completed.")

    def _spend_vital_energy(self):
        """Spend all Vital Energy in the selected Realm.

        Realm options:
        - Escalation: Bling, Shiny Bubbles, Thread of Purity
        - Nourishment: Insight EXP
        - Dark: Boss materials
        - Eureka: Eureka pieces
        - Breakthrough: Weekly boss (once per week)
        """
        realm_type = self.get_config("Realm Type")
        self.log_info(f"Spending Vital Energy in {realm_type} Realm...")
        self.info_set("Step", f"Realm: {realm_type}")

        # Open the Pear-Pal (phone menu) to access Realms
        self.send_key("tab", after_sleep=1)

        # Navigate to Realm section
        self.wait_click_feature("realm_menu_button", time_out=5, raise_if_not_found=False, after_sleep=0.5)

        # Select the specific realm type
        realm_feature_map = {
            "Escalation": "realm_escalation",
            "Nourishment": "realm_nourishment",
            "Dark": "realm_dark",
            "Eureka": "realm_eureka",
            "Breakthrough": "realm_breakthrough",
        }
        realm_feature = realm_feature_map.get(realm_type, "realm_escalation")
        self.wait_click_feature(realm_feature, time_out=5, raise_if_not_found=True, after_sleep=0.5)

        # Enter the realm
        self.wait_click_feature("realm_enter_button", time_out=3, raise_if_not_found=True, after_sleep=1)

        # Spend all available energy
        # Click on the max energy option
        self.wait_click_feature("realm_max_energy", time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # Confirm
        self.wait_click_ocr(match=re.compile("确认|Confirm"), time_out=3, raise_if_not_found=True, after_sleep=1)

        # Wait for realm completion
        self.sleep(5)

        # Claim rewards and exit
        self.wait_click_feature("realm_claim_button", time_out=30, raise_if_not_found=False, after_sleep=1)
        self.wait_click_feature("realm_exit_button", time_out=5, raise_if_not_found=False, after_sleep=0.5)

        self.log_info(f"Vital Energy spent in {realm_type} Realm.")

    def _dispatch_pear_pal(self):
        """Dispatch Pear-Pal on expedition for resources."""
        duration = self.get_config("Pear-Pal Duration")
        self.log_info(f"Dispatching Pear-Pal for {duration}...")
        self.info_set("Step", "Pear-Pal Dispatch")

        # Open Pear-Pal menu
        self.send_key("tab", after_sleep=1)
        self.wait_click_feature("pear_pal_menu_button", time_out=5, raise_if_not_found=False, after_sleep=0.5)

        # Go to expedition tab
        self.wait_click_feature("pear_pal_expedition_tab", time_out=3, raise_if_not_found=False, after_sleep=0.5)

        # Check if Pear-Pal is already on expedition
        already_dispatched = self.find_one("pear_pal_dispatched", threshold=0.8)
        if already_dispatched:
            self.log_info("Pear-Pal is already on expedition, skipping.")
            # Close menu
            self.send_key("escape", after_sleep=0.5)
            return

        # Select duration
        duration_feature_map = {
            "4h": "pear_pal_4h",
            "8h": "pear_pal_8h",
            "12h": "pear_pal_12h",
            "20h": "pear_pal_20h",
        }
        duration_feature = duration_feature_map.get(duration, "pear_pal_20h")
        self.wait_click_feature(duration_feature, time_out=3, raise_if_not_found=True, after_sleep=0.5)

        # Select resource type (prioritize Thread of Purity / Shining Particles)
        self.wait_click_feature("pear_pal_thread_purity", time_out=2, raise_if_not_found=False, after_sleep=0.5)

        # Dispatch
        self.wait_click_ocr(match=re.compile("出发|Dispatch"), time_out=3, raise_if_not_found=True, after_sleep=1)

        # Close menu
        self.send_key("escape", after_sleep=0.5)

        self.log_info(f"Pear-Pal dispatched for {duration}.")

    def _claim_mail(self):
        """Claim all mail rewards."""
        self.log_info("Claiming mail rewards...")
        self.info_set("Step", "Claiming Mail")

        # Open Pear-Pal (phone menu)
        self.send_key("tab", after_sleep=1)

        # Navigate to mail
        self.wait_click_feature("mail_menu_button", time_out=5, raise_if_not_found=False, after_sleep=0.5)

        # Claim all
        self.wait_click_feature("mail_claim_all", time_out=3, raise_if_not_found=False, after_sleep=1)

        # Confirm
        self.wait_click_ocr(match=re.compile("确认|Confirm"), time_out=2, raise_if_not_found=False, after_sleep=0.5)

        # Close mail
        self.send_key("escape", after_sleep=0.5)

        self.log_info("Mail rewards claimed.")
