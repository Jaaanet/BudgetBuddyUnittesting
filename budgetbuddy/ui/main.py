import os

from budgetbuddy.core.models import Income, Expense
from budgetbuddy.core.budget import Budget
from budgetbuddy.data import repository
from budgetbuddy.ui import summary

MONTH_NAMES = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


class BudgetBuddyApp:
    """Main controller for the BudgetBuddy program."""

    def __init__(self):
        # Load all saved profiles from the JSON file
        self.profiles = repository.load_profiles()
        # Keep both current month and current year for summaries
        self.current_month = 1
        self.current_year = 2025  # can be changed by the user

    # ===== Entry point =====

    def run(self):
        """Start the main menu loop."""
        while True:
            choice = self._main_menu()

            if choice == "1":
                self.show_guide()
            elif choice == "2":
                self.create_profile_flow()
            elif choice == "3":
                self.saved_profiles_menu()
            elif choice == "4":
                repository.save_profiles(self.profiles)
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    # ===== Main menu =====

    def _main_menu(self):
        print("\n=== BudgetBuddy Main Menu ===")
        print("1) Guide")
        print("2) Create profile")
        print("3) Saved profiles")
        print("4) Quit")
        return input("Choose an option: ").strip()

    def show_guide(self):
        """Read guide.txt stored in the same directory as main.py."""
        current_dir = os.path.dirname(__file__)
        guide_path = os.path.join(current_dir, "guide.txt")

        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                print("\n" + f.read())
        except FileNotFoundError:
            print("\nGuide file not found. Make sure guide.txt exists in the ui folder.")

    def create_profile_flow(self):
        name = input("Enter a name for the new profile: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        if name in self.profiles:
            print("A profile with that name already exists.")
            return

        repository.create_profile(self.profiles, name)
        repository.save_profiles(self.profiles)
        print("Profile '{}' created.".format(name))

    # ===== Saved profiles menu =====

    def saved_profiles_menu(self):
        while True:
            summary.print_profiles_list(self.profiles)
            print("\nOptions: o = open, r = rename, d = delete, b = back")
            choice = input("Choose: ").strip().lower()

            if choice == "b":
                return
            elif choice == "o":
                self._open_profile_flow()
            elif choice == "r":
                self._rename_profile_flow()
            elif choice == "d":
                self._delete_profile_flow()
            else:
                print("Invalid choice.")

    def _open_profile_flow(self):
        name = input("Profile name to open: ").strip()
        profile = self.profiles.get(name)
        if profile is None:
            print("No such profile.")
            return
        self.profile_summary_loop(profile)

    def _rename_profile_flow(self):
        old = input("Profile name to rename: ").strip()
        if old not in self.profiles:
            print("No such profile.")
            return
        new = input("New name: ").strip()
        if not new:
            print("Name cannot be empty.")
            return
        repository.rename_profile(self.profiles, old, new)
        repository.save_profiles(self.profiles)
        print("Profile renamed.")

    def _delete_profile_flow(self):
        name = input("Profile name to delete: ").strip()
        if name not in self.profiles:
            print("No such profile.")
            return
        confirm = input("Delete '{}'? (y/n): ".format(name)).strip().lower()
        if confirm == "y":
            repository.delete_profile(self.profiles, name)
            repository.save_profiles(self.profiles)
            print("Deleted.")

    # ===== Profile summary and actions =====

    def profile_summary_loop(self, profile):
        """
        Menu shown after opening a profile.

        New menu:

        1) Record income
        2) Record expense
        3) View all transactions this year (current_year)
        4) Change year
        5) View monthly summaries for this year (current_year)
        6) Back to Saved profiles
        """
        while True:
            # Print menu
            print("\nProfile menu for '{}':".format(profile.name))
            print("1) Record income")
            print("2) Record expense")
            print("3) View all transactions this year ({})".format(self.current_year))
            print("4) Change year")
            print("5) View monthly summaries for this year ({})".format(self.current_year))
            print("6) Back to Saved profiles")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.record_income_flow(profile)
            elif choice == "2":
                self.record_expense_flow(profile)
            elif choice == "3":
                self.view_year_transactions_flow(profile)
            elif choice == "4":
                self.change_year_flow()
            elif choice == "5":
                self.view_monthly_summaries_flow(profile)
            elif choice == "6":
                repository.save_profiles(self.profiles)
                return
            else:
                print("Invalid choice.")

    def record_income_flow(self, profile):
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Source/category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Income(date, amount, category, desc)
        profile.add_transaction(tx)

    def record_expense_flow(self, profile):
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Expense(date, amount, category, desc)
        profile.add_transaction(tx)

    # === View all transactions for the current year (with edit/delete submenu) ===

    def view_year_transactions_flow(self, profile):
        """
        Show all transactions in the current year for this profile,
        and provide a submenu to edit or delete.
        """
        year = self.current_year

        while True:
            prefix = "{:04d}-".format(year)  # matches "YYYY-"
            txs = [t for t in profile.transactions
                   if isinstance(t.date, str) and t.date.startswith(prefix)]

            print()
            summary.print_transactions(txs)

            if not txs:
                print("\nNo transactions for this year.")
                input("Press Enter to go back...")
                return

            print("\nOptions: e = edit, d = delete, b = back")
            choice = input("Choose: ").strip().lower()

            if choice == "b":
                return

            if choice not in ("e", "d"):
                print("Invalid choice.")
                continue

            # Ask which transaction to edit/delete
            try:
                index = int(input("Index of transaction: "))
            except ValueError:
                print("Invalid index.")
                continue

            if index < 0 or index >= len(txs):
                print("Index out of range.")
                continue

            target = txs[index]

            if choice == "e":
                # Edit the selected transaction
                print("Leave blank to keep existing value.")
                new_date = input("Date [{}]: ".format(target.date)).strip()
                new_amount = input("Amount [{}]: ".format(target.amount)).strip()
                new_cat = input("Category [{}]: ".format(target.category)).strip()
                new_desc = input("Description [{}]: ".format(target.description)).strip()

                if new_date:
                    target.date = new_date
                if new_amount:
                    try:
                        target.amount = float(new_amount)
                    except ValueError:
                        print("Invalid amount, keeping original.")
                if new_cat:
                    target.category = new_cat
                if new_desc:
                    target.description = new_desc

            elif choice == "d":
                # Delete the selected transaction
                confirm = input("Delete this transaction? (y/n): ").strip().lower()
                if confirm == "y":
                    profile.delete_transaction(target)
                    print("Transaction deleted.")

    # === View monthly summaries for the current year ===

    def view_monthly_summaries_flow(self, profile):
        """Print income and expense totals for each month of the current year."""
        budget = Budget(profile)
        year = self.current_year

        print("\n=== Summary for {} ({}) ===".format(profile.name, year))

        for month in range(1, 13):
            totals = budget.month_totals(month, year)
            month_name = MONTH_NAMES[month - 1]

            print("\n{}".format(month_name))
            print("Total income : {:.2f}".format(totals["income"]))
            print("Total expense: {:.2f}".format(totals["expense"]))

    # === Change year (keeps month as-is) ===

    def change_year_flow(self):
        """Allow the user to change the current year."""
        new_year = input("Year [{}]: ".format(self.current_year)).strip()
        if new_year:
            try:
                self.current_year = int(new_year)
                print("Year changed to {}.".format(self.current_year))
            except ValueError:
                print("Invalid year. Please enter a number.")


def run():
    """Helper so we can call budgetbuddy.run()."""
    app = BudgetBuddyApp()
    app.run()
