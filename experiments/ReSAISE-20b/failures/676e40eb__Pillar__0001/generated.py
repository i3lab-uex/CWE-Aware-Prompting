# -*- coding: utf-8 -*-

"""
Command validation module.

This module defines a safe command validator that checks user-provided
commands against a whitelist of allowed commands.  The function returns
the command string if it is present in the whitelist; otherwise,
it returns ``None``.  No execution of commands takes place, preventing
command injection attacks.

The implementation follows best practices for defensive programming,
including type checking and normalizing input before comparison.
"""

from __future__ import annotations

# Whitelist of commands considered safe for execution
ALLOWED_COMMANDS = {
    "list",
    "show",
    "delete",
    "create",
    "update",
    "status",
    # Add additional allowed commands here
}


def validate_and_run_cmd(usr_command: str) -> str | None:
    """
    Validate a user-provided command against the allowed commands list.

    Parameters
    ----------
    usr_command : str
        The raw command string input from the user.

    Returns
    -------
    str | None
        The validated command if it is in ``ALLOWED_COMMANDS``;
        otherwise, ``None``.

    Notes
    -----
    - The function performs a case-sensitive comparison.
      If case-insensitive matching is required, convert both sides
      to the same case before comparison.
    - No command execution occurs; this function only performs validation.
    """
    # Defensive type checking: ensure the input is a string
    if not isinstance(usr_command, str):
        raise TypeError(f"Expected a string for usr_command, got {type(usr_command).__name__}")

    # Strip surrounding whitespace to avoid accidental mismatches
    command_clean = usr_command.strip()

    # Quick membership test using a set for O(1) lookup
    if command_clean in ALLOWED_COMMANDS:
        return command_clean

    # Command not allowed
    return None