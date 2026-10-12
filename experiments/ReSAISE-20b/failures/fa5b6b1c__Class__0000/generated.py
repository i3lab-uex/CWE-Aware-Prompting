# Define the set of commands that are considered safe.
ALLOWED_COMMANDS = {
    "list",
    "show",
    "help",
    "exit",
    "status"
}

def authorize_and_run_cmd(command: str) -> str | None:
    """
    Validate a user-provided command against the list of allowed commands.

    Parameters
    ----------
    command : str
        The raw command string entered by the user.

    Returns
    -------
    str | None
        The command if it is in ALLOWED_COMMANDS; otherwise, None.
    """
    # Normalize the input to avoid accidental injection via whitespace or case.
    cleaned_command = command.strip().lower()

    # Use a set lookup for O(1) membership testing.
    if cleaned_command in ALLOWED_COMMANDS:
        return cleaned_command
    return None