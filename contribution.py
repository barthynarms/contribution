
from actions import (
    add_contribution, delete_contribution, edit_contribution,
    export_csv, receipt_for_contributor,
)
from admin import require_admin, set_admin_password
from reports import show_list, show_progress
from storage import load_data


def main():
    contributions = load_data()

    while True:
        print("\n1. Add contribution")
        print("2. Show progress")
        print("3. Show contributor list")
        print("4. Edit contribution")
        print("5. Delete a contribution")
        print("6. Export report (CSV)")
        print("7. Receipt text for a contributor")
        print("8. Change admin password")
        print("9. Exit")
        choice = input("\nSelect option (1-9): ").strip()

        if choice == "1":
            add_contribution(contributions)
        elif choice == "2":
            show_progress(contributions)
        elif choice == "3":
            show_list(contributions)
        elif choice == "4":
            edit_contribution(contributions)
        elif choice == "5":
            delete_contribution(contributions)
        elif choice == "6":
            export_csv(contributions)
        elif choice == "7":
            receipt_for_contributor(contributions)
        elif choice == "8":
            if require_admin():
                set_admin_password()
        elif choice == "9":
            print("Exiting... Final summary:")
            show_list(contributions)
            show_progress(contributions)
            break
        else:
            print("Invalid option, please choose 1-9.")


if __name__ == "__main__":
    main()