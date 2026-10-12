# -*- coding: utf-8 -*-
"""
Utility to validate a user-provided command against an allowed list.

The function returns the command string if it is present in ALLOWED_COMMANDS,
otherwise it returns None. No execution of the command is performed here
to keep the function safe and pure.
"""

from typing import List, Optional

# Example allowed commands – in real usage this should be defined elsewhere
ALLOWED_COMMANDS: List[str] = [
    "list",
    "status",
    "help",
    "exit",
    # Add more safe commands here
]


def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user command against ALLOWED_COMMANDS.

    Parameters
    ----------
    command : str
        The raw input string from the user.

    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise None.
    """
    # Normalize the input: strip leading/trailing whitespace
    normalized = command.strip()

    # Reject empty commands immediately
    if not normalized:
        return None

    # Perform a case-sensitive match against the allowed list
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # If not found, return None
    return None