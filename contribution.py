import json
import os
import csv
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "contributions.json")
target = 500000

#this is the file the webpage reads, point it to my github Desktop
WEB_DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")

def load_data():
    """Load saved contributions from file, if it exists.
    Also upgrades old-format entries (plain [name, amount] pairs)
    to the new dictionary format so old data files still work."""
    if not os.path.exists(DATA_FILE):
        return []  # no file yet, start empty
 
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []   #file is empty or corrupted, start fresh
    
    if not isinstance(data, list):
        return [] #file didn't contain a proper list, start fresh

    return data
 

def save_data(contributions):
    #Save the current contributions list to file.
    with open(DATA_FILE, "w") as f:
        json.dump(contributions, f, indent=2)

def save_web_data(contributions, raised, target):
    """write the data, the webpage needs into data.json, in the same folder
    Git repo is watching."""
    payload = {
        "target": target,
        "last_updated": now_string(),
        "contributions": contributions,
    }
    with open(WEB_DATA_FILE, "w") as f:
        json.dump(payload, f, indent=2)
    print ("📝 data.json updated - commit and push it to go live.")


def now_string():
    """ return the current date and time as a readable string."""
    return datetime.now().strftime("%I:%M %p %d/%m/%Y")

contributions = load_data()
raised = sum(entry["amount"] for entry in contributions)

def show_progress():
    remaining = target - raised
    percent = (raised / target) * 100
    bar_length = 30
    filled = int(bar_length * raised / target)
    bar = "█" * filled + "░" * (bar_length - filled)

    print("\n" + "=" * 45)
    print("       CONTRIBUTION PROGRESS TRACKER    ")
    print("=" * 45)
    print(f"Target Amount      : ₦{target:,.2f}")
    print(f"Amount Raised      : ₦{raised:,.2f}")
    print(f"Remaining          : ₦{remaining:,.2f}")
    print(f"Total Members      : {len(contributions)}")
    if contributions:
        avg = raised / len(contributions)
        print(f"Average/Member     : ₦{avg:,.2f}")
    print(f"Progress           : {percent:.1f}%")
    print(f"[{bar}] {percent:.0f}%")
    print("=" * 45)

def export_report():
    #write all contributions to a CSV file the user can open in excel/sheets
    filename = f"contributions_report_{datetime.now().strftime('%I:%M %p %d/%m/%Y')}.csv"
    filepath = os.path.join(SCRIPT_DIR, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["No.", "Name", "Amount", "Date"])
        for i, entry in enumerate(contributions, start=1):
            writer.writerow([i, entry["name"], entry["amount"], entry["date"]])
        writer.writerow([])
        writer.writerow(["Target", target])
        writer.writerow(["Total Raised", raised])
        writer.writerow(["Remaining", target - raised])
        writer.writerow(["Total Members", len(contributions)])
    return filepath

def show_list():
    print("\n--- Contribution List ---")
    if not contributions:
        print("No contributions yet.")
    for i, entry in enumerate(contributions, start=1):
        num = f"{i}."
        name = entry["name"]
        amount_str = f"₦{entry['amount']:,.2f}"
        print(f"{num:<4}{name:<22}{amount_str:<15}{entry['date']}")
    print("-" * 60)

while True:
    print("\n1. Add contribution")
    print("2. Show progress")
    print("3. Show contributor list")
    print("4. Edit contribution")
    print("5. Delete a contribution")
    print("6. Export report (CSV)")
    print("7. Exit")
    choice = input("\nSelect option (1-7): ").strip()

    if choice == "1":
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
                continue
            elif dup_choice not in ("1", "2"):
                print("Invalid choice. Cancelled.")
                continue
        else:
            dup_choice = "1"  # no duplicate, proceed normally
 
        try:
            amount = float(input("Amount contributed: ₦").strip())
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue
 
        raised += amount
        timestamp = now_string()
 
        if dup_choice == "2":
            # merge into the first existing entry for this name
            target_index = existing_indexes[0]
            entry = contributions[target_index]
            entry["amount"] += amount
            entry["date"] = timestamp  # update to the most recent contribution date
            print(f"✅ Added ₦{amount:,.2f} to {entry['name']}'s entry (new total: ₦{entry['amount']:,.2f})")
        else:
            contributions.append({"name": name, "amount": amount, "date": timestamp})
            print(f"✅ Added ₦{amount:,.2f} from {name} on {timestamp}")
 
        save_data(contributions)
        save_web_data(contributions, raised, target)

    elif choice == "2":
        show_progress()

    elif choice == "3":
        show_list()
    
    elif choice == "4":
        if not contributions:
            print("No contributor to edit.")
            continue

        show_list()
        try:
            index = int(input("Enter the number of the entry to edit: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue
        if index < 1 or index > len(contributions):
            print("The entry doesn't")
            continue

        entry = contributions[index - 1]
        print(f"Editing entry {index}: {entry['name']} - ₦{entry['amount']:,.2f} ({entry['date']})")

        new_name = input(f"New name (leave blank to keep '{entry['name']}'): ").strip()
        if new_name == "":
            new_name = entry["name"]
        
        new_amount_input = input(f"New amount(leave blank to keep ₦{entry['amount']:,.2f})").strip()
        if new_amount_input == "":
            new_amount = entry["amount"]
        else:
            try:
                new_amount = float(new_amount_input)
                if new_amount <= 0:
                    print("Amount must be greater than 0. Edit cancelled.")
                    continue
            except ValueError:
                print("Invalid amount. Edit cancelled.")
                continue
    
        raised -= entry["amount"]
        raised += new_amount
        entry["name"] = new_name
        entry["amount"] = new_amount
        entry["date"] = now_string()
        save_data(contributions)
        save_web_data(contributions, raised, target)
        print(f"✅ Entry {index} updated: {new_name} - ₦{new_amount:,.2f}")
    
    elif choice == "5":
        if not contributions:
            print("No contributions to delete.")
            continue

        show_list()
        try:
            index = int(input("Enter the number of the entry to delete: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue
        if index < 1 or index > len(contributions):
            print("That entry number doesn't exist.")
            continue

        entry = contributions[index - 1]
        confirm = input (f"Delete '{entry['name']} - ₦{entry['amount']:,.2f}'? (y/n): ").strip().lower()
        if confirm != "y":
            print("Delete cancelled.")
            continue
        raised -= entry["amount"]
        contributions.pop(index - 1)
        save_data(contributions)
        save_web_data(contributions, raised, target)
        print(f"🗑️ Deleted entry: {entry['name']} - ₦{entry['amount']:,.2f}")
        

    elif choice == "6":
        if not contributions:
            print("No contributions to export yet.")
            continue
        filepath = export_report()
        print(f"✅ Report_exported to: {filepath}")
    
    elif choice == "7":
        print("Exiting... Final summary:")
        show_list()
       
        show_progress()
        break

    else:
        print("Invalid option, please choose 1-7.")