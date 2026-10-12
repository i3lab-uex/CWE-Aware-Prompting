# -*- coding: utf-8 -*-

"""
Utility module for validating user commands against a whitelist.

The function :func:`check_and_execute_command` ensures that only
commands from the predefined ``ALLOWED_COMMANDS`` set are accepted.
It performs an exact match check, which mitigates injection risks
(CWE-74) by preventing any malformed or partially matching input from
being treated as a valid command.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed commands
# --------------------------------------------------------------------------- #

# A tuple is immutable; converting it to a set gives O(1) membership checks.
ALLOWED_COMMANDS = (
    "start",
    "stop",
    "restart",
    "status",
    "reload",
)

# Convert to a set once at import time for efficient lookups.
_ALLOWED_COMMANDS_SET = frozenset(ALLOWED_COMMANDS)


# --------------------------------------------------------------------------- #
# 2. Core function
# --------------------------------------------------------------------------- #

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user-supplied command against the whitelist.

    Parameters
    ----------
    usr_cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The validated command if it is in :data:`ALLOWED_COMMANDS`;
        otherwise ``None``.

    Notes
    -----
    - The comparison is case-sensitive; adjust if a different policy is needed.
    - No execution logic is included here – the caller should handle
      running the command after validation.
    - This function protects against injection by rejecting any input that
      does not match an allowed command exactly, thus preventing partial
      or malformed commands from being interpreted downstream.
    """
    # Trim whitespace to avoid accidental spaces causing a mismatch.
    command = usr_cmd.strip()

    # Perform an exact membership test against the whitelist.
    if command in _ALLOWED_COMMANDS_SET:
        return command

    # If the command is not allowed, return None.
    return None


# --------------------------------------------------------------------------- #
# 3. Example usage (for testing purposes)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple test harness
    import sys

    if len(sys.argv) != 2:
        print("Usage: python check_command.py <command>")
        sys.exit(1)

    user_input = sys.argv[1]
    validated = check_and_execute_command(user_input)
    if validated is None:
        print(f"Command '{user_input}' is not allowed.")
    else:
        print(f"Validated command: {validated}")