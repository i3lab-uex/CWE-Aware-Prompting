#!/usr/bin/env python3
"""
Utility to validate user-supplied commands against a whitelist.

The module defines `verify_and_run_command`, which checks if the
provided command string is present in a predefined set of safe
commands (`ALLOWED_COMMANDS`).  If the command is authorized, it
is returned unchanged; otherwise `None` is returned.

This function performs no execution itself – callers should use the
returned value to decide whether to run the command.  The design
avoids direct shell invocation, reducing the risk of injection attacks.
"""

from typing import Optional

# Define a set of safe commands that are allowed to be executed.
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "display_user_info",
    # Add other allowed commands here.
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the allowed commands list.

    Parameters
    ----------
    cmd_input : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The validated command string if it is in `ALLOWED_COMMANDS`;
        otherwise, None.

    Notes
    -----
    - The comparison is case-sensitive.  If a case-insensitive match is
      desired, convert `cmd_input` to the appropriate case before
      checking.
    - No attempt is made to execute the command; callers should use the
      returned value safely.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cmd_clean = cmd_input.strip()

    # Check membership in the allowed set.
    if cmd_clean in ALLOWED_COMMANDS:
        return cmd_clean

    # Command not authorized.
    return None


# Example usage (commented out to avoid accidental execution):
#
# if __name__ == "__main__":
#     user_cmd = input("Enter command: ")
#     validated_cmd = verify_and_run_command(user_cmd)
#     if validated_cmd is None:
#         print("Unauthorized command.")
#     else:
#         print(f"Executing safe command: {validated_cmd}")