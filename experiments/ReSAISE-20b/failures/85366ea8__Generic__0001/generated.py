# -*- coding: utf-8 -*-
"""
Utility module for safely validating user commands.

The `check_and_execute_command` function checks whether a given command string
belongs to the set of allowed commands.  If it does, the original command is
returned; otherwise `None` is returned.

The module deliberately avoids executing commands directly.  If execution
is required, it should be performed in a separate, secure context after this
validation step.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# 1. Define the list of allowed commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = [
    "list_files",
    "show_date",
    "print_hello",
    # Add other safe commands here
]

# Convert to a set for O(1) membership checks and to avoid accidental duplicates.
_ALLOWED_COMMANDS_SET = frozenset(ALLOWED_COMMANDS)


# --------------------------------------------------------------------------- #
# 2. Validation function
# --------------------------------------------------------------------------- #

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user-issued command against the allowed list.

    Parameters
    ----------
    usr_cmd : str
        The raw command string supplied by the user.

    Returns
    -------
    str | None
        * The original command string if it is in :data:`ALLOWED_COMMANDS`.
        * ``None`` otherwise.

    Notes
    -----
    The function performs a case‑sensitive comparison.  It does **not** execute
    the command; it merely signals whether execution is permitted.

    Example
    -------
    >>> check_and_execute_command("list_files")
    'list_files'
    >>> check_and_execute_command("rm -rf /") is None
    True
    """
    if not isinstance(usr_cmd, str):
        raise TypeError("Command must be a string")

    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cmd = usr_cmd.strip()

    if cmd in _ALLOWED_COMMANDS_SET:
        return cmd
    return None


# --------------------------------------------------------------------------- #
# 3. Example usage (commented out)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Demo: validate a command entered via the console
    user_input = input("Enter command: ")
    validated_cmd = check_and_execute_command(user_input)
    if validated_cmd:
        print(f"Command '{validated_cmd}' is allowed.")
        # Here you could safely call the corresponding function.
    else:
        print("Invalid command. No action taken.")