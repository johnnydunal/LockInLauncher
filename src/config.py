'''
This module manages the json configuration file for LockInLauncher.

This allows users to customize their experience by specifying which apps/websites are distracting and should be blocked.
'''

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Reading from json file
def load_config():
    try:
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    except Exception:
        print("Error: The config file was not found.")
        return None