#!/usr/bin/env python3
"""
Utility for validating user-supplied commands against a whitelist of safe commands.
"""

from __future__ import annotations

# A set of commands that are considered safe for execution.
ALLOWED_COMMANDS = frozenset({
    "list",
    "create",
    "delete",
    "update",
    "status",
})

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-provided command against the ALLOWED_COMMANDS whitelist.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user. Leading/trailing whitespace is ignored.

    Returns
    -------
    str | None
        The trimmed command string if it is present in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    - The check is case-sensitive: only commands that match exactly are allowed.
    - No attempt is made to execute the command; this function merely performs validation.
    """
    if not isinstance(user_command, str):
        return None

    cleaned = user_command.strip()
    return cleaned if cleaned in ALLOWED_COMMANDS else None