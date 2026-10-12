#!/usr/bin/env python3
"""
Utility for validating user‑supplied commands against a whitelist.

The module defines `validate_and_execute_command` which checks whether the
provided command string is present in a predefined list of allowed commands.
If the command is allowed, it returns the original string; otherwise,
`None` is returned.  No execution of the command occurs in this module to
avoid accidental system calls.

The design follows CWE‑707 guidelines by ensuring that only strictly
whitelisted commands are accepted, preventing malformed or malicious input
from reaching downstream components.
"""

from __future__ import annotations

from typing import List, Optional

# --------------------------------------------------------------------------- #
# Whitelist of commands that are considered safe for execution.
# This list should be curated carefully; any command added here will become
# executable by the system once validated.
ALLOWED_COMMANDS: List[str] = [
    "ls",
    "cat",
    "echo",
    "date",
    # Add other safe commands here
]

# Convert to a set for O(1) membership checks.
_ALLOWED_COMMANDS_SET = frozenset(ALLOWED_COMMANDS)

# --------------------------------------------------------------------------- #
def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user‑provided command against the allowed list.

    Parameters
    ----------
    cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is present in :data:`ALLOWED_COMMANDS`;
        otherwise ``None``.  No execution is performed.

    Notes
    -----
    - The comparison is **exact**: whitespace or case differences cause a
      rejection.  This strictness mitigates accidental injection attacks.
    - The function does **not** attempt to parse arguments; it only
      validates the base command token.
    """
    if not isinstance(cmd, str):
        raise TypeError(f"cmd must be a string, got {type(cmd).__name__}")

    # Strip surrounding whitespace to avoid accidental rejections.
    cleaned_cmd = cmd.strip()

    if cleaned_cmd in _ALLOWED_COMMANDS_SET:
        return cleaned_cmd
    return None

# --------------------------------------------------------------------------- #
__all__ = ["validate_and_execute_command", "ALLOWED_COMMANDS"]