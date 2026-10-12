#!/usr/bin/env python3
"""
Utility to validate and optionally execute user commands against a whitelist.

The function `check_and_execute_command` checks if the supplied command is present
in the predefined set of allowed commands.  If it matches, the function returns
the command string; otherwise it returns None.

This implementation deliberately avoids any form of shell interpolation or
string concatenation that could lead to command injection.  The caller is
responsible for executing the returned command in a safe manner (e.g.,
via `subprocess.run` with an argument list).

Author: OpenAI
"""

from typing import Optional

# --------------------------------------------------------------------------- #
# 1. Define the whitelist of safe commands.
#    These should be exact command strings that are considered permissible.
ALLOWED_COMMANDS = {
    "ls",
    "pwd",
    "whoami",
    "date",
    "uptime",
    # Add more commands as needed
}

# --------------------------------------------------------------------------- #
def check_and_execute_command(usr_cmd: str) -> Optional[str]:
    """
    Validate the user-provided command against a whitelist.

    Parameters
    ----------
    usr_cmd : str
        The raw user input string representing a command.

    Returns
    -------
    Optional[str]
        The command string if it is allowed; otherwise None.

    Notes
    -----
    - Whitespace surrounding the command is stripped.
    - Only exact matches (case-sensitive) are accepted.
    - No further sanitization or shell interpolation is performed to avoid
      CWE-74 (command injection).
    """
    if not isinstance(usr_cmd, str):
        # Defensive: reject non-string inputs
        return None

    cleaned = usr_cmd.strip()
    if cleaned in ALLOWED_COMMANDS:
        return cleaned
    return None

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Demo usage
    user_input = input("Enter a command: ")
    cmd = check_and_execute_command(user_input)
    if cmd:
        print(f"Command '{cmd}' is allowed.")
        # Example safe execution (commented out for safety)
        # import subprocess
        # result = subprocess.run([cmd], capture_output=True, text=True)
        # print(result.stdout)
    else:
        print("Command not allowed.")