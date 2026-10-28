"""Automated tests for the inventory manager and low-stock alerts.

Run from the project directory:

    python test_inventory.py

The tests point the database at a temporary file, so running them never
touches the real ``inventory.db`` used by the program.
"""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
from database import initialize_db
from inventory_manager import InventoryManager
import alerts
import powerbi_export


class InventoryManagerTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        # database.get_connection() reads this module-level name, so
        # pointing it at a temp file keeps the real inventory.db untouched.
        database.DATABASE_NAME = os.path.join(self.tmpdir.name, "test.db")
        initialize_db()
        self.manager = InventoryManager()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_list_items(self):
        self.manager.add_item("USB Cable", 25, 9.99)
        self.manager.add_item("Wireless Mouse", 12, 24.50)
        items = self.manager.get_all_items()
        self.assertEqual(len(items), 2)
        names = [item[1] for item in items]
        self.assertIn("USB Cable", names)
        self.assertIn("Wireless Mouse", names)
        cable = [item for item in items if item[1] == "USB Cable"][0]
        self.assertEqual(cable[2], 25)
        self.assertAlmostEqual(cable[3], 9.99)

    def test_search_is_case_insensitive_partial_match(self):
        self.manager.add_item("USB Cable", 25, 9.99)
        self.manager.add_item("usb hub", 8, 14.99)
        self.manager.add_item("Wireless Mouse", 12, 24.50)
        found = [item[1] for item in self.manager.search_items("usb")]
        self.assertEqual(sorted(found), ["USB Cable", "usb hub"])
        self.assertEqual(self.manager.search_items("keyboard"), [])

    def test_update_quantity(self):
        self.manager.add_item("USB Cable", 25, 9.99)
        item_id = self.manager.get_all_items()[0][0]
        self.manager.update_quantity(item_id, 40)
        self.assertEqual(self.manager.get_all_items()[0][2], 40)

    def test_delete_item(self):
        self.manager.add_item("USB Cable", 25, 9.99)
        self.manager.add_item("Wireless Mouse", 12, 24.50)
        item_id = [i for i in self.manager.get_all_items()
                   if i[1] == "USB Cable"][0][0]
        self.manager.delete_item(item_id)
        remaining = [item[1] for item in self.manager.get_all_items()]
        self.assertEqual(remaining, ["Wireless Mouse"])

    def test_low_stock_alert_lists_only_items_below_threshold(self):
        # Threshold is 10 (config.LOW_STOCK_THRESHOLD).
        self.manager.add_item("usb hub", 8, 14.99)
        self.manager.add_item("USB Cable", 25, 9.99)
        output = io.StringIO()
        with redirect_stdout(output):
            alerts.check_low_stock()
        self.assertIn("usb hub", output.getvalue())
        self.assertNotIn("USB Cable", output.getvalue())


class PowerBIExportTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        database.DATABASE_NAME = os.path.join(self.tmpdir.name, "test.db")
        initialize_db()
        self.manager = InventoryManager()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_export_writes_snapshot_and_summary(self):
        import csv

        self.manager.add_item("USB Cable", 25, 9.99)
        self.manager.add_item("usb hub", 8, 14.99)
        outdir = os.path.join(self.tmpdir.name, "powerbi")
        result = powerbi_export.export_powerbi(outdir)
        self.assertEqual(result["items"], 2)
        self.assertTrue(os.path.isfile(result["snapshot"]))
        self.assertTrue(os.path.isfile(result["summary"]))

        with open(result["snapshot"], newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 2)
        cable = [r for r in rows if r["name"] == "USB Cable"][0]
        self.assertEqual(cable["quantity"], "25")
        self.assertAlmostEqual(float(cable["stock_value"]), 249.75)
        self.assertEqual(cable["stock_status"], "In Stock")
        hub = [r for r in rows if r["name"] == "usb hub"][0]
        self.assertEqual(hub["stock_status"], "Low Stock")
        self.assertAlmostEqual(float(hub["stock_value"]), 119.92)

        with open(result["summary"], newline="", encoding="utf-8") as f:
            summary = list(csv.DictReader(f))
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["total_items"], "2")
        self.assertEqual(summary[0]["total_quantity"], "33")
        self.assertAlmostEqual(float(summary[0]["total_value"]), 369.67)
        self.assertEqual(summary[0]["low_stock_count"], "1")

    def test_export_on_empty_inventory(self):
        import csv

        outdir = os.path.join(self.tmpdir.name, "powerbi")
        result = powerbi_export.export_powerbi(outdir)
        self.assertEqual(result["items"], 0)
        with open(result["snapshot"], newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows, [])
        with open(result["summary"], newline="", encoding="utf-8") as f:
            summary = list(csv.DictReader(f))
        self.assertEqual(summary[0]["total_items"], "0")
        self.assertEqual(summary[0]["total_value"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
