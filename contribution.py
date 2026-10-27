
from actions import (
    add_contribution, delete_contribution, edit_contribution,
    export_csv, html_receipt_for_contributor, receipt_for_contributor,
)
from admin import require_admin, set_admin_password
from reports import search_contributions, show_list, show_progress
from storage import load_data, undo_last_change


def main():
    contributions = load_data()

    while True:
        print("\n 1. Add contribution")
        print(" 2. Show progress")
        print(" 3. Show contributor list")
        print(" 4. Search contributor")
        print(" 5. Edit contribution")
        print(" 6. Delete a contribution")
        print(" 7. Export report (CSV)")
        print(" 8. Receipt text for a contributor")
        print(" 9. Save HTML receipt (print / save as PDF)")
        print("10. Undo last change")
        print("11. Change admin password")
        print("12. Exit")
        choice = input("\nSelect option (1-12): ").strip()

        if choice == "1":
            add_contribution(contributions)
        elif choice == "2":
            show_progress(contributions)
        elif choice == "3":
            show_list(contributions)
        elif choice == "4":
            search_contributions(contributions)
        elif choice == "5":
            edit_contribution(contributions)
        elif choice == "6":
            delete_contribution(contributions)
        elif choice == "7":
            export_csv(contributions)
        elif choice == "8":
            receipt_for_contributor(contributions)
        elif choice == "9":
            html_receipt_for_contributor(contributions)
        elif choice == "10":
            result = undo_last_change()
            if result is not None:
                contributions = result
        elif choice == "11":
            if require_admin():
                set_admin_password()
        elif choice == "12":
            print("Exiting... Final summary:")
            show_list(contributions)
            show_progress(contributions)
            break
        else:
            print("Invalid option, please choose 1-12.")


if __name__ == "__main__":
    main()