from database import initialize_db
from inventory_manager import InventoryManager
from alerts import check_low_stock
from reports import generate_weekly_report


def menu():
    print("\n=== Inventory Management System ===")
    print("1. Add Item")
    print("2. Update Quantity")
    print("3. View All Items")
    print("4. Check Low Stock")
    print("5. Weekly Report")
    print("6. Delete Item")
    print("7. Exit")
    return input("Enter choice: ")


def main():
    initialize_db()
    manager = InventoryManager()

    while True:
        choice = menu()

        if choice == "1":
            try:
                name = input("Item name: ")
                qty = int(input("Quantity: "))
                price = float(input("Price: "))
                manager.add_item(name, qty, price)
                print("✔ Item added successfully.")
            except ValueError:
                print("❌ Invalid input. Quantity and price must be numbers.")

        elif choice == "2":
            try:
                item_id = int(input("Item ID: "))
                qty = int(input("New Quantity: "))
                manager.update_quantity(item_id, qty)
                print("✔ Quantity updated.")
            except ValueError:
                print("❌ Invalid input. ID and quantity must be numbers.")

        elif choice == "3":
            items = manager.get_all_items()
            if not items:
                print("No items found.")
            else:
                print("\nCurrent Inventory:")
                for item in items:
                    print(f"ID: {item[0]} | {item[1]} | Qty: {item[2]} | Price: {item[3]}")

        elif choice == "4":
            check_low_stock()

        elif choice == "5":
            generate_weekly_report()

        elif choice == "6":
            try:
                item_id = int(input("Item ID: "))
                manager.delete_item(item_id)
                print("✔ Item deleted successfully.")
            except ValueError:
                print("❌ Invalid input. ID must be a number.")

        elif choice == "7":
            print("Exiting system...")
            break

        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
