import json
import os

CONFIG_FILE = "config/config.json"


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(data):

    os.makedirs("config", exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_api_key():

    config = load_config()

    return config.get("api_key", "")


def set_api_key(key):

    config = load_config()

    config["api_key"] = key

    save_config(config)
