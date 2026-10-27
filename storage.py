
import json
import os
import shutil
from datetime import datetime

from config import BACKUP_FILE, DATA_FILE, WEB_DATA_FILE, TARGET


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
    # Back up the previous state so the last change can be undone.
    if os.path.exists(DATA_FILE):
        try:
            shutil.copy2(DATA_FILE, BACKUP_FILE)
        except OSError:
            pass 
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(contributions, f, indent=2)
    except OSError as e:
        print(f"❌ Could not save contributions.json: {e}")


def save_web_data(contributions):
    payload = {
        "target": TARGET,
        "last_updated": now_string(),
        "contributions": contributions,
    }
    try:
        with open(WEB_DATA_FILE, "w") as f:
            json.dump(payload, f, indent=2)
        print("📝 data.json updated - commit and push it to go live.")
    except OSError as e:
        print(f"❌ Could not update data.json: {e}")



def undo_last_change():
    if not os.path.exists(BACKUP_FILE):
        print("⚠️  No backup found — nothing to undo.")
        return None
    try:
        with open(BACKUP_FILE, "r") as f:
            backup_data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ Could not read backup: {e}")
        return None
    # make the current file the new backup (enables redo via undo again)
    if os.path.exists(DATA_FILE):
        try:
            shutil.copy2(DATA_FILE, BACKUP_FILE)
        except OSError:
            pass
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(backup_data, f, indent=2)
        save_web_data(backup_data)
        print("✅ Last change undone.")
        return backup_data
    except OSError as e:
        print(f"❌ Could not restore: {e}")
        return None


def total_raised(contributions):
    return sum(entry["amount"] for entry in contributions)