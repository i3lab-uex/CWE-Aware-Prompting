from typing import Optional, Set

# Define the set of commands that are considered safe.
ALLOWED_COMMANDS: Set[str] = {
    "ls",
    "cat",
    "echo",
    "pwd",
    "whoami",
}

def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate that the user supplied command is in the list of allowed commands.

    Parameters
    ----------
    usr_command : str
        The command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command string if it is allowed, otherwise None.
    """
    # Normalize the input: strip surrounding whitespace to avoid accidental mismatches
    cleaned_cmd = usr_command.strip()

    # Check membership in the allowed set.
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # If the command is not allowed, do not execute it; simply return None.
    return None