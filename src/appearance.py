'''
This module manages the appearance of the app, making the outputs look nice.
'''

import rich
from rich.panel import Panel
from rich.console import Console

from src.timer import display_time

# Manage the appearance of the terminal from now on
def manage_display(timer_length):
    show_gadgets(timer_length)

# Displays some gadgets in a table such as a focus timer
def show_gadgets(timer_length):
    display_time(timer_length)

# Displays the welcome message/banner after startup
def display_welcome_message():
    console = Console()
    console.print(Panel("[bold cyan]🔒 LockInLauncher[/bold cyan]\n[dim]One command. Zero distractions. Full focus.[/dim]", border_style="cyan", width = 48))