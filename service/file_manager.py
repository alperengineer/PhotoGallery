import json
import os

DATA_FILE = os.path.join("data", "photo_entry.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Veri kaydedilemedi: {e}")
