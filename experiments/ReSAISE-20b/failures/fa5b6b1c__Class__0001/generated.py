# -*- coding: utf-8 -*-

"""
Secure command authorization module.

This module defines a whitelist of safe commands and provides
a function to verify user‑supplied commands against that list.
The implementation avoids CWE‑74 by performing an exact match
and not interpolating or concatenating the command into a larger
string that could be interpreted by downstream components.
"""

from typing import Iterable, Optional

# Define the set of commands that are considered safe for execution.
ALLOWED_COMMANDS: set[str] = {
    "list",
    "status",
    "restart",
    "shutdown",
    # Add more allowed commands here
}


def authorize_and_run_cmd(command: str) -> Optional[str]:
    """
    Validate a user supplied command against the whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    - The check is performed using an exact string match. No leading/trailing
      whitespace or case normalization is applied; callers should provide the
      command in its canonical form.
    - No attempt is made to parse or execute the command here; this function
      only authorizes it. Execution should be performed by a separate,
      well‑controlled component that receives the returned string.
    """
    # Ensure command is a string to avoid type errors.
    if not isinstance(command, str):
        return None

    # Exact match against the whitelist; set lookup is O(1).
    if command in ALLOWED_COMMANDS:
        return command

    # If not allowed, do not expose any information about the whitelist.
    return None