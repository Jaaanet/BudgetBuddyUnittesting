# tests/test_summary.py

import io
import unittest
from contextlib import redirect_stdout

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
        # Profile and some transactions for printing tests
        self.profile = UserProfile("janet")
        self.profile.add_transaction(
            Income("2025-03-01", 300.0, "Salary", "March pay")
        )
        self.profile.add_transaction(
            Expense("2025-03-02", 40.0, "Food", "Dinner")
        )

    def tearDown(self):
        pass

    def test_print_profiles_list_nonempty(self):
        profiles = {
            "janet": self.profile,
            "travel": UserProfile("travel"),
        }

        buf = io.StringIO()
        with redirect_stdout(buf):
            summary.print_profiles_list(profiles)
        out = buf.getvalue()

        self.assertIn("Saved profiles", out)
        self.assertIn("janet", out)
        self.assertIn("travel", out)
        self.assertNotIn("(no profiles yet)", out)

    def test_print_transactions_empty_and_nonempty(self):
        # Empty list
        buf1 = io.StringIO()
        with redirect_stdout(buf1):
            summary.print_transactions([])
        out1 = buf1.getvalue()

        self.assertIn("(no transactions)", out1)
        self.assertGreater(len(out1.strip()), 0)
        self.assertTrue(out1.strip().endswith("(no transactions)"))
        self.assertNotIn("[0]", out1)

        # Non-empty list
        txs = self.profile.transactions
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            summary.print_transactions(txs)
        out2 = buf2.getvalue()

        self.assertIn("[0]", out2)
        self.assertIn("Salary", out2)
        self.assertIn("Food", out2)
        self.assertIn("2025-03-01", out2)


if __name__ == "__main__":
    unittest.main()
