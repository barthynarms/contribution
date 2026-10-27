import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(SCRIPT_DIR, "contributions.json")     
WEB_DATA_FILE = os.path.join(SCRIPT_DIR, "data.json")           
ADMIN_FILE = os.path.join(SCRIPT_DIR, "admin_config.json")
BACKUP_FILE = os.path.join(SCRIPT_DIR, "contributions_backup.json")

TARGET = 500000

PAGE_URL = "https://barthynarms.github.io/contribution/"