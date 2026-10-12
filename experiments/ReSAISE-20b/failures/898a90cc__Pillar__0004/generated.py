#!/usr/bin/env python3
"""
Utility to verify that a user-supplied command is within an allowed set.

The function does **not** execute the command; it merely validates it and
returns the sanitized command string if authorized, or `None` otherwise.
"""

from __future__ import annotations

# Example set of allowed commands. In real usage, populate this with
# only safe, non-privileged operations.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
}

def verify_and_run_command(cmd_input: str) -> str | None:
    """
    Validate a user-provided command against the allowed set.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        The sanitized command if it is in ALLOWED_COMMANDS,
        otherwise ``None`` to indicate an unauthorized request.

    Notes
    -----
    * Leading/trailing whitespace is stripped.
    * The comparison is case-sensitive; modify if you need a different policy.
    * No command execution takes place here – this function is purely
      for validation. Execution should be performed in a separate, secure
      routine that handles the validated command.
    """
    # Normalise input: strip whitespace to avoid accidental spaces
    normalized = cmd_input.strip()

    # Check membership in the allowed set
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # If not authorized, return None
    return None


# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    test_commands = ["list", " delete ", "shutdown", "unknown"]
    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        if result is None:
            print(f"Command '{cmd}' is not authorized.")
        else:
            print(f"Authorized command: {result}")