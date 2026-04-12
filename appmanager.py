'''
This module manages the opening and closing of applications, and ensures that they stay closed while in focus mode.
'''

import subprocess
import psutil
import time

import state

# List of apps to open and close
apps_to_open = [r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE", r"C:\Users\johnn\AppData\Local\Programs\Microsoft VS Code\Code.exe"]
blacklist = ["Spotify.exe", "Steam.exe", "Discord.exe", "Chrome.exe", "Netflix.exe"]

# Closing Apps:
def kill_distracting_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() in [app.lower() for app in blacklist]:
            try:
                proc.terminate()
                proc.wait(timeout=1.5)
            except psutil.TimeoutExpired:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    return "[green]Distracting apps have been closed.[/green]"

# Check for banned apps being open while in focus mode
def check_for_banned_apps():
    while state.is_locked_in:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() in [app.lower() for app in blacklist]:
                try:
                    proc.terminate()
                    proc.wait(timeout=1.5)
                except psutil.TimeoutExpired:
                    proc.kill()
                except psutil.NoSuchProcess:
                    pass
        time.sleep(4)  # Check every 4 seconds

# Opening Apps:
def openapps():
    try:
        for app in apps_to_open:
            subprocess.Popen(app)
        return "[green]" + str(len(apps_to_open)) + " apps have been successfully opened.[/green]"
    except Exception:
        return "[red]Error while opening apps.[/red]"