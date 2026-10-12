# -*- coding: utf-8 -*-
"""
A simple command validation module.

The function `check_and_run_command` ensures that a user-provided command
belongs to a predefined whitelist (`ALLOWED_COMMANDS`). If the command is
allowed, it is returned unchanged; otherwise `None` is returned.
"""

from __future__ import annotations

# Whitelist of trusted commands.  Extend this list as needed.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "deploy",
}

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate the user-provided command against a whitelist.

    Parameters
    ----------
    user_input : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise `None`.

    Notes
    -----
    - Leading and trailing whitespace are trimmed before validation.
    - The check is case-sensitive; adjust the logic if a different
      behaviour is required.
    """
    # Normalise whitespace: strip leading/trailing spaces and collapse internal
    # sequences of whitespace to a single space.  This mitigates accidental
    # injection via multiple spaces or newlines.
    command = " ".join(user_input.strip().split())

    # Perform a simple whitelist check
    if command in ALLOWED_COMMANDS:
        return command

    # Command not allowed – safe to return None
    return None