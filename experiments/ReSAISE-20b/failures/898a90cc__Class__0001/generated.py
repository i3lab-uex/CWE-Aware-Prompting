# verify_and_run_command.py

import re
from typing import Optional, Set

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS: Set[str] = {
    "list",           # e.g., list files
    "status",         # show status
    "help",           # display help information
    "restart_service",  # restart a specific service
}

# Regular expression to allow only alphanumeric characters and underscores.
_ALLOWED_CMD_REGEX = re.compile(r"^[A-Za-z0-9_]+$")

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Verify that the user supplied command is in the list of allowed commands.
    If it is, return the sanitized command string; otherwise, return None.

    Args:
        cmd_input: The raw user input containing the command name.
                   It may contain surrounding whitespace or extraneous
                   characters that should be trimmed.

    Returns:
        The command string if it is authorized, otherwise None.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches.
    cmd = cmd_input.strip()

    # Reject commands that contain disallowed characters to mitigate injection risk.
    if not _ALLOWED_CMD_REGEX.fullmatch(cmd):
        return None

    # Ensure the command is in the allowed set.
    if cmd not in ALLOWED_COMMANDS:
        return None

    # At this point, the command is safe to use downstream.
    return cmd