#!/usr/bin/env python3
"""
Utility to validate user commands against a whitelist of trusted commands.
"""

from __future__ import annotations

# Whitelist of allowed command strings
ALLOWED_COMMANDS = {
    "list",
    "create",
    "delete",
    "update",
    "status",
}

def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate that the supplied command is in ALLOWED_COMMANDS.

    Parameters
    ----------
    command : str
        The user-provided command string.

    Returns
    -------
    str | None
        The original command if it is authorized, otherwise ``None``.

    Notes
    -----
    * Comparison is case-sensitive; adjust if a different policy is required.
    * No execution occurs in this function – it only performs authorization.
    """
    if not isinstance(command, str):
        return None

    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    return None