# Allowed commands list (example)
ALLOWED_COMMANDS = {
    "ls",
    "pwd",
    "whoami",
    "date",
}

def validate_and_execute_command(cmd: str) -> str | None:
    """
    Validate a user-provided command against the allowed list.

    Parameters
    ----------
    cmd : str
        The command supplied by the user.

    Returns
    -------
    str | None
        The validated command if it is in ALLOWED_COMMANDS; otherwise None.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned_cmd = cmd.strip()

    # Ensure the command is exactly one of the allowed commands
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # If not allowed, do not return the command
    return None