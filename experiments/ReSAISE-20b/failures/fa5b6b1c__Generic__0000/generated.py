# -*- coding: utf-8 -*-
"""
Utility module for safely authorizing user commands.
"""

from __future__ import annotations

# Define a set of allowed command strings.  The set allows O(1) membership checks.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "status",
    "restart",
    "shutdown",
}

def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate a user-provided command against the trusted list of commands.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in :data:`ALLOWED_COMMANDS`; otherwise ``None``.

    Notes
    -----
    - The comparison is case‑sensitive.  If you want to allow case‑insensitive
      matching, convert both the input and the allowed list entries to a common
      case (e.g., lowercasing) before comparison.
    - No command execution is performed here; the function merely authorizes
      the command.  The caller should handle actual execution.
    """
    # Basic sanity checks: ensure input is a string and not empty
    if not isinstance(command, str) or not command:
        return None

    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned = command.strip()

    return cleaned if cleaned in ALLOWED_COMMANDS else None