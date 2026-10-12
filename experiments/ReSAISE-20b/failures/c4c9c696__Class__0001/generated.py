#!/usr/bin/env python3
"""
Utility to validate and return a user‑supplied command.

The function ensures that the input matches exactly one of the
predefined safe commands.  It performs strict string comparison,
strips surrounding whitespace, and uses a set for efficient lookup.
"""

from __future__ import annotations

import re
from typing import Optional, Set


# --------------------------------------------------------------------------- #
# 1. Define the set of commands that are considered safe.
#    Add or remove entries as needed for your application.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS: Set[str] = {
    "start",
    "stop",
    "restart",
    "status",
    "backup",
    "restore",
}

# --------------------------------------------------------------------------- #
# 2. Regular expression for a valid command token
#    Allows only alphanumeric characters and underscores to prevent
#    injection of shell metacharacters or other unsafe tokens.
# --------------------------------------------------------------------------- #
_VALID_COMMAND_RE = re.compile(r"^[a-zA-Z0-9_]+$")


def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate the user‑supplied command against a trusted list.

    Parameters
    ----------
    user_input : str
        Raw input string from the user, possibly containing whitespace or
        malicious characters.

    Returns
    -------
    Optional[str]
        The sanitized command string if it is allowed; otherwise, ``None``.

    Notes
    -----
    * The function strips leading/trailing whitespace.
    * It rejects any command that contains characters outside the
      ``_VALID_COMMAND_RE`` pattern to mitigate injection risks.
    * No execution is performed; the caller must decide how to handle
      the returned command string.
    """
    # Normalise input: strip whitespace and collapse internal spaces
    cleaned = " ".join(user_input.strip().split())

    # Reject empty input early
    if not cleaned:
        return None

    # Ensure the command contains only safe characters
    if not _VALID_COMMAND_RE.match(cleaned):
        return None

    # Strict membership test against the allowed set
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Not permitted
    return None


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     for cmd in ["  start ", "stop;", "restart", "invalid_cmd"]:
#         result = check_and_run_command(cmd)
#         print(f"Input: {cmd!r} -> Result: {result!r}")