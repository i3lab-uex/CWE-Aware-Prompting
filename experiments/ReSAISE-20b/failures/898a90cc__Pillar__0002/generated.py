#!/usr/bin/env python3
"""
verify_and_run_command.py

This module provides a secure command verification function that ensures only
predefined safe commands are accepted. It guards against CWE-707 by validating
the structure of the command before any downstream processing.

Author: ChatGPT
"""

from typing import Optional, Set

# Define the set of allowed commands. Extend this list as needed.
ALLOWED_COMMANDS: Set[str] = {
    "START",
    "STOP",
    "RESTART",
    "STATUS",
    # Add other safe commands here
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the allowed set.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The validated command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The comparison is case-sensitive and whitespace-trimmed.
    - No command execution occurs in this function; it only verifies
      the command's legitimacy.  Execution should be handled elsewhere.
    """
    if not isinstance(cmd_input, str):
        # Reject non-string inputs outright
        return None

    # Normalize input: strip leading/trailing whitespace
    cmd_clean = cmd_input.strip()

    if cmd_clean in ALLOWED_COMMANDS:
        return cmd_clean

    # Command not authorized
    return None


# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     user_cmd = input("Enter command: ")
#     validated = verify_and_run_command(user_cmd)
#     if validated:
#         print(f"Executing command: {validated}")
#     else:
#         print("Unauthorized or malformed command.")