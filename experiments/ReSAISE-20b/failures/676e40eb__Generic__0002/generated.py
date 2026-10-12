# validate_and_run_cmd.py

from typing import Optional, Iterable


# A predefined list (or set) of safe commands.
ALLOWED_COMMANDS: Iterable[str] = {
    "list",
    "status",
    "restart",
    "shutdown",
    # Add other trusted commands here
}


def validate_and_run_cmd(usr_command: str) -> Optional[str]:
    """
    Validate a user-provided command against the trusted ALLOWED_COMMANDS list.

    Parameters
    ----------
    usr_command : str
        The command string supplied by the user.

    Returns
    -------
    Optional[str]
        The original command if it is trusted; otherwise, None.
    """
    # Normalize the command: strip whitespace and collapse internal spaces
    cleaned_cmd = " ".join(usr_command.strip().split())

    # Use a set for O(1) membership checks
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # If not allowed, do not proceed
    return None