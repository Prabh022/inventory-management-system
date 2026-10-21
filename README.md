# Inventory Management System

A lightweight inventory management system built with Python and SQLite. It runs in the command line and stores everything in a local SQLite database file (`inventory.db`), which is created automatically the first time you run the program — there is no database server to set up.

## Features

- Add, update, and delete inventory items
- View all items currently in the inventory
- Low-stock alerts: warns you when an item's quantity falls below a threshold (default 10, changeable in `config.py`)
- Weekly inventory report showing every item, which items are low on stock, and the total inventory value
- Persistent storage using SQLite, so your data is still there the next time you run it

## Tech Stack

- Python 3.x
- SQLite (through Python's built-in `sqlite3` module)
- `tabulate` (used to print the weekly report table)

## Setup

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

Then use the on-screen menu:

```
1. Add Item
2. Update Quantity
3. View All Items
4. Check Low Stock
5. Weekly Report
6. Delete Item
7. Exit
```

## Project Structure

```
main.py               - Command-line menu and program entry point
inventory_manager.py  - Add, update, delete, and list operations on items
database.py           - SQLite connection and inventory table setup
alerts.py             - Low-stock check
reports.py            - Weekly inventory report
config.py             - Settings: database filename and low-stock threshold
requirements.txt      - Python packages needed to run the project
```
