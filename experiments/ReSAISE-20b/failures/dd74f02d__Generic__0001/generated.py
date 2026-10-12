# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list",
    "status",
    "restart",
    "shutdown",
    "help"
}

def run_command_if_safe(user_command: str):
    """
    Validate a user-supplied command against the set of allowed commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS, otherwise None.
    """
    # Normalise the input: strip whitespace and keep case-sensitive comparison
    command = user_command.strip()
    return command if command in ALLOWED_COMMANDS else None