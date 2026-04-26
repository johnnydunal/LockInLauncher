'''
This module manages the blocking of certain websites by modifying the hosts file.
'''

# todo: add a function to block websites by adding them as an entry to the hosts file

from src.config import load_config

# List of websites to block, loaded from the .config file
project_info = load_config()
# blocked_sites = project_info["blocked_sites"]