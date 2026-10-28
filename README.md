# Inventory Management System

A lightweight inventory management system built with Python and SQLite. It runs in the command line and stores everything in a local SQLite database file (`inventory.db`), which is created automatically the first time you run the program — there is no database server to set up.

## Features

- Add, update, and delete inventory items
- View all items currently in the inventory
- Search items by name (case-insensitive partial match)
- Low-stock alerts: warns you when an item's quantity falls below a threshold (default 10, changeable in `config.py`)
- Weekly inventory report showing every item, which items are low on stock, and the total inventory value
- Power BI export (menu option 8): dumps the inventory as two CSVs shaped for Power BI Desktop — a per-item snapshot with computed stock value and stock status, and a one-row KPI summary — see `powerbi/README.md` for the dashboard setup
- Persistent storage using SQLite, so your data is still there the next time you run it
- Automated tests (`test_inventory.py`) covering add, list, search, update, delete, and low-stock alerts — they run against a temporary database, so they never touch your real `inventory.db`

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
7. Search Items by Name
8. Export for Power BI
9. Exit
```

## Power BI export

Menu option 8 writes two CSVs into `powerbi/` for Power BI Desktop:
`inventory_snapshot.csv` (one row per item, with stock value and
stock status) and `inventory_summary.csv` (total items, quantity,
value, and low-stock count for card visuals). Full setup — including
suggested visuals — is in `powerbi/README.md`. Re-run the export
after changing the inventory, then refresh the data in Power BI.

## Project Structure

```
main.py               - Command-line menu and program entry point
inventory_manager.py  - Add, update, delete, list, and search operations on items
database.py           - SQLite connection and inventory table setup
test_inventory.py     - Automated tests (run: `python test_inventory.py`)
alerts.py             - Low-stock check
reports.py            - Weekly inventory report
powerbi_export.py     - Export inventory data as CSVs shaped for Power BI
powerbi/README.md     - How to connect Power BI Desktop to the exported CSVs
config.py             - Settings: database filename and low-stock threshold
requirements.txt      - Python packages needed to run the project
```
