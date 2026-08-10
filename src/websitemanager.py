'''
This module manages the blocking of certain websites by modifying the system hosts file.

Notes:
- Entries added in the hosts file are marked with "# LockInLauncher Blocked Website"
- On Windows the hosts file is usually at 'C:\Windows\System32\drivers\etc\hosts'.
- Modifying the hosts file requires administrator privileges; operations will raise an error if run without them.
'''

from __future__ import annotations

import os
import shutil
import ctypes
from typing import List, Optional

from rich import print

from src.config import load_config

# Hosts file path (Windows by default, Unix fallback)
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

# Markers used to delimit the block section added by this app
MARKER_START = '# LockInLauncher blocked sites start'
MARKER_END = '# LockInLauncher blocked sites end'

BACKUP_SUFFIX = '.lockin.bak'


# Return list containing blocked sites
def _get_blocked_sites_from_config():
    config = load_config()
    if not config:
        return []
    return config.get('blocked_sites')


# Return content of the hosts file
def _read_hosts():
    if not os.path.exists(HOSTS_PATH):
        raise FileNotFoundError(f"Hosts file not found: {HOSTS_PATH}")
    with open(HOSTS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


# Write content to the hosts file
def _write_hosts(content):
    # This will raise PermissionError if not run with sufficient privileges
    with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


def _split_block_section(content):
    if MARKER_START in content and MARKER_END in content:
        start = content.index(MARKER_START)
        end = content.index(MARKER_END, start) + len(MARKER_END)
        pre = content[:start]
        block = content[start:end]
        post = content[end:]
        return pre, block, post
    return content, '', ''


# Returns whether the program has admin rights (necessary for modifying the hosts file)
def _check_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0


# Copy the current hosts file to a backup and return its path.
def backup_hosts():
    dst = HOSTS_PATH + BACKUP_SUFFIX
    shutil.copy2(HOSTS_PATH, dst)
    return dst


# Restore the hosts file from the given backup (or the default backup)
def restore_backup(backup_path=None):
    if backup_path is None:
        backup_path = HOSTS_PATH + BACKUP_SUFFIX
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup not found: {backup_path}")
    shutil.copy2(backup_path, HOSTS_PATH)


def apply_blocked_sites(sites: Optional[List[str]] = None):
    """Write the blocked sites section into the hosts file.

    If `sites` is None, the list is loaded from the project config
    (`load_config()['blocked_sites']`). Passing an empty list will remove
    any existing LockInLauncher-managed section.
    """
    if sites is None:
        sites = _get_blocked_sites_from_config()

    content = _read_hosts()
    pre, block, post = _split_block_section(content)

    # If no sites provided, remove existing block section (if any)
    if not sites:
        if block:
            new_content = pre + post.lstrip('\n')
            _write_hosts(new_content)
            print('[green]Removed LockInLauncher block section from hosts file.[/green]')
        else:
            print('[dim]No LockInLauncher block section present; nothing to do.[/dim]')
        return

    # Build block content
    entries: List[str] = []
    for site in sites:
        host = site.lower()
        # avoid duplicates in the provided list
        if not host:
            continue
        # Add per-entry comment to make each line identifiable
        entries.append(f'127.0.0.1 {host} # LockInLauncher Website Blocker')
        if not host.startswith('www.'):
            entries.append(f'127.0.0.1 www.{host} # LockInLauncher Website Blocker')

    block_lines = '\n'.join([MARKER_START] + entries + [MARKER_END])

    # Compose new hosts content
    new_content = pre
    if not new_content.endswith('\n'):
        new_content += '\n'
    new_content += block_lines + '\n' + post.lstrip('\n')

    # Backup current hosts then write new content
    try:
        backup_hosts()
    except PermissionError:
        # Let the write raise a more explicit PermissionError below
        pass

    try:
        _write_hosts(new_content)
    except PermissionError as e:
        raise PermissionError('Writing hosts file failed: run as Administrator') from e

    print(f'[green]Wrote {len(entries)} blocked host entries to hosts file.[/green]')


def remove_block_section() -> None:
    """Remove the LockInLauncher-managed section from the hosts file."""
    content = _read_hosts()
    pre, block, post = _split_block_section(content)
    if not block:
        print('[dim]No LockInLauncher block section present; nothing to remove.[/dim]')
        return
    new_content = pre + post.lstrip('\n')
    _write_hosts(new_content)
    print('[green]Removed LockInLauncher block section from hosts file.[/green]')


__all__ = [
    'apply_blocked_sites',
    'remove_block_section',
    'backup_hosts',
    'restore_backup',
]