# List of commands that are allowed to be executed.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "exit",
    # Add other safe commands here
}

def check_and_execute_command(usr_cmd: str) -> str | None:
    """
    Validate a user-provided command against the set of allowed commands.

    Parameters
    ----------
    usr_cmd : str
        The command string input by the user.

    Returns
    -------
    str | None
        The original command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    cleaned_cmd = usr_cmd.strip()

    # Exact match check – no partial or substring matching to avoid injection
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Command not allowed
    return None