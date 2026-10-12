#!/usr/bin/env python3
"""
validate_and_run_cmd module

This module contains a single function that validates a user-supplied command
against a predefined whitelist of allowed commands.  If the command is present
in the whitelist, it is returned unchanged; otherwise, None is returned.

The function performs basic type checking and normalises the command string
by stripping surrounding whitespace before validation.
"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# Configuration:  List of safe commands.  Add or remove entries as needed.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS: _t.FrozenSet[str] = frozenset(
    {
        "ls",
        "pwd",
        "whoami",
        "date",
        "uptime",
    }
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def validate_and_run_cmd(usr_command: _t.Any) -> _t.Optional[str]:
    """
    Validate a user-provided command against the allowed list.

    Parameters
    ----------
    usr_command : Any
        The user input.  Only strings are considered valid.

    Returns
    -------
    Optional[str]
        The command string if it is present in ALLOWED_COMMANDS;
        otherwise, None.

    Notes
    -----
    * The function does **not** execute the command; it merely validates it.
    * Leading/trailing whitespace is stripped before validation.
    * The check is case-sensitive; adjust `ALLOWED_COMMANDS` accordingly
      if a different behaviour is desired.
    """
    # Basic type validation: only strings are acceptable
    if not isinstance(usr_command, str):
        return None

    # Normalise input: strip whitespace
    cmd = usr_command.strip()

    # Quick membership test using the frozenset for O(1) lookups
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # Not allowed: return None
    return None


# --------------------------------------------------------------------------- #
# Example usage (commented out; remove if you wish to run tests)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_commands = [" ls ", "rm -rf /", 123, None, "whoami"]
    for cmd in test_commands:
        result = validate_and_run_cmd(cmd)
        print(f"Input: {cmd!r} -> Output: {result!r}")