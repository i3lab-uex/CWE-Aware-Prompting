# Define the set of safe commands that are permitted to run.
ALLOWED_COMMANDS = {
    "list_files",
    "show_disk_usage",
    "print_date",
    "check_system_status",
}

def run_command_if_safe(user_command: str) -> str | None:
    """
    Validate a user-supplied command against the list of allowed commands.

    Parameters
    ----------
    user_command : str
        The command input by the user.

    Returns
    -------
    str | None
        The original command if it is allowed; otherwise, None.
    """
    # Normalize the input to avoid accidental mismatches caused by whitespace or case
    normalized = user_command.strip()

    # Perform a fast membership test against the immutable set of allowed commands
    if normalized in ALLOWED_COMMANDS:
        return normalized

    # If the command is not authorized, explicitly deny execution
    return None