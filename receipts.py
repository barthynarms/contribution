"""Thank-you receipt text to paste into WhatsApp or SMS."""
import os
from datetime import datetime

from config import PAGE_URL, SCRIPT_DIR, TARGET
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


def save_receipt_html(entry, paid, contributions):
    """Generate a printable HTML receipt file. Open in a browser and use Print → Save as PDF."""
    raised = total_raised(contributions)
    parts = entry["name"].strip().split()
    first_name = parts[0].title() if parts else "there"
    name_display = " ".join(w.title() for w in parts)
    percent = (raised / TARGET * 100) if TARGET > 0 else 0
    percent_capped = min(percent, 100)
    generated = datetime.now().strftime("%I:%M %p %d/%m/%Y")
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_name = "".join(c if c.isalnum() else "_" for c in entry["name"])
    filename = f"receipt_{safe_name}_{stamp}.html"
    filepath = os.path.join(SCRIPT_DIR, filename)

    # Pre-format values to avoid f-string nesting issues
    paid_str = f"\u20a6{paid:,.2f}"
    total_str = f"\u20a6{entry['amount']:,.2f}"
    raised_str = f"\u20a6{raised:,.2f}"
    target_str = f"\u20a6{TARGET:,.2f}"
    bar_pct = f"{percent_capped:.1f}"
    percent_label = f"{percent_capped:.1f}%"
    entry_date = entry['date']

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Receipt \u2013 {name_display}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@500;600;700&family=Karla:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Karla', sans-serif; background: #F7F4EC; color: #1A1A16; padding: 40px 20px; }}
  .receipt {{ max-width: 480px; margin: 0 auto; background: #fff; border-radius: 14px; padding: 40px; box-shadow: 0 4px 32px rgba(0,0,0,.09); }}
  .logo {{ font-family: 'Bitter', serif; font-size: 20px; font-weight: 700; color: #1F3A2E; margin-bottom: 28px; }}
  .badge {{ display: inline-block; background: #E8F5EE; color: #1F7A4D; font-size: 13px; font-weight: 600; padding: 4px 12px; border-radius: 20px; margin-bottom: 14px; }}
  h1 {{ font-family: 'Bitter', serif; font-size: 22px; font-weight: 700; color: #1A1A16; margin-bottom: 6px; }}
  .greeting {{ color: #5B5A4F; font-size: 15px; margin-bottom: 28px; }}
  .amount-box {{ background: #F7F4EC; border-radius: 10px; padding: 20px 24px; margin-bottom: 24px; }}
  .amount-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: #5B5A4F; margin-bottom: 6px; }}
  .amount-value {{ font-family: 'Bitter', serif; font-size: 38px; font-weight: 700; color: #1F3A2E; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 15px; }}
  td {{ padding: 10px 0; border-bottom: 1px solid #DDD8C6; vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  td:first-child {{ color: #5B5A4F; width: 50%; }}
  td:last-child {{ text-align: right; font-weight: 500; }}
  .prog-label {{ font-size: 13px; color: #5B5A4F; margin-bottom: 8px; }}
  .bar-track {{ height: 10px; background: #E7E2D1; border-radius: 5px; overflow: hidden; margin-bottom: 8px; }}
  .bar-fill {{ height: 100%; background: linear-gradient(90deg, #34523F, #C9973A); border-radius: 5px; width: {bar_pct}%; }}
  .prog-meta {{ display: flex; justify-content: space-between; font-size: 13px; color: #5B5A4F; margin-bottom: 24px; }}
  .footer-note {{ font-size: 13px; color: #5B5A4F; border-top: 1px solid #DDD8C6; padding-top: 20px; }}
  .footer-note a {{ color: #1F7A4D; text-decoration: none; }}
  .print-btn {{ margin-top: 24px; display: block; width: 100%; padding: 12px; background: #1F3A2E;
    color: #fff; border: none; border-radius: 8px; font-family: 'Karla', sans-serif;
    font-size: 15px; font-weight: 600; cursor: pointer; }}
  @media print {{ body {{ background: white; padding: 0; }} .receipt {{ box-shadow: none; }} .print-btn {{ display: none; }} }}
</style>
</head>
<body>
<div class="receipt">
  <div class="logo">\U0001f33f Fundraising Tracker</div>
  <div class="badge">\u2705 Payment Confirmed</div>
  <h1>Thank you, {first_name}!</h1>
  <p class="greeting">Your contribution has been received and recorded.</p>
  <div class="amount-box">
    <div class="amount-label">Amount received</div>
    <div class="amount-value">{paid_str}</div>
  </div>
  <table>
    <tr><td>Contributor</td><td>{name_display}</td></tr>
    <tr><td>Total contributed</td><td>{total_str}</td></tr>
    <tr><td>Date of payment</td><td>{entry_date}</td></tr>
    <tr><td>Receipt generated</td><td>{generated}</td></tr>
  </table>
  <p class="prog-label">Group progress</p>
  <div class="bar-track"><div class="bar-fill"></div></div>
  <div class="prog-meta">
    <span>{raised_str} raised of {target_str}</span>
    <span>{percent_label}</span>
  </div>
  <p class="footer-note">Track live progress: <a href="{PAGE_URL}">{PAGE_URL}</a></p>
  <button class="print-btn" onclick="window.print()">\U0001f5a8\ufe0f Print / Save as PDF</button>
</div>
</body>
</html>"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\u2705 HTML receipt saved: {filepath}")
        print("   Open it in a browser and click 'Print / Save as PDF'.")
        return filepath
    except OSError as e:
        print(f"\u274c Could not save HTML receipt: {e}")
        return None