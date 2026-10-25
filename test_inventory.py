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


if __name__ == "__main__":
    unittest.main(verbosity=2)
