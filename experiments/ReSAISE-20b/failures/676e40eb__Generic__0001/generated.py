#!/usr/bin/env python3
"""
validate_and_run_cmd module

This module contains a single function, `validate_and_run_cmd`, which checks
whether a user supplied command is present in the list of trusted commands.
If it is, the command string is returned; otherwise None is returned.

The list of allowed commands is defined as a set for O(1) membership checks.
"""

from typing import Optional

# Define the trusted commands.  In a real application this list might be
# read from a configuration file or environment variable.
ALLOWED_COMMANDS = {
    "ls",
    "cat",
    "echo",
    "date",
    "uptime",
    # Add additional safe commands here
}

def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user supplied command against the ALLOWED_COMMANDS set.

    Parameters
    ----------
    usr_command : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS; otherwise None.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned_cmd = usr_command.strip()

    # Check if the cleaned command is in the set of allowed commands.
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd
    else:
        # Optionally, log the attempt here.
        return None

# Example usage
if __name__ == "__main__":
    # Simulate user input
    cmd = input("Enter command: ")
    result = validate_and_run_cmd(cmd)
    if result:
        print(f"Command '{result}' is allowed.")
        # Here you would execute the command safely, e.g., via subprocess
    else:
        print("Command not allowed.")