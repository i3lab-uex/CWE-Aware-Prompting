# verify_and_run_command.py

from typing import Optional, Set


# Define the set of commands that are considered safe.
ALLOWED_COMMANDS: Set[str] = {
    "list",
    "show",
    "delete",
    "update",
    "create",
}

def verify_and_run_command(command: str) -> Optional[str]:
    """
    Validate a user-provided command against the set of allowed commands.

    Parameters
    ----------
    command : str
        The raw command string entered by the user.

    Returns
    -------
    Optional[str]
        The original command if it is in ALLOWED_COMMANDS; otherwise, None.

    Notes
    -----
    - The comparison is case-sensitive and uses exact string matching.
    - Leading/trailing whitespace is ignored to avoid accidental mismatches.
    - No command execution takes place here; this function merely performs validation.
    """
    # Normalise the input: strip whitespace, but keep case.
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # If the command is not allowed, return None.
    return None