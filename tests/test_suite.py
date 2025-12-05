# tests/test_suite.py

import unittest

from .test_repository import TestRepository
from .test_csvio import TestCsvIO
from .test_summary import TestSummary
from .test_main import TestBudgetBuddyApp
from .test_budget import TestBudget
from .test_models import TestUserProfile


def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    for test_class in (TestRepository, TestCsvIO, TestSummary, TestBudgetBuddyApp, TestBudget, TestUserProfile):
        test_suite.addTests(loader.loadTestsFromTestCase(test_class))

    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
