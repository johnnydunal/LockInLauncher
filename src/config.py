'''
This module manages the json configuration file for LockInLauncher, as well as the "lockin config" command.

This allows users to customize their experience by specifying which apps/websites are distracting and should be blocked.
'''

from rich import print
from rich.markup import escape
import json
import os

# Define path to config file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# READING FROM JSON FILE
def load_config():
    try:
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    except Exception:
        print("[red]Error: The config file was not found.[/red]")
        return None

# WRITING TO JSON FILE
def save_config(config_data):
    try:
        with open(CONFIG_PATH, 'w') as file:
            json.dump(config_data, file, indent=4)
    except Exception:
        print("[red]Error: Could not write to the config file.[/red]")

# MANAGING CONFIGURATION SETTINGS
def manage_config():
    config = load_config()
    if config is None:
        return
    
    # Displaying saved config info:
    for key, value in config.items():
        print(escape(f"{key}: {value}"))
    
    # Testing the adding of an app to the blocked apps list:
    app_to_block = input("What app would you like to block?")
    add_blocked_app(app_to_block)
    remove_blocked_app(input("What app would you like to remove?"))

# Adding a blocked app
def add_blocked_app(app_name):
    config = load_config()
    if config is None:
        return
    
    if app_name in config["blocked_apps"]:
        print(f"[yellow]{app_name} is already in the blocked apps list.[/yellow]")
        return
    
    try:
        config["blocked_apps"].append(app_name)
        save_config(config)
        print(f"[green]{app_name} has been added to the blocked apps list.[/green]")
    except Exception:
        print(f"[red]Error: Could not add {app_name} to the blocked apps list.[/red]")

# Removing a blocked app
def remove_blocked_app(app_name):
    config = load_config()
    if config is None:
        return
    
    if app_name not in config["blocked_apps"]:
        print(f"[yellow]{app_name} is not in the blocked apps list. Check for typos.[/yellow]")
        return
    
    try:
        config["blocked_apps"].remove(app_name)
        save_config(config)
        print(f"[green]{app_name} has been removed from the blocked apps list.[/green]")
    except Exception:
        print(f"[red]Error: Could not remove {app_name} from the blocked apps list.[/red]")