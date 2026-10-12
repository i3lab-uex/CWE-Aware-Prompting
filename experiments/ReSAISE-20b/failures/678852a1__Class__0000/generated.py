#!/usr/bin/env python3
"""
A simple command validator that ensures a user‑supplied command is in an allowed list.
The function returns the command string if it is permitted, otherwise None.
"""

from typing import Optional

# List of commands that are considered safe to run.
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "date",
    "uptime",
]

def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate the user‑provided command against a whitelist.

    Parameters
    ----------
    cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS; otherwise None.

    Notes
    -----
    - The comparison is performed after stripping leading/trailing whitespace.
    - No further parsing or escaping is done; the command must exactly match one of
      the allowed strings to be accepted. This mitigates injection risks (CWE‑74).
    """
    # Normalise whitespace
    cleaned_cmd = cmd.strip()

    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Command is not permitted
    return None