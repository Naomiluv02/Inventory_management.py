import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import os
import csv

# Define the filename for storing the inventory
inventory_file = 'inventory.json'

# Predefined categories
categories = [
    'Electronics', 'Groceries', 'Office Supplies', 'Clothing',
    'Household Items', 'Toys', 'Books', 'Beauty Products', 'Pet Supplies', 'Movies'
]


# Initialize inventory as a nested dictionary
def initialize_inventory():
    if os.path.exists(inventory_file):
        with open(inventory_file, 'r') as file:
            loaded_inventory = json.load(file)
    else:
        loaded_inventory = {}

    # Ensure all predefined categories are in the inventory
    for category in categories:
        if category not in loaded_inventory or not isinstance(loaded_inventory[category], dict):
            loaded_inventory[category] = {}
    return loaded_inventory


inventory = initialize_inventory()


def save_inventory():
    with open(inventory_file, 'w') as file:
        json.dump(inventory, file, indent=4)


def add_item():
    category = category_var.get()
    if not category:
        messagebox.showerror("Error", "Please select a category.")
        return

    item_name = simpledialog.askstring("Input", "Enter item name:")
    if not item_name:
        messagebox.showerror("Error", "Item name cannot be empty.")
        return

    try:
        quantity = int(simpledialog.askstring("Input", f"Enter quantity for '{item_name}':"))
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    if item_name in inventory[category]:
        messagebox.showinfo("Info", f"Item '{item_name}' already exists in {category}. Use update to change quantity.")
    else:
        inventory[category][item_name] = quantity
        save_inventory()
        messagebox.showinfo("Success", f"Added '{item_name}' with quantity {quantity} to {category}.")


def update_quantity():
    category = category_var.get()
    if not category:
        messagebox.showerror("Error", "Please select a category.")
        return

    item_name = simpledialog.askstring("Input", "Enter item name to update:")
    if not item_name:
        messagebox.showerror("Error", "Item name cannot be empty.")
        return

    if item_name in inventory[category]:
        try:
            quantity = int(simpledialog.askstring("Input", f"Enter new quantity for '{item_name}':"))
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return
        inventory[category][item_name] = quantity
        save_inventory()
        messagebox.showinfo("Success", f"Updated '{item_name}' to quantity {quantity} in {category}.")
    else:
        messagebox.showerror("Error", f"Item '{item_name}' not found in {category}.")


def remove_item():
    category = category_var.get()
    if not category:
        messagebox.showerror("Error", "Please select a category.")
        return

    item_name = simpledialog.askstring("Input", "Enter item name to remove:")
    if not item_name:
        messagebox.showerror("Error", "Item name cannot be empty.")
        return

    if item_name in inventory[category]:
        del inventory[category][item_name]
        save_inventory()
        messagebox.showinfo("Success", f"Removed '{item_name}' from {category}.")
    else:
        messagebox.showerror("Error", f"Item '{item_name}' not found in {category}.")


def display_inventory():
    category = category_var.get()
    if not category:
        messagebox.showerror("Error", "Please select a category.")
        return

    if category not in inventory:
        messagebox.showerror("Error", f"Category '{category}' not found in inventory.")
        return

    if inventory[category]:
        inventory_list = "\n".join([f"{item}: {quantity}" for item, quantity in inventory[category].items()])
        messagebox.showinfo(f"Current Inventory in {category}", inventory_list)
    else:
        messagebox.showinfo(f"Current Inventory in {category}", f"{category} is empty.")


def search_item():
    search_term = simpledialog.askstring("Search", "Enter item name to search:")
    if not search_term:
        messagebox.showerror("Error", "Search term cannot be empty.")
        return

    results = []
    for category, items in inventory.items():
        if isinstance(items, dict):
            for item, quantity in items.items():
                if search_term.lower() in item.lower():
                    results.append(f"{item} (Category: {category}, Quantity: {quantity})")

    if results:
        messagebox.showinfo("Search Results", "\n".join(results))
    else:
        messagebox.showinfo("Search Results", "No items found.")


def export_inventory():
    with open('inventory_export.csv', 'w', newline='') as csvfile:
        fieldnames = ['Category', 'Item', 'Quantity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for category, items in inventory.items():
            if isinstance(items, dict):
                for item, quantity in items.items():
                    writer.writerow({'Category': category, 'Item': item, 'Quantity': quantity})

    messagebox.showinfo("Export Inventory", "Inventory has been exported to 'inventory_export.csv'.")


def import_inventory():
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row['Category']
                item = row['Item']
                quantity = int(row['Quantity'])

                if category in inventory:
                    inventory[category][item] = quantity
                else:
                    inventory[category] = {item: quantity}

        save_inventory()
        messagebox.showinfo("Import Inventory", "Inventory has been imported successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import inventory: {e}")


low_stock_threshold = 5  # This can set dynamically if needed


def check_low_stock():
    low_stock_items = []
    for category, items in inventory.items():
        if isinstance(items, dict):
            for item, quantity in items.items():
                if quantity <= low_stock_threshold:
                    low_stock_items.append(f"{item} (Category: {category}, Quantity: {quantity})")

    if low_stock_items:
        messagebox.showinfo("Low Stock Alert", "\n".join(low_stock_items))
    else:
        messagebox.showinfo("Low Stock Alert", "No items are below the low stock threshold.")


def dashboard_overview():
    try:
        total_items = sum(
            quantity for category in inventory.values() if isinstance(category, dict) for quantity in category.values())
        overview = f"Total Items: {total_items}\n\n"

        low_stock_items = [f"{item} (Category: {category}, Quantity: {quantity})" for category, items in
                           inventory.items() if isinstance(items, dict) for item, quantity in items.items() if
                           quantity <= low_stock_threshold]
        if low_stock_items:
            overview += "Low Stock Items:\n" + "\n".join(low_stock_items)
        else:
            overview += "Low Stock Items: None"

        messagebox.showinfo("Dashboard Overview", overview)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(f"Error: {e}")


def main():
    global category_var

    root = tk.Tk()
    root.title("Inventory Management System")

    # Create a LabelFrame for user inputs with background color
    userinfoframe = tk.LabelFrame(root, text="Inventory Management", bg="#e6e6ff", fg="#4b0082")
    userinfoframe.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    # Add category dropdown
    tk.Label(userinfoframe, text="Select Category", bg="#e6e6ff", fg="#4b0082").grid(row=0, column=0, padx=8, pady=8)
    category_var = tk.StringVar()
    category_menu = ttk.Combobox(userinfoframe, textvariable=category_var)
    category_menu['values'] = categories
    category_menu.grid(row=0, column=1, padx=5, pady=5)

    # Add buttons inside the LabelFrame
    tk.Button(userinfoframe, text="Add Item", command=add_item, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Update Quantity", command=update_quantity, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=2, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Remove Item", command=remove_item, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=3, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Display Inventory", command=display_inventory, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=4, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Search Item", command=search_item, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=5, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Export Inventory", command=export_inventory, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=6, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Import Inventory", command=import_inventory, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=7, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Check Low Stock", command=check_low_stock, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=8, column=0, padx=5, pady=5)
    tk.Button(userinfoframe, text="Dashboard Overview", command=dashboard_overview, width=20, height=2, bg="#ccccff", fg="#4b0082").grid(row=9, column=0, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
