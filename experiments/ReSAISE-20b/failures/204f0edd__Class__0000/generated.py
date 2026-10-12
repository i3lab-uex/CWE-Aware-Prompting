# -*- coding: utf-8 -*-
"""
Utility module for safely validating user‑supplied commands.

The function `check_and_run_command` verifies that a command string is
contained in the predefined set `ALLOWED_COMMANDS`.  If the command is
allowed it is returned unchanged; otherwise ``None`` is returned.
No execution or external side effects are performed.

This implementation guards against injection attacks by requiring an
exact match and rejecting any command that contains additional
characters or whitespace beyond the allowed tokens.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Configuration: a set of commands that are considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "START",
    "STOP",
    "RESTART",
    "STATUS",
    # Add more allowed commands here as needed.
}

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(command: str) -> str | None:
    """
    Validate a user‑supplied command against the list of allowed commands.

    Parameters
    ----------
    command : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise ``None``.

    Notes
    -----
    - Leading and trailing whitespace are stripped before validation.
    - The comparison is case‑sensitive; adjust the logic if a different
      behaviour is required.
    - No execution of the command occurs in this function; it merely
      performs validation.  Downstream code should handle execution
      after verifying the return value is not ``None``.
    """
    # Normalise input: strip whitespace but preserve internal characters
    normalized = command.strip()

    # Direct membership test against the safe set.
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # If not allowed, reject silently.
    return None