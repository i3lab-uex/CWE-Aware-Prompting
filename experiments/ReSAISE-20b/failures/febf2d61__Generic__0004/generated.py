# verify_and_run_command.py

ALLOWED_COMMANDS = [
    "list_users",
    "show_status",
    "restart_service",
    "shutdown_system",
    # Add more allowed commands as needed
]

def verify_and_run_command(command: str):
    """
    Validate a user-provided command against a whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The raw user input representing a command.

    Returns
    -------
    str | None
        The validated command string if it is in ALLOWED_COMMANDS,
        otherwise None.

    Notes
    -----
    - The function performs a case-sensitive exact match.
    - No command execution is performed here; the caller can handle
      execution after validation if needed.
    """
    # Basic sanity check: ensure command is a string
    if not isinstance(command, str):
        return None

    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned = command.strip()

    if cleaned in ALLOWED_COMMANDS:
        return cleaned

    # Command not allowed
    return None