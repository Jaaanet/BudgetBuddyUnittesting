# tests/test_repository.py

import unittest
from pathlib import Path

from budgetbuddy.data import repository
from budgetbuddy.core.models import UserProfile, Income


class TestRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Use a temporary JSON file so we don't touch the real
        budgetbuddy_data.json used by the actual program.
        """
        cls.original_data_file = repository.DATA_FILE
        cls.test_data_file = Path("test_budgetbuddy_data.json")
        repository.DATA_FILE = cls.test_data_file

    @classmethod
    def tearDownClass(cls):
        """Restore original DATA_FILE and delete the temporary JSON."""
        repository.DATA_FILE = cls.original_data_file
        if cls.test_data_file.exists():
            cls.test_data_file.unlink()

    def setUp(self):
        """Start each test with a clean profiles dict and no JSON file."""
        self.profiles = {}
        if repository.DATA_FILE.exists():
            repository.DATA_FILE.unlink()

    def tearDown(self):
        """Clean up any JSON created during the test."""
        if repository.DATA_FILE.exists():
            repository.DATA_FILE.unlink()

    def test_create_save_and_load_profiles(self):
        # Create two profiles
        p1 = repository.create_profile(self.profiles, "janet")
        p2 = repository.create_profile(self.profiles, "trip")

        # Add a transaction to first profile
        p1.add_transaction(Income("2025-01-01", 100.0, "Salary", "Jan pay"))

        # In-memory checks
        self.assertIn("janet", self.profiles)
        self.assertIn("trip", self.profiles)
        self.assertEqual(len(self.profiles), 2)
        self.assertIsInstance(p1, UserProfile)

        # Save to JSON
        repository.save_profiles(self.profiles)
        self.assertTrue(repository.DATA_FILE.exists())

        # Load back from JSON
        loaded = repository.load_profiles()

        self.assertIsInstance(loaded, dict)
        self.assertIn("janet", loaded)
        self.assertIn("trip", loaded)
        self.assertEqual(set(loaded.keys()), {"janet", "trip"})
        self.assertIsInstance(loaded["janet"], UserProfile)
        self.assertGreaterEqual(len(loaded["janet"].transactions), 1)

    def test_rename_and_delete_profile(self):
        # Create two profiles
        repository.create_profile(self.profiles, "oldname")
        repository.create_profile(self.profiles, "keep")

        self.assertIn("oldname", self.profiles)
        self.assertIn("keep", self.profiles)
        self.assertEqual(len(self.profiles), 2)
        self.assertIsInstance(self.profiles["oldname"], UserProfile)

        # Rename one profile
        repository.rename_profile(self.profiles, "oldname", "newname")

        self.assertNotIn("oldname", self.profiles)
        self.assertIn("newname", self.profiles)
        self.assertEqual(self.profiles["newname"].name, "newname")
        self.assertEqual(len(self.profiles), 2)

        # Delete the renamed profile
        repository.delete_profile(self.profiles, "newname")

        self.assertNotIn("newname", self.profiles)
        self.assertIn("keep", self.profiles)
        self.assertEqual(len(self.profiles), 1)
        self.assertEqual(self.profiles["keep"].name, "keep")


if __name__ == "__main__":
    unittest.main()
