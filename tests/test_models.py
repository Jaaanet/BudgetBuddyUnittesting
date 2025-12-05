# %%
import unittest
from budgetbuddy.core.models import UserProfile, Income, Expense

class TestUserProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tx1 = Income("2025-12-02", 1000, "job")
        cls.tx2 = Expense("2025-12-08", 25, "lunch")
        cls.tx3 = Expense("2025-12-13", 600, "christmas shopping")
        cls.tx4 = Income("2025-12-16", 1500, "job")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.user = UserProfile("Rachel")
        self.user.add_transactions(self.tx1)
        self.user.add_transactions(self.tx2)
        self.user.add_transactions(self.tx3)
        self.user.add_transactions(self.tx4)

    def tearDown(self):
        pass

#first test case
    def test_list_transactions(self):
        txs = self.user.list_transactions()
        #assertions
        self.assertEqual(len(txs), 4)
        self.assertGreater(txs[1].amount, 100)
        self.assertIs(txs[3], self.tx4)
        self.assertTrue(txs[0].category == "job")

#second test case
    def test_recent_transactions(self):
        recent = self.user.recent_transactions(12, 2025, 3)
        #assertions
        self.assertEqual(len(recent), 3)
        self.assertNotIn(self.tx1, recent)
        self.assertLess(recent[2].amount, 1000)
        self.assertIs(recent[-1], self.tx4)

unittest.main(argv=[''], verbosity=2, exit=False)


