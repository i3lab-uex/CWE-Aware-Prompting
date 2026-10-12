# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "start",
    "stop",
    "restart",
    "status",
    "help",
}

def check_and_run_command(command: str):
    """
    Validate that the supplied command is in the list of allowed commands.

    Parameters
    ----------
    command : str
        The user-supplied command string to validate.

    Returns
    -------
    str | None
        The original command if it is authorized; otherwise, None.

    Notes
    -----
    This function performs a simple membership check against the predefined
    ALLOWED_COMMANDS set. No actual execution of the command occurs here.
    """
    if not isinstance(command, str):
        # Reject non-string inputs for safety
        return None

    # Strip surrounding whitespace and normalize case if desired.
    cmd_clean = command.strip().lower()

    return cmd_clean if cmd_clean in ALLOWED_COMMANDS else None