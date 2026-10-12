# check_and_run_command.py

from __future__ import annotations
from typing import Optional, List


# Define the list of commands that are safe to execute.
ALLOWED_COMMANDS: List[str] = [
    "list_files",
    "show_date",
    "display_help",
    # Add more safe commands here as needed.
]


def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user-provided command against the allowed list.

    Parameters
    ----------
    command_input : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The comparison is case-sensitive and exact; no partial matching.
    - Leading/trailing whitespace is ignored to avoid accidental mismatches.
    """
    # Normalise input: strip whitespace but preserve internal structure
    cleaned_command = command_input.strip()

    # Check against the allowed commands list.
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command

    # Command is not permitted
    return None


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_commands = [
        " list_files ",
        "invalid_command",
        "SHOW_DATE",  # case-sensitive: will be rejected
    ]

    for cmd in test_commands:
        result = check_and_run_command(cmd)
        print(f"Input: {cmd!r} -> Result: {result}")