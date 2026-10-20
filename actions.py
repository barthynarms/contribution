
from admin import require_admin
from receipts import print_receipt
from reports import export_report, show_list
from storage import now_string, save_data, save_web_data


def ask_entry_number(contributions, prompt):
    """Ask for an entry number from the list. Returns the entry, or None if invalid."""
    try:
        index = int(input(prompt).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None
    if index < 1 or index > len(contributions):
        print("That entry number doesn't exist.")
        return None
    return index


def add_contribution(contributions):
    if not require_admin():
        return
    name = input("Contributor name: ").strip()

    # check for existing entries with the same name (case-insensitive)
    existing_indexes = [
        i for i, entry in enumerate(contributions)
        if entry["name"].strip().lower() == name.lower()
    ]

    if existing_indexes:
        print(f"⚠️  '{name}' already has {len(existing_indexes)} entry(ies):")
        for i in existing_indexes:
            e = contributions[i]
            print(f"   - {e['name']}: ₦{e['amount']:,.2f}  ({e['date']})")

        print("\nWhat would you like to do?")
        print("1. Add as a new/separate entry anyway")
        print("2. Add this amount to their existing entry")
        print("3. Cancel")
        dup_choice = input("Choose an option (1-3): ").strip()

        if dup_choice == "3":
            print("Cancelled.")
            return
        elif dup_choice not in ("1", "2"):
            print("Invalid choice. Cancelled.")
            return
    else:
        dup_choice = "1"  # no duplicate, proceed normally

    try:
        amount = float(input("Amount contributed: ₦").strip())
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    timestamp = now_string()

    if dup_choice == "2":
        # merge into the first existing entry for this name
        entry = contributions[existing_indexes[0]]
        entry["amount"] += amount
        entry["date"] = timestamp  # update to the most recent contribution date
        print(f"✅ Added ₦{amount:,.2f} to {entry['name']}'s entry (new total: ₦{entry['amount']:,.2f})")
    else:
        entry = {"name": name, "amount": amount, "date": timestamp}
        contributions.append(entry)
        print(f"✅ Added ₦{amount:,.2f} from {name} on {timestamp}")

    save_data(contributions)
    save_web_data(contributions)
    print_receipt(entry, amount, contributions)


def edit_contribution(contributions):
    if not require_admin():
        return
    if not contributions:
        print("No contributor to edit.")
        return

    show_list(contributions)
    index = ask_entry_number(contributions, "Enter the number of the entry to edit: ")
    if index is None:
        return

    entry = contributions[index - 1]
    print(f"Editing entry {index}: {entry['name']} - ₦{entry['amount']:,.2f} ({entry['date']})")

    new_name = input(f"New name (leave blank to keep '{entry['name']}'): ").strip()
    if new_name == "":
        new_name = entry["name"]

    new_amount_input = input(f"New amount (leave blank to keep ₦{entry['amount']:,.2f}): ").strip()
    if new_amount_input == "":
        new_amount = entry["amount"]
    else:
        try:
            new_amount = float(new_amount_input)
            if new_amount <= 0:
                print("Amount must be greater than 0. Edit cancelled.")
                return
        except ValueError:
            print("Invalid amount. Edit cancelled.")
            return

    entry["name"] = new_name
    entry["amount"] = new_amount
    entry["date"] = now_string()
    save_data(contributions)
    save_web_data(contributions)
    print(f"✅ Entry {index} updated: {new_name} - ₦{new_amount:,.2f}")


def delete_contribution(contributions):
    if not require_admin():
        return
    if not contributions:
        print("No contributions to delete.")
        return

    show_list(contributions)
    index = ask_entry_number(contributions, "Enter the number of the entry to delete: ")
    if index is None:
        return

    entry = contributions[index - 1]
    confirm = input(f"Delete '{entry['name']} - ₦{entry['amount']:,.2f}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Delete cancelled.")
        return
    contributions.pop(index - 1)
    save_data(contributions)
    save_web_data(contributions)
    print(f"🗑️ Deleted entry: {entry['name']} - ₦{entry['amount']:,.2f}")


def export_csv(contributions):
    if not contributions:
        print("No contributions to export yet.")
        return
    filepath = export_report(contributions)
    print(f"✅ Report exported to: {filepath}")


def receipt_for_contributor(contributions):
    if not contributions:
        print("No contributions yet.")
        return
    show_list(contributions)
    index = ask_entry_number(contributions, "Enter the number of the contributor: ")
    if index is None:
        return
    entry = contributions[index - 1]
    print_receipt(entry, entry["amount"], contributions)