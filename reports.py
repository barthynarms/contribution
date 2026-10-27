
import csv
import os
from datetime import datetime

from config import SCRIPT_DIR, TARGET
from storage import total_raised


def show_progress(contributions):
    raised = total_raised(contributions)

    print("\n" + "=" * 45)
    print("       CONTRIBUTION PROGRESS TRACKER    ")
    print("=" * 45)
    print(f"Target Amount      : ₦{TARGET:,.2f}")
    print(f"Amount Raised      : ₦{raised:,.2f}")

    if TARGET <= 0:
        print("⚠️  Target amount is not set (TARGET = 0). Update config.py.")
        print("=" * 45)
        return

    remaining = TARGET - raised
    percent = (raised / TARGET) * 100
    bar_length = 30
    filled = int(bar_length * raised / TARGET)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"Remaining          : ₦{remaining:,.2f}")
    print(f"Total Members      : {len(contributions)}")
    if contributions:
        avg = raised / len(contributions)
        print(f"Average/Member     : ₦{avg:,.2f}")
    print(f"Progress           : {percent:.1f}%")
    print(f"[{bar}] {percent:.0f}%")
    print("=" * 45)


def show_list(contributions):
    print("\n--- Contribution List ---")
    if not contributions:
        print("No contributions yet.")
    for i, entry in enumerate(contributions, start=1):
        num = f"{i}."
        name = entry["name"]
        amount_str = f"₦{entry['amount']:,.2f}"
        print(f"{num:<4}{name:<22}{amount_str:<15}{entry['date']}")
    print("-" * 60)


def export_report(contributions):
    raised = total_raised(contributions)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filepath = os.path.join(SCRIPT_DIR, f"contributions_report_{stamp}.csv")

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["No.", "Name", "Amount", "Date"])
        for i, entry in enumerate(contributions, start=1):
            writer.writerow([i, entry["name"], entry["amount"], entry["date"]])
        writer.writerow([])
        writer.writerow(["Target", TARGET])
        writer.writerow(["Total Raised", raised])
        writer.writerow(["Remaining", TARGET - raised])
        writer.writerow(["Total Members", len(contributions)])
    return filepath


def search_contributions(contributions):
    if not contributions:
        print("No contributions yet.")
        return
    query = input("Search name: ").strip()
    if not query:
        print("No search term entered.")
        return
    results = [
        (i + 1, entry)
        for i, entry in enumerate(contributions)
        if query.lower() in entry["name"].lower()
    ]
    if not results:
        print(f"No contributors found matching '{query}'.")
        return
    print(f"\n--- Search Results for '{query}' ---")
    for num, entry in results:
        amount_str = f"₦{entry['amount']:,.2f}"
        print(f"{num:<4}{entry['name']:<22}{amount_str:<15}{entry['date']}")
    print("-" * 60)