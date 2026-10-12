# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "echo_hello",
    "shutdown_system",
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-supplied command against the allowed commands list.

    Parameters
    ----------
    user_command : str
        The command string provided by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Normalise the command: strip surrounding whitespace and ensure it is a single word
    command = user_command.strip()

    # Reject empty commands or those containing spaces (to avoid compound commands)
    if not command or " " in command:
        return None

    # Check against the set of allowed commands
    if command in ALLOWED_COMMANDS:
        return command

    # If not found, return None to indicate an unauthorized command
    return None