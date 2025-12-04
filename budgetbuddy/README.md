# BudgetBuddy
A simple command-line budget tracking package for managing income, expenses, and multiple user profiles.  
BudgetBuddy provides yearly and monthly summaries, transaction editing, and persistent data storage using JSON.

---

## Features

- **Multiple profiles**
  - Create, rename, delete, and open profiles
  - Each profile stores independent transactions

- **Record transactions**
  - Income or Expense
  - Includes date, amount, category, and optional description

- **Yearly transaction view**
  - View all transactions for a selected year
  - Edit or delete transactions through a submenu

- **Monthly summaries**
  - For each month of the chosen year:
    - total income  
    - total expenses

- **Guide file**
  - External `guide.txt` stored in `ui/`
  - Loaded safely using a relative path

- **Persistent storage**
  - All data saved in `budgetbuddy_data.json`

---

## Package Structure

budgetbuddy/
    __init__.py          # exposes budgetbuddy.run()
    
    core/
        __init__.py
        models.py        # UserProfile, Transaction, Income, Expense
        budget.py        # Month totals, calculations, helpers
    
    data/
        __init__.py
        repository.py    # load/save JSON, manage profile storage
        csvio.py         # (optional) CSV import/export
    
    ui/
        __init__.py
        main.py          # CLI menus and program controller
        summary.py       # pretty-printed text summaries and listings
        guide.txt        # help/guide text displayed in the menu



The main data file (`budgetbuddy_data.json`) is created in the **same directory where the program is run**.

---

## Running the Program

Create a runner python file (eg. test.py) that contains:

```
import budgetbuddy
budgetbuddy.run()
```
and run:
`python test.py`

notes: the test file should be in the same directory as the package!

## Profile Menu Example
```
Profile menu for 'janet':
1) Record income
2) Record expense
3) View all transactions this year (2025)
4) Change year
5) View monthly summaries for this year (2025)
6) Back to Saved profiles

Yearly view submenu:
[0] 2025-03-12 | Expense | 12.50 | Food | Lunch
[1] 2025-03-15 | Income  | 100.00 | Gift | Birthday

Options: e = edit, d = delete, b = back
```

## Data Storage

BudgetBuddy reads/writes profiles through:  
`budgetbuddy/data/repository.py`


JSON file:  

`budgetbuddy_data.json`
is automatically generated on first run.

## Requirements
Built on Python 3.8+ and uses only the Python standard library:
- json
- os
- pathlib
No external installation needed.

## Purpose
This project demonstrates:
- Python package design
- Separation of logic (core), storage (data), and UI (command-line interface)
- JSON-based persistence
- Clean class-based modeling for profiles and transactions
- Multi-file architecture for medium-size programs
Created for a graduate-level software development course.

