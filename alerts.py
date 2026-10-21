from database import get_connection
from config import LOW_STOCK_THRESHOLD


def check_low_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity FROM inventory WHERE quantity < ?", (LOW_STOCK_THRESHOLD,))
    low_stock_items = cursor.fetchall()
    conn.close()

    if low_stock_items:
        print("\n🔔 LOW STOCK ALERTS:")
        for item in low_stock_items:
            print(f" - {item[0]} (Qty: {item[1]})")
