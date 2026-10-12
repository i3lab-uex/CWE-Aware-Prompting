# -*- coding: utf-8 -*-

"""
Utility module to validate user-provided commands against a whitelist.
"""

from typing import Optional, Iterable


# Define the list (or set) of commands that are allowed to run.
# Extend this with any other trusted commands as needed.
ALLOWED_COMMANDS: set[str] = {
    "list",
    "status",
    "restart",
    "update",
    "shutdown",
}


def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate the user-provided command against a predefined whitelist.

    Parameters
    ----------
    usr_command : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is present in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - This function performs a simple membership check and does *not*
      execute the command.  Execution logic should be implemented
      elsewhere, using this function only for validation.
    - The check is case-sensitive.  If case-insensitive matching
      is required, normalise the input and whitelist accordingly.
    """
    # Normalise whitespace to avoid accidental mismatches
    cleaned_command = usr_command.strip()

    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command
    else:
        return None


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_cmd = "restart"
    result = validate_and_run_cmd(test_cmd)
    if result:
        print(f"Command '{result}' is allowed.")
    else:
        print("Invalid command!")