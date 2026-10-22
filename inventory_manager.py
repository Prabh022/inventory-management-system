from database import get_connection


class InventoryManager:

    def add_item(self, name, quantity, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
            (name, quantity, price)
        )
        conn.commit()
        conn.close()

    def update_quantity(self, item_id, new_quantity):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE id = ?",
            (new_quantity, item_id)
        )
        conn.commit()
        conn.close()

    def delete_item(self, item_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM inventory WHERE id = ?",
            (item_id,)
        )
        conn.commit()
        conn.close()

    def get_all_items(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        conn.close()
        return items

    def search_items(self, search_term):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM inventory WHERE name LIKE ?",
            (f"%{search_term}%",)
        )
        items = cursor.fetchall()
        conn.close()
        return items
