# tests/test_csvio.py

import os
import csv
import unittest

from budgetbuddy.data import csvio
from budgetbuddy.core.models import UserProfile, Income, Expense, Transaction


class TestCsvIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_path = "test_transactions.csv"

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.csv_path):
            os.remove(cls.csv_path)

    def setUp(self):
        # Fresh profile with known transactions for each test
        self.profile = UserProfile("janet")
        self.profile.add_transaction(
            Income("2025-01-10", 200.0, "Salary", "Part-time job")
        )
        self.profile.add_transaction(
            Expense("2025-01-11", 50.0, "Food", "Groceries")
        )

    def tearDown(self):
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    def test_export_profile_to_csv(self):
        # Export to CSV
        csvio.export_profile_to_csv(self.profile, self.csv_path)

        # CSV file should exist
        self.assertTrue(os.path.exists(self.csv_path))

        # Read back the CSV and inspect rows
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 2)
        self.assertEqual(
            set(rows[0].keys()),
            {"date", "amount", "category", "description", "type"},
        )
        # Check content of first row
        self.assertEqual(rows[0]["date"], "2025-01-10")
        self.assertEqual(rows[0]["category"], "Salary")
        self.assertEqual(rows[0]["type"], "income")

    def test_import_transactions_from_csv(self):
        # First export from original profile
        csvio.export_profile_to_csv(self.profile, self.csv_path)

        # Import into a new profile
        new_profile = UserProfile("copy")
        csvio.import_transactions_from_csv(new_profile, self.csv_path)

        self.assertEqual(len(new_profile.transactions), len(self.profile.transactions))
        self.assertIsInstance(new_profile.transactions[0], Transaction)
        self.assertEqual(new_profile.transactions[0].date, "2025-01-10")
        self.assertEqual(new_profile.transactions[1].category, "Food")
        self.assertAlmostEqual(new_profile.transactions[1].amount, 50.0, places=2)


if __name__ == "__main__":
    unittest.main()
