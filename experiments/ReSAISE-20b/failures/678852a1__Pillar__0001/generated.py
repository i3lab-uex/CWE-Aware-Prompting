# validate_and_execute_command.py

from typing import Optional, List

# Define the list of commands that are considered safe to execute.
ALLOWED_COMMANDS: List[str] = [
    "list_files",
    "disk_usage",
    "show_processes",
    # Add more commands as needed.
]

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
        The validated command if it is in ALLOWED_COMMANDS; otherwise None.

    Notes
    -----
    * The function performs a strict equality check. No partial matches or pattern
      matching are allowed, which mitigates the risk of command injection.
    * The comparison is case‑sensitive. If a case‑insensitive check is required,
      normalise both strings (e.g., using .lower()) before comparison.
    """
    # Trim whitespace to avoid accidental mismatches
    cleaned_cmd = cmd.strip()

    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # If the command is not allowed, do not expose any details.
    return None