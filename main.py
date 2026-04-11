# Typer

import typer
from rich import print
import time

app = typer.Typer()

run = False

@app.command()
def start():
    run = True
    print("[green]Session started![/green]")

@app.command()
def stop():
    print("Program is stopping...")
    run = False

# Opening Apps:

import subprocess

@app.command()
def openapp():
    try:
        subprocess.Popen("spotify")
        subprocess.Popen(r"C:\Users\johnn\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        print("[green]App opened![/green]")
    except FileNotFoundError:
        print("[red]Error: Could not locate app.[/red]")
    except Exception:
        print("[red]Error while opening app.[/red]")


if __name__ == "__main__":
    app()