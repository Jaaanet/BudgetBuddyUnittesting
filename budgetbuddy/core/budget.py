# %%
from typing import Dict, List
from budgetbuddy.core.models import UserProfile, Transaction

class Budget:
    '''
    This class calculates income, expenses, and recent n (for user-chosen value of n) 
    transactions for a user's budget for a given month.
    '''
    def __init__(self, profile: UserProfile):
        self.profile = profile

    def month_totals(self, month: int, year: int):
        '''
        Returns dictionary for the month that includes overall income, overall expenses, and net amount.
        '''
        #all transactions for the month and year
        txs = self.profile.list_transactions(month, year)
        income = 0.0
        expense = 0.0
        #go through transactions one by one
        for t in txs:
            #checks if transaction is income
            if t.get_type() == "income":
                income += t.amount
            #if not income, checks if transaction is an expense
            elif t.get_type() == "expense":
                expense += t.amount
        net = income - expense
        #results are returned as a dictionary
        return {"income": income, "expense": expense, "net": net}

    def month_transactions(self, month: int, year: int):
        '''
        returns all transactions for month and year
        '''
        return self.profile.list_transactions(month, year)

    def recent_transactions(self, month: int, year: int):
        '''
        Returns latest n transactions for the month (for whatever value of n the user chooses).
        If there are less than n transaction it returns everything.
        '''
        txs = self.month_transactions(month, year)
        #if less than n transactions, returns everything
        # if len(txs) <= n:
        return txs
        # else:
        #     #returns last n transactions if more than n total transactions
            #return txs[-n:]

        

# %%



