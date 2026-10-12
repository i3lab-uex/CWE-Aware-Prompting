# -*- coding: utf-8 -*-
"""
Safe command validation module.

This module provides a single function, :func:`check_and_run_command`,
which verifies that a user-supplied command string is exactly one of the
predefined safe commands.  If the command is authorized it is returned;
otherwise ``None`` is returned.

The implementation performs a strict membership test against a
predefined set of allowed commands.  No string manipulation or pattern
matching is used, thereby preventing injection attacks such as those
described in CWE‑74.
"""

from __future__ import annotations

# Define the set of commands that are considered safe.  Add or remove
# entries as your application requires.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "help",
}

def check_and_run_command(command: str) -> str | None:
    """
    Validate a user-supplied command against the allowed set.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in :data:`ALLOWED_COMMANDS`;
        otherwise ``None``.
    """
    # Strip leading/trailing whitespace to avoid accidental rejections
    # due to formatting issues, but do not alter the command content.
    normalized = command.strip()

    # Perform a strict membership test.  This prevents any
    # injection of unexpected characters or patterns.
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command not authorized
    return None