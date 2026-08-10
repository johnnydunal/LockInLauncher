'''
    This module is just for testing features that might be implemented later!
'''

import win32console, win32gui, win32con
import ctypes
import time
import keyboard

from src.websitemanager import _get_blocked_sites_from_config

def run_tests():
    pass
    # print(_get_blocked_sites_from_config())
    # print(ctypes.windll.shell32.IsUserAnAdmin() != 0) # Returns whether the program has admin rights (necessary for modifying the hosts file)

# Attempt at disabling Ctrl+C using the keyboard module. Careful, since this makes it hard to quit the program (which is technically what we want!).
def disable_ctrl_c():
    try:
        wait_forever()
    except KeyboardInterrupt:
        print("Ctrl+C is disabled during testing! Please use the designated method to end the test. (If you want to end the test, just close this window. But try it out first! 👀)")
    ''' Disable Ctrl+C
    keyboard.add_hotkey('ctrl+m', laugh_at_user)
    # Note: using add_hotkey does not seem to work. try something else!
    '''

# Attempt at blocking 'X' button. Not fully working.
def block_closing_of_terminal_window():
    hwnd = win32console.GetConsoleWindow()
    if hwnd:
        hMenu = win32gui.GetSystemMenu(hwnd, 0)
        print("11")
        win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
        print("22")
    
    # Inform tester
    print("Try closing this window. It should be blocked! (You can end the test by pressing Ctrl+C)")
    # keep window open while testing
    while True:
        pass
        time.sleep(1)

# Laughs at user :)
def laugh_at_user():
    print("Haha, you thought you could close the window? Nice try! 😆")

# Waits forever to allow testing of programs
def wait_forever():
    while True:
        time.sleep(1)