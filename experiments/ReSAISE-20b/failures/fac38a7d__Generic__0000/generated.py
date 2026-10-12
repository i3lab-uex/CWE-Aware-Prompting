# Define the set of commands that are allowed to be executed.
ALLOWED_COMMANDS = [
    "list_files",
    "show_date",
    "display_status",
    # Add more safe commands here
]

def check_and_run_command(command_input: str):
    """
    Validate the user-provided command against a predefined list of allowed commands.

    Parameters
    ----------
    command_input : str
        The raw command string entered by the user.

    Returns
    -------
    str | None
        The original command string if it is allowed, otherwise None.
    """
    # Strip surrounding whitespace to avoid accidental mismatches
    command = command_input.strip()

    # Perform a case-sensitive exact match against the allowed list.
    if command in ALLOWED_COMMANDS:
        return command
    return None