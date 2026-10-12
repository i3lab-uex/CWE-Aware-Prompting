#!/usr/bin/env python3
"""
Safe command validator.

This module defines a function that verifies whether a user-supplied command is
present in a whitelist of allowed commands.  If the command is authorized,
the original string is returned; otherwise, `None` is returned.

The implementation deliberately avoids side‑effects and uses a set for
O(1) membership checks.  No external libraries are required.
"""

from __future__ import annotations

from typing import Optional, Set

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #

#: A set of commands that are considered safe for execution.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "start",
    "stop",
    "restart",
    "status",
    # Add additional safe commands here
}

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the whitelist.

    Parameters
    ----------
    command : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in :data:`ALLOWED_COMMANDS`; otherwise
        ``None`` to indicate that the command is not authorized.

    Notes
    -----
    * The check is performed in constant time relative to the size of the
      whitelist (O(1)) because :class:`set` membership is hashed.
    * The function does **not** execute the command; it merely verifies
      its legitimacy.  Execution should be handled elsewhere.
    """
    # Normalise the command to avoid accidental mismatches due to whitespace
    cmd = command.strip()

    # Quick membership test; set lookup is O(1).
    if cmd in ALLOWED_COMMANDS:
        return cmd

    # Command not authorized
    return None


# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove to test manually)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python safe_command.py <command>")
        sys.exit(1)

    user_cmd = sys.argv[1]
    result = check_and_run_command(user_cmd)
    if result is None:
        print(f"Command '{user_cmd}' is not authorized.")
    else:
        print(f"Command '{result}' passed validation.")