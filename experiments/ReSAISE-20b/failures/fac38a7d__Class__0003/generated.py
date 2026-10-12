#!/usr/bin/env python3
"""
Safe command checker.

This module defines a single function, `check_and_run_command`, that verifies
whether an input string is one of the permitted commands.  It returns the
command if it is allowed, otherwise `None`.  No execution of external code
is performed here – the caller can decide what to do with a valid command.

Security note:
    * The function performs an exact string comparison against a whitelist.
      No shell execution or string interpolation is performed, so it is
      safe from command injection (CWE‑74).
    * Leading/trailing whitespace is ignored to allow user-friendly input.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
}

# --------------------------------------------------------------------------- #
# 2. Main helper
# --------------------------------------------------------------------------- #

def check_and_run_command(command_input: str) -> str | None:
    """
    Validate a user-provided command against the allowed set.

    Parameters
    ----------
    command_input : str
        The raw input string from the user.  It may contain leading or trailing
        whitespace, which is ignored.

    Returns
    -------
    str | None
        The cleaned command string if it matches an allowed command;
        otherwise `None`.

    Raises
    ------
    TypeError
        If ``command_input`` is not a string.
    """
    if not isinstance(command_input, str):
        raise TypeError("command_input must be a string")

    # Strip whitespace to allow users to enter commands with accidental spaces.
    cleaned = command_input.strip()

    # Perform an exact match against the whitelist.  No partial or regex
    # matching is used to avoid accidental matches that could be abused.
    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None

# --------------------------------------------------------------------------- #
# 3. Example usage (not executed when imported)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Demo: read a command from stdin and print whether it is allowed.
    import sys

    user_input = sys.stdin.readline()
    result = check_and_run_command(user_input)
    if result:
        print(f"Allowed command: {result}")
    else:
        print("Command not allowed.")