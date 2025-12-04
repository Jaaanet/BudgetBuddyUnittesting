# tests/test_main.py

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from budgetbuddy.ui.main import BudgetBuddyApp
from budgetbuddy.core.models import UserProfile


class TestBudgetBuddyApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Ensure guide.txt exists in the same directory as main.py so
        show_guide() has something to print.
        """
        from budgetbuddy.ui import main as main_mod

        cls.ui_dir = os.path.dirname(main_mod.__file__)
        cls.guide_path = os.path.join(cls.ui_dir, "guide.txt")

        if not os.path.exists(cls.guide_path):
            with open(cls.guide_path, "w", encoding="utf-8") as f:
                f.write("=== BudgetBuddy Guide ===\nThis is a test guide.\n")

    @classmethod
    def tearDownClass(cls):
        # We leave guide.txt in place since the real app uses it.
        pass

    def setUp(self):
        # Patch load_profiles so __init__ doesn't touch disk
        patcher = patch("budgetbuddy.ui.main.repository.load_profiles", return_value={})
        self.mock_load = patcher.start()
        self.addCleanup(patcher.stop)

        self.app = BudgetBuddyApp()

    def tearDown(self):
        # Any per-test cleanup can go here (none needed now)
        pass

    def test_show_guide_prints_text(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.app.show_guide()
        out = buf.getvalue()

        self.assertIn("Guide", out)
        self.assertIn("BudgetBuddy", out)
        self.assertGreater(len(out.strip()), 0)
        self.assertNotIn("Guide file not found", out)

    def test_create_profile_flow_adds_profile(self):
        # Simulate typing "janet" and patch save_profiles so we don't write JSON
        with patch("builtins.input", side_effect=["janet"]), \
             patch("budgetbuddy.ui.main.repository.save_profiles") as mock_save:

            self.app.create_profile_flow()

        self.assertIn("janet", self.app.profiles)
        self.assertIsInstance(self.app.profiles["janet"], UserProfile)
        self.assertEqual(self.app.profiles["janet"].name, "janet")
        self.assertTrue(mock_save.called)


if __name__ == "__main__":
    unittest.main()
