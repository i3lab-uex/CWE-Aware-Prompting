# Safe command verification module

from typing import Optional

# Define the set of commands that are allowed to be executed.
ALLOWED_COMMANDS = {
    "list_files",
    "show_date",
    "display_disk_usage",
    "echo_hello",
    # Add more safe commands as needed
}

def verify_and_run_command(cmd_input: str) -> Optional[str]:
    """
    Validate a user-supplied command against the allowed commands list.

    Parameters
    ----------
    cmd_input : str
        The raw command string provided by the user.

    Returns
    -------
    Optional[str]
        The validated command if it is in ALLOWED_COMMANDS, otherwise None.
    """
    # Normalise input: strip whitespace and collapse internal spaces
    cleaned_cmd = " ".join(cmd_input.strip().split())

    # Check if the command is in the allowed set
    if cleaned_cmd in ALLOWED_COMMANDS:
        return cleaned_cmd

    # Command not authorized
    return None