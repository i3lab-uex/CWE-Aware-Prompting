# -*- coding: utf-8 -*-

"""
Utility module for validating and executing user commands.

The `verify_and_run_command` function checks whether a given command string
belongs to the set of allowed commands.  If it does, the command is returned
so that the caller may execute it; otherwise `None` is returned.

This module deliberately does **not** execute the command itself to avoid
security risks.  The caller should handle execution in a controlled
environment.
"""

from __future__ import annotations

# Define the list of commands that are considered safe for the user to run.
ALLOWED_COMMANDS = [
    "list",
    "show",
    "status",
    "help",
    # Add other allowed commands here
]


def verify_and_run_command(command: str) -> str | None:
    """
    Verify that a user-provided command is in the list of allowed commands.

    Parameters
    ----------
    command : str
        The raw input string supplied by the user. Leading/trailing whitespace
        is stripped before validation.

    Returns
    -------
    str | None
        The trimmed command string if it is allowed; otherwise ``None``.
    """
    # Strip whitespace to avoid accidental mismatches due to surrounding spaces
    cleaned = command.strip()

    # Use a set for O(1) lookup if the list is large
    allowed_set = set(ALLOWED_COMMANDS)

    return cleaned if cleaned in allowed_set else None