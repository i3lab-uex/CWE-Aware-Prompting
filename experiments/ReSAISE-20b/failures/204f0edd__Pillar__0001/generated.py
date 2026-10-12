# -*- coding: utf-8 -*-

"""
Safe command validation module.

The function `check_and_run_command` ensures that a user-supplied command
matches one of the predefined safe commands in `ALLOWED_COMMANDS`.
If the command is not authorized, the function returns None.
"""

from typing import Optional

# Define a set of allowed commands (add or modify as needed)
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
    "help",
}

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the allowed commands list.

    Parameters
    ----------
    command : str
        The user-inputted command to be validated.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The comparison is case-sensitive. Adjust as required.
    - No side effects are performed; the function only validates and returns
      the command string. Execution of the command should be handled separately.
    """
    if command in ALLOWED_COMMANDS:
        return command
    return None