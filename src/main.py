'''
Welcome to LockInLauncher!

LockInLauncher is a productivity automation tool that eliminates distractions and instantly configures a focused workspace,
helping users stay locked into deep work.

Created by: Johnny Dunal
'''

import typer
from rich import print
import threading
import time
import keyboard
import msvcrt

from src.appmanager import kill_distracting_apps, openapps, check_for_banned_apps
from src.appearance import display_welcome_message, manage_display
from src.config import manage_config
import src.state as state

app = typer.Typer()

# The command that starts a session
@app.command()
def start():

    # Start the session:
    state.is_locked_in = True
    display_welcome_message()

    # Find length of study session:
    session_length = 0
    while True:
        length = input("How many minutes do you want to focus for? ")
        try:
            session_length = int(length)
            if 0 < session_length < 360:
                break
            else:
                print("[red]Please enter a valid length![/red]")
        except Exception:
            print("[red]Please enter a valid number![/red]")
            
    print()
    kill_distracting_apps()
    openapps()
    print("[cyan]Session started! It will end automatically one your timer runs out. Stay FOCUSED![/cyan]")
    print("[yellow]Note: Closing this window is cheating. But we won't stop you... 👀[/yellow]")
    print()
    
    # Start a background thread for the timer and other utilities
    appearance_thread = threading.Thread(target=manage_display, args=(session_length,), daemon=True)
    appearance_thread.start()
    time.sleep(0.1) # to ensure that the gadgets and timers are loaded before proceeding

    # Start a background thread to continuously check for and kill distracting apps
    killer_thread = threading.Thread(target=check_for_banned_apps, daemon=True)
    killer_thread.start()

    # Keep the main thread alive while session is still active
    while True:
        time.sleep(1)
        if state.is_locked_in == False:
            end_session()

# Triggered when ending session
def end_session():
    state.is_locked_in = False
    flush_input()
    print()
    print("[cyan]Session ended. Great job staying focused![/cyan]")
    print("[purple]Note: Use 'lockin config' to customize your settings if desired![/purple]")
    time.sleep(1)
    exit()

# Flush terminal input after session ends
def flush_input():
    while msvcrt.kbhit():
        msvcrt.getch()

# The command that allows user to customize settings/preferences
@app.command()
def config():
    print("[red]Note: This config menu is still a work in progress![/red]") # TEMPORARY
    display_welcome_message()
    manage_config()

if __name__ == "__main__":
    app()