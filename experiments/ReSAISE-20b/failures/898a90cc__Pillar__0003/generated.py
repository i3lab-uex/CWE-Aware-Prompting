#!/usr/bin/env python3
"""
Safe command verification module.

This module defines a single public function, `verify_and_run_command`, which checks
whether a user-supplied command string is present in a predefined set of allowed
commands. If the command is permitted, it is returned unchanged; otherwise,
`None` is returned.

The implementation avoids any form of command execution or shell interpolation
to mitigate injection risks.  It also normalises the input by stripping leading
and trailing whitespace and collapsing internal sequences of whitespace to a
single space.  This ensures that variations in user formatting do not bypass the
check.

The module is intentionally lightweight and contains no external dependencies.
"""

from __future__ import annotations

import re
from typing import Optional, Set

# --------------------------------------------------------------------------- #
# Configuration:  Define the set of commands that are considered safe.
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: Set[str] = {
    "list",
    "help",
    "status",
    "restart",
    "shutdown",
    # Add more commands as needed
}

# --------------------------------------------------------------------------- #
# Utility:  Normalise command strings for consistent comparison.
# --------------------------------------------------------------------------- #

def _normalise(cmd: str) -> str:
    """
    Normalises a command string by stripping leading/trailing whitespace and
    collapsing internal whitespace sequences into a single space.

    Parameters:
        cmd (str): The raw command string from the user.

    Returns:
        str: A normalised version of the command suitable for comparison.
    """
    # Remove leading/trailing whitespace
    cmd = cmd.strip()
    # Collapse internal whitespace sequences to a single space
    return re.sub(r"\s+", " ", cmd)


# --------------------------------------------------------------------------- #
# Public API:  Command verification.
# --------------------------------------------------------------------------- #

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Verify that a user-supplied command is within the list of allowed commands.

    This function performs strict validation and does **not** execute the
    command.  It simply returns the normalised command string if it is
    authorised, or `None` otherwise.

    Parameters:
        cmd_input (str): The raw command string supplied by the user.

    Returns:
        Optional[str]: The normalised command if authorised; otherwise `None`.

    Security notes:
        - No external process execution is performed.
        - Input is normalised to avoid whitespace-based bypasses.
        - The comparison is case-sensitive; adjust as required.
    """
    # Normalise the input to ensure consistent matching
    cmd_normalised = _normalise(cmd_input)

    # Check if the normalised command is in the allowed set
    if cmd_normalised in ALLOWED_COMMANDS:
        return cmd_normalised

    # Command not authorised
    return None


# --------------------------------------------------------------------------- #
# Example usage (for local testing only; remove or guard under __main__ in real code).
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_commands = [
        "  list ",
        "help",
        "restart now",   # not allowed
        "shutdown",
        "invalid command",
    ]

    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Output: {result!r}")