# -*- coding: utf-8 -*-
"""
Utility to validate user supplied commands against a whitelist of trusted
commands.  The function returns the command if it is allowed, otherwise
`None`.

This module intentionally avoids executing any commands; it only performs a
safe membership test to prevent CWE-707 (improper neutralization) and other
injection attacks.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Whitelist of safe commands.  Adjust as necessary for your application.
# --------------------------------------------------------------------------- #
ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "help",
    "exit",
}

def check_and_run_command(user_input: str) -> str | None:
    """
    Validate a user-provided command against the whitelist of allowed commands.

    Parameters
    ----------
    user_input : str
        Raw command string supplied by the user.

    Returns
    -------
    str | None
        The sanitized command if it is in `ALLOWED_COMMANDS`; otherwise,
        ``None``.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    command = user_input.strip()

    # Ensure the input is a simple string without special characters that
    # could be interpreted by a shell or other downstream component.
    # For stricter validation, uncomment the following regex check:
    #
    # import re
    # if not re.fullmatch(r"[A-Za-z_]+", command):
    #     return None

    if command in ALLOWED_COMMANDS:
        return command
    return None


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_inputs = ["list", "   show  ", "rm -rf /", "exit"]
    for inp in test_inputs:
        result = check_and_run_command(inp)
        print(f"Input: {inp!r} -> Output: {result}")