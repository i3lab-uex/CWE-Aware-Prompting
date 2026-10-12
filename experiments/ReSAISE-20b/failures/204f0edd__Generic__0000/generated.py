# safe_command.py

"""
Utility module for validating user-supplied commands against a whitelist.

The function `check_and_run_command` checks if the supplied command is
present in the globally defined ALLOWED_COMMANDS set. If it is, the command
is returned unchanged; otherwise, None is returned to indicate that the
command is not authorized.

This implementation focuses on security by ensuring only explicitly allowed
commands can be executed and avoids any dynamic code execution or shell
injection vulnerabilities.
"""

from typing import Optional

# Define the set of commands that are considered safe.  In a real application
# this list should be populated with the exact commands you intend to allow.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
}

def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the whitelist.

    Parameters
    ----------
    command : str
        The user-inputted command to validate.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The comparison is case-sensitive; adjust the logic if a case-insensitive
      check is desired.
    - No side effects (such as executing the command) occur in this function;
      it merely validates and returns the command.  Execution should be
      handled elsewhere with proper security controls.
    """
    # Strip whitespace to avoid accidental rejections of commands like " list "
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # If the command is not authorized, do not return it.
    return None