# -*- coding: utf-8 -*-
"""
Utility module for validating user-provided commands against a whitelist.
"""

from typing import Optional, Iterable

# Define the set of allowed commands. Adjust this list to your application's needs.
ALLOWED_COMMANDS: frozenset[str] = frozenset(
    [
        "list",
        "create",
        "delete",
        "update",
        "status",
    ]
)


def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the ALLOWED_COMMANDS whitelist.

    Parameters
    ----------
    user_input : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is present in ALLOWED_COMMANDS;
        otherwise, None.

    Notes
    -----
    - The comparison is case-sensitive.  If a case-insensitive match is desired,
      normalise the input before checking.
    - No execution of commands occurs in this function; it merely validates
      the request.  The caller should handle execution separately.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned = user_input.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Command not allowed; returning None signals rejection
    return None


# Example usage (uncomment for quick test)
# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     result = check_and_run_command(cmd)
#     if result is None:
#         print("Command not allowed.")
#     else:
#         print(f"Executing command: {result}")