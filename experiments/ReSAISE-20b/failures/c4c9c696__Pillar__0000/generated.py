# SPDX-License-Identifier: MIT

"""
Utility to validate user commands against a whitelist of allowed commands.

The function `check_and_run_command` accepts a string representing a user-provided
command.  It returns the command unchanged if it is present in the
`ALLOWED_COMMANDS` set; otherwise, it returns `None`.

The implementation performs basic type checking and uses a set for O(1)
lookup.  No command execution is performed in this module, preventing
CWE‑707 related risks of improperly neutralized structured data.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of commands considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "help",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate a user-provided command against the whitelist.

    Parameters
    ----------
    user_input : str
        The raw input string from the user.

    Returns
    -------
    str | None
        The original command if it is in `ALLOWED_COMMANDS`; otherwise,
        ``None``.
    """
    # Ensure the input is a string; reject other types to avoid surprises.
    if not isinstance(user_input, str):
        return None

    # Trim surrounding whitespace to avoid accidental mismatches.
    command = user_input.strip()

    # Perform a case-sensitive check against the allowed set.
    if command in ALLOWED_COMMANDS:
        return command

    # If not allowed, silently refuse by returning None.
    return None