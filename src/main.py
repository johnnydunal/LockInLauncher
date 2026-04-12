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

from src.appmanager import kill_distracting_apps, openapps, check_for_banned_apps
import src.state as state

app = typer.Typer()


# The command that starts a session
@app.command()
def start():
    state.is_locked_in = True
    print(kill_distracting_apps())
    print(openapps())

    # Start a background thread to continuously check for and kill distracting apps
    killer_thread = threading.Thread(target=check_for_banned_apps, daemon=True)
    killer_thread.start()

    print("[green]Session started![/green]")

    # Wait for the user to end the session
    while True:
        user_command = input("Type 'end' to end your session: ")
        if user_command == "end":
            state.is_locked_in = False
            print("[green]Session ended. Great job staying focused![/green]")
            time.sleep(1)
            break


@app.command()
def config():
    print("This is where the configuration menu will be implemented.")


if __name__ == "__main__":
    app()