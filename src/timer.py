'''
This module manages the timing of focused work sessions.
'''

from rich.live import Live
from rich.table import Table
import time
import src.state as state

def display_time(timer_length):
    time_remaining = timer_length * 60
    
    with Live(Table(title="Live Data"), refresh_per_second=2) as live:
        while time_remaining >= 0:
            minutes = time_remaining // 60
            seconds = time_remaining % 60

            table = Table()
            table.add_column("Current Time")
            table.add_column("Focus Timer")
            table.add_row(str(time.strftime("%I:%M %p")), f"{minutes}:{seconds:02d}")
            live.update(table)
            time.sleep(1)
            time_remaining -= 1
        
        # Time ran out
        state.is_locked_in = False