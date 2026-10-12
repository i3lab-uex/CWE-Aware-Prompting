# validate_and_execute_command.py

from typing import Optional

# List of commands that are safe to allow the user to run.
ALLOWED_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    # Add more safe commands here
]

def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user-provided command against the list of allowed commands.

    Parameters
    ----------
    cmd : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS, otherwise None.

    Notes
    -----
    * The function does **not** execute the command. It only performs validation.
    * Leading/trailing whitespace is ignored.
    * The comparison is case-sensitive; adjust as needed for your use case.
    """
    # Strip whitespace to avoid accidental mismatches
    cleaned_cmd = cmd.strip()

    # Quick membership test
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Not allowed
    return None