# -*- coding: utf-8 -*-
"""
Utility to validate user supplied commands against a whitelist.

The function simply checks that the provided command is present in
`ALLOWED_COMMANDS`.  No execution or string interpolation takes place,
preventing injection attacks (CWE‑74).
"""

from typing import Optional, Iterable

# Define a whitelist of safe commands.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "delete",
    "create",
    "update",
}

def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user command against the allowed set.

    Parameters
    ----------
    usr_command : str
        The raw user input command.

    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise, None.
    """
    # Normalise input: strip whitespace and collapse internal spaces
    command = " ".join(usr_command.strip().split())

    # Check membership in the whitelist
    if command in ALLOWED_COMMANDS:
        return command

    # Not allowed – reject silently
    return None