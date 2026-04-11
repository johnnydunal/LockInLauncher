import typer
from rich import print
import subprocess
import psutil

app = typer.Typer()

# The command that starts a session
@app.command()
def start():
    print(kill_distracting_apps())
    print(openapps())
    print("[green]Session started![/green]")

@app.command()
def stop():
    print("The program has been stopped.")

# List of apps to open and close
apps_to_open = [r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE", r"C:\Users\johnn\AppData\Local\Programs\Microsoft VS Code\Code.exe"]
blacklist = ["Spotify.exe", "Steam.exe", "Discord.exe"]

# Closing Apps:

def kill_distracting_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() in [app.lower() for app in blacklist]:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except psutil.TimeoutExpired:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
    return "[green]Distracting apps have been closed.[/green]"

# Opening Apps:

def openapps():
    try:
        for app in apps_to_open:
            subprocess.Popen(app)
        return "[green]" + str(len(apps_to_open)) + " apps have been successfully opened.[/green]"
    except Exception:
        return "[red]Error while opening apps.[/red]"


if __name__ == "__main__":
    app()