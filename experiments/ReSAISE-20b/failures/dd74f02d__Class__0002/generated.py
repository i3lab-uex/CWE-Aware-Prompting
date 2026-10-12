# Define the set of allowed commands that are considered safe.
ALLOWED_COMMANDS = {
    "list_files",
    "show_status",
    "restart_service",
    "shutdown_system",
}

def run_command_if_safe(user_command: str):
    """
    Validate a user-supplied command against the predefined set of safe commands.

    Parameters
    ----------
    user_command : str
        The command string supplied by the user.

    Returns
    -------
    str | None
        The original command if it is authorized; otherwise, None.
    """
    # Ensure the input is a string to avoid accidental type issues
    if not isinstance(user_command, str):
        return None

    # Strip leading/trailing whitespace to avoid accidental mismatches
    command = user_command.strip()

    # Compare the cleaned command against the allowed set.
    if command in ALLOWED_COMMANDS:
        return command
    else:
        return None