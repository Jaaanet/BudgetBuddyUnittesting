import csv
from budgetbuddy.core.models import Transaction


def export_profile_to_csv(profile, filepath):
    """Write all transactions from a profile to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["date", "amount", "category", "description", "type"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for tx in profile.transactions:
            writer.writerow(tx.to_dict())


def import_transactions_from_csv(profile, filepath):
    """Read transactions from a CSV file and add them to a profile."""
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tx = Transaction.from_dict(row)
            profile.add_transaction(tx)
