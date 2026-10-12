# SPDX-License-Identifier: MIT
"""
Utility to validate user-supplied commands against a whitelist.

The module protects against command injection by rejecting any
command that is not explicitly listed in `ALLOWED_COMMANDS`.  No string
interpolation or concatenation of user input is performed, so there is
no risk of an attacker crafting a command that escapes the whitelist.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Define a set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "echo_hello",
    # Add more allowed commands here.
}

def check_and_run_command(command: str) -> str | None:
    """
    Validate a user-supplied command against the allowed set.

    Parameters
    ----------
    command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is authorized; otherwise, `None`.

    Notes
    -----
    - No attempt is made to execute the command.  The function simply
      performs a whitelist check.
    - Leading/trailing whitespace is stripped to avoid accidental
      mismatches.
    """
    # Normalise the command string: strip whitespace and convert to lower case
    # (if case-insensitivity is desired).  If case-sensitive matching is
    # required, comment out the lower() call.
    normalized = command.strip()

    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command not authorized
    return None