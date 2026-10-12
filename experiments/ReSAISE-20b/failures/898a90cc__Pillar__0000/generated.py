# -*- coding: utf-8 -*-
"""
Utility module to validate user-supplied commands against a whitelist.

The `verify_and_run_command` function checks whether the supplied command
exists in the predefined set of safe commands (`ALLOWED_COMMANDS`).  If it does,
the command string is returned unchanged; otherwise `None` is returned.

The function performs a strict membership test and does not execute any
command.  It also normalises whitespace to avoid accidental mismatches.

Security Note:
    - No external input is executed, preventing command injection.
    - The whitelist (`ALLOWED_COMMANDS`) should be maintained with care
      to avoid accidental inclusion of unsafe commands.
"""

from __future__ import annotations

import logging
from typing import Optional, Set

# Configure basic logging (can be overridden by the host application)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# Example whitelist of safe commands
ALLOWED_COMMANDS: Set[str] = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the whitelist.

    Parameters
    ----------
    cmd_input : str
        The raw command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is authorised; otherwise, None.

    Raises
    ------
    TypeError
        If ``cmd_input`` is not a string.

    Notes
    -----
    - Leading/trailing whitespace is trimmed.
    - The comparison is case-sensitive to avoid accidental matches
      (e.g., "Restart_Service" would be rejected).
    - The function does not execute the command; it merely performs
      validation.  Execution should be handled elsewhere.
    """
    if not isinstance(cmd_input, str):
        raise TypeError(f"cmd_input must be a string, got {type(cmd_input).__name__}")

    # Normalise whitespace to avoid accidental mismatches
    normalized_cmd = cmd_input.strip()

    if normalized_cmd in ALLOWED_COMMANDS:
        logging.debug(f"Command authorised: {normalized_cmd}")
        return normalized_cmd
    else:
        logging.warning(f"Unauthorized command attempt: {normalized_cmd}")
        return None

# Example usage (commented out to prevent accidental execution)
if __name__ == "__main__":
    test_commands = ["list_files", "invalid_command", "  show_status  "]
    for cmd in test_commands:
        result = verify_and_run_command(cmd)
        if result is not None:
            print(f"Command '{result}' is authorised.")
        else:
            print(f"Command '{cmd.strip()}' is NOT authorised.")