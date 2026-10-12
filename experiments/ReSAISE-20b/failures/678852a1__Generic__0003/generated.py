import re
from typing import Optional

# Define the set of allowed commands. Adjust as needed.
ALLOWED_COMMANDS = [
    "list",
    "status",
    "restart",
    "shutdown",
]

def _normalize_command(cmd: str) -> str:
    """
    Normalizes the command string by stripping surrounding whitespace
    and converting to lowercase. This helps avoid accidental mismatches.
    """
    return cmd.strip().lower()

def validate_and_execute_command(cmd: str) -> Optional[str]:
    """
    Validate a user-provided command against the list of allowed commands.
    
    Parameters
    ----------
    cmd : str
        The command supplied by the user.

    Returns
    -------
    Optional[str]
        The normalized command if it is in ALLOWED_COMMANDS; otherwise None.
    
    Notes
    -----
    This function performs no execution itself. It merely validates and
    returns the command so that a caller can safely execute it.
    
    Security Considerations
    -----------------------
    * The command is matched exactly against the allowed list after
      normalizing whitespace and case.
    * No attempt to parse or interpret arguments is made; any
      additional input is ignored.
    """
    normalized = _normalize_command(cmd)

    # Ensure the command matches exactly one of the allowed commands
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # Optionally, warn or log that an invalid command was attempted
    return None