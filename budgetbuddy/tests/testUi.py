# tests/test_ui.py

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from budgetbuddy.ui.main import BudgetBuddyApp
from budgetbuddy.ui import summary
from budgetbuddy.core.models import UserProfile, Income, Expense


class TestSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.profile = UserProfile("janet")
        self.profile.add_transaction(
            Income("2025-01-10", 100.0, "Salary", "Pay")
        )
        self.profile.add_transaction(
            Expense("2025-01-11", 20.0, "Food", "Snacks")
        )

    def tearDown(self):
        pass

    def test_print_profiles_list(self):
        profiles = {
            "janet": self.profile,
            "travel": UserProfile("travel"),
        }

        buf = io.StringIO()
        with redirect_stdout(buf):
            summary.print_profiles_list(profiles)
        out = buf.getvalue()

        self.assertIn("=== Saved profiles ===", out)
        self.assertIn("[0] janet", out)
        self.assertIn("[1] travel", out)
        self.assertNotIn("(no profiles yet)", out)

    def test_print_transactions_empty_and_nonempty(self):
        # empty list
        buf1 = io.StringIO()
        with redirect_stdout(buf1):
            summary.print_transactions([])
        out1 = buf1.getvalue()

        self.assertIn("(no transactions)", out1)
        self.assertNotIn("date | type", out1)
        self.assertEqual(out1.strip().endswith("(no transactions)"), True)
        self.assertGreater(len(out1), 0)

        # non-empty list
        txs = self.profile.transactions
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            summary.print_transactions(txs)
        out2 = buf2.getvalue()

        self.assertIn("date | type | category | amount | notes", out2)
        self.assertIn("[0]", out2)
        self.assertIn("Salary", out2)
        self.assertIn("Food", out2)


class TestBudgetBuddyApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # make sure a guide file exists where main.py expects it
        from budgetbuddy.ui import main as main_mod
        cls.ui_dir = os.path.dirname(main_mod.__file__)
        cls.guide_path = os.path.join(cls.ui_dir, "guide.txt")

        if not os.path.exists(cls.guide_path):
            with open(cls.guide_path, "w", encoding="utf-8") as f:
                f.write("=== BudgetBuddy Guide ===\nThis is a test guide.\n")

    @classmethod
    def tearDownClass(cls):
        # leave the guide file in place for the real app
        pass

    def setUp(self):
        # start with a fresh app – load_profiles() will see whatever JSON exists
        self.app = BudgetBuddyApp()

    def tearDown(self):
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
        # simulate typing "janet" then hit Enter
        with patch("builtins.input", side_effect=["janet"]), \
             patch("budgetbuddy.ui.main.repository.save_profiles") as mock_save:

            self.app.create_profile_flow()

        self.assertIn("janet", self.app.profiles)
        self.assertIsInstance(self.app.profiles["janet"], UserProfile)
        self.assertEqual(self.app.profiles["janet"].name, "janet")
        self.assertTrue(mock_save.called)


if __name__ == "__main__":
    unittest.main()
