"""Export inventory data as CSV files shaped for Power BI.

Power BI Desktop cannot read the app's SQLite file directly in a
portable way, so this module dumps two flat tables that Power BI
imports with Get Data -> Text/CSV:

- inventory_snapshot.csv: one row per item, with a computed
  stock_value (quantity x price) and a stock_status flag
  ("Low Stock" when quantity is below the threshold in config.py,
  otherwise "In Stock").
- inventory_summary.csv: a single row of KPIs for card visuals --
  total items, total quantity, total inventory value, and the
  number of low-stock items.

Run from the project directory (or use menu option 8):

    python -c "from powerbi_export import export_powerbi; export_powerbi()"

Re-run the export whenever the inventory changes, then refresh the
data in Power BI. See powerbi/README.md for the dashboard setup.
"""

import csv
import os

import database
from config import LOW_STOCK_THRESHOLD

DEFAULT_OUTPUT_DIR = "powerbi"

SNAPSHOT_HEADERS = ["id", "name", "quantity", "price", "stock_value", "stock_status"]
SUMMARY_HEADERS = ["total_items", "total_quantity", "total_value", "low_stock_count"]


def _fetch_items():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, price FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return items


def export_powerbi(output_dir=DEFAULT_OUTPUT_DIR):
    """Write the snapshot and summary CSVs; return their paths and item count."""
    items = _fetch_items()
    os.makedirs(output_dir, exist_ok=True)

    snapshot_path = os.path.join(output_dir, "inventory_snapshot.csv")
    with open(snapshot_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(SNAPSHOT_HEADERS)
        for item_id, name, quantity, price in items:
            writer.writerow([
                item_id,
                name,
                quantity,
                price,
                round(quantity * price, 2),
                "Low Stock" if quantity < LOW_STOCK_THRESHOLD else "In Stock",
            ])

    total_quantity = sum(item[2] for item in items)
    total_value = round(sum(item[2] * item[3] for item in items), 2)
    low_stock_count = sum(1 for item in items if item[2] < LOW_STOCK_THRESHOLD)
    summary_path = os.path.join(output_dir, "inventory_summary.csv")
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(SUMMARY_HEADERS)
        writer.writerow([len(items), total_quantity, total_value, low_stock_count])

    return {"snapshot": snapshot_path, "summary": summary_path, "items": len(items)}
