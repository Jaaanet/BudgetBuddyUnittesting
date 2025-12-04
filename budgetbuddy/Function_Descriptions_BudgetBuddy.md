# Function Descriptions for Our Budget Buddy Program
## Core Sub-Package
### models.py Module
### Classes: Transaction, Income, Expense, UserProfile
### Class: Transaction
#### Methods:
- to_dict(self): Converts the transaction object into a dictionary
- from_dict(cls, data): Creates the transaction type (Income or Expense) based on the transaction dictionary
- get_type(self): Returns the type of transaction as a string- just "transaction" for the base case
### Class: Income (Inherits from Transaction)
#### Method:
- get_type(self): Returns the type of transaction as a string- income
### Class: Expense (Inherits from Transaction)
#### Method:
- get_type(self): Returns the type of transaction as a string- expense
### Class: UserProfile
#### Methods:
- add_transactions(self, tx): Adds a transaction object to the user's profile
- list_transactions(self, month=None, year=None): Returns transactions for the chosen month and year or all transactions if no month/year chosen
- recent_transactions(self, month, year, n): Returns the latest n transactions for the given n, month, and year 
- delete_transaction(self, tx): Deletes a chosen transaction from the user's profile
- to_dict(self): Converts the profile into a dictionary that includes all transactions
- from_dict(cls, data): Creates a UserProfile from a dictionary
### budget.py Module
### Class: Budget
#### Methods:
- month_totals(self, month: int, year: int): Returns a dictionary that contains the total income for the month, total expenses for the month, and net balance
- month_transactions(self, month: int, year: int): Returns all transactions for the given month and year
- recent_transactions(self, month: int, year: int, n: int): Returns the latest n transactions for the given n, month, and year. If there were less than n transactions, it returns all the transactions for that month and year

## data Sub-Package
### csvio.py Module
#### Functions:
- export_profile_to_csv(profile, filepath): Exports all transactions from a UserProfile to a CSV file where every transaction is saved and includes the date, amount, category, description, and type
- import_transactions_from_csv(profile, filepath): Reads a CSV file with transaction information and adds the transactions to the UserProfile
### repository.py Module
#### Functions: 
- load_profiles(): Reads saved JSON file with profiles, turns the profiles into dictionaries, and converts them into UserProfile objects
- save_profiles(profiles): Saves user profiles to the JSON file from the profiles dictionary
- create_profile(profiles, name): Creates a new (empty) UserProfile and adds it to the profile's dictionary
- delete_profile(profiles, name): Deletes a chosen profile if the profile's name exists in the profiles dictionary
- rename_profile(profiles, old, new): Renames a profile within the profiles dictionary if the old name exists

## ui Sub-Package
### main.py Module
### Class: BudgetBuddyApp
#### Methods:
- run(self): Starts the main loop that shows the navigation menu and collects user input
- _main_menu(self): Gives all the main menu options and lets user choose an option
- show_guide(self): Reads the guide.txt file to explain how to use the profile
- create_profile_flow(self): Lets the user create a new named profile and saves it 
- saved_profiles_menu(self): Lets the user choose to open, rename, or delete a profile or go back to the main menu
- _open_profile_flow(self): Lets the user choose a profile and open it if it exists
- _rename_profile_flow(self): Lets users rename an existing profile
- _delete_profile_flow(self): Lets the user delete an existing profile, and asks for confirmation before deletion
- profile_summary_loop(self, profile: UserProfile): Gives all the profile menu options and lets user choose where to go
- record_income_flow(self, profile): Collects the date, amount, category, and description of an income object and adds it to the user's profile
- record_expense_flow(self, profile): Collects the date, amount, category, and description of an expense object and adds it to the user's profile
- view_year_transactions_flow(self, profile): Shows a summary for all of the transactions for a chosen year and lets the user edit or delete any previous transactions
- view_monthly_summaries_flow(self, profile): Shows a summary of all transactions per month of the current year
- change_year_flow(self): Lets the user choose a different year to switch to
#### Function (outside of class):
- run(): Simple way to start the program outside of the class

### summary.py Module
#### Functions:
- print_summary_page(profile, month, year): Prints a summary of all transactions for a given profile and month/year
- print_transaction(transactions): Prints the list of transactions in a table-like form for readability
- print_profiles_list(profiles): Prints the names of all saved profiles
