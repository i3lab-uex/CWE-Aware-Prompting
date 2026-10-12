# verify_and_run_command.py

"""
This module provides a secure way to validate user‑supplied commands against
a predefined whitelist of allowed commands. The function `verify_and_run_command`
ensures that only exact matches are accepted, preventing injection
(CWE‑74) by avoiding any string interpolation or execution of untrusted input.
"""

from typing import List, Optional

# --------------------------------------------------------------------------- #
# 1. Whitelist of commands that are safe to run
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS: List[str] = [
    "list_users",
    "backup_database",
    "refresh_cache",
    "shutdown_service",
]

# --------------------------------------------------------------------------- #
# 2. Validation function
# --------------------------------------------------------------------------- #

def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate the supplied command against a whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The raw user input representing a command name.

    Returns
    -------
    Optional[str]
        The validated command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    * The comparison is a strict equality check; no partial matches or
      case‑insensitive matching are performed.
    * No further processing (e.g., string interpolation or shell execution)
      is done here. The caller should handle actual execution in a
      controlled environment.
    """
    # Strip surrounding whitespace to avoid accidental mismatches due to user input formatting
    cleaned_command = command.strip()

    # Check for an exact match in the whitelist
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command

    # If not allowed, return None
    return None


# --------------------------------------------------------------------------- #
# 3. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     user_input = input("Enter command: ")
#     result = verify_and_run_command(user_input)
#     if result:
#         print(f"Command '{result}' is allowed and can be executed.")
#     else:
#         print("Invalid command. Access denied.")