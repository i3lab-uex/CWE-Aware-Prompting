#!/usr/bin/env python3
"""
Module: command_verifier

This module provides a single function `verify_and_run_command` that
ensures a user-provided command is within an allowed set before it
is considered for execution.  The function does **not** execute the
command; it simply validates and returns the command string if it is
safe, or `None` otherwise.

The implementation follows best practices to mitigate CWE‑707
(Improper Neutralization of Structured Data) by:
* Normalising the input (trimming whitespace).
* Performing an exact membership test against a predefined
  immutable set of allowed commands.
* Rejecting any input that contains characters that could be used for
  shell injection or other unintended behaviour.
"""

from __future__ import annotations

import re
from typing import Optional, Set

# ----------------------------------------------------------------------
# Configuration: Allowed commands.
# ----------------------------------------------------------------------
# Using a frozenset makes the collection immutable and hashable,
# which helps prevent accidental modification at runtime.
ALLOWED_COMMANDS: Set[str] = frozenset(
    {
        "list_files",
        "show_date",
        "ping_google",
        "echo_hello",
    }
)

# ----------------------------------------------------------------------
# Helper: Regular expression to detect suspicious characters.
# ----------------------------------------------------------------------
# We allow only alphanumeric characters and underscores.  Any
# character outside this set will cause the command to be rejected.
_SAFETY_REGEX = re.compile(r"^[A-Za-z0-9_]+$")

# ----------------------------------------------------------------------
def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate that the supplied command is in the allowed list and
    conforms to a safe pattern.

    Parameters
    ----------
    command : str
        The raw user input representing the desired command.

    Returns
    -------
    Optional[str]
        The normalized command string if it is allowed and safe,
        otherwise `None`.

    Notes
    -----
    * The function performs no side effects beyond validation.
    * If the command passes validation, it can be passed to an
      execution routine elsewhere in the application.
    """
    if not isinstance(command, str):
        # Non-string inputs are automatically rejected
        return None

    # Normalise: strip leading/trailing whitespace
    normalized = command.strip()

    if not normalized:
        # Empty string after stripping is invalid
        return None

    # Check for prohibited characters that might lead to injection.
    if not _SAFETY_REGEX.match(normalized):
        return None

    # Perform the membership test against the immutable set.
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Command not recognized
    return None


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Simple demonstration of usage
    test_commands = [
        "list_files",
        " list_files ",
        "delete_all",   # disallowed
        "echo_hello",
        "echo$HOME",    # contains unsafe character
    ]

    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        if result is not None:
            print(f"✅ Allowed: {result}")
        else:
            print(f"❌ Disallowed or unsafe: {cmd!r}")