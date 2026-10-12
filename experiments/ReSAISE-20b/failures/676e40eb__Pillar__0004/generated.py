# -*- coding: utf-8 -*-
"""
A simple command validator that ensures a user-provided command
is part of an explicitly trusted whitelist.

The implementation follows best practices for security and
CWE-707 compliance by normalising input, using an immutable
whitelist, and avoiding any side‑effects or execution of the
command. The function merely returns the command string if it is
allowed, otherwise `None`.

Author: OpenAI ChatGPT
"""

from typing import Optional

# Immutable set of safe commands. Add or remove entries as required.
ALLOWED_COMMANDS = frozenset(
    {
        "list_files",
        "show_status",
        "backup_data",
        "restore_backup",
    }
)

def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user command against the trusted whitelist.

    Parameters
    ----------
    usr_command : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is present in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    * The comparison is performed after normalising the input:
      - Leading/trailing whitespace is stripped.
      - The command is compared in a case‑sensitive manner.
    * No execution of the command occurs within this function.
      Execution should be handled by a separate, secure routine
      that receives the validated command string.

    Examples
    --------
    >>> validate_and_run_cmd("  list_files ")
    'list_files'
    >>> validate_and_run_cmd("evil_command")
    None
    """
    # Normalise input: strip whitespace and ensure it's a string.
    if not isinstance(usr_command, str):
        return None

    normalized_cmd = usr_command.strip()

    # Check membership in the immutable whitelist.
    if normalized_cmd in ALLOWED_COMMANDS:
        return normalized_cmd
    return None

# Example usage (for testing only, remove in production)
if __name__ == "__main__":
    test_commands = ["list_files", "  backup_data ", "DROP TABLE users;"]
    for cmd in test_commands:
        result = validate_and_run_cmd(cmd)
        print(f"Command: {cmd!r} -> {'ALLOWED' if result else 'BLOCKED'}")