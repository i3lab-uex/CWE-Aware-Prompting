#!/usr/bin/env python3
"""
Utility to validate user-provided commands against a whitelist.
"""

from typing import Optional, Iterable


# Define the list (or set) of allowed commands. Extend as needed.
ALLOWED_COMMANDS: Iterable[str] = [
    "list_files",
    "show_date",
    "display_memory_usage",
    "print_env",
    # Add more safe commands here
]

# Convert to a set for O(1) membership checks.
_ALLOWED_SET = set(ALLOWED_COMMANDS)


def check_and_run_command(user_input: str) -> Optional[str]:
    """
    Validate the user-provided command against a trusted whitelist.

    Parameters
    ----------
    user_input : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The validated command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    This function performs only a whitelist check. It does *not* execute the command.
    Execution should be handled by another part of the application that is guaranteed
    to run only trusted commands.
    """
    # Strip whitespace and normalize the command (e.g., case-sensitive or not)
    cmd = user_input.strip()

    # Basic sanity checks: non-empty and purely alphanumeric with underscores
    if not cmd or not cmd.replace("_", "").isalnum():
        return None

    # Check membership in the allowed set
    if cmd not in _ALLOWED_SET:
        return None

    # At this point the command is trusted
    return cmd


# Example usage (for testing purposes only):
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python validate.py <command>")
        sys.exit(1)

    user_cmd = sys.argv[1]
    validated = check_and_run_command(user_cmd)
    if validated:
        print(f"Command '{validated}' is allowed.")
    else:
        print(f"Command '{user_cmd}' is NOT allowed.")