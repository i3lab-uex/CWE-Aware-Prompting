# -*- coding: utf-8 -*-
"""
Safe command validation module.

This module provides a helper function `run_command_if_safe` that checks
whether a user-supplied command is present in the predefined set of
allowed commands.  If the command is permitted, it is returned unchanged;
otherwise `None` is returned.

The function performs strict string comparison and normalises whitespace
to avoid accidental matching of malicious input that could exploit
CWE‑74 injection vulnerabilities.
"""

# --------------------------------------------------------------------------- #
# 1. Configuration: Define the set of allowed commands
# --------------------------------------------------------------------------- #

ALLOWED_COMMANDS = {
    "list",          # Example command: list files
    "status",        # Example command: show status
    "restart",       # Example command: restart service
    "shutdown",      # Example command: shutdown system
}

# --------------------------------------------------------------------------- #
# 2. Helper function: Validate user input against allowed commands
# --------------------------------------------------------------------------- #

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-supplied command against the set of allowed commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is present in ``ALLOWED_COMMANDS``;
        otherwise, ``None``.

    Notes
    -----
    * The comparison is case-sensitive and requires an exact match.
    * Leading/trailing whitespace is stripped to prevent accidental
      mismatches due to formatting.
    """
    if not isinstance(user_command, str):
        # Reject non-string inputs early
        return None

    # Normalise whitespace: strip leading/trailing spaces and collapse internal
    # multiple spaces to a single space. This helps avoid injection via
    # whitespace manipulation.
    normalized = " ".join(user_command.strip().split())

    return normalized if normalized in ALLOWED_COMMANDS else None

# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid accidental execution)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     cmd = input("Enter command: ")
#     safe_cmd = run_command_if_safe(cmd)
#     if safe_cmd is None:
#         print("Command not authorized.")
#     else:
#         print(f"Executing safe command: {safe_cmd}")