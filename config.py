import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def get_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get(key: str, default=None):
    return get_config().get(key, default)