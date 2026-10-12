# check_and_run_command.py

from typing import Optional, List


# Define a list of commands that are considered safe to execute.
ALLOWED_COMMANDS: List[str] = [
    "list",
    "show",
    "status",
    "restart",
    "shutdown",
]


def check_and_run_command(command_input: str) -> Optional[str]:
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Args:
        command_input: The raw input string from the user.

    Returns:
        The validated command string if it is allowed, otherwise None.
    """
    # Strip leading/trailing whitespace and normalize to lower case
    normalized = command_input.strip().lower()

    # Reject empty strings immediately
    if not normalized:
        return None

    # Ensure the command exactly matches one of the allowed commands.
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # For security, do not reveal whether the command was partially correct.
    return None