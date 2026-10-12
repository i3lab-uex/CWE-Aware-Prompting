# Safe command validation utility

ALLOWED_COMMANDS = {
    "list",
    "show",
    "status",
    "restart",
    "shutdown",
}

def check_and_run_command(command: str):
    """
    Validate a user-supplied command against a whitelist of allowed commands.

    Parameters
    ----------
    command : str
        The user-provided command string.

    Returns
    -------
    str | None
        The original command if it is permitted; otherwise, None.
    """
    # Normalise the command: strip whitespace and convert to lowercase
    normalized = command.strip().lower()

    # Check against the whitelist
    if normalized in ALLOWED_COMMANDS:
        return command  # Return the original string for further processing
    return None