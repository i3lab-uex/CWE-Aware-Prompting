# -*- coding: utf-8 -*-

"""
Utility module to validate user supplied commands against a whitelist of
safe commands.  The `run_command_if_safe` function simply checks whether
the command is in the ALLOWED_COMMANDS set and returns it if so, otherwise
returns None.
"""

from __future__ import annotations

# Define the set of safe commands.  In a real application this list would
# be read from configuration or environment variables and kept in sync with
# the actual commands that are allowed to run.
ALLOWED_COMMANDS = {
    "ls",
    "pwd",
    "cat",
    "echo",
    "date",
    # Add more safe commands here as needed
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user supplied command against the whitelist of safe commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    * The function performs a case-sensitive comparison.
    * Only the command name is checked; arguments are not validated.
      If argument validation is required, this function should be
      extended accordingly.

    Examples
    --------
    >>> run_command_if_safe("ls")
    'ls'
    >>> run_command_if_safe("rm -rf /")
    None
    """
    # Strip leading/trailing whitespace and split on spaces to isolate the command name.
    command_name = user_command.strip().split()[0] if user_command else ""

    # Return the original command only if it is whitelisted.
    return user_command if command_name in ALLOWED_COMMANDS else None