#!/usr/bin/env python3
"""
Secure command validation.

This module defines a set of safe commands and provides the function
`run_command_if_safe`, which checks whether a user-supplied command is in
that set.  If the command is allowed, it is returned unchanged; otherwise,
`None` is returned to indicate that execution should be blocked.

The implementation avoids any form of string interpolation or command
construction, thereby mitigating CWE-74 (injection) risks.
"""

from __future__ import annotations

import typing as _t

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {
        "start",
        "stop",
        "restart",
        "status",
        "update",
    }
)


def run_command_if_safe(user_command: str) -> _t.Optional[str]:
    """
    Validate a user-supplied command against the list of allowed commands.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is present in ``ALLOWED_COMMANDS``;
        otherwise, ``None``.

    Notes
    -----
    * The check is performed using an exact string match; no transformations
      (e.g., case folding, whitespace trimming) are applied.  This ensures that
      commands cannot be disguised by subtle variations.
    * The function does **not** execute the command.  It merely validates
      and returns it so that a downstream component can decide whether to
      run it safely.
    """
    # Direct membership test – O(1) lookup due to set/frozenset.
    if user_command in ALLOWED_COMMANDS:
        return user_command
    return None


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_commands = ["start", "delete", "STATUS", "restart"]
    for cmd in test_commands:
        result = run_command_if_safe(cmd)
        print(f"Command: {cmd!r} -> {'Allowed' if result else 'Rejected'}")