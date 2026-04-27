'''
This module manages the json configuration file for LockInLauncher, as well as the "lockin config" command.

This allows users to customize their experience by specifying which apps/websites are distracting and should be blocked.
'''

import rich
from rich.markup import escape
import json
import os
import time
import psutil
import subprocess

# Default config values (used if config file doesn't exist)
DEFAULT_CONFIG = {
    "user_name": "",
    "blocked_apps": [],
    "apps_to_open": []
}

# Define path to config file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
CONFIG_PATH = os.path.join(os.environ["APPDATA"], "LockInLauncher", "config.json")

# READING FROM JSON FILE
def load_config():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    try:
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        with open(CONFIG_PATH, 'r') as file:
            return json.load(file)
    except Exception:
        rich.print("[red]Error: The config file was not found.[/red]")
        return None

# WRITING TO JSON FILE
def save_config(config_data):
    try:
        with open(CONFIG_PATH, 'w') as file:
            json.dump(config_data, file, indent=4)
    except Exception:
        rich.print("[red]Error: Could not write to the config file.[/red]")

# MANAGING CONFIGURATION SETTINGS
def manage_config():
    config = load_config()
    if config is None:
        rich.print("[red]Error: Could not load config. Make sure the config file exists and is properly formatted.[/red]")
        return

    # Greet user
    print()
    if not len(config["user_name"]) == 0:
        rich.print(f"[cyan]Welcome to the config menu, [bold]{config['user_name']}[/bold]![/cyan]")
    else:
        rich.print("[cyan]Welcome to the config menu![/cyan]")
    rich.print("[dim]Here, you can customize your settings and preferences, such as what apps are blocked or opened during lockin sessions.[/dim]")
    print()

    message_array = ["Type the number that corresponds with the command you wish to run:", "1) View Settings", "2) Modify Name", "3) Add/Remove Blocked App", "4) Add/Remove Open on Startup App", "5) Exit"]

    while True:
        slow_type(message_array, 0.006)
        print()
        command = str(input(">>> "))
        print()

        match command:
            case "1":
                view_settings()
            case "2":
                modify_name()
            case "3":
                add_or_remove_blocked_app()
            case "4":
                add_or_remove_open_on_startup_app()
            case "5":
                exit_config()
            case _:
                rich.print("[red]Please enter a valid number 1-5![/red]")

        print() # For Spacing   

# For making the text type slowly rather than all at once
def slow_type(text_array, time_between_letters):
    for line in text_array:
        for char in line:
            print(char, end = '', flush = True)
            time.sleep(time_between_letters)
        print() # For new line after each line

# VIEWING Config Settings
def view_settings():
    # Adding the name:
    if not len(load_config()["user_name"]) == 0:
        name = load_config()["user_name"]
    else:
        name = "Not Set"
    settings = ["Name:", name, "", "Blocked Apps:"]

    # Adding the blocked apps:
    blocked_apps = load_config()["blocked_apps"]
    if blocked_apps:
        settings.extend(blocked_apps)
        settings.append("")
    else:
        settings.append("None")
        settings.append("")

    # Adding the apps to open:
    apps_to_open = load_config()["apps_to_open"]
    if apps_to_open:
        settings.append("Apps to Open on Startup:")
        settings.extend(apps_to_open)
    else:
        settings.append("Apps to Open on Startup:")
        settings.append("None")

    slow_type(settings, 0.006)

# MODIFYING Name
def modify_name():
    name = input("What's your name? ")
    if len(name) > 60:
        rich.print("[red]Too long![/red]")
        return
    elif len(name) == 0:
        rich.print("[red]Please enter a valid name.[/red]")
        return
    config = load_config()
    config["user_name"] = name
    save_config(config)
    slow_type(["Your name was updated."], 0.04)

# Ask whether to ADD or REMOVE blocked app
def add_or_remove_blocked_app():
    while True:
        command = input("Type 'add' to add a blocked app, or 'remove' to remove one: ")
        if command.lower() == "add":
            print()
            add_blocked_app()
            break
        elif command.lower() == "remove":
            print()
            remove_blocked_app()
            break
        else:
            rich.print("[red]Please enter a valid command ('add' or 'remove').[/red]")

# ADDING a blocked app
def add_blocked_app():
    config = load_config()
    if config is None:
        return
    
    # Getting app name from user:
    rich.print("[dim]Tip: To find the exact app name, open the app, then open Task Manager (Ctrl+Shift+Esc) → Details tab. Look for the .exe name (e.g. discord.exe)[/dim]")
    app_name = input("Now, enter the name of the app's process: ").strip().lower()
    print()

    # Veryfying App:
    if not app_name in [proc.info['name'].lower() for proc in psutil.process_iter(['name'])]:
        rich.print(f"[yellow]⚠️ '{app_name}' doesn't appear to be running right now.[/yellow]")
        rich.print("[yellow]Make sure the app is open and the name matches exactly (e.g. discord.exe).[/yellow]")
        confirm = input("Add it anyway? (y/n): ")
        if confirm.lower() != "y":
            return
    
    if app_name in [app.strip().lower() for app in config["blocked_apps"]]:
        rich.print(f"[yellow]{app_name} is already in the blocked apps list.[/yellow]")
        return
    
    try:
        config["blocked_apps"].append(app_name)
        save_config(config)
        rich.print(f"[green]{app_name} has been added to the blocked apps list.[/green]")
    except Exception:
        rich.print(f"[red]Error: Could not add {app_name} to the blocked apps list.[/red]")

# REMOVING a blocked app
def remove_blocked_app():
    config = load_config()
    if config is None:
        return

    # In case there are no blocked apps
    if len(config["blocked_apps"]) == 0:
        rich.print("[cyan]There are currently no blocked apps. Try adding some![/cyan]")
        return

    # Showing options to the user
    rich.print("[cyan]Currently Blocked Apps:[/cyan]")
    for app in config["blocked_apps"]:
        rich.print(f"[dim]{app}[/dim]")
    
    app_name = input("Enter the name of the app to remove: ").strip().lower()
    
    # Check if the app exists in blocked_apps
    match = next((app for app in config["blocked_apps"] if app.lower() == app_name), None)
    if match is None:
        rich.print(f"[yellow]⚠️ '{app_name}' is not in the blocked apps list. Check for typos![/yellow]")
        return
    
    try:
        config["blocked_apps"].remove(match)
        save_config(config)
        rich.print(f"[green]{match} has been removed from the blocked apps list.[/green]")
    except Exception:
        rich.print(f"[red]Error: Could not remove {app_name} from the blocked apps list.[/red]")

# Ask whether to ADD or REMOVE an open on startup app
def add_or_remove_open_on_startup_app():
    while True:
        command = input("Type 'add' to add an app to open on startup, or 'remove' to remove one: ")
        if command.lower() == "add":
            print()
            add_open_on_startup_app()
            break
        elif command.lower() == "remove":
            print()
            remove_open_on_startup_app()
            break
        else:
            rich.print("[red]Please enter a valid command ('add' or 'remove').[/red]")

# ADDING an open on startup app
def add_open_on_startup_app():
    config = load_config()
    if config is None:
        return
    
    # Telling user how to find the app path:
    rich.print("[dim cyan]Note: To find an app's full path:[/dim cyan]")
    rich.print("[dim cyan] 1. Open the app[/dim cyan]")
    rich.print("[dim cyan] 2. Open Task Manager (Ctrl+Shift+Esc) → Details tab[/dim cyan]")
    rich.print("[dim cyan] 3. Right click the process → 'Open file location'[/dim cyan]")
    rich.print("[dim cyan] 4. Click the address bar at the top of the folder that opens — it becomes a text field[/dim cyan]")
    rich.print("[dim cyan] 5. Copy that path and add a backslash + the .exe name at the end[/dim cyan]")
    rich.print("[dim cyan]   *For Example:  C:/Program Files/Notion/Notion.exe[/dim cyan]")
    print()

    # Getting the app path from user:
    app_path = input("Now, enter the full path of the app: ").strip()
    print()

    # Veryfying App:
    slow_type(["Verifying App Path....."], 0.08) # For the effect
    try:
        proc = subprocess.Popen(app_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.terminate() # immediately close it, just testing if it works
        rich.print("[green]File path was verified.[/green]")
        print()
    except Exception:
        rich.print("[red]Error: Check your file path and try again.[/red]")
        return
    
    if app_path in [app.strip() for app in config["apps_to_open"]]:
        rich.print(f"[yellow]This app is already in the apps to open list.[/yellow]")
        return
    
    try:
        config["apps_to_open"].append(app_path)
        save_config(config)
        rich.print(f"[green]This app has been added to the apps to open list.[/green]")
    except Exception:
        rich.print(f"[red]Error: Could not add this app to the apps to open list.[/red]")

# REMOVING an open on startup app
def remove_open_on_startup_app():
    config = load_config()
    if config is None:
        return

    # In case there are no blocked apps
    if len(config["apps_to_open"]) == 0:
        rich.print("[cyan]There are currently no apps set to open on startup. Try adding some![/cyan]")
        return

    # Showing options to the user
    rich.print("[cyan]Current Apps set to Open on Startup:[/cyan]")
    for i, app in enumerate(config["apps_to_open"], 1):
        rich.print(f"[dim white]{i}) {app}[/dim white]")
    
    app_num = input("Enter the number next to the app you want to remove: ").strip()

    # Trying to remove user's chosen app
    try:
        app_num = int(app_num)
        if 1 <= app_num <= len(config["apps_to_open"]):
            try:
                del config["apps_to_open"][i - 1]
                save_config(config)
                rich.print(f"[green]This app has been removed from the apps to open list.[/green]")
            except Exception:
                rich.print(f"[red]Error: Could not remove this app from the apps to open list.[/red]") # Error while removing
        else:
            rich.print("[red]Please enter a valid number![/red]") # Number was out of range
            return
    except ValueError:
        rich.print("[red]Please enter a valid number![/red]") # Number was not an int
        return

# EXITING
def exit_config():
    slow_type(["Thanks for using LockInLauncher!", "Questions or feedback? Open an issue at github.com/johnnydunal/LockInLauncher"], 0.02)
    exit()