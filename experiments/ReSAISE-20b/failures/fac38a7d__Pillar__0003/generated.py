#!/usr/bin/env python3
"""
Secure command validation module.

This module provides a single function, `check_and_run_command`, which verifies
that a user‑supplied command is part of a pre‑approved whitelist.  If the
command is valid, it is returned unchanged; otherwise `None` is returned.
The function deliberately performs only a strict equality check against a
set of allowed commands, thereby preventing accidental or malicious execution
of unintended code.

CWE-707 Considerations:
    * The function ensures that the input is a well‑formed string before
      comparing it against the whitelist.
    * It does not interpret or parse the command, thus avoiding
      structure‑related vulnerabilities.
"""

from __future__ import annotations

import re
from typing import Optional, Set


# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed commands
#    NOTE: In a real application this list should be populated from a secure
#          configuration source or environment variable.  For demonstration
#          purposes we hard‑code a small sample list.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "delete",
    "create",
    "update",
}

# --------------------------------------------------------------------------- #
# 2. Helper: Normalise input
# --------------------------------------------------------------------------- #
def _normalise_command(command: str) -> str:
    """
    Normalise a command string for comparison.

    - Strips leading/trailing whitespace.
    - Collapses internal whitespace to a single space.
    - Leaves case unchanged (exact match is required).
    """
    # Collapse internal whitespace
    collapsed = re.sub(r"\s+", " ", command.strip())
    return collapsed


# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #
def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate that the supplied command is in the allowed whitelist.

    Parameters
    ----------
    command_input : str
        The raw user input representing a command.

    Returns
    -------
    Optional[str]
        The normalised command string if it is allowed; otherwise None.

    Raises
    ------
    TypeError
        If ``command_input`` is not a string.
    """
    if not isinstance(command_input, str):
        raise TypeError("command_input must be a string")

    normalised = _normalise_command(command_input)

    if normalised in ALLOWED_COMMANDS:
        return normalised
    else:
        return None


# --------------------------------------------------------------------------- #
# 4. Demo / test harness (executed only when run as a script)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_commands = [
        "  list ",
        "delete",
        "unknown",
        "create   new",  # not in whitelist
        "SHOW",          # case-sensitive mismatch
    ]

    for cmd in test_commands:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Output: {result!r}")