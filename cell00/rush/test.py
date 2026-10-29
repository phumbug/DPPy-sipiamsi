#!/usr/bin/env python3

# ===== EXPENSE TRACKER =====
# Data:
#   expenses -> a LIST of DICTIONARIES, one dictionary per expense
#   settings -> a DICTIONARY that stores the monthly budget
#   CATEGORIES -> a LIST of allowed categories

CATEGORIES = ["food", "transport", "shopping", "bills", "other"]

expenses = []
settings = {"budget": 5000.0}


# ---------- Input helpers (they never crash on bad input) ----------

def get_amount(prompt):
    """Ask until the user types a number greater than 0. Returns a float."""
    while True:
        text = input(prompt)
        try:
            amount = float(text)
        except ValueError:
            print("Error: please type a number, e.g. 120 or 45.50")
            continue
        # Rule 1: amount must be positive
        if amount <= 0:
            print("Error: amount must be greater than 0.")
        elif amount > 1000000:
            print("Error: amount is too large.")
        else:
            return amount


def get_category():
    """Ask until the user types a category from the allowed list."""
    while True:
        print("Categories: " + ", ".join(CATEGORIES))
        category = input("Category: ").strip().lower()
        # Rule 2: category must be in the allowed list
        if category in CATEGORIES:
            return category
        else:
            print(f"Error: '{category}' is not a valid category.")


def get_item_name():
    """Ask until the user types a non-empty name."""
    while True:
        name = input("Item name: ").strip()
        if name == "":
            print("Error: item name cannot be empty.")
        else:
            return name


def choose_expense():
    """Ask for an expense number. Returns its index, or -1 if invalid."""
    if len(expenses) == 0:
        print("No expenses yet.")
        return -1
    view_expenses()
    text = input("Expense number: ")
    if not text.isdigit():
        print("Error: please type a number from the list.")
        return -1
    number = int(text)
    if number < 1 or number > len(expenses):
        print(f"Error: expense #{number} does not exist.")
        return -1
    return number - 1


# ---------- Data processing ----------

def calculate_total():
    """Return the total of all expenses."""
    total = 0
    for expense in expenses:
        total = total + expense["amount"]
    return total


def total_by_category():
    """Return a dictionary: category -> total spent."""
    totals = {}
    for category in CATEGORIES:
        totals[category] = 0
    for expense in expenses:
        totals[expense["category"]] += expense["amount"]
    return totals


def find_biggest():
    """Return the expense with the highest amount (or None if empty)."""
    if len(expenses) == 0:
        return None
    biggest = expenses[0]
    for expense in expenses:
        if expense["amount"] > biggest["amount"]:
            biggest = expense
    return biggest


def confirm_if_over_budget(extra):
    """Rule 3: warn if this amount pushes the total over budget.
    Returns True if we should save the expense, False if cancelled."""
    new_total = calculate_total() + extra
    if new_total > settings["budget"]:
        over = new_total - settings["budget"]
        print(f"Warning: this puts you {over:.2f} THB over your budget!")
        answer = input("Save anyway? (y/n): ").strip().lower()
        if answer == "y":
            return True
        else:
            print("Cancelled. Nothing was saved.")
            return False
    return True


# ---------- Menu actions ----------

def add_expense():
    name = get_item_name()
    category = get_category()
    amount = get_amount("Amount (THB): ")
    if confirm_if_over_budget(amount):
        expenses.append({"item": name, "category": category, "amount": amount})
        print(f"Added: {name} ({category}) {amount:.2f} THB")


def view_expenses():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    print("\n#   Item                 Category     Amount")
    number = 1
    for expense in expenses:
        print(f"{number:<3} {expense['item']:<20} {expense['category']:<12} "
              f"{expense['amount']:>10.2f}")
        number += 1


def update_expense():
    index = choose_expense()
    if index == -1:
        return
    old = expenses[index]
    print(f"Updating: {old['item']} ({old['category']}) {old['amount']:.2f}")
    name = get_item_name()
    category = get_category()
    amount = get_amount("New amount (THB): ")
    # Only the difference counts toward the budget check
    if confirm_if_over_budget(amount - old["amount"]):
        expenses[index] = {"item": name, "category": category, "amount": amount}
        print("Expense updated.")


def delete_expense():
    index = choose_expense()
    if index == -1:
        return
    removed = expenses.pop(index)
    print(f"Deleted: {removed['item']}")


def show_summary():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    total = calculate_total()
    budget = settings["budget"]

    print("\n--- Spending by category ---")
    totals = total_by_category()
    for category in CATEGORIES:
        if totals[category] > 0:
            percent = totals[category] / total * 100
            print(f"{category:<12} {totals[category]:>10.2f} THB "
                  f"({percent:.0f}% of total spent)")

    biggest = find_biggest()
    print(f"\nBiggest expense: {biggest['item']} ({biggest['amount']:.2f} THB)")
    print(f"Total spent: {total:.2f} / {budget:.2f} THB")

    # Budget status
    if total > budget:
        print("Status: OVER BUDGET")
    elif total >= budget * 0.8:
        print("Status: Careful, you have used 80% or more of your budget")
    else:
        print(f"Status: OK, {budget - total:.2f} THB left")


def set_budget():
    print(f"Current budget: {settings['budget']:.2f} THB")
    settings["budget"] = get_amount("New monthly budget (THB): ")
    print("Budget updated.")


# ---------- Main menu ----------

def show_menu():
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Update expense")
    print("4. Delete expense")
    print("5. Summary")
    print("6. Set budget")
    print("7. Exit")


def main():
    running = True
    while running:
        show_menu()
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            update_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            show_summary()
        elif choice == "6":
            set_budget()
        elif choice == "7":
            print("Goodbye!")
            running = False
        else:
            print("Invalid choice. Please type a number from 1 to 7.")


try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\nGoodbye!")