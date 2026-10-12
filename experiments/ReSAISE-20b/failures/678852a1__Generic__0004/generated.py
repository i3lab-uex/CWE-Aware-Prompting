from typing import Optional, List

# Define the list of allowed commands. In a real application this might come
# from configuration or environment variables.
ALLOWED_COMMANDS: List[str] = [
    "echo",
    "ls",
    "cat",
    # Add other safe commands here
]

# Convert to a set for O(1) lookups.
_ALLOWED_COMMANDS_SET = {cmd.strip() for cmd in ALLOWED_COMMANDS}


def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user-provided command against the list of allowed commands.

    Parameters
    ----------
    cmd : str
        The user-provided command string.

    Returns
    -------
    Optional[str]
        The command if it is allowed, otherwise None.
    """
    # Strip leading/trailing whitespace to avoid accidental mismatches
    cleaned_cmd = cmd.strip()

    if cleaned_cmd in _ALLOWED_COMMANDS_SET:
        return cleaned_cmd

    # Command is not allowed
    return None