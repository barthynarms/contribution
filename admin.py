
import getpass
import hashlib
import hmac
import json
import os
import secrets

from config import ADMIN_FILE, SCRIPT_DIR

admin_logged_in = False  


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)


def keep_admin_file_private():
    gitignore = os.path.join(SCRIPT_DIR, ".gitignore")
    existing = ""
    if os.path.exists(gitignore):
        with open(gitignore, "r") as f:
            existing = f.read()
    if "admin_config.json" not in existing:
        with open(gitignore, "a") as f:
            f.write("\n# Admin password (keep private)\nadmin_config.json\n")


def set_admin_password():
    
    print("\n🔐 Create an admin password (press Enter on an empty line to cancel).")
    while True:
        pw = getpass.getpass("New password (at least 6 characters): ")
        if pw == "":
            print("Cancelled.")
            return False
        if len(pw) < 6:
            print("Too short. Use at least 6 characters.")
            continue
        if getpass.getpass("Confirm password: ") != pw:
            print("Passwords do not match. Try again.")
            continue
        break
    salt = secrets.token_bytes(16)
    with open(ADMIN_FILE, "w") as f:
        json.dump({"salt": salt.hex(), "hash": hash_password(pw, salt).hex()}, f)
    keep_admin_file_private()
    print("✅ Admin password saved.")
    return True


def require_admin():
    global admin_logged_in
    if admin_logged_in:
        return True

    if not os.path.exists(ADMIN_FILE): 
        admin_logged_in = set_admin_password()
        return admin_logged_in

    try:
        with open(ADMIN_FILE, "r") as f:
            saved = json.load(f)
        salt, saved_hash = bytes.fromhex(saved["salt"]), saved["hash"]
    except (OSError, ValueError, KeyError):
        print("⚠️  admin_config.json is damaged. Delete it to create a new password.")
        return False

    for attempts_left in (2, 1, 0):
        pw = getpass.getpass("🔐 Admin password: ")
        if hmac.compare_digest(hash_password(pw, salt).hex(), saved_hash):
            admin_logged_in = True
            return True
        print(f"❌ Wrong password. {attempts_left} attempt(s) left.")
    print("🔒 Action cancelled.")
    return False