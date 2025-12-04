# BudgetBuddyUnittesting
This Work is mainly used for unittesting of the project budgetbuddy


## Test Structure

All tests are stored in the top-level `tests/` package:

tests/
    __init__.py\
    test_repository.py # tests for budgetbuddy.data.repository\
    test_csvio.py # tests for budgetbuddy.data.csvio\
    test_summary.py # tests for budgetbuddy.ui.summary\
    test_main.py # tests for budgetbuddy.ui.main (BudgetBuddyApp)\
    test_suite.py # combined test suite\


Each test file contains a single test class:

- `TestRepository` (for `repository.py`)
- `TestCsvIO` (for `csvio.py`)
- `TestSummary` (for `summary.py`)
- `TestBudgetBuddyApp` (for `main.py`)

Each class:

- Uses `setUpClass`, `tearDownClass`, `setUp`, and `tearDown`
- Contains **at least two test methods**
- Each test method contains **at least four assertions**, checking both normal behaviour and edge cases

### What is tested

**Data package**

- `test_repository.py`
  - Creating profiles (`create_profile`)
  - Saving and loading profiles to/from a JSON file (`save_profiles`, `load_profiles`)
  - Renaming and deleting profiles (`rename_profile`, `delete_profile`)
  - Uses a temporary JSON file so the real `budgetbuddy_data.json` is never modified

- `test_csvio.py`
  - Exporting a profile’s transactions to CSV (`export_profile_to_csv`)
  - Importing transactions from CSV into a new profile (`import_transactions_from_csv`)
  - Verifies file creation, header fields, and transaction content

**UI package**

- `test_summary.py`
  - `print_profiles_list` for non-empty profile lists
  - `print_transactions` for both empty and non-empty transaction lists
  - Captures `stdout` to assert on the printed content

- `test_main.py`
  - `show_guide()` correctly reads and prints `guide.txt` via a relative path
  - `create_profile_flow()` creates a new profile and calls `save_profiles`
  - Uses `unittest.mock.patch` to simulate user input and avoid writing to disk

### Running the tests

From the project root (the folder that contains `budgetbuddy/` and `tests/` which is `BudgetBuddyUnittesting`):

**Run the combined test suite:**

```bash
python -m tests.test_suite
