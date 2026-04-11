# Testing typer

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

if __name__ == "__main__":
    app()