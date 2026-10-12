# -*- coding: utf-8 -*-
"""
Utility module for validating user-provided commands against a whitelist.
The module is intentionally lightweight and avoids executing any code.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Whitelist of safe commands
# --------------------------------------------------------------------------- #

# Using a frozenset for immutability and O(1) membership checks
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        "list",
        "status",
        "restart",
        "shutdown",
        "help",
    }
)

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate a user-provided command against the allowed list.

    Parameters
    ----------
    user_input : str
        The raw input string from the user, e.g. `"  restart  "`.

    Returns
    -------
    str | None
        The trimmed command if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    * Leading/trailing whitespace is removed.
    * The check is case-sensitive; adjust `ALLOWED_COMMANDS` or add a
      normalisation step if you need case-insensitive matching.
    * No command is executed in this function – it merely validates the
      input.  Execution should be performed by a separate, carefully
      audited routine.
    """
    # Normalise input: strip whitespace and ensure a non-empty string
    cleaned = user_input.strip()
    if not cleaned:
        return None

    # Secure membership test
    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tests = ["restart", "  shutdown  ", "invalid", "", "help"]
    for cmd in tests:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result}")