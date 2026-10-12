# -*- coding: utf-8 -*-
"""
Utility for validating user supplied commands against a whitelist.
"""

from typing import Optional

# Example list of allowed commands. In production, load this from a secure config file.
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "date",
    "uptime",
]

def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user-provided command against the allowed commands list.

    Parameters
    ----------
    cmd : str
        The user supplied command string. It is expected to be a simple
        command name without arguments, as this function only checks the
        presence of the command in ``ALLOWED_COMMANDS``.

    Returns
    -------
    Optional[str]
        The original command if it is in ``ALLOWED_COMMANDS``; otherwise
        ``None``.

    Notes
    -----
    * This function performs no argument parsing or sanitisation; it only
      verifies that the command name itself is allowed.
    * In a real-world scenario, you would also want to restrict the
      execution environment (e.g., using a chroot jail, setuid drop,
      or containers) to mitigate any potential security risk from
      executing system commands.
    """
    # Normalise the command: strip whitespace and convert to lowercase
    # (if you want case-insensitive matching). Adjust as needed.
    cmd_clean = cmd.strip()

    if cmd_clean in ALLOWED_COMMANDS:
        return cmd_clean

    # If the command is not allowed, we do not execute it.
    return None