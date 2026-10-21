from database import get_connection
from config import LOW_STOCK_THRESHOLD
from tabulate import tabulate


def generate_weekly_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity, price FROM inventory")
    items = cursor.fetchall()
    conn.close()

    print("\n📊 Weekly Inventory Report")
    print(tabulate(items, headers=["Item", "Quantity", "Price"], tablefmt="grid"))

    low_stock_items = [item for item in items if item[1] < LOW_STOCK_THRESHOLD]

    print("\n🔔 Low Stock Items:")
    if low_stock_items:
        for item in low_stock_items:
            print(f" - {item[0]} (Qty: {item[1]})")
    else:
        print(" None")

    total_value = sum(item[1] * item[2] for item in items)
    print(f"\n💰 Total Inventory Value: ${total_value:.2f}")
