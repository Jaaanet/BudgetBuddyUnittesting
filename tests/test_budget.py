# %%
import unittest
from budgetbuddy.core.budget import Budget

class TestTransaction:
    def __init__(self, amount, tx_type):
        self.amount = amount
        self.tx_type = tx_type

    def get_type(self):
        return self.tx_type

class TestUserProfile:
    def __init__(self, transactions):
        self.transactions = transactions

    def list_transactions(self, month, year):
        return self.transactions

class TestBudget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #creates fake transactions
        cls.tx1 = TestTransaction(500, "income")
        cls.tx2 = TestTransaction(1500, "income")
        cls.tx3 = TestTransaction(300, "expense")
        cls.tx4 = TestTransaction(1000, "expense")

    @classmethod
    def tearDownClass(cls):
         pass

    def setUp(self):
        self.profile = TestUserProfile([self.tx1, self.tx2, self.tx3, self.tx4])
        self.budget = Budget(self.profile)
        self.month = 12
        self.year = 2025

    def tearDown(self):
        pass
        
#first test case
    def test_month_totals(self):
        output = self.budget.month_totals(self.month, self.year)
        #assert statements
        self.assertEqual(output["income"], 2000)
        self.assertEqual(output["expense"], 1300)
        self.assertTrue(output["income"] > output["expense"])
        self.assertIn("net", output)

#second test case
    def test_month_transactions(self):
        txs = self.budget.month_transactions(self.month, self.year)
        #assert statements
        self.assertEqual(len(txs), 4)
        self.assertEqual(txs[0].amount, 500)
        self.assertNotEqual(txs[1].amount, 80)
        self.assertEqual(txs[2].get_type(), "expense")

#third test case (might as well since there were only 3 methods)
    def test_recent_transactions(self):
        txs = self.budget.recent_transactions(self.month, self.year)
        #assert statements
        self.assertEqual(len(txs), 4)
        self.assertEqual(txs[1].amount, 1500)
        self.assertTrue(len(txs) > 0)
        self.assertNotEqual(txs[0].amount, 100)

unittest.main(argv=[''], verbosity=2, exit=False) 


