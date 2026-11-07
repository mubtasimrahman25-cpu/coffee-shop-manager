# Coffee Shop Manager - Step 5
# Take orders, print bills, save sales, track stock, restock, and show a daily report.
# Prices are in Bangladeshi Taka (Tk).

import csv
import json
import os
from datetime import datetime

SALES_FILE = "sales.csv"
STOCK_FILE = "stock.json"

# The menu: item name -> price in Tk
# Change these to match the real shop.
menu = {
    "Milk Tea": 20,
    "Hot Coffee": 60,
    "Cold Coffee": 100,
    "Chicken Roll": 50,
    "Chicken Singara": 25,
    "Chicken Sandwich": 100,
    "French Fries": 80,
}

# What each item uses up: beans in grams, milk in ml
# Food items use none, so they are always available.
recipes = {
    "Milk Tea": {"beans": 0, "milk": 100},
    "Hot Coffee": {"beans": 15, "milk": 100},
    "Cold Coffee": {"beans": 18, "milk": 150},
    "Chicken Roll": {"beans": 0, "milk": 0},
    "Chicken Singara": {"beans": 0, "milk": 0},
    "Chicken Sandwich": {"beans": 0, "milk": 0},
    "French Fries": {"beans": 0, "milk": 0},
}

# What the shop starts with on the first day
starting_stock = {"beans": 500, "milk": 3000}

LOW_STOCK_WARNING = {"beans": 100, "milk": 500}


def load_stock():
    # If we saved stock before, read it. Otherwise start fresh.
    if os.path.exists(STOCK_FILE):
        with open(STOCK_FILE) as f:
            return json.load(f)
    return dict(starting_stock)


def save_stock(stock):
    with open(STOCK_FILE, "w") as f:
        json.dump(stock, f)


def can_make(item, stock):
    # Check there is enough of every ingredient for this item
    for ingredient, amount in recipes[item].items():
        if stock[ingredient] < amount:
            return False
    return True


def use_ingredients(item, stock):
    for ingredient, amount in recipes[item].items():
        stock[ingredient] -= amount


def show_stock(stock):
    print(f"\nStock left: {stock['beans']}g beans, {stock['milk']}ml milk")
    for ingredient, limit in LOW_STOCK_WARNING.items():
        if stock[ingredient] < limit:
            print(f"WARNING: {ingredient} is running low! Time to restock.")


def show_menu():
    print("\n=== Welcome to Bean There Cafe ===")
    for number, (name, price) in enumerate(menu.items(), start=1):
        print(f"{number}. {name} - Tk {price}")


def take_order(stock):
    order = []
    names = list(menu.keys())

    while True:
        choice = input("\nEnter item number (or 0 to finish): ")

        if not choice.isdigit():
            print("Please type a number.")
            continue

        choice = int(choice)

        if choice == 0:
            break
        if 1 <= choice <= len(names):
            item = names[choice - 1]
            if can_make(item, stock):
                use_ingredients(item, stock)
                order.append(item)
                print(f"Added {item}")
            else:
                print(f"Sorry, we are out of ingredients for {item}.")
        else:
            print("That number is not on the menu.")

    return order


def print_bill(order):
    if not order:
        print("\nNo items ordered.")
        return 0

    print("\n--- Your Bill ---")
    total = 0
    for item in order:
        price = menu[item]
        print(f"{item:<18} Tk {price}")
        total += price
    print("-------------------")
    print(f"{'Total':<18} Tk {total}")
    return total


def save_sale(order, total):
    # Add one row to sales.csv: date/time, items, total
    file_exists = os.path.exists(SALES_FILE)

    with open(SALES_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["time", "items", "total"])
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        writer.writerow([now, "; ".join(order), total])

    print("Sale saved.")


def sales_report():
    # Read sales.csv and summarise today's sales
    if not os.path.exists(SALES_FILE):
        print("\nNo sales yet.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    orders = 0
    revenue = 0
    item_counts = {}

    with open(SALES_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only count rows from today
            if not row["time"].startswith(today):
                continue
            orders += 1
            revenue += float(row["total"])
            for item in row["items"].split("; "):
                item_counts[item] = item_counts.get(item, 0) + 1

    print(f"\n=== Sales Report for {today} ===")
    if orders == 0:
        print("No sales today.")
        return

    items_sold = sum(item_counts.values())
    top_count = max(item_counts.values())
    # If two items tie, list all of them
    best_sellers = [name for name, count in item_counts.items() if count == top_count]

    print(f"Orders today:  {orders}")
    print(f"Items sold:    {items_sold}")
    print(f"Money earned:  Tk {revenue:.0f}")
    print(f"Best seller:   {', '.join(best_sellers)} ({top_count} sold)")

    print("\nBreakdown:")
    for name, count in item_counts.items():
        print(f"  {name:<18} {count}")


def restock(stock):
    # Add new supplies when the owner buys more
    print("\n--- Restock ---")
    print(f"Current stock: {stock['beans']}g beans, {stock['milk']}ml milk")
    print("1. Coffee beans (g)")
    print("2. Milk (ml)")

    choice = input("What did you buy? ")
    if choice == "1":
        ingredient, unit = "beans", "g"
    elif choice == "2":
        ingredient, unit = "milk", "ml"
    else:
        print("Please choose 1 or 2.")
        return

    amount = input(f"How many {unit} to add? ")
    if not amount.isdigit() or int(amount) == 0:
        print("Please type a number bigger than 0.")
        return

    stock[ingredient] += int(amount)
    save_stock(stock)
    print(f"Added {amount}{unit}.")
    show_stock(stock)


def new_order(stock):
    show_menu()
    show_stock(stock)
    order = take_order(stock)
    total = print_bill(order)
    if order:
        save_sale(order, total)
        save_stock(stock)
        show_stock(stock)


def main():
    stock = load_stock()

    while True:
        print("\n--- Main Menu ---")
        print("1. Take an order")
        print("2. Today's sales report")
        print("3. Restock")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            new_order(stock)
        elif choice == "2":
            sales_report()
        elif choice == "3":
            restock(stock)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3 or 4.")


main()
