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
