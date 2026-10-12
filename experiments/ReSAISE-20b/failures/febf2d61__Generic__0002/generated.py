#!/usr/bin/env python3
"""
Utility module to validate and optionally execute user‑supplied commands.
The command is considered safe only if it matches one of the predefined
allowed strings in ALLOWED_COMMANDS.
"""

import subprocess
from typing import Optional

# ----------------------------------------------------------------------
# Configuration: define the set of commands that are permitted.
# In a real application this list would be read from a secure config file
# or environment variable rather than hard‑coded.
ALLOWED_COMMANDS = {
    "list-files",
    "show-date",
    "print-hello",
}

# ----------------------------------------------------------------------
def _map_command_to_shell(command: str) -> Optional[str]:
    """
    Translate a user‑friendly command into the actual shell command to run.
    If the command is not in ALLOWED_COMMANDS, return None.
    """
    mapping = {
        "list-files": "ls -l",
        "show-date": "date",
        "print-hello": 'echo "Hello, world!"',
    }
    return mapping.get(command)

# ----------------------------------------------------------------------
def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate the supplied command against ALLOWED_COMMANDS.
    
    Parameters
    ----------
    command : str
        The user‑supplied command string.

    Returns
    -------
    Optional[str]
        The original command if it is allowed, otherwise None.

    Raises
    ------
    ValueError
        If the command string is empty or contains only whitespace.
    
    Notes
    -----
    * The function does **not** execute the command; it merely checks for
      validity.  Execution can be performed separately using
      :func:`_map_command_to_shell` if desired.
    * Security: By limiting to a fixed mapping, we avoid command injection
      vulnerabilities that arise from directly interpolating user input into
      a shell.
    """
    # Basic sanity check: command must be non‑empty after stripping whitespace
    stripped = command.strip()
    if not stripped:
        raise ValueError("Command cannot be empty or whitespace only.")

    # Check against the allowed set (case‑sensitive by default)
    if stripped in ALLOWED_COMMANDS:
        return stripped

    # Command not allowed
    return None

# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage: attempt to run a command if it's allowed
    import sys

    try:
        user_cmd = sys.argv[1]
    except IndexError:
        print("Usage: python verify_and_run_command.py <command>")
        sys.exit(1)

    verified = verify_and_run_command(user_cmd)
    if verified is None:
        print(f"Command '{user_cmd}' is not allowed.")
        sys.exit(1)

    shell_cmd = _map_command_to_shell(verified)
    if shell_cmd is None:
        print(f"No mapping found for command '{verified}'.")
        sys.exit(1)

    # Execute the mapped shell command safely using subprocess
    result = subprocess.run(shell_cmd, shell=True, check=False,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True)
    print(result.stdout)