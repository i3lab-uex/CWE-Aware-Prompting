#!/usr/bin/env python3
"""
Secure command validator.

This module defines `check_and_run_command`, which ensures that a user-provided
command is part of a predefined whitelist (`ALLOWED_COMMANDS`). If the command
is allowed, it is returned unchanged; otherwise `None` is returned.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Configuration: define the safe commands here.                               #
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "echo_hello",
    "shutdown_system",  # example of a sensitive command that must be tightly controlled
}

# --------------------------------------------------------------------------- #
#  Function: check_and_run_command                                            #
# --------------------------------------------------------------------------- #

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate a user-provided command against the whitelist.

    Parameters
    ----------
    user_input : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in ``ALLOWED_COMMANDS``; otherwise
        ``None``.

    Notes
    -----
    * The function performs a case-sensitive membership check.
    * No execution of the command is performed here; callers should handle
      actual execution after validation.
    * Leading/trailing whitespace is stripped to avoid accidental mismatches.
    """
    # Normalise input: strip whitespace but preserve case
    cmd = user_input.strip()

    # Quick membership test using a set for O(1) lookups
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # Command not allowed; signal failure
    return None


# --------------------------------------------------------------------------- #
#  Example usage (for testing only)                                           #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python check_command.py <command>")
        sys.exit(1)

    cmd = sys.argv[1]
    result = check_and_run_command(cmd)
    if result is None:
        print(f"Command '{cmd}' is not allowed.")
    else:
        print(f"Command '{result}' is valid and can be executed.")