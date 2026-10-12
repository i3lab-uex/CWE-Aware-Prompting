#!/usr/bin/env python3
"""
Utility to validate user supplied commands against a whitelist of allowed
commands.  The function returns the command string only if it matches an
entry in ALLOWED_COMMANDS; otherwise it returns None.

The implementation avoids command injection by never concatenating user input
into shell commands.  It uses an immutable set for fast membership tests and
normalises the input before comparison.
"""

from __future__ import annotations

import re
from typing import Optional, Set

# --------------------------------------------------------------------------- #
# 1. Define the whitelist of safe commands.
#    The set should contain *exact* command strings that are allowed to run.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS: Set[str] = {
    "list_files",
    "show_status",
    "restart_service",
    "update_config",
    # Add more allowed commands here.
}

# --------------------------------------------------------------------------- #
# 2. Helper function: normalise user input
#    * Strip leading/trailing whitespace.
#    * Collapse internal whitespace to a single space (prevents hidden tricks).
# --------------------------------------------------------------------------- #
def _normalise_command(cmd: str) -> str:
    """
    Normalise a command string by stripping whitespace and collapsing
    consecutive spaces.  This reduces the risk of subtle injection vectors.
    """
    # Remove leading/trailing whitespace
    cmd = cmd.strip()
    # Collapse any sequence of whitespace characters into a single space
    cmd = re.sub(r"\s+", " ", cmd)
    return cmd

# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #
def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate the user-supplied command against a trusted whitelist.

    Parameters
    ----------
    user_input : str
        Raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The normalised command if it is in ALLOWED_COMMANDS, otherwise None.
    """
    # Normalise the input to avoid hidden whitespace tricks
    cmd = _normalise_command(user_input)

    # Quick rejection if the command is not in the whitelist
    if cmd not in ALLOWED_COMMANDS:
        return None

    # The command is safe; it can be passed to the downstream component
    return cmd


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_inputs = [
        "  list_files ",
        "show_status",
        "restart_service",
        "invalid_command",
        "list_files; rm -rf /",  # malicious attempt
    ]

    for inp in test_inputs:
        result = check_and_run_command(inp)
        if result is not None:
            print(f"Allowed command: {result}")
        else:
            print(f"Rejected input: {inp!r}")