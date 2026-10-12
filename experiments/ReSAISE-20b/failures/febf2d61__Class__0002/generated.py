# -*- coding: utf-8 -*-

"""
Utility to validate user‑supplied commands against a whitelist.

The function `verify_and_run_command` checks whether the supplied command
is present in the predefined list `ALLOWED_COMMANDS`.  It returns the
command string if it is allowed, otherwise it returns `None`.

The implementation deliberately does **not** execute the command; callers
must decide how to handle a valid command.  This avoids potential
injection vulnerabilities (CWE‑74) by never concatenating or interpreting
the command string in any downstream component.
"""

from typing import Optional, List

# Define the whitelist of allowed commands.
ALLOWED_COMMANDS: List[str] = [
    "status",
    "restart",
    "update",
    "backup",
    "shutdown",
]

def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the whitelist.

    Parameters
    ----------
    command : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in `ALLOWED_COMMANDS`,
        otherwise None.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # If the command is not allowed, silently reject it.
    return None