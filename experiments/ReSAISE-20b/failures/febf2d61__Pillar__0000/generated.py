#!/usr/bin/env python3
"""
Utility to validate user‑issued commands against a whitelist.

The module defines `verify_and_run_command` which checks if the supplied
command string exists in the predefined list of allowed commands.
If it does, the command is returned unchanged; otherwise `None` is
returned.  No execution of external code occurs, mitigating the risk
of command injection or other security issues.

The implementation uses a set for O(1) look‑ups and normalises the
input by stripping surrounding whitespace to avoid accidental mismatches.
"""

from __future__ import annotations

from typing import Optional, Iterable


# Example whitelist of allowed commands.
ALLOWED_COMMANDS: set[str] = {
    "list",
    "show",
    "delete",
    "update",
    "create",
}


def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate the supplied command against ALLOWED_COMMANDS.

    Parameters
    ----------
    command : str
        The raw user input representing a command.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The check is case‑sensitive; commands must match exactly.
    - Leading/trailing whitespace is removed before validation to avoid
      accidental mismatches.
    """
    if not isinstance(command, str):
        # Non‑string input cannot be a valid command.
        return None

    cleaned = command.strip()
    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None


# If this module is executed as a script, demonstrate usage.
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python verify_and_run_command.py <command>")
        sys.exit(1)

    user_cmd = " ".join(sys.argv[1:])
    result = verify_and_run_command(user_cmd)
    if result is None:
        print(f"Command '{user_cmd}' is not allowed.")
    else:
        print(f"Executing allowed command: {result}")