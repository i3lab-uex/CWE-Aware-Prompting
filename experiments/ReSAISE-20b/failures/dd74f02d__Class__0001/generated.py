# -*- coding: utf-8 -*-
"""
Utility to validate user-supplied commands against a whitelist of safe commands.

The module deliberately does **not** execute the command; it only performs validation.
Execution should be handled elsewhere, after this function has confirmed that the
command is allowed.

CWE-74 (Injection) Mitigation:
  - The function strictly compares the entire command string against a
    predefined set of allowed commands.
  - No user input is interpolated into command templates or shell strings
    without prior validation, eliminating the risk of injection.
"""

from __future__ import annotations

import typing as _t

# Define a set of commands that are considered safe.
ALLOWED_COMMANDS: _t.Set[str] = {
    "list",
    "show",
    "status",
    "restart",
    "shutdown",
}

def run_command_if_safe(user_command: str) -> _t.Optional[str]:
    """
    Validate a user-supplied command against the allowed set.

    Parameters
    ----------
    user_command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original `user_command` if it is exactly one of the allowed
        commands; otherwise, ``None``.
    """
    # Strip surrounding whitespace to avoid accidental mismatches due to
    # formatting issues.  Leading/trailing spaces are not considered part of
    # the command itself.
    cleaned = user_command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None

# Example usage (for illustration only; remove or guard with `if __name__ == "__main__":`
# if you plan to run this module directly).
if __name__ == "__main__":
    test_commands = ["list", "delete ", "  status", "invalid"]
    for cmd in test_commands:
        result = run_command_if_safe(cmd)
        print(f"Command: {cmd!r} -> {'ALLOWED' if result else 'REJECTED'}")