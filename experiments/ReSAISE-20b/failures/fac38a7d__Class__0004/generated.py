# -*- coding: utf-8 -*-
"""
Utility module for safely validating user‑issued commands.

The function `check_and_run_command` verifies that a supplied command string
belongs to the predefined set of allowed commands.  It performs strict
equality comparison after normalising whitespace, which prevents command
injection (CWE‑74) by ensuring that no additional arguments or shell
metacharacters can be appended to a valid command.
"""

from __future__ import annotations

import re
from typing import Optional, Set

# --------------------------------------------------------------------------- #
# Configuration: allowed commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: Set[str] = {
    "status",
    "restart",
    "shutdown",
    "update",
    "backup",
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _normalize_command(cmd: str) -> str:
    """
    Normalise a command string by stripping leading/trailing whitespace
    and collapsing internal whitespace to a single space.

    Args:
        cmd: The raw command string from the user.

    Returns:
        A canonicalised version of the command suitable for comparison.
    """
    # Collapse any sequence of whitespace into a single space
    collapsed = re.sub(r"\s+", " ", cmd.strip())
    return collapsed.lower()  # case‑insensitive matching

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user‑supplied command against the allowed list.

    The function performs strict equality checks after normalisation.
    If the input matches an allowed command, the canonicalised command
    string is returned; otherwise None is returned.

    Args:
        command_input: Raw user input intended to be a command name.

    Returns:
        The canonicalised command string if it is allowed, otherwise None.
    """
    normalized = _normalize_command(command_input)

    # Use a set for O(1) membership checks
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command is not allowed – silently reject
    return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment for testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_commands = [
        "  status ",
        "RESTART",
        "shutdown; rm -rf /",      # malicious attempt
        "update now",              # invalid: extra argument
    ]

    for cmd in test_commands:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result}")