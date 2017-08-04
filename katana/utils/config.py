import os

def has_json_config():
    return bool(os.path.exists("katana.json"))