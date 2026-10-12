# run_command_if_safe.py

from typing import Optional, Set


# Define the set of commands that are considered safe.
# These should be explicit strings with no shell metacharacters
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "help",
    "exit",
    # Add any other safe commands here
}


def run_command_if_safe(user_command: str) -> Optional[str]:
    """
    Validate a user-supplied command against the set of allowed commands.

    Parameters
    ----------
    user_command : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is in ALLOWED_COMMANDS; otherwise None.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned_command = user_command.strip()

    # The comparison is case-sensitive; adjust if a different policy is needed.
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command

    # Command not authorized
    return None