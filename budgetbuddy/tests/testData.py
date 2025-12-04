
# tests/testData.py

import os
import json
import unittest
from pathlib import Path
from budgetbuddy.data import repository, csvio
from budgetbuddy.core.models import UserProfile, Income, Expense


class TestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test JSON file so we don't touch real data
        cls.original_data_file = repository.DATA_FILE
        cls.test_data_file = Path("test_budgetbuddy_data.json")
        repository.DATA_FILE = cls.test_data_file

    @classmethod
    def tearDownClass(cls):
        # Restore original path and remove test file
        repository.DATA_FILE = cls.original_data_file
        if cls.test_data_file.exists():
            cls.test_data_file.unlink()

    def setUp(self):
        # Fresh profiles dict for each test
        self.profiles = {}
        # Make sure file is clean at start of each test
        if repository.DATA_FILE.exists():
            repository.DATA_FILE.unlink()

    def tearDown(self):
        # Clean up between tests
        if repository.DATA_FILE.exists():
            repository.DATA_FILE.unlink()

    def test_create_save_and_load_profiles(self):
        # create two profiles
        p1 = repository.create_profile(self.profiles, "janet")
        p2 = repository.create_profile(self.profiles, "trip")

        # add a transaction so to_dict/from_dict are exercised
        p1.add_transaction(Income("2025-01-01", 100.0, "Salary", "Jan pay"))

        # assertions on in-memory dict
        self.assertIn("janet", self.profiles)
        self.assertIn("trip", self.profiles)
        self.assertEqual(len(self.profiles), 2)
        self.assertIsInstance(p1, UserProfile)

        # save and load back
        repository.save_profiles(self.profiles)
        self.assertTrue(repository.DATA_FILE.exists())

        loaded = repository.load_profiles()
        self.assertIn("janet", loaded)
        self.assertIn("trip", loaded)
        self.assertIsInstance(loaded["janet"], UserProfile)
        self.assertEqual(
            set(loaded.keys()),
            {"janet", "trip"},
        )

    def test_rename_and_delete_profile(self):
        repository.create_profile(self.profiles, "oldname")
        repository.create_profile(self.profiles, "keep")
        self.assertIn("oldname", self.profiles)
        self.assertIn("keep", self.profiles)

        # rename
        repository.rename_profile(self.profiles, "oldname", "newname")

        self.assertNotIn("oldname", self.profiles)
        self.assertIn("newname", self.profiles)
        self.assertEqual(self.profiles["newname"].name, "newname")
        self.assertEqual(len(self.profiles), 2)

        # delete
        repository.delete_profile(self.profiles, "newname")
        self.assertNotIn("newname", self.profiles)
        self.assertIn("keep", self.profiles)
        self.assertEqual(len(self.profiles), 1)


class TestCsvIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_path = "test_transactions.csv"

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.csv_path):
            os.remove(cls.csv_path)

    def setUp(self):
        # fresh profile with known transactions each test
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
        csvio.export_profile_to_csv(self.profile, self.csv_path)

        self.assertTrue(os.path.exists(self.csv_path))

        with open(self.csv_path, newline="", encoding="utf-8") as f:
            rows = list(json.reader)  # placeholder line
