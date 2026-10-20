"""Thank-you receipt text to paste into WhatsApp or SMS."""
from config import TARGET, PAGE_URL
from storage import total_raised


def build_receipt(entry, paid, contributions):
    """Make the receipt message for one contributor."""
    raised = total_raised(contributions)
    parts = entry["name"].strip().split()
    first_name = parts[0].title() if parts else "there"
    percent = (raised / TARGET) * 100
    lines = [
        f"Hello {first_name},",
        "",
        "Thank you for your contribution! 🙏",
        f"Amount received: ₦{paid:,.2f}",
        f"Date: {entry['date']}",
        f"Your total so far: ₦{entry['amount']:,.2f}",
        "",
        f"Group progress: ₦{raised:,.2f} of ₦{TARGET:,.2f} ({percent:.1f}%)",
        f"Track progress: {PAGE_URL}",
    ]
    return "\n".join(lines)


def print_receipt(entry, paid, contributions):
    print("\n" + "*" * 45)
    print("📋 RECEIPT TEXT (copy and send on WhatsApp)")
    print("-" * 45)
    print(build_receipt(entry, paid, contributions))
    print("*" * 45)