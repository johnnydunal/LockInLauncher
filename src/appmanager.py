'''
This module manages the opening and closing of applications, and ensures that they stay closed while in focus mode.
'''

from rich import print
import subprocess
import psutil
import time

import src.state as state
from src.config import load_config

# List of apps to open and close, loaded from the .config file
project_info = load_config() # reading in data from the config file
blocked_apps = project_info["blocked_apps"]
apps_to_open = project_info["apps_to_open"]

# Closing Apps:
def kill_distracting_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() in [app.lower() for app in blocked_apps]:
            try:
                proc.terminate()
                proc.wait(timeout=1)
            except psutil.TimeoutExpired:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    # return "[green]Distracting apps have been closed.[/green]"

# Check for banned apps being open while in focus mode
def check_for_banned_apps():
    while state.is_locked_in:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() in [app.lower() for app in blocked_apps]:
                try:
                    proc.terminate()
                    proc.wait(timeout=1)
                except psutil.TimeoutExpired:
                    proc.kill()
                except psutil.NoSuchProcess:
                    pass
        time.sleep(4)  # Check every 4 seconds

# Opening Apps:
def openapps():
    apps_failed_to_open = 0
    for app in apps_to_open:
        try:
            subprocess.Popen(app, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            apps_failed_to_open += 1
    if not apps_failed_to_open == 0:
        print("[red]Failed to open " + str(apps_failed_to_open) + " app(s).[/red]")
        print("[red]Run 'lockin config' to make sure the app names in your settings are correct.[/red]\n")