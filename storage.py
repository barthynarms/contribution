
import json
import os
from datetime import datetime

from config import DATA_FILE, WEB_DATA_FILE, TARGET


def now_string():
    return datetime.now().strftime("%I:%M %p %d/%m/%Y")


def load_data():
    if not os.path.exists(DATA_FILE):
        return [] 

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return [] 

    if not isinstance(data, list):
        return [] 

    return data


def save_data(contributions):
    with open(DATA_FILE, "w") as f:
        json.dump(contributions, f, indent=2)


def save_web_data(contributions):
    payload = {
        "target": TARGET,
        "last_updated": now_string(),
        "contributions": contributions,
    }
    with open(WEB_DATA_FILE, "w") as f:
        json.dump(payload, f, indent=2)
    print("📝 data.json updated - commit and push it to go live.")


def total_raised(contributions):
    return sum(entry["amount"] for entry in contributions)