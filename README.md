
# Contribution Tracker

A simple tool for tracking group contributions towards a fundraising target. You record contributions from a Python command-line program, and a web page shows the live progress to everyone.

The default target is **₦500,000** and all amounts are in Naira (₦).

## What's inside

| File | What it does |
| --- | --- |
| `contribution.py` | The command-line program you use to add, edit, delete and view contributions |
| `contributions.json` | Your saved records (the program's own database) |
| `data.json` | The data the web page reads. The program updates it automatically |
| `index.html` | The progress page: shows the amount raised, a progress bar and the list of contributors |

## Features

- Add a contribution (name, amount, date and time are saved automatically)
- Warns you when a name already exists, so you can add a separate entry or add to the existing one
- Show progress: target, amount raised, amount remaining, number of members, average per member and a progress bar
- Show the full contributor list
- Edit or delete an entry
- Export a CSV report you can open in Excel or Google Sheets
- Updates `data.json` after every change so the web page stays current

## Current contributions

Progress as of 02:36 PM, 07/10/2026:

| Target | Raised | Remaining | Progress |
| --- | --- | --- | --- |
| ₦500,000.00 | ₦378,000.00 | ₦122,000.00 | 75.6% |

`[██████████████████████░░░░░░░░] 76%`

| No. | Name | Amount | Date |
| --- | --- | --- | --- |
| 1 | Helen Ogeh | ₦30,000.00 | 11:30 AM 18/09/2026 |
| 2 | Blessing Franics | ₦38,000.00 | 11:27 AM 18/09/2026 |
| 3 | Engr Bartholowew | ₦200,000.00 | 11:28 AM 18/09/2026 |
| 4 | Joy Iorfa | ₦40,000.00 | 11:29 AM 18/09/2026 |
| 5 | Aondofa Ushahemba | ₦20,000.00 | 02:33 PM 07/10/2026 |
| 6 | Faith Owicho | ₦50,000.00 | 02:36 PM 07/10/2026 |

**Total members:** 6 | **Average per member:** ₦63,000.00

> This table is a snapshot. For the live numbers, open the progress page (`index.html`).

## Requirements

- Python 3 (no extra packages needed)
- Git and a GitHub account (to publish the web page)

## How to use

1. Open a terminal in this folder and run:

   ```bash
   python contribution.py
   ```

2. Choose an option from the menu:

   ```
   1. Add contribution
   2. Show progress
   3. Show contributor list
   4. Edit contribution
   5. Delete a contribution
   6. Export report (CSV)
   7. Exit
   ```

3. After adding, editing or deleting, the program updates `data.json`. To make the change show on the web page, commit and push it:

   ```bash
   git add contributions.json data.json
   git commit -m "Update contributions"
   git push
   ```

## Changing the target amount

Open `contribution.py` and change this line near the top:

```python
target = 500000
```

## Setting up the web page

`index.html` loads its numbers from `data.json` on GitHub. Near the bottom of `index.html` there is a line like this:

```javascript
const DATA_URL = "https://raw.githubusercontent.com/barthynarms/contribution/main/data.json?t=" + Date.now();
```

Make sure it points to **this** repository and the `main` branch, with your own GitHub username.

To put the page online for free with GitHub Pages:

1. Go to the repository **Settings → Pages**.
2. Under **Branch**, choose `main` and the `/ (root)` folder, then click **Save**.
3. After a minute, your page will be live at `https://barthynarms.github.io/contribution/`.

## Data format

Each contribution is stored like this:

```json
{
  "name": "Jane Doe",
  "amount": 50000.0,
  "date": "02:36 PM 07/10/2026"
}
```

`data.json` wraps the list together with the target and the last update time:

```json
{
  "target": 500000,
  "last_updated": "02:36 PM 07/10/2026",
  "contributions": []
}
```

## Notes

- Keep `contributions.json` safe. It is the main record of all contributions.
- The CSV report is saved in the same folder as `contribution.py`.

## License

See the [LICENSE](LICENSE) file.