# Changes in this standalone version

This version was prepared from the `Inventory Management/` folder of the
`python-projects-portfolio` repo (source files fetched 2026-10-21) so the
project can stand on its own as a single repository. The original code,
structure, and naming are preserved — the changes below are only what was
needed to make the project actually run and to make its documentation
accurate.

## Fixes

1. **database.py — fixed a broken import; the app could not start at all.**
   The live code imports `PRABH` from config.py
   (`from config import PRABH`, then `sqlite3.connect(PRABH)`), but
   config.py does not define `PRABH` — it defines
   `DATABASE_NAME = "inventory.db"`. Running the app raised an
   `ImportError` before anything else happened. The import and the
   `sqlite3.connect()` call now use `DATABASE_NAME`, which is what the code
   was clearly meant to use (it is the database filename).

2. **Delete is now actually implemented.**
   The old README listed "Add, update, and delete inventory items" as a
   headline feature, but there was no delete function anywhere in the code
   and no delete option in the menu. Added a `delete_item()` method to
   `InventoryManager` (written in the same style as `add_item()` and
   `update_quantity()`) and a "Delete Item" option to the menu in main.py.
   The menu is now: 6 = Delete Item, 7 = Exit (Exit was option 6 before).

3. **reports.py — the weekly report now shows what the README said it
   shows, where that is actually possible.**
   Before, `generate_weekly_report()` printed only a table of items. It
   now also prints the low-stock items (quantity below the threshold from
   config.py) and the total inventory value (quantity × price, summed over
   all items) — both computable from the data the program already stores.
   The old README also claimed the report lists "items added" and "items
   updated". That part is **not** implemented, on purpose: the database
   stores no dates or timestamps, so there is no honest way to know when
   an item was added or last changed. The new README only claims what the
   report really shows.

4. **models.py removed.**
   It defined an `InventoryItem` class whose `save()` method did exactly
   what `InventoryManager.add_item()` already does. Nothing in the project
   imported it, so it was dead code.

5. **requirements.txt added.**
   The old README's run instructions already said
   `pip install -r requirements.txt`, but no such file existed — while
   reports.py imports the third-party `tabulate` package, which does not
   come with Python. The file now exists and lists `tabulate`.

6. **The "~40%" claim is gone.**
   The old README said the project "reduced manual stock-checking time by
   ~40%". There is no measurement behind that number, so it does not
   appear in the new README.

7. **Not carried over:** the empty (0-byte) file named `python` that sat
   in the original folder. It contained nothing and was not part of the
   program.

## What was NOT changed

- config.py and alerts.py are carried over exactly as they were.
- Everywhere else, the original logic, function names, menu wording, and
  printed messages are unchanged. The only edits are the ones listed
  above.

## Update — October 25, 2026

**Automated tests.** Added `test_inventory.py` (5 tests, standard library
only): add-and-list, case-insensitive partial search, update quantity,
delete, and low-stock alerts (only items below the threshold of 10 are
flagged). The tests point the database at a temporary file, so running
them never touches the real `inventory.db`. Verified: all 5 tests pass
(`Ran 5 tests ... OK`).

## Update — October 22, 2026

**Feature: search items by name.** `InventoryManager` gained a
`search_items()` method (case-insensitive partial match using SQL
`LIKE`), and the menu gained a "Search Items by Name" option (option 7;
Exit moved to 8). Verified with a scripted run: with "USB Cable",
"Wireless Mouse", and "usb hub" in stock, searching "usb" returned the
two USB items, and searching "keyboard" reported no matches.

## Update — October 28, 2026

**Feature: Power BI export.** New `powerbi_export.py` (menu option 8;
Exit moved to 9) dumps the inventory as two CSVs shaped for Power BI
Desktop: `inventory_snapshot.csv` (one row per item, with computed
stock_value and a stock_status flag — "Low Stock" below the threshold
of 10, otherwise "In Stock") and `inventory_summary.csv` (one row of
KPIs: total items, total quantity, total inventory value, low-stock
count). A `powerbi/README.md` guide explains the Power BI Desktop
setup and suggested visuals. No Power BI file is checked in — the
dashboard is built from live exported data, so nothing here is sample
or placeholder data. Tests added (2 new tests, 7 total): snapshot
rows, computed values, status flags, summary totals, and the empty
inventory case, all against a temporary database. Verified: all
7 tests pass (`Ran 7 tests ... OK`); a scripted menu run wrote both
CSVs with correct values.
