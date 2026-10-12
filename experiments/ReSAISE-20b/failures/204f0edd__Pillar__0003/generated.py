# safe_command_executor.py

from typing import Optional, Set


# Define a set of commands that are considered safe.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "status",
    "restart",
    "shutdown",
    # Add more safe commands here as needed.
}


def check_and_run_command(command: str) -> Optional[str]:
    """
    Validate that the supplied command is in the set of allowed commands.

    Args:
        command (str): The user-supplied command string.

    Returns:
        Optional[str]: The original command if it is allowed, otherwise None.
    """
    # Normalise the input to avoid accidental whitespace or case issues.
    cmd = command.strip().lower()

    # Ensure the command is exactly one of the allowed strings.
    if cmd in ALLOWED_COMMANDS:
        # The command is safe to execute; return it unchanged.
        return cmd

    # Command not authorized – reject it.
    return None