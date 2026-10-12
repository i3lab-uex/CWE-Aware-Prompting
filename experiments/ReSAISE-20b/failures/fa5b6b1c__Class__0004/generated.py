# -*- coding: utf-8 -*-
"""
Secure command authorization module.

The function `authorize_and_run_cmd` checks whether a user-supplied command
belongs to a predefined set of trusted commands (`ALLOWED_COMMANDS`).  If the
command is authorized, it is returned unchanged; otherwise `None` is returned.
"""

from typing import Optional

# Define a set of safe, allowed commands.  This should be populated with the
# actual commands that are considered secure for your environment.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart_service",
    "shutdown",
    # Add more safe commands here.
}

def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user-provided command against the allowed list.

    Parameters
    ----------
    command : str
        The command string supplied by a user.

    Returns
    -------
    Optional[str]
        The original command if it is in `ALLOWED_COMMANDS`; otherwise None.
    """
    # Normalise input: strip whitespace and lower-case for case-insensitive match
    # (adjust as needed for your use case).
    cmd_normalized = command.strip().lower()

    if cmd_normalized in ALLOWED_COMMANDS:
        # Command is authorized; return the original string (not the normalized form)
        # to preserve any required case or formatting.
        return command
    return None